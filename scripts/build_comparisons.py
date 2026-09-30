"""Freeze evidence snapshots for the authored comparisons; never promote ontology edges."""
import argparse
import json
from pathlib import Path
from comparison_contract import fingerprint, load_baseline, verify_inputs

ROOT = Path(__file__).resolve().parents[1]

def build(baseline_path):
    model = json.loads((ROOT/'data/ontology.json').read_text())
    sources = json.loads((ROOT/'data/sources.json').read_text())
    draft = json.loads((ROOT/'data/comparison-drafts.json').read_text())
    baseline = load_baseline(baseline_path)
    verify_inputs(model, draft, baseline)
    nodes = {n['id']: n for n in model['nodes']}
    manifests = {s['id']: s for s in sources['sources']}
    result = dict(version='1', release=model['release'], input_research_commit=baseline['input_research_commit'],
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
    from comparison_validation import check_comparisons
    check_comparisons(result, model, sources, baseline=baseline, draft=draft)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    for p in ['data/comparisons.json', 'dist/comparisons.json']:
        (ROOT/p).write_text(encoded)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', required=True, type=Path, help='Explicit reviewed comparison baseline contract')
    args = parser.parse_args()
    print(f"Built {len(build(args.baseline)['records'])} comparison records; no ontology promotion")
