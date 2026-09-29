"""Negative tests for the acceptance boundary; originals are never mutated."""
import copy
import json
import unittest
from pathlib import Path
from acceptance import validate_claims, standards_for_grade
ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT/'data/ontology.json').read_text())
SOURCES = json.loads((ROOT/'data/sources.json').read_text())

class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(BASE)
    def node(self, suffix):
        return next(n for n in self.data['nodes'] if n['id'].endswith(suffix))
    def invalid(self, message):
        with self.assertRaisesRegex(ValueError, message):
            validate_claims(self.data, SOURCES)
    def test_baseline(self):
        validate_claims(self.data, SOURCES)
    def test_unknown_relation(self):
        self.data['edges'][0]['relation']='UNSUPPORTED_RELATION'
        self.invalid('unsupported relation')
    def test_wrong_endpoint_type(self):
        self.data['edges'][0]['to']='wc:grade:7'
        self.invalid('endpoint types')
    def test_missing_locator(self):
        del self.node('ny-7-rp-2')['source_locator']
        self.invalid('missing source_locator')
    def test_missing_edge_locator(self):
        del self.data['edges'][0]['source_locator']
        self.invalid('missing source_locator')
    def test_invalid_page(self):
        self.node('ny-7-rp-2')['pdf_page']=9999
        self.invalid('invalid source page')
    def test_missing_concept_rationale(self):
        del self.node('concept:proportional-relationship')['parsing_rationale']
        self.invalid('missing parsing rationale')
    def test_changed_derivation(self):
        self.node('identify-unit-rate')['derived_from']='wc:grade:7'
        self.invalid('invalid derivation')
    def test_lost_representation(self):
        self.node('identify-unit-rate')['qualifiers'].pop()
        self.invalid('qualifiers changed')
    def test_all_qualifiers_deleted(self):
        self.node('identify-unit-rate')['qualifiers']=[]
        self.invalid('qualifiers changed')
    def test_lost_unit_rate_qualifier(self):
        self.node('explain-proportional-point')['qualifiers'].pop()
        self.invalid('qualifiers changed')
    def test_lost_action(self):
        self.node('identify-unit-rate')['action']=''
        self.invalid('missing action')
    def test_changed_object(self):
        self.node('identify-unit-rate')['object']='any number'
        self.invalid('object changed')
    def test_exhaustive_strategy_misreading(self):
        self.node('ny-7-rp-2a')['source_annotations'][0]['interpretation']='Both strategies are mandatory.'
        self.invalid('interpretation changed')
    def test_annotation_deleted(self):
        self.node('ny-7-rp-2c')['source_annotations']=[]
        self.invalid('missing source annotation')
    def test_rejected_parent_stale_export_fails(self):
        self.node('ny-7-rp-2')['status']='REJECTED'
        self.invalid('inadmissible expected projection')
        self.assertEqual(standards_for_grade(self.data,7),[])
    def test_rejected_records_retained_after_projection_update(self):
        self.node('ny-7-rp-2')['status']='REJECTED'
        for s in self.data['students']: s['grade7_standard_ids']=[]
        validate_claims(self.data,SOURCES)
        self.assertEqual(len(self.data['nodes']),15)
    def test_unresolved_assignment_excluded(self):
        edge=next(e for e in self.data['edges'] if e['id']=='wc:edge:grade-2b')
        edge['status']='PROVISIONAL'
        self.assertNotIn('wc:standard:ny-7-rp-2b',standards_for_grade(self.data,7))
        self.invalid('inadmissible expected projection')
    def test_unknown_node_type(self):
        self.node('ny-7-rp-2')['type']='Invented'
        self.invalid('unknown node type')

if __name__=='__main__': unittest.main(verbosity=2)
