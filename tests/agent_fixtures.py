"""Synthetic orchestration fixtures; never use these as classroom evidence."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def context_fixture(source_root, owners=('dlp-morning-work', 'dlp-maths-lesson', 'dlp-maths-lesson')):
    source_root = Path(source_root)
    source_root.mkdir(exist_ok=True, parents=True)
    request = {'schema_version':1, 'requested_date':'2026-09-08', 'requested_output':'powerpoint'}
    request_path = source_root/'request.json'
    request_path.write_text(json.dumps(request)+'\n')
    values = dict(active_year_profile='year-4-5', pack_profile='default', date='2026-09-08',
                  term_week='Term 3 Week 8', day='Tuesday', timetable='Synthetic timetable',
                  mathematics_focus='Mass', english_focus='Narrative', lesson_status='advance-as-scheduled')
    context = {key:dict(resolved=True,value=value,source='request.json') for key,value in values.items()}
    profile = 'references/year-level-profiles/year-4-5.md'
    context['active_year_profile'].update(source=profile, status='calibrated')
    context.update(schema_version=2, generation_run_id='test-generation-20260908', frozen=True,
        timetable_instances=[dict(id=f'instance-{i+1}', owner=owner, start=f'{8+i:02}:30',
            duration_minutes=30, purpose='Synthetic contract verification') for i,owner in enumerate(owners)],
        required_artifacts=['deck','briefing'], output_constraints={'deck':True,'briefing':True},
        unresolved_fields=[], source_provenance=[
            dict(id='request-source',kind='user_request',path='request.json',sha256=hashlib.sha256(request_path.read_bytes()).hexdigest()),
            dict(id='profile-source',kind='year_profile',path=profile,sha256=hashlib.sha256((ROOT/profile).read_bytes()).hexdigest())])
    return request, context

def component_result(request):
    instance = request['instance']
    task_id = instance['id']+'-task'
    evidence = dict(observation='Synthetic evidence for control-plane tests, not a teaching-quality judgement.',
                    citations=['component:'+task_id])
    return dict(protocol_version=1, generation_run_id=request['generation_run_id'],
        invocation_id=request['invocation_id'], agent_id=request['agent_id'],
        context_sha256=request['context_sha256'], status='PASS', result_type='COMPONENT',
        component=dict(instance_id=instance['id'],owner=instance['owner'],
            active_year_profile=request['context']['active_year_profile']['value'],status='PASS',
            estimated_minutes=20,artefact=request['output_contract']['path'],
            checks=[dict(id=c['check_id'],status='PASS',evidence=evidence.copy()) for c in request['expected_checks']],
            content={'tasks':[dict(id=task_id,instance_id=instance['id'],operation='calculate',
                fields={'prompt':'Calculate 2 + 3.','answer':'5'},
                demands=[dict(id=task_id+'-response',action='calculate',answer_quote='5')])]}))
