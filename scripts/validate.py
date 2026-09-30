import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data/ontology.json').read_text())
sources = json.loads((root / 'data/sources.json').read_text())
from acceptance import validate_claims
validate_claims(data, sources)
site_data = json.loads((root / 'dist/data.json').read_text())
assert data == site_data, 'Published data differs from ontology source'
assert data['policy_snapshot'] == sources['snapshot_date'] == '2026-09-28'
node_ids = [n['id'] for n in data['nodes']]
edge_ids = [e['id'] for e in data['edges']]
source_ids = {s['id'] for s in sources['sources']}
assert len(node_ids) == len(set(node_ids)) and len(edge_ids) == len(set(edge_ids))
allowed = {'SOURCE', 'PARSED', 'NORMALIZED', 'INFERRED', 'PROVISIONAL', 'CONTESTED', 'REJECTED'}
for item in data['nodes'] + data['edges']:
    assert item['status'] in allowed and item['source_id'] in source_ids, item
for edge in data['edges']:
    assert edge['from'] in node_ids and edge['to'] in node_ids, edge
for student in data['students']:
    assert all(s in node_ids for s in student['grade7_standard_ids'])
assert data['students'][0]['grade7_standard_ids'] == data['students'][1]['grade7_standard_ids']
print(f"Valid: {len(node_ids)} nodes, {len(edge_ids)} edges, {len(source_ids)} source records")

for name in ['sources','corpus-plan','source-review']:
    assert json.loads((root / f'data/{name}.json').read_text()) == json.loads((root / f'dist/{name}.json').read_text()), name
plan = json.loads((root / 'data/corpus-plan.json').read_text())
review = json.loads((root / 'data/source-review.json').read_text())
assert len({f['id'] for f in plan['families']}) == len(plan['families'])
assert all(f['source_id'] in source_ids for f in plan['families'])
assert all(c['source_id'] in source_ids for c in review['claims'])
import hashlib
ingestion = None
if (root / 'data/ingestion-manifest.json').exists():
    from ingest_sources import check
    ingestion = check(root)
for source in sources['sources']:
    if source['acquisition_status'] == 'full-document-acquired':
        content = (root / source['archive_path']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == source['sha256']
        assert len(content) == source['bytes']
        if not (root / 'data/ingestion-manifest.json').exists():
            extracted = json.loads((root / 'sources/extracted' / (Path(source['archive_path']).stem + '.pages.json')).read_text())
            assert len(extracted['pages']) == source['page_count']
            assert extracted['sha256'] == source['sha256']
if ingestion:
    full_record = next(d for d in ingestion['documents'] if d['source_id'] == 'src:nysed:math-full')
    page_artifact = next(a for a in full_record['artifacts'] if a['path'].endswith('/pages.json'))
    full_text = json.loads((root / page_artifact['path']).read_text())
    # Public receipt images must be the same bytes as the hashed extraction bundles.
    public_evidence = {'src:nysed:math-full': 'math-full', 'src:nysed:math-2017': 'math-crosswalk', 'src:nysed:ela-full':'ela-full', 'src:nysed:science-full':'science-full', 'src:nysed:math-timeline-2023':'math-timeline', 'src:nysed:ela-math-roadmap-overview':'ela-math-roadmap'}
    for record in ingestion['documents']:
        if record['source_id'] not in public_evidence:
            continue
        for artifact in record['artifacts']:
            if artifact['path'].endswith('.png'):
                public_path = root / 'dist/evidence' / public_evidence[record['source_id']] / Path(artifact['path']).name
                assert hashlib.sha256(public_path.read_bytes()).hexdigest() == artifact['sha256'], public_path
else:
    full_text = json.loads((root / 'sources/extracted/nys-next-generation-mathematics-p-12-standards.pages.json').read_text())
page90 = ' '.join(full_text['pages'][89]['text'].split())
page_texts = {}
for record in ingestion['documents']:
    artifact = next(a for a in record['artifacts'] if a['path'].endswith('/pages.json'))
    page_texts[record['source_id']] = json.loads((root / artifact['path']).read_text())['pages']
def source_text(item):
    return ' '.join(page_texts[item['source_id']][item['pdf_page']-1]['text'].split())
for item in data['nodes']:
    if item.get('original_text'):
        assert ' '.join(item['original_text'].split()) in source_text(item), item['id']
assert len([n for n in data['nodes'] if n.get('parent_standard_id') == 'wc:standard:ny-7-rp-2']) == 4
for n in data['nodes']:
    for annotation in n.get('source_annotations', []):
        assert annotation['source_id'] in source_ids and 1 <= annotation['pdf_page'] <= len(page_texts[annotation['source_id']])
        assert ' '.join(annotation['original_text'].split()) in source_text(annotation), annotation['id']
    if n['type'] == 'Expectation':
        assert n['derived_from'] in node_ids and n.get('parsing_rationale'), n['id']
        assert any(e['from'] == n['id'] and e['to'] == n['derived_from'] and e['relation'] == 'DERIVED_FROM' for e in data['edges'])
for suffix in 'abcd':
    assert len([n for n in data['nodes'] if n['type'] == 'Expectation' and n.get('derived_from') == 'wc:standard:ny-7-rp-2' + suffix]) == 1
assert not any(e['relation'] in {'EXPECTED_BY', 'PREREQUISITE'} for e in data['edges'])
assert all(s['effective_date'] is None for s in sources['sources']), 'Do not invent exact effective days from month/season evidence'
print('Valid: source review and corpus inventory match public data; temporal precision preserved')

journey = json.loads((root / 'data/journey.json').read_text())
assert journey == json.loads((root / 'dist/journey.json').read_text())
assert journey['policy_snapshot'] == data['policy_snapshot']
assert journey['state'] == 'EXPECTED'
assert all(s['pathway_id'] == journey['id'] and s['state'] == 'EXPECTED' for s in data['students'])
assert [g for stage in journey['stages'] for g in stage['grades']] == list(range(13))
assert len({s['id'] for s in journey['stages']}) == 5
for stage in journey['stages']:
    assert stage['default_grade'] in stage['grades'] if stage['grades'] else stage['default_grade'] is None
    assert all(s in source_ids for s in stage.get('source_ids', []))
print('Valid: shared K–12 journey, 13 grades and transition scaffold; no mastery data')

for claim in review['claims']:
    if claim['status'] == 'SOURCE':
        assert ' '.join(claim['original_text'].split()) in source_text(claim), claim['id']
print('Valid: each source quotation checked against its own document and page')

from comparison_validation import check_comparisons
comparisons = json.loads((root/'data/comparisons.json').read_text())
assert comparisons == json.loads((root/'dist/comparisons.json').read_text()), 'Comparison export mismatch'
check_comparisons(comparisons, data, sources)
drafts = json.loads((root/'data/comparison-drafts.json').read_text())
assert len(drafts['records']) == len(comparisons['records']), 'Comparison draft count mismatch'
for draft, record in zip(drafts['records'], comparisons['records']):
    assert all(record.get(k) == v for k, v in draft.items()), 'Comparison draft/export mismatch'
for record in comparisons['records']:
    for evidence in record['evidence']:
        assert ' '.join(evidence['quotation'].split()) in source_text(evidence), record['id']
print('Valid: comparison evidence snapshots and exports; no graph promotion')

# A completed audit applies only to its exact reviewed data, not future edits.
release = json.loads((root/'dist/release.json').read_text())
if release.get('audit_status') == 'pass-with-recorded-limits':
    audit = json.loads((root/release['audit_record']).read_text())
    assert audit['result'] == release['audit_status'] and audit['release'] == data['release']
    assert not audit['blocking_findings'], 'Audit has blocking findings'
    required = {'data/ontology.json','data/comparisons.json','data/comparison-drafts.json','data/sources.json','data/journey.json'}
    assert set(audit['reviewed_sha256']) == required, 'Incomplete audit snapshot'
    for path, digest in audit['reviewed_sha256'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest, f'Stale independent audit: {path}'
    print('Valid: independent audit matches the exact reviewed data snapshot')
