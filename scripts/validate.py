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
