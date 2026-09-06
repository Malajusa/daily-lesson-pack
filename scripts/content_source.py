"""Shared source API for deck/PDF builders; no parallel rewriting of tasks."""
import argparse
import json
from pathlib import Path
from pack_evidence import read, validate_content, expected_checks, digest

class ContentSource:
    def __init__(self, path):
        self.path = Path(path)
        self.content = read(path)
        errors = validate_content(self.content)
        if errors:
            raise ValueError('\n'.join(errors))
        self.records = {t['id']:t for t in self.content['tasks']}
        self.records.update(self.content.get('documents', {}))
        self.bindings = []

    def text(self, record, field):
        return self.records[record]['fields'][field]

    def bind(self, artifact, record, field, page, **location):
        """Record shape_id (PPTX) or bbox in PDF points after final layout."""
        self.text(record, field)
        entry = dict(artifact=artifact, record=record, field=field, page=page, **location)
        self.bindings.append(entry)
        return entry

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--content', required=True)
    p.add_argument('--manifest', required=True)
    p.add_argument('--method', choices=['semantic','visual'], required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    source = ContentSource(args.content)
    manifest = read(args.manifest)
    from pack_evidence import ROOT
    record = {'schema_version':3, 'manifest_sha256':digest(args.manifest),
              'content_sha256':digest(args.content),
              'requirements_sha256':digest(ROOT/'references/qa-requirements.json'),
              'checks':[{'id':key,'subject':subject,'result':'UNREVIEWED','observation':'','citations':[]}
                        for key,subject in sorted(expected_checks(source.content,manifest,args.method))]}
    Path(args.out).write_text(json.dumps(record,indent=2)+'\n')

if __name__ == '__main__':
    main()
