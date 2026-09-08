#!/usr/bin/env python3
"""Provider-neutral, fail-closed orchestration above the existing release pipeline.

A host supplies real agent executions and a canonical assembler. Without either,
no model-generated assertion can substitute for the missing work or evidence.
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import json
import shutil
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agent_adapter import AgentAdapter, AgentExecution, JsonCommandAdapter
from agent_pipeline import RepositoryPipeline
from agent_protocol import (ProtocolError, aggregate_components, component_request, read_json,
    safe_path, sha256_file, sha256_json, validate_component_result, validate_json, write_json_atomic)
from agent_registry import AgentRegistry
from agent_state import ExecutionState
from build_execution_plan import (build_execution_plan, freeze_context, source_path,
                                  validate_execution_plan)
from dlp_build_runtime import validate_request
from validate_agent_artifacts import route_defects, validate_review_result


class IntegrityError(ProtocolError):
    """Pinned evidence/context changed; retrying would conceal a trust violation."""


def fresh(prefix: str) -> str:
    return prefix + '-' + uuid.uuid4().hex


class DailyPackOrchestrator:
    def __init__(self, *, registry: AgentRegistry, adapter: AgentAdapter, run_root: Path,
                 max_parallelism: int | None = None, pipeline: RepositoryPipeline | None = None,
                 timeout: float = 300):
        self.registry, self.adapter = registry, adapter
        self.run_root = Path(run_root).resolve()
        defaults = registry.payload['execution_defaults']
        limit = defaults['max_parallelism'] if max_parallelism is None else max_parallelism
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= defaults['max_parallelism']:
            raise ProtocolError('Parallelism must be positive and within the registry limit')
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= 3600:
            raise ProtocolError('Invocation timeout must be between 0 and 3600 seconds')
        self.semaphore, self.timeout = asyncio.Semaphore(limit), timeout
        self.serial = asyncio.Lock()
        self.pipeline = pipeline or RepositoryPipeline(None)
        self.pinned: dict[Path, str] = {}
        self.attempts: dict[str, int] = {}
        self.accepted: dict[str, dict] = {}
        self.metrics: list[dict] = []
        self.execution_ids: set[str] = set()
        self.generation_actors: set[str] = set()
        self.review_actors: set[str] = set()
        self.candidate = None

    def _pin(self, path: Path) -> None:
        path = Path(path).resolve()
        digest = sha256_file(path)
        if path in self.pinned and self.pinned[path] != digest:
            raise IntegrityError('Pinned file changed: ' + str(path))
        self.pinned[path] = digest

    def _verify(self) -> None:
        for path, digest in self.pinned.items():
            if not path.is_file() or sha256_file(path) != digest:
                raise IntegrityError('Pinned file changed: ' + str(path))

    def _record(self, relative: str, payload: dict) -> Path:
        path = safe_path(self.run_root, relative)
        write_json_atomic(path, payload, immutable=True)
        self._pin(path)
        return path

    async def _dispatch(self, request: dict, *, generation: bool) -> AgentExecution:
        self._verify()
        agent = self.registry.get(request['agent_id'])
        validate_json(request, self.registry.root/'schemas/agent-request.schema.json')
        self._record('requests/'+request['invocation_id']+'.json', request)
        for reference in request['references']:
            path = safe_path(self.registry.root, reference['path'])
            if sha256_file(path) != reference['sha256']:
                raise IntegrityError('Reference changed before invocation: ' + str(path))
            self._pin(path)
        started = time.perf_counter()
        metric = dict(generation_run_id=self.context['generation_run_id'],
                      invocation_id=request['invocation_id'], agent_id=agent.id,
                      instance_id=request['instance']['id'] if request['instance'] else None,
                      attempt=self.attempts.get(request['instance']['id'], 1) if request['instance'] else 1,
                      started_at=datetime.now(timezone.utc).isoformat(), status='FAIL',
                      input_tokens=None, output_tokens=None,
                      defects_created=0, defects_repaired=0)
        try:
            async def invoke():
                async with self.semaphore:
                    return await asyncio.wait_for(self.adapter.invoke(agent_id=agent.id,
                                                  request=copy.deepcopy(request)), self.timeout)
            if agent.parallelizable:
                execution = await invoke()
            else:
                async with self.serial:
                    execution = await invoke()
            self._verify()
            if not isinstance(execution, AgentExecution):
                raise ProtocolError('Host must return a real AgentExecution receipt, not result JSON alone')
            execution.validate_receipt()
            self._record('results/'+request['invocation_id']+'.json', execution.result)
            transcript = safe_path(self.run_root, 'results/'+request['invocation_id']+'.txt')
            with transcript.open('x', encoding='utf-8', newline='') as stream:
                stream.write(execution.transcript)
            self._pin(transcript)
            self._record('results/'+request['invocation_id']+'-receipt.json', dict(
                source=execution.source, actor=execution.actor, execution_id=execution.execution_id,
                transcript_sha256=sha256_file(transcript),
                result_sha256=sha256_json(execution.result)))
            if execution.execution_id in self.execution_ids or execution.execution_id == self.context['generation_run_id']:
                raise ProtocolError('Host execution ID must be unique and independent of generation identity')
            self.execution_ids.add(execution.execution_id)
            opposite = self.review_actors if generation else self.generation_actors
            if execution.actor in opposite:
                raise ProtocolError('Reviewer execution must be independent of every generation actor')
            (self.generation_actors if generation else self.review_actors).add(execution.actor)
            supplied = execution.result.get('metrics', {})
            for key in ('input_tokens', 'output_tokens'):
                metric[key] = supplied.get(key)
            metric['status'] = 'RETURNED'  # Transport success is not component/review acceptance.
            metric['defects_created'] = len(execution.result.get('defects', []))
            return execution
        except Exception as exc:
            metric['error'] = type(exc).__name__ + ': ' + str(exc)
            self._verify()
            raise
        finally:
            metric['finished_at'] = datetime.now(timezone.utc).isoformat()
            metric['latency_ms'] = round((time.perf_counter()-started)*1000)
            self.metrics.append(metric)
            write_json_atomic(self.run_root/'metrics.json', {'invocations':self.metrics})

    def _accepted_metric(self, invocation_id: str, passed: bool, *, repaired: int = 0) -> None:
        for metric in self.metrics:
            if metric['invocation_id'] == invocation_id:
                metric['status'] = 'PASS' if passed else 'FAIL'
                metric['defects_repaired'] = repaired if passed else 0
        write_json_atomic(self.run_root/'metrics.json', {'invocations':self.metrics})

    def _protocol_defect(self, instance: dict, message: str, invocation_id: str) -> dict:
        return dict(defect_id=fresh('def'),generation_run_id=self.context['generation_run_id'],
            review_run_id='protocol-'+invocation_id,check_id='PROTOCOL.COMPONENT',
            severity='release_blocking',owner=instance['owner'],scope='instance',instance_id=instance['id'],
            description='Component handoff did not meet the execution contract.',
            evidence={'observation':'Rejected handoff: '+message,'citations':['requests/'+invocation_id+'.json']},
            required_correction='Correct the reported handoff failure within this instance: '+message)

    def _review_request(self, agent_id: str, *, instance: dict | None, bindings: dict,
                        checks: list[dict], inputs: list[dict]) -> dict:
        invocation_id = fresh('review')
        return dict(protocol_version=1, generation_run_id=self.context['generation_run_id'],
            invocation_id=invocation_id,agent_id=agent_id,
            task_type='REVIEW_COMPONENT' if instance else 'REVIEW_PACK',
            context_sha256=sha256_json(self.context),context=copy.deepcopy(self.context),
            instance=copy.deepcopy(instance),references=self.registry.references_for(agent_id,self.context),
            defects=[],expected_checks=checks,input_artifacts=inputs,review_run_id=fresh('qa'),bindings=bindings,
            permissions=dict(may_mutate_context=False,may_modify_other_instances=False,may_release=False),
            output_contract={'schema':'schemas/review-result.schema.json','path':'reviews/'+invocation_id+'.json'})

    async def _critic(self, instance: dict, result: dict, request: dict) -> list[dict]:
        critic_id = self.registry.get(instance['owner']).raw.get('post_generation_review')
        if not critic_id:
            return []
        path = safe_path(self.run_root, result['component']['artefact'])
        review = self._review_request(critic_id,instance=instance,checks=request['expected_checks'],
            inputs=[{'path':str(path),'sha256':sha256_file(path),'text':path.read_text(encoding='utf-8')}],
            bindings=dict(artifact_sha256=sha256_file(path),manifest_sha256=None,
                          content_sha256=sha256_json(result['component']['content']),
                          requirements_sha256=sha256_file(self.registry.root/'references/qa-requirements.json')))
        node = 'critic:'+instance['id']
        self.state.begin(node, review['invocation_id'])
        try:
            execution = await self._dispatch(review,generation=False)
            validate_review_result(execution.result,review,
                {'instances':[instance],'tasks':result['component']['content']['tasks']},{'bindings':[]})
            self._record(review['output_contract']['path'], execution.result)
            passed = execution.result['status']=='PASS' and not execution.result['defects']
            self.state.finish(node,passed)
            self._accepted_metric(review['invocation_id'],passed)
            if not passed and not execution.result['defects']:
                raise ProtocolError('Critic did not pass and supplied no actionable defect')
            return execution.result['defects']
        except Exception:
            if self.state.nodes[node]['state']=='RUNNING':
                self.state.finish(node,False)
            raise

    async def _generate(self, instance: dict, defects: list[dict] | None = None) -> None:
        key, owner = instance['id'],self.registry.get(instance['owner'])
        defects = copy.deepcopy(defects or [])
        while self.attempts.get(key,0) < owner.max_attempts:
            self.attempts[key] = self.attempts.get(key,0)+1
            invocation_id = fresh('gen')
            request = component_request(self.context,instance,self.registry,invocation_id,defects=defects)
            if key in self.accepted:
                path=safe_path(self.run_root,self.accepted[key]['component']['artefact'])
                request['input_artifacts']=[dict(path=str(path),sha256=sha256_file(path),text=path.read_text(encoding='utf-8'))]
            node='generate:'+key
            if self.state.passed(node):
                self.state.invalidate(node)
            self.state.begin(node,invocation_id)
            try:
                execution=await self._dispatch(request,generation=True)
                validate_component_result(execution.result,request,self.context)
                if execution.result['status']!='PASS':
                    raise ProtocolError('Component checks report FAIL: '+json.dumps(execution.result['component']['checks']))
            except IntegrityError:
                self.state.finish(node,False)
                raise
            except Exception as exc:
                self.state.finish(node,False)
                self._accepted_metric(invocation_id,False)
                defects=[self._protocol_defect(instance,str(exc),invocation_id)]
                self._record('defects/'+invocation_id+'.json',{'defects':defects})
                continue
            result=copy.deepcopy(execution.result)
            self._record(result['component']['artefact'],result)
            self.state.finish(node,True)
            self._accepted_metric(invocation_id,True)
            self.accepted[key]=result
            defects=await self._critic(instance,result,request)
            if not defects:
                self._accepted_metric(invocation_id,True,repaired=len(request['defects']))
                write_json_atomic(self.run_root/'components'/key/'accepted.json',
                                  {'path':result['component']['artefact'],'sha256':sha256_json(result)})
                return
            self._record('defects/'+invocation_id+'-critic.json',{'defects':defects})
            self.state.invalidate(node)
        raise ProtocolError(f'{key} exhausted its cumulative {owner.max_attempts}-attempt generation/repair budget')

    async def _generations(self, instances: list[dict], defects: dict | None = None) -> None:
        if not self.registry.payload['execution_defaults']['parallel_generation']:
            for instance in instances:
                await self._generate(instance,(defects or {}).get(instance['id']))
            return
        results=await asyncio.gather(*(self._generate(i,(defects or {}).get(i['id'])) for i in instances),
                                     return_exceptions=True)
        failures=[str(result) for result in results if isinstance(result,BaseException)]
        if failures:
            raise ProtocolError('\n'.join(failures))

    async def _pack_review(self, agent_id: str) -> tuple[dict, AgentExecution | None]:
        candidate=self.candidate
        content,manifest=read_json(candidate.root/'content.json'),read_json(candidate.root/'manifest.json')
        method='visual' if agent_id=='visual-reviewer' else 'semantic'
        checks=([dict(check_id='RUNTIME.PROVENANCE',target='pack')] if agent_id=='provenance-reviewer'
                else self.pipeline.expected(candidate,method))
        request=self._review_request(agent_id,instance=None,bindings=candidate.hashes(),checks=checks,
                                     inputs=self.pipeline.review_inputs(candidate))
        node='qa:'+agent_id
        self.state.begin(node,request['invocation_id'])
        try:
            if agent_id=='provenance-reviewer':
                self._record('requests/'+request['invocation_id']+'.json',request)
                result=await self.pipeline.provenance(candidate,request)
                execution=None
            else:
                execution=await self._dispatch(request,generation=False)
                result=execution.result
            validate_review_result(result,request,content,manifest)
            self._verify()
            self._record(request['output_contract']['path'],result)
            passed=result['status']=='PASS'
            self.state.finish(node,passed)
            self._accepted_metric(request['invocation_id'],passed)
            return result,execution
        except Exception:
            if self.state.nodes[node]['state']=='RUNNING':
                self.state.finish(node,False)
            raise

    def _status(self, status: str, **details) -> dict:
        result=dict(status=status,generation_run_id=self.context['generation_run_id'],
                    release_ready=status=='RELEASED',attempts=self.attempts.copy(),**details)
        if self.candidate:
            result.setdefault('candidate',str(self.candidate.root))
        write_json_atomic(self.run_root/'run-status.json',result)
        return result

    async def run(self, *, request: dict, context: dict, source_root: Path,
                  plan: dict | None = None, stop_after_components: bool = False) -> dict:
        if self.run_root.exists():
            raise ProtocolError('Run directory already exists; history cannot be overwritten')
        errors=validate_request(request)
        if errors:
            raise ProtocolError('\n'.join(errors))
        self.context=freeze_context(context,self.registry,source_root)
        if request['requested_date']!=self.context['date']['value']:
            raise ProtocolError('Request date differs from frozen context')
        self.plan=copy.deepcopy(plan) if plan is not None else build_execution_plan(self.context,self.registry)
        validate_execution_plan(self.context,self.plan,self.registry)
        self.run_root.mkdir(parents=True,exist_ok=False)
        self.request_path=self._record('context/request.json',request)
        self.context_path=self._record('context/context.json',self.context)
        self._record('plan/execution-plan.json',self.plan)
        self.state=ExecutionState(self.plan,self.run_root/'plan/state.json')
        for path in (self.registry.root/'schemas').glob('*.schema.json'):
            self._pin(path)
        self._pin(self.registry.root/'skills/registry.v2.json')
        for source in self.context['source_provenance']:
            path=source_path(source,self.registry,source_root)
            self._pin(path)
            target=safe_path(self.run_root,'context/sources/'+source['id']+'/'+source['path'])
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,target)
            self._pin(target)
        try:
            await self._generations(self.context['timetable_instances'])
            revision=0
            while True:
                self._verify()
                revision+=1
                record,content=aggregate_components(self.context,list(self.accepted.values()))
                record_path=self._record(f'components/aggregate-{revision}/component-record.json',record)
                content_path=self._record(f'components/aggregate-{revision}/content.json',content)
                if stop_after_components:
                    return self._status('COMPONENTS_VALIDATED',component_record=str(record_path),content=str(content_path))
                self.state.begin('assemble',fresh('assemble'))
                try:
                    self.candidate=await self.pipeline.assemble(run_root=self.run_root,
                        request_path=self.request_path,context_path=self.context_path,content_path=content_path,
                        component_record_path=record_path,revision=revision)
                    for path in self.pipeline.snapshot(self.candidate):
                        self._pin(path)
                    self._verify()
                    self.state.finish('assemble',True)
                except Exception:
                    self.state.finish('assemble',False)
                    raise
                agents=('semantic-reviewer','visual-reviewer','provenance-reviewer')
                values=await asyncio.gather(*(self._pack_review(a) for a in agents),return_exceptions=True)
                failures=[str(v) for v in values if isinstance(v,BaseException)]
                if failures:
                    raise ProtocolError('\n'.join(failures))
                reviews=dict(zip(agents,values))
                defects=[d for result,_ in values for d in result['defects']]
                self._record(f'defects/revision-{revision}.json',{'defects':defects})
                if not defects:
                    self._verify()
                    self.state.begin('release',fresh('release'))
                    try:
                        released=await self.pipeline.release(self.candidate,reviews,
                            generation_actors=self.generation_actors,run_root=self.run_root)
                        self._verify()
                    except Exception:
                        self.state.finish('release',False)
                        raise
                    self.state.finish('release',released['status']=='RELEASED')
                    status=released.pop('status')
                    return self._status(status,**released)
                blockers=[d for d in defects if d['severity']=='release_blocking']
                if not blockers:
                    return self._status('CANDIDATE',reason='Warnings require explicit disposition; none were silently waived.',defects=defects)
                manifest=read_json(self.candidate.root/'manifest.json')
                grouped=route_defects(blockers,content,manifest)
                affected=[i for i in self.context['timetable_instances'] if i['id'] in grouped]
                exhausted=[i['id'] for i in affected if self.attempts[i['id']]>=self.registry.get(i['owner']).max_attempts]
                if exhausted:
                    return self._status('CANDIDATE',reason='Cumulative repair budget exhausted: '+', '.join(exhausted),defects=defects)
                for instance in affected:
                    self.state.invalidate('generate:'+instance['id'])
                await self._generations(affected,grouped)
        except Exception as exc:
            # Evidence remains inspectable; no partial component acceptance is release.
            return self._status('CANDIDATE' if self.candidate else 'BLOCKED',
                                reason=type(exc).__name__+': '+str(exc))


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('request','context','sources','config','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--stop-after',choices=('components','release'),default='release')
    parser.add_argument('--max-parallelism',type=int)
    args=parser.parse_args()
    try:
        config=read_json(args.config)
        if set(config)-{'agents','assembly_command','timeout_seconds'}:
            raise ProtocolError('Unknown host configuration key')
        timeout=config.get('timeout_seconds',300)
        orchestrator=DailyPackOrchestrator(registry=AgentRegistry.load(),
            adapter=JsonCommandAdapter(config['agents'],timeout=timeout),run_root=args.out,
            pipeline=RepositoryPipeline(config.get('assembly_command'),timeout=timeout),
            timeout=timeout,max_parallelism=args.max_parallelism)
        status=asyncio.run(orchestrator.run(request=read_json(args.request),context=read_json(args.context),
                       source_root=args.sources,stop_after_components=args.stop_after=='components'))
        print(json.dumps(status,indent=2))
        return 0 if status['status'] in ('COMPONENTS_VALIDATED','RELEASED') else 1
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    raise SystemExit(main())
