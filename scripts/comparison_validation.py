"""Structural/evidence integrity checks, not an automated semantic verdict."""
from build_comparisons import fingerprint

AXES = ['Action', 'Object', 'Evidence', 'Required product', 'Placement', 'Boundary']

def check_comparisons(comparisons, model, manifest):
    def require(value, message):
        if not value:
            raise ValueError(message)
    nodes = {n['id']: n for n in model['nodes']}
    sources = {s['id']: s for s in manifest['sources']}
    require(comparisons['release'] == model['release'], 'Comparison release mismatch')
    require(comparisons['policy_snapshot'] == model['policy_snapshot'], 'Comparison snapshot mismatch')
    require(comparisons['reviewer_type'] == 'builder' and comparisons['independent_review'] == 'pending-package-3', 'Unsupported review promotion')
    ids = [r['id'] for r in comparisons['records']]
    require(len(ids) == len(set(ids)), 'Duplicate comparison ID')
    for r in comparisons['records']:
        require(r['status'] in {'PROVISIONAL', 'REJECTED'}, 'Unsupported comparison disposition')
        require(r['promoted_to_ontology'] is False, 'Comparison promotion is forbidden')
        require(r['review_status'] == 'builder-reviewed; independent review pending', 'Unsupported record review promotion')
        require(len(r['node_ids']) == 2 and len(set(r['node_ids'])) == 2, 'Invalid comparison pair')
        require(len(r['subjects']) == 2 and len(set(r['subjects'])) == 2, 'Invalid subject pair')
        for field in ['id','title','proposal','commonality','decision','not_established','next_evidence','source_context','disposition_label']:
            require(isinstance(r.get(field), str) and r[field].strip(), f'Missing comparison {field}')
        require([a['axis'] for a in r['axes']] == AXES, 'Incomplete comparison axes')
        require(all(isinstance(a.get(side),str) and a[side].strip() for a in r['axes'] for side in ['left','right']), 'Missing axis value')
        require([e['node_id'] for e in r['evidence']] == r['node_ids'], 'Evidence pair mismatch')
        for e in r['evidence']:
            n = nodes.get(e['node_id'])
            require(n and n['type'] == 'Expectation', 'Missing comparison expectation')
            parent = nodes[n['derived_from']]
            require(e['node_fingerprint'] == fingerprint(n), 'Stale expectation snapshot')
            require(e['standard_id'] == parent['id'] and e['standard_fingerprint'] == fingerprint(parent), 'Stale standard snapshot')
            for key in ['source_id','pdf_page','source_locator']:
                require(e[key] == parent[key], f'Comparison {key} mismatch')
            require(e['quotation'] == parent['original_text'], 'Comparison quotation mismatch')
            require(e['source_sha256'] == sources[e['source_id']]['sha256'], 'Comparison source hash mismatch')
        # Candidate records are not inserted into the graph or student projections.
        require(not any(r['id'] in [e['id'],e['from'],e['to']] for e in model['edges']), 'Comparison leaked into graph')
        require(not any(r['id'] == n['id'] for n in model['nodes']), 'Comparison leaked into nodes')
    return True
