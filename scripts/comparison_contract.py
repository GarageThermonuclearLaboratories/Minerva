"""Bounded comparison input contract. Integrity checks are not semantic review."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_FIELDS = ['policy_snapshot', 'nodes', 'edges', 'students', 'hypotheses', 'findings']

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def load_baseline(path=ROOT/'data/comparison-baseline.json'):
    return json.loads(Path(path).read_text())

def verify_inputs(model, draft, baseline):
    if baseline.get('model_fields') != MODEL_FIELDS:
        raise ValueError('Invalid baseline field coverage')
    if fingerprint({key: model[key] for key in MODEL_FIELDS}) != baseline['model_fingerprint']:
        raise ValueError('Changed model requires explicit baseline review')
    for key in ['method', 'scope']:
        if draft.get(key) != baseline[key]:
            raise ValueError(f'Comparison {key} differs from reviewed contract')

def verify_subjects(record, nodes, baseline):
    for subject, ident in zip(record['subjects'], record['node_ids']):
        expectation = nodes[ident]
        parent = nodes[expectation['derived_from']]
        binding = baseline['subject_bindings'].get(parent['source_id'])
        if not binding or expectation['source_id'] != parent['source_id']:
            raise ValueError('Comparison subject source mismatch')
        subject_node = nodes.get(binding['id'], {})
        if (subject != binding['label'] or subject_node.get('label') != subject
                or subject_node.get('type') != 'Subject'
                or subject_node.get('source_id') != parent['source_id']):
            raise ValueError('Comparison subject identity mismatch')
