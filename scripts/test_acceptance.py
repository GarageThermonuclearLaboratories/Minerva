"""Negative tests for the acceptance boundary; originals are never mutated."""
import copy
import json
import unittest
from pathlib import Path
from acceptance import validate_claims, standards_for_grade, standards_for_band
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
        self.assertEqual(standards_for_grade(self.data,7),['wc:standard:ny-7r1'])
    def test_rejected_records_retained_after_projection_update(self):
        self.node('ny-7-rp-2')['status']='REJECTED'
        for s in self.data['students']: s['grade7_standard_ids']=standards_for_grade(self.data,7)
        validate_claims(self.data,SOURCES)
        self.assertEqual(len(self.data['nodes']),len(json.loads((ROOT/'data/ontology.json').read_text())['nodes']))
    def test_unresolved_assignment_excluded(self):
        edge=next(e for e in self.data['edges'] if e['id']=='wc:edge:grade-2b')
        edge['status']='PROVISIONAL'
        self.assertNotIn('wc:standard:ny-7-rp-2b',standards_for_grade(self.data,7))
        self.invalid('inadmissible expected projection')
    def test_unknown_node_type(self):
        self.node('ny-7-rp-2')['type']='Invented'
        self.invalid('unknown node type')

    def test_ela_scope_loss(self):
        self.node('cite-evidence-infer')['qualifiers'].pop()
        self.invalid('qualifiers changed')
    def test_ela_source_wording_loss(self):
        self.node('ny-7r1')['original_text']='Cite textual evidence.'
        self.invalid('source wording changed')

    def test_science_not_assigned_to_grade7(self):
        self.assertFalse(any('ms-ps2' in x for x in standards_for_grade(self.data,7)))
        self.assertEqual(len(standards_for_band(self.data,'wc:grade-band:6-8')),2)
    def test_science_false_exact_grade_fails(self):
        edge=copy.deepcopy(next(e for e in self.data['edges'] if e['relation']=='ASSIGNED_TO_GRADE_BAND'))
        edge.update(id='bad-exact-grade',relation='ASSIGNED_TO_GRADE',to='wc:grade:7')
        self.data['edges'].append(edge)
        self.invalid('unsupported exact-grade assignment')
    def test_science_band_membership_changed(self):
        self.node('grade-band:6-8')['grades']=[7]
        self.invalid('grades changed')
    def test_science_boundary_deleted(self):
        self.node('standard:ms-ps2-2')['source_annotations'].pop()
        self.invalid('missing source annotation')
    def test_science_qualifier_lost(self):
        self.node('argue-gravitational-interactions')['qualifiers'].pop()
        self.invalid('qualifiers changed')
    def test_science_rejected_assignment_excluded(self):
        next(e for e in self.data['edges'] if e['id']=='wc:edge:ms-ps2-2-assigned_to_grade_band')['status']='REJECTED'
        self.assertEqual(standards_for_band(self.data,'wc:grade-band:6-8'),['wc:standard:ms-ps2-4'])
        self.invalid('inadmissible band projection')
    def test_science_mismatched_band_fails(self):
        self.node('standard:ms-ps2-2')['grade_band_id']='wc:grade:7'
        self.invalid('invalid grade-band target')

if __name__=='__main__': unittest.main(verbosity=2)
