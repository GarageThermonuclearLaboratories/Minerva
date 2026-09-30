import copy
import json
import unittest
from pathlib import Path
from comparison_validation import check_comparisons

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

if __name__=='__main__':unittest.main(verbosity=2)
