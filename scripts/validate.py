import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data/ontology.json').read_text())
sources = json.loads((root / 'data/sources.json').read_text())
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
for source in sources['sources']:
    if source['acquisition_status'] == 'full-document-acquired':
        content = (root / source['archive_path']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == source['sha256']
        assert len(content) == source['bytes']
        extracted = json.loads((root / 'sources/extracted' / (Path(source['archive_path']).stem + '.pages.json')).read_text())
        assert len(extracted['pages']) == source['page_count']
        assert extracted['sha256'] == source['sha256']
full_text = json.loads((root / 'sources/extracted/nys-next-generation-mathematics-p-12-standards.pages.json').read_text())
page90 = ' '.join(full_text['pages'][89]['text'].split())
for item in data['nodes']:
    if item.get('original_text'):
        assert ' '.join(item['original_text'].split()) in page90, item['id']
assert len([n for n in data['nodes'] if n.get('parent_standard_id') == 'wc:standard:ny-7-rp-2']) == 4
assert all(s['effective_date'] is None for s in sources['sources']), 'Do not invent exact effective days from month/season evidence'
print('Valid: source review and corpus inventory match public data; temporal precision preserved')
