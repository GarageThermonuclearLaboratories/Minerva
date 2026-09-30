// Exercise receipt generation against real data without browser/network dependencies.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const elements = new Map();
const element = key => {
  if (!elements.has(key)) elements.set(key, {innerHTML:'', textContent:'', scrollIntoView(){}});
  return elements.get(key);
};
const context = vm.createContext({
  document: {querySelector:element, querySelectorAll:()=>[]},
  input: {model:read('data/ontology.json'), manifest:read('data/sources.json'),
    corpus:read('data/corpus-plan.json'), review:read('data/source-review.json'),
    release:read('dist/release.json'), journey:read('data/journey.json')}
});
const code = fs.readFileSync(path.join(root, 'dist/app.js'), 'utf8');
vm.runInContext(code.split("\ndocument.querySelectorAll('.rail button').forEach(b=>b.onclick")[0], context);
vm.runInContext('({model,manifest,corpus,review,release,journey}=input)', context);
for (const n of context.input.model.nodes.filter(n=>n.type==='Expectation')) {
  vm.runInContext(`showReceipt(${JSON.stringify(n.id)})`, context);
  const source = context.input.model.nodes.find(s=>s.id===n.derived_from);
  context.quote = source.original_text;
  const escaped = vm.runInContext('esc(quote)', context);
  assert.ok(element('#receipt-body').innerHTML.includes(escaped), n.id);
  assert.ok(element('#receipt-body').innerHTML.includes(n.derived_from), n.id);
}
vm.runInContext("showReceipt('wc:expectation:decide-proportional')", context);
assert.ok(element('#receipt-body').innerHTML.includes('include but are not limited'));
vm.runInContext("showReceipt('wc:expectation:identify-unit-rate')", context);
for (const word of ['tables','graphs','equations','diagrams','verbal descriptions'])
  assert.ok(element('#receipt-body').innerHTML.includes(word));
for (const name of ['atlas','curriculum','wildcats','workbench','journey','findings','log'])
  vm.runInContext(`view=${JSON.stringify(name)};render()`, context);
console.log('Verified all expectation receipts, preserved qualifiers/notes, and seven view render functions');
for(let g=0;g<=12;g++){
  const outputs=[];
  for(const student of ['Eva','Matthew']){
    vm.runInContext(`view='wildcats';transition=false;grade=${g};student='${student}';render()`,context);
    outputs.push(element('#view').innerHTML.match(/data-node="[^"]+"/g)||[]);
    assert.ok(element('#view').innerHTML.includes(g===7?'Partially mapped':'Not yet mapped'));
  }
  assert.deepEqual(outputs[0],outputs[1]);
  assert.equal(outputs[0].length,g===7?13:0);
}
for(const stage of context.input.journey.stages){
  vm.runInContext(`selectStage('${stage.id}')`,context);
  assert.ok(element('#view').innerHTML.includes(stage.title));
}
assert.ok(element('#view').innerHTML.includes('no diploma decision'));
assert.ok(!element('#view').innerHTML.includes('data-node='));
console.log('Verified all 13 grades for both avatars, five stage selections, and transition abstention');
// A retained source quote must not mask missing parsed fields.
const contract=read('data/acceptance/ny-7-rp-2.json');
for(const [id, fields] of Object.entries(contract.expectations)){
  const n=context.input.model.nodes.find(n=>n.id===id);
  for(const field of ['derived_from','action','object','qualifiers']) assert.deepEqual(n[field],fields[field],id+': '+field);
  vm.runInContext(`showReceipt(${JSON.stringify(id)})`,context);
  const parsed=element('#receipt-body').innerHTML.match(/<dl><dt>Action<\/dt>([\s\S]*?)<\/dl>/)?.[1];
  assert.ok(parsed,id+': structured parsed fields absent');
  for(const value of [fields.action,fields.object,...fields.qualifiers]){
    context.value=value;assert.ok(parsed.includes(vm.runInContext('esc(value)',context)),id+': parsed field absent');
  }
}
const baseline=JSON.stringify(context.input.model);
function reset(){Object.assign(context.input.model,JSON.parse(baseline));}
for(const status of ['REJECTED','CONTESTED','PROVISIONAL','NORMALIZED','INFERRED']){
  reset();context.input.model.nodes.find(n=>n.id==='wc:standard:ny-7-rp-2').status=status;
  assert.equal(vm.runInContext('standardsForGrade(7).length',context),1,status+' parent excludes subparts');
  vm.runInContext("view='wildcats';grade=7;transition=false;render()",context);
  assert.ok(!element('#view').innerHTML.includes('data-node="wc:standard:ny-7-rp-2'));
}
reset();context.input.model.edges.find(e=>e.id==='wc:edge:grade-2b').status='REJECTED';
assert.ok(!vm.runInContext('standardsForGrade(7).map(n=>n.id)',context).includes('wc:standard:ny-7-rp-2b'));
reset();context.input.model.nodes.find(n=>n.id==='wc:expectation:identify-unit-rate').status='CONTESTED';
vm.runInContext("view='wildcats';render()",context);
assert.ok(!element('#view').innerHTML.includes('data-node="wc:expectation:identify-unit-rate"'));
reset();context.input.model.edges.find(e=>e.id==='wc:edge:parse-2b').status='REJECTED';
assert.equal(vm.runInContext("expectationsForStandard('wc:standard:ny-7-rp-2b').length",context),0);
reset();
console.log('Acceptance UI checks passed: structured fields independent of quotes; unsupported nodes, assignments, derivations, and rejected parent subparts excluded.');
