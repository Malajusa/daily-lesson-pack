#!/usr/bin/env python3
"""Resolve versioned instructional preferences without inventing lesson facts."""
from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
from agent_protocol import ProtocolError, read_json, sha256_file, validate_json, write_json_atomic
from teacher_context_store import SettingsStore, validate_state, validate_values
from year_profile_registry import YearProfileRegistry

ROOT=Path(__file__).resolve().parents[1]
DEFAULTS='config/creator-defaults.json'
SCHEMA='schemas/instructional-calibration.schema.json'


def resolve(*, state=None, on: str, overrides=None, request_source=None,
            unit_id=None, lesson_id=None, progression_id=None, root: Path=ROOT) -> dict:
    root=Path(root).resolve()
    today=date.fromisoformat(on)
    defaults=read_json(root/DEFAULTS)
    if defaults.get('schema_version')!=1 or not defaults.get('revision'):
        raise ProtocolError('Unsupported creator-defaults schema')
    values=dict(defaults['values']); validate_values(values,root=root)
    provenance={k:dict(source=DEFAULTS,revision=defaults['revision'],scope={'kind':'default'}) for k in values}
    architecture=read_json(root/'references/default-pack-profile.json')
    for key,value in [('literacy_sequence_count',architecture['literacy_warmup']['sequence_count']),
                      ('numeracy_prompt_answer_pairs',architecture['numeracy_warmup']['prompt_answer_pairs'])]:
        values[key]=value
        provenance[key]=dict(source='references/default-pack-profile.json',revision=architecture['schema_version'],scope={'kind':'default'})
    state=state if state is not None else {'schema_version':1,'revision':0,'entries':[]}
    validate_state(state,root=root)
    applicable=[]
    for entry in state['entries']:
        scope=entry['scope']; kind=scope['kind']
        matches=(kind=='standing' or kind=='date' and date.fromisoformat(scope['start'])<=today<=date.fromisoformat(scope['end'])
                 or kind=='unit' and scope['id']==unit_id or kind=='lesson' and scope['id']==lesson_id
                 or kind=='progression' and scope['id']==progression_id)
        if matches:
            priority={'standing':0,'unit':1,'progression':1,'date':2,'lesson':3}[kind]
            applicable.append((priority,entry['revision'],entry))
    for _,__,entry in sorted(applicable,key=lambda item:item[:2]):
        for name,value in entry['values'].items():
            values[name]=value
            provenance[name]=dict(source=entry['source'],revision=entry['revision'],scope=entry['scope'])
    if overrides:
        if not isinstance(request_source,str) or not request_source.strip():
            raise ProtocolError('Current overrides need an actual request source')
        validate_values(overrides,root=root)
        for name,value in overrides.items():
            values[name]=value; provenance[name]=dict(source=request_source,revision=0,scope={'kind':'current'})
    registry=YearProfileRegistry.load(root)
    profile=registry.get(values['active_year_profile'])
    if values['active_year_profile'] != defaults['values']['active_year_profile']:
        # A profile switch must not carry the creator-only curriculum/retrieval defaults.
        for name,value in [('main_curriculum_year',max(profile['curriculum_anchor']['years'])),('retrieval_years',[])]:
            if provenance[name]['scope']['kind']=='default':
                values[name]=value
                provenance[name]=dict(source=profile['path'],revision=profile['revision'],scope={'kind':'profile'})
    validate_values(values,root=root)
    result={'schema_version':1,'on':on,'settings_revision':state['revision'],
            'defaults_sha256':sha256_file(root/DEFAULTS),'values':values,'provenance':provenance,
            'profile':{'id':profile['profile_id'],'source':profile['path'],'revision':profile['revision'],
                       'status':profile['status'],'release_mode':registry.release_mode(profile['profile_id'])}}
    validate_json(result,root/SCHEMA)
    return result


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--on',required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--store',type=Path);parser.add_argument('--teacher');parser.add_argument('--classroom')
    parser.add_argument('--overrides',type=Path);parser.add_argument('--request-source')
    for name in ('unit-id','lesson-id','progression-id'): parser.add_argument('--'+name)
    args=parser.parse_args()
    try:
        state=SettingsStore(args.store).read(args.teacher,args.classroom) if args.store else None
        result=resolve(state=state,on=args.on,overrides=read_json(args.overrides) if args.overrides else None,
            request_source=args.request_source,unit_id=args.unit_id,lesson_id=args.lesson_id,progression_id=args.progression_id)
        write_json_atomic(args.out,result,immutable=True)
        return 0
    except (ValueError,OSError) as exc: parser.exit(1,str(exc)+'\n')

def validate_calibration(calibration: dict, *, root: Path=ROOT) -> None:
    """Validate supplied sidecars against public sources, not their status claims."""
    validate_json(calibration,Path(root)/SCHEMA)
    validate_values(calibration['values'],root=Path(root))
    if set(calibration['values']) != set(calibration['provenance']):
        raise ProtocolError('Every resolved preference must have exactly one provenance entry')
    if calibration['defaults_sha256'] != sha256_file(Path(root)/DEFAULTS):
        raise ProtocolError('Calibration uses changed creator defaults')
    registry=YearProfileRegistry.load(root)
    record=registry.get(calibration['values']['active_year_profile'])
    expected={'id':record['profile_id'],'source':record['path'],'revision':record['revision'],
              'status':record['status'],'release_mode':registry.release_mode(record['profile_id'])}
    if calibration['profile']!=expected: raise ProtocolError('Calibration profile disagrees with registry')


def freeze_calibration(context: dict, *, root: Path, source_root: Path) -> None:
    """Mutate only the coordinator's fresh context copy. Never write private state."""
    from agent_protocol import safe_path
    root=Path(root)
    provenance=context.get('source_provenance')
    if not isinstance(provenance,list): raise ProtocolError('source_provenance must be a list')
    try: on=context['date']['value']
    except (KeyError,TypeError) as exc: raise ProtocolError('A source-backed lesson date is required') from exc
    supplied=context.get('instructional_calibration')
    source=context.get('calibration_source')
    profile_value=context.get('active_year_profile',{}).get('value')
    selected_profile=profile_value or read_json(root/DEFAULTS)['values']['active_year_profile']
    profile_override={'active_year_profile':selected_profile}
    default=resolve(on=on,root=root,overrides=profile_override,request_source='registered-profile-selection')
    if supplied is None:
        calibration=default; source=DEFAULTS
    elif source==DEFAULTS:
        if supplied!=default: raise ProtocolError('Default-only calibration cannot assert saved/current overrides')
        calibration=supplied
    else:
        bindings=[s for s in provenance if isinstance(s,dict) and source in (s.get('path'),s.get('id'))]
        if not source or len(bindings)!=1 or bindings[0]['kind']!='runtime_school_source':
            raise ProtocolError('Supplied calibration requires one hashed runtime sidecar')
        path=safe_path(source_root,bindings[0]['path'])
        if sha256_file(path)!=bindings[0]['sha256'] or read_json(path)!=supplied:
            raise ProtocolError('Calibration sidecar does not match its source bytes')
        calibration=supplied
    validate_calibration(calibration,root=root)
    if calibration['on']!=on: raise ProtocolError('Calibration applies to a different lesson date')
    ident=calibration['values']['active_year_profile']
    if profile_value and profile_value!=ident: raise ProtocolError('Calibration/context profile mismatch')
    record=YearProfileRegistry.load(root).get(ident)
    if 'active_year_profile' not in context:
        context['active_year_profile']={'value':ident,'source':record['path'],'resolved':True}
    def bind(path,ident,kind):
        matches=[s for s in provenance if isinstance(s,dict) and s.get('path')==path]
        expected=sha256_file(root/path)
        if matches:
            if len(matches)!=1 or matches[0]['kind']!=kind or matches[0]['sha256']!=expected:
                raise ProtocolError('Changed calibration provenance: '+path)
        else: provenance.append(dict(id=ident,kind=kind,path=path,sha256=expected))
    bind(DEFAULTS,'creator-defaults','repository_reference')
    bind('references/default-pack-profile.json','pack-defaults','repository_reference')
    bind(record['path'],'selected-year-profile','year_profile')
    expected_counts={'literacy':calibration['values']['literacy_sequence_count'],
                     'numeracy':calibration['values']['numeracy_prompt_answer_pairs']}
    counts=context.get('warmup_counts',{})
    if not isinstance(counts,dict) or any(key not in expected_counts or type(value) is not int or value!=expected_counts[key]
                                        for key,value in counts.items()):
        raise ProtocolError('Warm-up counts must agree with source-backed calibration')
    context['instructional_calibration']=calibration
    context['calibration_source']=source
    context['warmup_counts']=expected_counts


def instructional_context_errors(context: dict, *, require_release: bool = False, root: Path = ROOT) -> list[str]:
    """Validate preferences on direct finalisation too; legacy defaults remain readable."""
    try:
        calibration = context.get('instructional_calibration')
        if calibration is None:
            architecture = read_json(Path(root)/'references/default-pack-profile.json')
            expected = {'literacy':architecture['literacy_warmup']['sequence_count'],
                        'numeracy':architecture['numeracy_warmup']['prompt_answer_pairs']}
        else:
            validate_calibration(calibration,root=root)
            if calibration['on'] != context.get('date',{}).get('value'):
                raise ProtocolError('Calibration date does not match the lesson')
            if calibration['profile']['id'] != context.get('active_year_profile',{}).get('value'):
                raise ProtocolError('Calibration profile does not match the lesson')
            values = calibration['values']
            expected = {'literacy':values['literacy_sequence_count'],
                        'numeracy':values['numeracy_prompt_answer_pairs']}
            if require_release:
                profile = YearProfileRegistry.load(root).get(values['active_year_profile'])
                if (calibration['profile']['release_mode'] != 'normal' or
                        values['main_curriculum_year'] not in profile['curriculum_anchor']['years']):
                    raise ProtocolError('Requested main curriculum has not been calibrated for classroom release')
        counts = context.get('warmup_counts',{})
        if not isinstance(counts,dict) or any(k not in expected or type(v) is not int or v != expected[k]
                                            for k,v in counts.items()):
            raise ProtocolError('Warm-up counts disagree with the resolved preferences/defaults')
        return []
    except (ValueError,OSError,KeyError,TypeError,AttributeError) as exc:
        return ['Invalid instructional calibration: '+str(exc)]


def prepare_host_context(context: dict, request: dict, *, settings: dict | None,
                         source_root: Path, request_source: str, root: Path = ROOT) -> dict:
    """Load host-selected private state before execution, never persist a model output.

    The trusted host owns request authentication and namespace selection. This
    helper verifies request/source binding and creates a private runtime sidecar;
    it is not proof that a deployment has a durable volume or an authorised user.
    """
    import copy
    from agent_protocol import safe_path,sha256_json
    if settings is not None and (not isinstance(settings,dict) or set(settings) != {'store','teacher','classroom'}):
        raise ProtocolError('Settings binding requires exactly store, teacher and classroom')
    result = copy.deepcopy(context)
    if result.get('instructional_calibration') is not None:
        raise ProtocolError('Resolve host settings from a fresh context, not a previously frozen run')
    source_root=Path(source_root).resolve()
    bindings=[item for item in result.get('source_provenance',[]) if item.get('path')==request_source]
    request_path=safe_path(source_root,request_source)
    if (len(bindings)!=1 or bindings[0].get('kind')!='user_request' or
            bindings[0].get('sha256')!=sha256_file(request_path) or read_json(request_path)!=request):
        raise ProtocolError('Current preference instruction must match its actual hashed request source')
    if request.get('requested_date') != result.get('date',{}).get('value'):
        raise ProtocolError('Request/context date mismatch')
    state = SettingsStore(Path(settings['store']),root=root).read(settings['teacher'],settings['classroom']) if settings else None
    scope=request.get('instructional_scope',{})
    if (not isinstance(scope,dict) or set(scope)-{'unit_id','lesson_id','progression_id'} or
            any(not isinstance(v,str) or not v.strip() for v in scope.values())):
        raise ProtocolError('Instructional scope needs explicit unit, lesson or progression identifiers')
    overrides=request.get('instructional_overrides')
    if overrides is not None: validate_values(overrides,root=root)
    calibration=resolve(state=state,on=request['requested_date'],overrides=overrides,
                        request_source=request_source,root=root,**scope)
    relative='.dlp-calibration/'+sha256_json(calibration)+'.json'
    path=safe_path(source_root,relative)
    if path.exists():
        if read_json(path)!=calibration:raise ProtocolError('Existing calibration sidecar changed')
    else:write_json_atomic(path,calibration,immutable=True)
    result['instructional_calibration']=calibration
    result['calibration_source']=relative
    result['active_year_profile']={'value':calibration['profile']['id'],'source':calibration['profile']['source'],'resolved':True}
    result['source_provenance'].append({'id':'instructional-calibration','kind':'runtime_school_source',
                                        'path':relative,'sha256':sha256_file(path)})
    return result


if __name__ == '__main__':
    raise SystemExit(main())
