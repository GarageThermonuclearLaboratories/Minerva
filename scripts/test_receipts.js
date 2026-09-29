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
console.log('Verified six expectation receipts, preserved qualifiers/notes, and seven view render functions');
for(let g=0;g<=12;g++){
  const outputs=[];
  for(const student of ['Eva','Matthew']){
    vm.runInContext(`view='wildcats';transition=false;grade=${g};student='${student}';render()`,context);
    outputs.push(element('#view').innerHTML.match(/data-node="[^"]+"/g)||[]);
    assert.ok(element('#view').innerHTML.includes(g===7?'Partially mapped':'Not yet mapped'));
  }
  assert.deepEqual(outputs[0],outputs[1]);
  assert.equal(outputs[0].length,g===7?11:0);
}
for(const stage of context.input.journey.stages){
  vm.runInContext(`selectStage('${stage.id}')`,context);
  assert.ok(element('#view').innerHTML.includes(stage.title));
}
assert.ok(element('#view').innerHTML.includes('no diploma decision'));
assert.ok(!element('#view').innerHTML.includes('data-node='));
console.log('Verified all 13 grades for both avatars, five stage selections, and transition abstention');
