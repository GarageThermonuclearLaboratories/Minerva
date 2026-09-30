// DOM interaction checks. jsdom does not verify browser layout or visual quality.
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict');
const {JSDOM}=require('jsdom');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..'), read=p=>fs.readFileSync(path.join(root,p),'utf8');
async function setup(lateInterface=false, delayed=false){
  const dom=new JSDOM(read('dist/index.html'),{runScripts:'outside-only',url:'https://minerva.test/'});
  const w=dom.window, errors=[];
  w.addEventListener('error',e=>errors.push(e.error));
  w.HTMLElement.prototype.scrollIntoView=function(){};w.scrollTo=()=>{};
  let resolveData;const gate=new Promise(r=>resolveData=r);
  w.fetch=async name=>{if(delayed)await gate;return {ok:true,json:async()=>JSON.parse(read('dist/'+name))};};
  vm.runInContext(read('dist/app.js'),dom.getInternalVMContext());
  if(lateInterface)await new Promise(r=>setImmediate(r));
  vm.runInContext(read('dist/interface.js'),dom.getInternalVMContext());
  await new Promise(r=>setImmediate(r));
  return {dom,w,d:w.document,errors,resolveData};
}
(async()=>{
  const slow=await setup(false,true);
  slow.d.querySelector('[data-view="workbench"]').click();
  assert.deepEqual(slow.errors,[]);slow.resolveData();await new Promise(r=>setImmediate(r));
  assert.ok(slow.d.querySelector('.coverage-table'));slow.dom.window.close();
  const {dom,w,d,errors}=await setup();
  const model=JSON.parse(read('data/ontology.json'));
  assert.ok(d.querySelector('#receipt').hidden,'Receipt starts collapsed');
  assert.equal(d.querySelector('#release-label').textContent,'v0.0.7 · Wednesday science');
  assert.ok(d.querySelector('.trace-preview [data-node]'));
  d.querySelector('.trace-parsed [data-node]').click();
  assert.ok(!d.querySelector('#receipt').hidden);
  assert.ok(d.querySelector('#receipt-body').textContent.includes('Recognize and represent proportional relationships between quantities.'));
  d.querySelector('#expand-receipt').click();assert.ok(d.querySelector('#receipt').classList.contains('expanded'));
  d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert.ok(d.querySelector('#receipt').hidden);
  d.querySelector('#receipt-toggle').click();assert.ok(!d.querySelector('#receipt').hidden);
  d.querySelector('[data-lens]').click();
  assert.ok(d.querySelector('#view').textContent.includes('Eva · Grade 7'));
  assert.equal(d.querySelector('.lens-target')?.dataset.node,'wc:expectation:recognize-proportional');
  w.showReceipt('wc:concept:proportional-relationship');
  const conceptLens=d.querySelector('[data-lens]');
  assert.ok(conceptLens);conceptLens.click();assert.equal(d.querySelector('.lens-target').dataset.node,'wc:expectation:recognize-proportional');
  w.showReceipt('wc:standard:ny-7r1');
  assert.ok(d.querySelector('#receipt-body a[href="evidence/ela-full/page-82.png"]'));
  w.showReceipt('wc:standard:ms-ps2-2');
  assert.ok(d.querySelector('#receipt-body a[href="evidence/science-full/page-33.png"]'));
  assert.ok(d.querySelector('#receipt-body').textContent.includes('Assessment Boundary'));
  d.querySelector('[data-lens]').click();
  assert.equal(d.querySelector('.lens-target').dataset.node,'wc:standard:ms-ps2-2');
  assert.ok(d.querySelector('.band-context').textContent.includes('not additional Grade 7 assignments'));
  for(const n of model.nodes){w.showReceipt(n.id);assert.ok(d.querySelector('#receipt-body').textContent.includes(n.id));}
  d.querySelector('#receipt-body [data-neighborhood]').click();
  const verifyGraph=()=>{
    const nodes=[...d.querySelectorAll('.graph-node')].map(x=>x.dataset.node);
    assert.ok(nodes.length<=20&&nodes.every(id=>model.nodes.some(n=>n.id===id)));
    for(const edge of d.querySelectorAll('.graph-edge')){
      const original=model.edges.find(e=>e.id===edge.dataset.edge);assert.ok(original);
      assert.ok(nodes.includes(original.from)&&nodes.includes(original.to));
    }
  };
  verifyGraph();d.querySelector('#graph-expand').click();verifyGraph();assert.ok(d.querySelector('#graph-expand').disabled);
  d.querySelector('#graph-reset').click();assert.equal(d.querySelectorAll('.graph-node').length,9);
  for(const nav of d.querySelectorAll('.rail button')){nav.click();assert.ok(d.querySelector('#view').textContent.trim());assert.equal(nav.getAttribute('aria-current'),'page');}
  d.querySelector('[data-view="wildcats"]').click();
  for(let grade=0;grade<=12;grade++){
    let previous;
    for(const student of ['Eva','Matthew']){
      d.querySelector(`[data-student="${student}"]`).click();d.querySelector(`[data-grade="${grade}"]`).click();
      const ids=[...d.querySelectorAll('#view [data-node]')].map(n=>n.dataset.node);
      assert.equal(ids.length,(grade===7?13:0)+([6,7,8].includes(grade)?4:0));if(previous)assert.deepEqual(ids,previous);previous=ids;
      assert.ok(d.querySelector('#view').textContent.includes(grade===7?'Partially mapped':'Not yet mapped'));
      assert.equal(d.querySelectorAll('.grade-map .unmapped').length,12);
    }
  }
  d.querySelector('[data-stage="transition"]').click();assert.ok(d.querySelector('#view').textContent.includes('no diploma decision'));
  d.querySelector('[data-view="workbench"]').click();assert.equal(d.querySelectorAll('[data-family]').length,12);
  const toggle=d.querySelector('[data-family]'),detail=d.getElementById(toggle.getAttribute('aria-controls'));
  assert.ok(detail.hidden);toggle.click();assert.ok(!detail.hidden);toggle.click();assert.ok(detail.hidden);
  assert.ok(!d.querySelector('#epistemic-notice').open);
  d.querySelector('#activity-log').click();assert.equal(d.querySelectorAll('.log-entry time').length,7);
  assert.ok(d.querySelector('#view').textContent.includes('PROVISIONAL'));
  assert.deepEqual(errors,[]);dom.window.close();
  const late=await setup(true);assert.ok(late.d.querySelector('.trace-preview'));assert.deepEqual(late.errors,[]);late.dom.window.close();
  console.log('DOM checks passed: 8 views, 26 Receipts, graph integrity/expansion, student lens, 13 grades × 2 avatars, matrix controls, Escape/focus controls, and both script/data arrival orders.');
})().catch(e=>{console.error(e);process.exit(1);});
