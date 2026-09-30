"""Freeze evidence snapshots for the authored comparisons; never promote ontology edges."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def build():
    model = json.loads((ROOT/'data/ontology.json').read_text())
    sources = json.loads((ROOT/'data/sources.json').read_text())
    draft = json.loads((ROOT/'data/comparison-drafts.json').read_text())
    nodes = {n['id']: n for n in model['nodes']}
    manifests = {s['id']: s for s in sources['sources']}
    result = dict(version='1', release=model['release'], input_research_commit='6b64e00d3fe710ebb256770cdd475c9cfded88c1',
                  policy_snapshot=model['policy_snapshot'], date='2026-09-30', reviewer_type='builder',
                  independent_review='pending-package-3', method=draft['method'], scope=draft['scope'], records=[])
    for raw in draft['records']:
        record = dict(raw, promoted_to_ontology=False, review_status='builder-reviewed; independent review pending', evidence=[])
        for ident in raw['node_ids']:
            n = nodes[ident]; parent = nodes[n['derived_from']]; source = manifests[parent['source_id']]
            record['evidence'].append(dict(node_id=ident, node_fingerprint=fingerprint(n), standard_id=parent['id'],
                standard_fingerprint=fingerprint(parent), source_id=parent['source_id'], source_sha256=source['sha256'],
                pdf_page=parent['pdf_page'], source_locator=parent['source_locator'], quotation=parent['original_text']))
        result['records'].append(record)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    for p in ['data/comparisons.json', 'dist/comparisons.json']:
        (ROOT/p).write_text(encoded)
    return result

if __name__ == '__main__':
    print(f"Built {len(build()['records'])} comparison records; no ontology promotion")
