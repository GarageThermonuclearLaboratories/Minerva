"""Reassemble any split archived source, verifying bytes before an atomic write."""
import hashlib
import json
from pathlib import Path
from ingest_sources import ROOT, inside

def restore(root=ROOT):
    for source in json.loads((root/'data/sources.json').read_text())['sources']:
        if not source.get('archive_parts'):
            continue
        target=inside(root,source['archive_path'])
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest()!=source['sha256']:
                raise ValueError('Existing archive differs: '+source['id'])
            continue
        chunks=[]
        for part in source['archive_parts']:
            blob=inside(root,part['path']).read_bytes()
            if hashlib.sha256(blob).hexdigest()!=part['sha256']:
                raise ValueError('Archive part differs: '+part['path'])
            chunks.append(blob)
        blob=b''.join(chunks)
        if len(blob)!=source['bytes'] or hashlib.sha256(blob).hexdigest()!=source['sha256']:
            raise ValueError('Reassembled archive differs: '+source['id'])
        temporary=target.with_suffix('.restore.tmp')
        with temporary.open('xb') as f: f.write(blob)
        temporary.replace(target)
        print('Restored exact bytes:',source['id'])
if __name__=='__main__': restore()
