import copy
import json
import unittest
import subprocess
import sys
import tempfile
from unittest.mock import patch
from pathlib import Path
from comparison_validation import check_comparisons
from comparison_contract import load_baseline
from build_comparisons import build

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())

class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.c=read('data/comparisons.json');self.m=read('data/ontology.json');self.s=read('data/sources.json')
    def check(self):return check_comparisons(self.c,self.m,self.s)
    def invalid(self,part):
        with self.assertRaisesRegex(ValueError,part):self.check()
    def test_baseline(self):
        self.assertTrue(self.check());self.assertEqual(len(self.c['records']),3)
        self.assertEqual([r['status'] for r in self.c['records']],['PROVISIONAL','REJECTED','REJECTED'])
        self.assertEqual((len(self.m['nodes']),len(self.m['edges']),len(self.m['findings'])),(26,31,0))
    def test_quote_tamper(self):
        self.c['records'][0]['evidence'][0]['quotation']='All evidence is interchangeable.';self.invalid('quotation mismatch')
    def test_stale_source(self):
        self.c['records'][0]['evidence'][0]['source_sha256']='bad';self.invalid('source hash mismatch')
    def test_stale_expectation(self):
        next(n for n in self.m['nodes'] if n['id']==self.c['records'][0]['node_ids'][0])['action']='Understand';self.invalid('Stale expectation')
    def test_lost_source_boundary(self):
        next(n for n in self.m['nodes'] if n['id']=='wc:standard:ms-ps2-4')['source_annotations']=[];self.invalid('Stale standard')
    def test_false_promotion(self):
        self.c['records'][0]['promoted_to_ontology']=True;self.invalid('promotion is forbidden')
    def test_false_review(self):
        self.c['independent_review']='passed';self.invalid('review promotion')
    def test_missing_axis(self):
        self.c['records'][0]['axes'].pop();self.invalid('Incomplete comparison axes')
    def test_wrong_pair(self):
        self.c['records'][0]['evidence'].reverse();self.invalid('Evidence pair mismatch')
    def test_graph_leak(self):
        self.m['edges'].append(dict(id=self.c['records'][0]['id'],**{'from':self.c['records'][0]['node_ids'][0],'to':self.c['records'][0]['node_ids'][1]}));self.invalid('leaked into graph')
    def test_unsupported_disposition(self):
        self.c['records'][0]['status']='SOURCE';self.invalid('Unsupported comparison disposition')
    def test_missing_rationale(self):
        self.c['records'][1]['decision']='';self.invalid('Missing comparison decision')
    def test_false_baseline(self):
        self.c['input_research_commit']='0'*40;self.invalid('baseline commit mismatch')
    def test_false_method(self):
        self.c['method']='invented';self.invalid('method mismatch')
    def test_false_scope(self):
        self.c['scope']='All subjects and all grades';self.invalid('scope mismatch')
    def test_coordinated_method_change(self):
        draft=read('data/comparison-drafts.json');draft['method']=self.c['method']='invented'
        with self.assertRaisesRegex(ValueError,'method mismatch'):
            check_comparisons(self.c,self.m,self.s,draft=draft)
    def test_coordinated_scope_change(self):
        draft=read('data/comparison-drafts.json');draft['scope']=self.c['scope']='Exhaustive'
        with self.assertRaisesRegex(ValueError,'scope mismatch'):
            check_comparisons(self.c,self.m,self.s,draft=draft)
    def test_wrong_subject_label(self):
        self.c['records'][0]['subjects'][0]='Mathematics';self.invalid('subject identity mismatch')
    def test_reversed_subjects(self):
        self.c['records'][0]['subjects'].reverse();self.invalid('subject identity mismatch')
    def test_unpaired_model_change(self):
        self.m['students'][0]['label']='Changed avatar';self.invalid('explicit baseline review')
    def test_incomplete_baseline_projection(self):
        baseline=load_baseline();baseline['model_fields'].remove('students')
        with self.assertRaisesRegex(ValueError,'field coverage'):
            check_comparisons(self.c,self.m,self.s,baseline=baseline)
    def build_in_sandbox(self, change=None):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data').mkdir();(root/'dist').mkdir()
            draft=read('data/comparison-drafts.json')
            if change:change(self.m,draft)
            for name,value in [('ontology',self.m),('sources',self.s),('comparison-drafts',draft)]:
                (root/f'data/{name}.json').write_text(json.dumps(value))
            outputs=[root/'data/comparisons.json',root/'dist/comparisons.json']
            for output in outputs:output.write_text('unchanged sentinel')
            with patch('build_comparisons.ROOT',root):
                if change:
                    with self.assertRaises(ValueError):build(ROOT/'data/comparison-baseline.json')
                    self.assertTrue(all(p.read_text()=='unchanged sentinel' for p in outputs))
                else:
                    build(ROOT/'data/comparison-baseline.json')
                    self.assertTrue(all(p.read_bytes()==(ROOT/'data/comparisons.json').read_bytes() for p in outputs))
    def test_rebuild_is_byte_identical(self):self.build_in_sandbox()
    def test_generator_rejects_changed_model_without_writing(self):
        self.build_in_sandbox(lambda m,d:m['students'][0].update(label='Changed'))
    def test_generator_rejects_coordinated_subject_error_without_writing(self):
        self.build_in_sandbox(lambda m,d:d['records'][0]['subjects'].__setitem__(0,'Mathematics'))
    def test_generator_requires_explicit_baseline(self):
        result=subprocess.run([sys.executable,str(ROOT/'scripts/build_comparisons.py')],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertIn('--baseline',result.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
