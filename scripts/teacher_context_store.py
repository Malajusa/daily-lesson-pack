#!/usr/bin/env python3
"""Private, revisioned SQLite settings for a trusted host, never a learner database.

Namespace isolation is not authentication. The host authenticates the teacher,
chooses the namespace and supplies authority from an actual teacher request.
Keep this database on the host's private persistent volume, outside the package.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import copy
from datetime import date
import json
import os
from pathlib import Path
import sqlite3
import sys

from agent_protocol import ProtocolError, parse_json, json_bytes

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'active_year_profile', 'main_curriculum_year', 'retrieval_years',
          'differentiation_mode', 'locale', 'timezone', 'literacy_sequence_count',
          'numeracy_prompt_answer_pairs'}

class SettingsError(ProtocolError):
    """A settings operation failed or cannot be authorised by this host."""


def validate_values(values: dict, *, root: Path = ROOT) -> None:
    if not isinstance(values, dict) or not values or set(values) - FIELDS:
        raise SettingsError('Unknown/empty settings; timetable, focus and attainment are not preferences')
    json_bytes(values)
    for name, value in values.items():
        if name in ('main_curriculum_year','literacy_sequence_count','numeracy_prompt_answer_pairs'):
            limit = 12 if name == 'main_curriculum_year' else 20
            if type(value) is not int or not 1 <= value <= limit:
                raise SettingsError(f'{name} must be an integer from 1 to {limit}')
        elif name == 'retrieval_years':
            if (not isinstance(value,list) or any(type(y) is not int or not 1 <= y <= 12 for y in value)
                    or len(value) != len(set(value))):
                raise SettingsError('retrieval_years must contain unique year numbers')
        elif name == 'active_year_profile':
            from year_profile_registry import YearProfileRegistry
            YearProfileRegistry.load(root).get(value)
        elif name == 'differentiation_mode' and value != 'point-of-need':
            raise SettingsError('Fixed year/ability membership is not a supported differentiation mode')
        elif name == 'timezone':
            from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
            try:
                if not isinstance(value,str): raise ValueError('Timezone must be text')
                ZoneInfo(value)
            except (ValueError, ZoneInfoNotFoundError) as exc:
                raise SettingsError('Unknown timezone') from exc
        elif name == 'locale' and value not in ('en-AU', 'en-GB', 'en-US', 'en-NZ'):
            raise SettingsError('Unsupported locale; add a verified convention before using another locale')


def validate_scope(scope: dict) -> None:
    if not isinstance(scope,dict): raise SettingsError('Scope must be an object')
    kind = scope.get('kind')
    expected = {'standing':{'kind'}, 'date':{'kind','start','end'},
                'unit':{'kind','id'}, 'lesson':{'kind','id'}, 'progression':{'kind','id'}}
    if kind not in expected or set(scope) != expected[kind]:
        raise SettingsError('Scope fields do not match standing/date/unit/lesson/progression')
    if kind == 'date':
        try:
            start, end = date.fromisoformat(scope['start']), date.fromisoformat(scope['end'])
            if start > end: raise ValueError('Reversed date range')
        except (ValueError,TypeError) as exc: raise SettingsError('Invalid date scope') from exc
    elif kind != 'standing' and (not isinstance(scope['id'],str) or not scope['id'].strip()):
        raise SettingsError('Scope needs an explicit identifier')


def validate_state(state: dict, *, root: Path = ROOT) -> None:
    if (not isinstance(state,dict) or state.get('schema_version') != 1 or
            type(state.get('revision')) is not int or state['revision'] < 0 or
            not isinstance(state.get('entries'),list) or set(state) != {'schema_version','revision','entries'}):
        raise SettingsError('Unknown or corrupt settings snapshot')
    seen = set()
    for entry in state['entries']:
        if not isinstance(entry,dict): raise SettingsError('Invalid settings entry')
        if set(entry) != {'values','scope','revision','source'}:
            raise SettingsError('Unknown settings entry fields')
        validate_values(entry.get('values'),root=root)
        validate_scope(entry.get('scope'))
        scope_key = json.dumps(entry['scope'],sort_keys=True)
        for field in entry['values']:
            key=(scope_key,field)
            if key in seen: raise SettingsError('Duplicate field in the same settings scope')
            seen.add(key)
        if (type(entry.get('revision')) is not int or not 1 <= entry['revision'] <= state['revision']
                or not isinstance(entry.get('source'),str) or not entry['source'].strip()):
            raise SettingsError('Settings entry has invalid revision/source')


def _authority(authority: dict) -> str:
    if (not isinstance(authority,dict) or authority.get('kind') != 'teacher_request'
            or not isinstance(authority.get('source_id'),str) or not authority['source_id'].strip()):
        raise SettingsError('Only an authenticated host handling a teacher request may change settings')
    return authority['source_id']


def _namespace(teacher: str, classroom: str) -> None:
    if any(not isinstance(v,str) or not v.strip() or len(v)>200 or '\x00' in v for v in (teacher,classroom)):
        raise SettingsError('Teacher and classroom identifiers must be explicit non-empty strings')


class SettingsStore:
    def __init__(self, path: Path, *, root: Path = ROOT):
        self.root = Path(root).resolve()
        self.path = Path(path).expanduser().resolve()
        if self.path.is_relative_to(self.root):
            raise SettingsError('Private settings must be outside the repository/installed package')

    @contextmanager
    def _connection(self, *, write=False):
        connection = None
        created = False
        try:
            if write:
                self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
                try:
                    fd = os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                    os.close(fd)
                    created = True
                except FileExistsError: pass
            connection = sqlite3.connect(self.path.as_uri()+('?mode=rw' if write else '?mode=ro'),
                                         uri=True,timeout=10,isolation_level=None)
            connection.execute('PRAGMA busy_timeout=10000')
            if write:
                connection.execute('PRAGMA synchronous=FULL')
                connection.execute('PRAGMA secure_delete=ON')
                connection.execute('BEGIN IMMEDIATE')
            version = connection.execute('PRAGMA user_version').fetchone()[0]
            if created and version == 0:
                connection.execute('CREATE TABLE snapshots (teacher TEXT NOT NULL, classroom TEXT NOT NULL, '
                                   'revision INTEGER NOT NULL, payload TEXT NOT NULL, '
                                   'PRIMARY KEY(teacher,classroom,revision))')
                connection.execute('PRAGMA user_version=1')
                # Commit schema creation independently of the first preference write.
                # A rejected compare-and-swap must not leave a poisoned empty file.
                connection.commit()
                if write:
                    connection.execute('BEGIN IMMEDIATE')
            elif version != 1:
                raise SettingsError('Unknown/corrupt settings database version; no automatic reset')
            yield connection
            if write: connection.commit()
        except (OSError,sqlite3.Error) as exc:
            if connection is not None and connection.in_transaction: connection.rollback()
            raise SettingsError('Settings operation failed; save is not confirmed: '+str(exc)) from exc
        except Exception:
            if connection is not None and connection.in_transaction: connection.rollback()
            raise
        finally:
            if connection is not None: connection.close()

    def _read(self, connection, teacher, classroom, revision=None):
        query = 'SELECT revision,payload FROM snapshots WHERE teacher=? AND classroom=?'
        params = [teacher,classroom]
        if revision is not None:
            query += ' AND revision=?'; params.append(revision)
        row = connection.execute(query+' ORDER BY revision DESC LIMIT 1',params).fetchone()
        result = parse_json(row[1]) if row else {'schema_version':1,'revision':0,'entries':[]}
        validate_state(result,root=self.root)
        if row and row[0] != result['revision']:
            raise SettingsError('Settings row and payload revisions disagree')
        if row is None and revision not in (None,0):
            raise SettingsError('Missing historical settings revision')
        return result

    def read(self, teacher: str, classroom: str) -> dict:
        _namespace(teacher,classroom)
        if not self.path.exists(): return {'schema_version':1,'revision':0,'entries':[]}
        with self._connection() as conn: return self._read(conn,teacher,classroom)

    def history(self, teacher: str, classroom: str) -> list[dict]:
        _namespace(teacher,classroom)
        if not self.path.exists(): return []
        with self._connection() as conn:
            rows = conn.execute('SELECT revision,payload FROM snapshots WHERE teacher=? AND classroom=? ORDER BY revision',
                                (teacher,classroom)).fetchall()
            states = []
            for revision, payload in rows:
                state = parse_json(payload)
                validate_state(state,root=self.root)
                if revision != state['revision']:
                    raise SettingsError('Historical settings row and payload revisions disagree')
                states.append(state)
            return states

    def _mutate(self, teacher, classroom, expected_revision, authority, operation):
        _namespace(teacher,classroom)
        source = _authority(authority)
        if type(expected_revision) is not int or expected_revision < 0:
            raise SettingsError('A non-negative expected_revision is required')
        with self._connection(write=True) as conn:
            old = self._read(conn,teacher,classroom)
            if old['revision'] != expected_revision:
                raise SettingsError('Settings revision conflict; reload before applying the teacher change')
            new = operation(conn,copy.deepcopy(old),source)
            new['revision'] = expected_revision+1
            validate_state(new,root=self.root)
            text = json_bytes(new).decode('utf-8')
            conn.execute('INSERT INTO snapshots VALUES (?,?,?,?)',(teacher,classroom,new['revision'],text))
        # A new connection verifies the specific committed revision, not merely in-memory state.
        with self._connection() as conn:
            confirmed = self._read(conn,teacher,classroom,new['revision'])
        if confirmed != new: raise SettingsError('Read-after-write verification failed; save unconfirmed')
        return confirmed

    def change(self, teacher, classroom, values, *, expected_revision, authority, scope):
        _authority(authority)
        validate_values(values,root=self.root)
        validate_scope(scope)
        def operation(conn, old, source):
            for entry in old['entries']:
                if entry['scope'] == scope:
                    entry['values'] = {k:v for k,v in entry['values'].items() if k not in values}
            old['entries'] = [e for e in old['entries'] if e['values']]
            old['entries'].append({'values':copy.deepcopy(values),'scope':copy.deepcopy(scope),
                                   'source':source,'revision':old['revision']+1})
            return old
        return self._mutate(teacher,classroom,expected_revision,authority,operation)

    def undo(self, teacher, classroom, *, expected_revision, authority):
        def operation(conn, old, source):
            if old['revision'] < 1: raise SettingsError('No settings change to undo')
            return self._read(conn,teacher,classroom,old['revision']-1)
        return self._mutate(teacher,classroom,expected_revision,authority,operation)

    def forget(self, teacher, classroom, fields, *, expected_revision, authority):
        if not isinstance(fields,list) or not fields or set(fields)-FIELDS:
            raise SettingsError('Specify known fields to forget')
        def strip(state):
            for entry in state['entries']:
                entry['values'] = {k:v for k,v in entry['values'].items() if k not in fields}
            state['entries'] = [e for e in state['entries'] if e['values']]
            return state
        def operation(conn, old, source):
            rows = conn.execute('SELECT revision,payload FROM snapshots WHERE teacher=? AND classroom=?',
                                (teacher,classroom)).fetchall()
            for revision,payload in rows:
                redacted = strip(parse_json(payload))
                conn.execute('UPDATE snapshots SET payload=? WHERE teacher=? AND classroom=? AND revision=?',
                             (json_bytes(redacted).decode(),teacher,classroom,revision))
            return strip(old)
        return self._mutate(teacher,classroom,expected_revision,authority,operation)

    def reset(self, teacher, classroom, *, expected_revision, authority):
        return self.forget(teacher,classroom,sorted(FIELDS),expected_revision=expected_revision,authority=authority)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['show','export','change','undo','forget','reset'])
    parser.add_argument('--store',type=Path,required=True)
    parser.add_argument('--teacher',required=True); parser.add_argument('--classroom',required=True)
    parser.add_argument('--expected-revision',type=int); parser.add_argument('--source-id')
    parser.add_argument('--teacher-authorised',action='store_true')
    parser.add_argument('--values'); parser.add_argument('--scope',default='{"kind":"standing"}')
    parser.add_argument('--fields',nargs='+')
    args=parser.parse_args()
    try:
        store=SettingsStore(args.store)
        if args.operation in ('show','export'): result=store.read(args.teacher,args.classroom)
        else:
            authority={'kind':'teacher_request' if args.teacher_authorised else 'untrusted','source_id':args.source_id}
            kwargs={'expected_revision':args.expected_revision,'authority':authority}
            if args.operation=='change':
                result=store.change(args.teacher,args.classroom,parse_json(args.values),scope=parse_json(args.scope),**kwargs)
            elif args.operation=='forget': result=store.forget(args.teacher,args.classroom,args.fields,**kwargs)
            else: result=getattr(store,args.operation)(args.teacher,args.classroom,**kwargs)
        print(json_bytes(result).decode(),end=''); return 0
    except (ValueError,OSError,TypeError) as exc: parser.exit(1,str(exc)+'\n')

if __name__=='__main__': raise SystemExit(main())
