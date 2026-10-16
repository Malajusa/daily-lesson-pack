"""Bounded structural evidence checks; source/teaching meaning needs semantic QA."""
from __future__ import annotations
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


def record(slide, marker):
    text = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ''
    lines = [x[len(marker):].strip() for x in text.splitlines() if x.startswith(marker)]
    if not lines:
        return None
    if len(lines) != 1:
        raise ValueError('exactly one notes record required')
    value = json.loads(lines[0])
    if not isinstance(value, dict):
        raise ValueError('notes record must be an object')
    return value


def cue_status(role, target, previous, prior_cues, history_known):
    if role in {'REMINDER', 'SUPPORT', 'RETRY'}:
        return 'supported'
    if target in previous or prior_cues:
        return 'recently_cued'
    return 'no_identified_recent_target_cue' if history_known is True else 'unknown'


def audit_literacy(entries, presentation, count):
    """Return None for legacy/default decks; mode-aware issues otherwise."""
    records = []
    errors = []
    def fail(code, slide=0):
        errors.append(dict(code=code, message=code.replace('_', ' '), slide=slide))
    for entry in entries:
        try:
            data = record(presentation.slides[entry['slide']-1], 'DLP_LITERACY:')
        except (ValueError, TypeError):
            data = {}; fail('literacy_evidence_invalid', entry['slide'])
        records.append(data)
    if not any(x is not None for x in records):
        return None
    groups = defaultdict(list)
    previous = set()
    for entry, data in zip(entries, records):
        n = entry['slide']; role = entry['role']
        if not isinstance(data, dict) or not data:
            fail('literacy_evidence_missing', n); continue
        target = data.get('target_rule')
        if not isinstance(target, str) or not target.strip():
            fail('literacy_target_missing', n); target = ''
        if data.get('mode') not in {'supported_practice','question_first_check'}:
            fail('literacy_mode_invalid', n)
        if data.get('mode') == 'question_first_check' and not (isinstance(data.get('selection_source'), str) and data['selection_source'].strip()):
            fail('literacy_selection_missing', n)
        groups[entry['number']].append((entry, data))
        if role in {'QUESTION','RETRY'}:
            prior = data.get('prior_cues'); known = data.get('history_known')
            if not isinstance(prior, list) or not all(isinstance(x,str) and x.strip() for x in prior) or not isinstance(known,bool):
                fail('literacy_cue_history_invalid',n); prior=[]; known=False
            expected = cue_status(role, target, previous, prior, known)
            if data.get('mode') == 'supported_practice': expected = 'supported'
            if data.get('cue_status') != expected:
                fail('literacy_cue_label_inaccurate',n)
            if 'response' in data or 'result' in data:
                fail('literacy_attempts_not_separated',n)
        # Earlier questions can also rehearse the target, as can feedback/reminders.
        previous.add(target)
    if sorted(groups) != list(range(1,count+1)):
        fail('literacy_warmup_count')
    for rows in groups.values():
        roles=[e['role'] for e,d in rows]; mode=rows[0][1].get('mode')
        allowed= [['REMINDER','QUESTION','ANSWER']] if mode=='supported_practice' else [['QUESTION','ANSWER'],['QUESTION','SUPPORT','RETRY','ANSWER']]
        if roles not in allowed: fail('literacy_warmup_mode_sequence',rows[0][0]['slide'])
        if len({d.get('target_rule') for e,d in rows}) != 1 or len({d.get('mode') for e,d in rows}) != 1:
            fail('literacy_item_identity_mismatch',rows[0][0]['slide'])
        slides=[e['slide'] for e,d in rows]
        if slides != list(range(slides[0],slides[0]+len(slides))): fail('literacy_feedback_not_adjacent',slides[0])
        if any(e['total'] != count for e,d in rows): fail('literacy_warmup_total',slides[0])
    # Disallow repeated/interleaved item runs and out-of-order item numbers.
    runs=[]
    for e in entries:
        if not runs or runs[-1]!=e['number']:runs.append(e['number'])
    if runs != list(range(1,count+1)): fail('literacy_warmup_item_order')
    return errors


def _normal(text):
    return ' '.join(text.split())


def audit_reading(presentation, deck_path):
    errors=[]; sources={}; models=set(); stages=[]; active=False; pending=None
    def fail(code,n):errors.append(dict(code=code,message=code.replace('_',' '),slide=n))
    records=[]
    for n,slide in enumerate(presentation.slides,1):
        try:data=record(slide,'DLP_READING:')
        except (ValueError,TypeError):fail('reading_evidence_invalid',n);data={}
        if data is not None: active=True;records.append((n,data))
    if not active:return []
    for n,data in records:
        role=data.get('role');sid=data.get('source_id')
        if not isinstance(sid,str) or not sid:fail('reading_source_id_missing',n);continue
        if role=='SOURCE':
            if sid in sources:fail('reading_source_duplicate',n)
            source=data.get('source_text','')
            if not isinstance(source,str) or not source.strip():fail('reading_source_empty',n);continue
            sources[sid]=source
            try:
                path=(Path(deck_path).parent/data['handout_path']).resolve()
                if hashlib.sha256(path.read_bytes()).hexdigest()!=data['handout_sha256']:
                    fail('reading_handout_hash_mismatch',n)
                import fitz
                with fitz.open(path) as pdf: text=' '.join(p.get_text() for p in pdf)
                if _normal(source) not in _normal(text):fail('reading_handout_text_mismatch',n)
            except (KeyError,OSError,ValueError,TypeError,ImportError):fail('reading_source_access_unverified',n)
        elif role=='MODEL':
            if sid not in sources:fail('reading_source_not_available',n)
            if not (isinstance(data.get('think_aloud'), str) and data['think_aloud'].strip()):fail('reading_think_aloud_missing',n)
            models.add(sid)
        elif role in {'QUESTION','ANSWER'}:
            if data.get('mode')!='whole_text':fail('reading_mode_invalid',n)
            if role=='QUESTION' and not (isinstance(data.get('selection_source'), str) and data['selection_source'].strip()):fail('reading_selection_missing',n)
            if sid not in sources:fail('reading_source_not_available',n)
            if sid not in models:fail('reading_model_missing',n)
            stage=data.get('stage')
            if stage not in {'guided','reduced_support'}:fail('reading_stage_invalid',n)
            if role=='QUESTION':
                if pending is not None:fail('reading_feedback_missing',n)
                pending=(n,sid,stage)
                if stage=='reduced_support' and (sid,'guided') not in stages:fail('reading_guided_stage_missing',n)
                stages.append((sid,stage))
            if role=='ANSWER':
                if pending != (n-1,sid,stage):fail('reading_feedback_identity_mismatch',n)
                pending=None
            quotes=data.get('evidence_quotes')
            if not isinstance(quotes,list) or not quotes or any(not isinstance(q,str) or not q.strip() or q not in sources.get(sid,'') for q in quotes):fail('reading_evidence_quote_unsupported',n)
            if data.get('independent_transfer') is True:fail('reading_false_transfer_claim',n)
        else:fail('reading_role_invalid',n)
    if pending is not None:fail('reading_feedback_missing',pending[0])
    for sid in sources:
        if (sid,'guided') not in stages or (sid,'reduced_support') not in stages:fail('reading_application_stages_missing',0)
    # Require metadata on every numbered reading pair in a whole-text sequence.
    covered={n for n,d in records if d.get('role') in {'QUESTION','ANSWER'}}
    for n,slide in enumerate(presentation.slides,1):
        text='\n'.join(sh.text for sh in slide.shapes if sh.has_text_frame)
        if re.search(r'SHARED\s+READING\s+\d+\s+OF\s+\d+',text,re.I) and n not in covered:
            fail('reading_pair_evidence_missing',n)
    return errors
