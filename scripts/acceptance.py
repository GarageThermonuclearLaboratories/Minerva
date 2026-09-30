"""Bounded claim acceptance rules; no inferred relation is admitted implicitly."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'SOURCE', 'PARSED', 'NORMALIZED', 'INFERRED', 'PROVISIONAL', 'CONTESTED', 'REJECTED'}
TYPES = {'Grade', 'GradeBand', 'Subject', 'Domain', 'Standard', 'Expectation', 'Concept'}
RELATIONS = {
    'PART_OF': {('Standard', 'Standard'), ('Standard', 'Domain')},
    'ASSIGNED_TO_GRADE': {('Standard', 'Grade')},
    'ASSIGNED_TO_GRADE_BAND': {('Standard', 'GradeBand')},
    'DERIVED_FROM': {('Expectation', 'Standard'), ('Concept', 'Standard')},
    'USES_CONCEPT': {('Expectation', 'Concept')},
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def eligible(item):
    # SOURCE/PARSED here means source-edition projection, not verified policy applicability.
    return bool(item) and item.get('status') in {'SOURCE', 'PARSED'}

def standards_for_grade(data, grade):
    nodes = {n['id']: n for n in data['nodes']}
    def active(n, seen=None):
        seen = set() if seen is None else seen
        if not eligible(n) or n['id'] in seen:
            return False
        parent = n.get('parent_standard_id')
        if not parent:
            return True
        link = any(e['relation'] == 'PART_OF' and e['from'] == n['id'] and e['to'] == parent and eligible(e) for e in data['edges'])
        return link and active(nodes.get(parent), seen | {n['id']})
    ids = {e['from'] for e in data['edges'] if e['relation'] == 'ASSIGNED_TO_GRADE'
           and e['to'] == f'wc:grade:{grade}' and eligible(e) and eligible(nodes.get(e['to']))}
    return [n['id'] for n in data['nodes'] if n['type'] == 'Standard' and n['id'] in ids and active(n)]

def standards_for_band(data, band_id):
    nodes = {n['id']: n for n in data['nodes']}
    ids = {e['from'] for e in data['edges'] if e['relation'] == 'ASSIGNED_TO_GRADE_BAND'
           and e['to'] == band_id and eligible(e) and eligible(nodes.get(band_id))}
    return [n['id'] for n in data['nodes'] if n['type'] == 'Standard' and n['id'] in ids and eligible(n)]

def validate_claims(data, manifest):
    nodes = {n['id']: n for n in data['nodes']}
    sources = {s['id']: s for s in manifest['sources']}
    items = data['nodes'] + data['edges']
    require(len({i['id'] for i in items}) == len(items), 'Duplicate claim ID')
    for item in items:
        ident = item['id']
        require(item.get('status') in STATUSES, f'{ident}: invalid status')
        source = sources.get(item.get('source_id'))
        require(source is not None, f'{ident}: unknown source')
        for field in ['source_locator', 'review_status']:
            require(isinstance(item.get(field), str) and bool(item[field].strip()), f'{ident}: missing {field}')
        page = item.get('pdf_page')
        require(type(page) is int and 1 <= page <= (source.get('page_count') or 0), f'{ident}: invalid source page')
        require(source.get('acquisition_status') == 'full-document-acquired', f'{ident}: source bytes not acquired')
    for n in nodes.values():
        ident = n['id']
        require(n.get('type') in TYPES, f'{ident}: unknown node type')
        if n['type'] == 'GradeBand':
            grades = n.get('grades')
            require(isinstance(grades, list) and bool(grades) and all(type(g) is int and 0 <= g <= 12 for g in grades) and grades == sorted(set(grades)), f'{ident}: invalid grade band')
        if n.get('grade_band_id'):
            band = nodes.get(n['grade_band_id'])
            require(band is not None and band['type'] == 'GradeBand', f'{ident}: invalid grade-band target')
            require(any(e['relation'] == 'ASSIGNED_TO_GRADE_BAND' and e['from'] == ident and e['to'] == band['id'] for e in data['edges']), f'{ident}: missing grade-band assignment')
            require(not any(e['relation'] == 'ASSIGNED_TO_GRADE' and e['from'] == ident for e in data['edges']), f'{ident}: unsupported exact-grade assignment')
        if n['type'] == 'Standard':
            require(bool(n.get('original_text', '').strip()), f'{ident}: missing source wording')
        if n['type'] in {'Expectation', 'Concept'}:
            parent = nodes.get(n.get('derived_from'))
            require(parent is not None and parent['type'] == 'Standard', f'{ident}: invalid derivation')
            require(bool(n.get('parsing_rationale', '').strip()), f'{ident}: missing parsing rationale')
            require(n['source_id'] == parent['source_id'] and n['pdf_page'] == parent['pdf_page'], f'{ident}: derivation provenance differs')
        if n['type'] == 'Expectation':
            for field in ['action', 'object']:
                require(bool(n.get(field, '').strip()), f'{ident}: missing {field}')
            require(isinstance(n.get('qualifiers'), list) and all(isinstance(q, str) and q.strip() for q in n['qualifiers']), f'{ident}: invalid qualifiers')
            require(any(e['relation'] == 'DERIVED_FROM' and e['from'] == ident and e['to'] == n['derived_from'] for e in data['edges']), f'{ident}: missing derivation edge')
        if n.get('parent_standard_id'):
            parent = nodes.get(n['parent_standard_id'])
            require(parent is not None and parent['type'] == 'Standard', f'{ident}: invalid parent')
            require(any(e['relation'] == 'PART_OF' and e['from'] == ident and e['to'] == parent['id'] for e in data['edges']), f'{ident}: missing parent edge')
            seen = {ident}
            while parent:
                require(parent['id'] not in seen, f'{ident}: cyclic parent chain')
                seen.add(parent['id'])
                parent = nodes.get(parent.get('parent_standard_id'))
    for e in data['edges']:
        a, b = nodes.get(e['from']), nodes.get(e['to'])
        require(a is not None and b is not None, f"{e['id']}: missing endpoint")
        require((a['type'], b['type']) in RELATIONS.get(e['relation'], set()), f"{e['id']}: unsupported relation or endpoint types")
        require(e['source_id'] == a['source_id'] and e['pdf_page'] == a['pdf_page'], f"{e['id']}: edge provenance differs")
        if e['relation'] == 'DERIVED_FROM':
            require(a.get('derived_from') == b['id'], f"{e['id']}: contradictory derivation")
        if e['relation'] == 'ASSIGNED_TO_GRADE_BAND':
            require(a.get('grade_band_id') == b['id'], f"{e['id']}: contradictory grade-band assignment")
    expected = standards_for_grade(data, 7)
    for student in data['students']:
        require(student['grade7_standard_ids'] == expected, f"{student['id']}: stale or inadmissible expected projection")
        require(student['middle_school_band_standard_ids'] == standards_for_band(data, 'wc:grade-band:6-8'), f"{student['id']}: stale or inadmissible band projection")
    for fixture_path in sorted((ROOT / 'data/acceptance').glob('*.json')):
        fixture = json.loads(fixture_path.read_text())
        for ident, fields in fixture.get('nodes', {}).items():
            for field, value in fields.items():
                require(nodes.get(ident, {}).get(field) == value, f'{ident}: source-reviewed {field} changed; review required')
        for ident, wording in fixture.get('standards', {}).items():
            require(nodes.get(ident, {}).get('original_text') == wording, f'{ident}: source wording changed; review required')
        for ident, fields in fixture['expectations'].items():
            n = nodes.get(ident)
            require(n is not None, f'{ident}: missing bounded expectation')
            for field, value in fields.items():
                require(n.get(field) == value, f'{ident}: source-reviewed {field} changed; review required')
        for ident, fields in fixture['annotations'].items():
            annotations = {a['id']: a for n in nodes.values() for a in n.get('source_annotations', [])}
            require(ident in annotations, f'{ident}: missing source annotation')
            for field, value in fields.items():
                require(annotations[ident].get(field) == value, f'{ident}: source annotation {field} changed; review required')
