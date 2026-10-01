// Bounded record queries. No external model, generated facts, or graph writes.
(function(root){
  const VERSION='bounded-record-query-v2';
  const EXAMPLES=[
    'What expectations have we mapped for Matthew?',
    'Which science expectations belong to the middle-school band?',
    'What connects English and science?',
    'What does 7R1 say?',
    'What have we mapped in Grade 5?'
  ];
  const SUBJECTS=[
    ['Mathematics',/\b(math|mathematics)\b/],['English Language Arts',/\b(english|ela|language arts|reading)\b/],
    ['Science',/\bscience\b/],['Social Studies',/\b(history|social studies)\b/],
    ['Arts',/\b(arts|art|music|dance|theater|visual arts|media arts)\b/],
    ['World Languages',/\b(world languages|spanish|french)\b/],['Physical Education',/\b(physical education|pe)\b/],
    ['Health',/\bhealth\b/],['Technology',/\btechnology\b/],
    ['Computer Science and Digital Fluency',/\b(computer science|digital fluency|computing)\b/],
    ['Family and Consumer Sciences',/\b(family and consumer sciences|facs)\b/],
    ['Career Development and Occupational Studies',/\b(cdos|career development|occupational studies)\b/]
  ];
  const WORD_GRADES={kindergarten:0,first:1,second:2,third:3,fourth:4,fifth:5,sixth:6,seventh:7,eighth:8,ninth:9,tenth:10,eleventh:11,twelfth:12,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,eleven:11,twelve:12};
  function normal(s){return String(s).toLowerCase().replace(/[–—]/g,'-').replace(/[’']/g,'').replace(/[^a-z0-9.-]+/g,' ').trim();}
  function answer(question,context){
    const q=normal(question),{model,manifest,comparisons}=context;
    const result=(kind,title,summary,items=[],limits=[])=>({version:VERSION,kind,title,summary,items,limits,question:String(question),model_release:model.release,policy_snapshot:model.policy_snapshot});
    const stop=(reason,text)=>result('unanswered',reason,text,[],['This answer does not establish an absence of requirements. Try one of the supported example questions.']);
    if(!q)return stop('Ask a question','Choose an example or enter a question about the mapped records.');
    if(q.length>500)return stop('Question is too long','Use one question of up to 500 characters.');
    if(/\b(mastered|mastery|learned|knows|know already|passed|complete|completed|score|scores|proficient|demonstrated|can matthew|can eva|does matthew know|does eva know)\b/.test(q)||/\bable\b/.test(q)&&!/\b(?:expected|should)\b/.test(q))return stop('No mastery evidence','Matthew and Eva are fictional reference students. The model contains expectations, but no evidence of what either has learned or demonstrated.');
    if(/\b(today|current|currently|latest|law|legally|mandatory|graduate|graduation|diploma|credits|regents|2026)\b/.test(q))return stop('Applicability is unresolved','This checkpoint preserves source-edition expectations. It cannot establish current legal applicability, diploma eligibility or graduation requirements.');
    if(/\b(prerequisite|prerequisites|before|after|progression|transfer|builds on|build upon|build on)\b/.test(q))return stop('Relationship is not established','No prerequisite, developmental sequence or transfer relationship has been accepted in this model. A source Receipt or a candidate analogy alone cannot establish one.');
    if(/\b(lesson|worksheet|homework|solve|calculate|quiz|teach|explain why|ignore|override|pretend|invent)\b/.test(q))return stop('Outside this question layer','Ask Minerva retrieves mapped expectations and comparison records. This version does not generate lessons, solve exercises or create additional claims.');
    if(/\bhow\b/.test(q))return stop('Method questions are not supported','This version retrieves records. It does not explain how to learn, teach, assess or perform an expectation.');
    if(/\bonly\b/.test(q))return stop('Selection is ambiguous','This version does not infer what “only” modifies. Ask for a subject, one grade, exact-grade assignments or the shared band directly.');
    const nodes=new Map(model.nodes.map(n=>[n.id,n])),sources=new Map(manifest.sources.map(s=>[s.id,s]));
    const eligible=n=>!!n&&['SOURCE','PARSED'].includes(n.status);
    const sourced=n=>{const s=sources.get(n?.source_id);return !!s&&!!s.sha256&&Number.isInteger(n.pdf_page)&&n.pdf_page>0&&n.pdf_page<=s.page_count&&!!n.source_locator;};
    function active(n,seen=new Set()){
      if(!eligible(n)||!sourced(n)||seen.has(n.id))return false;
      if(!n.parent_standard_id)return true;
      return model.edges.some(e=>e.relation==='PART_OF'&&e.from===n.id&&e.to===n.parent_standard_id&&eligible(e)&&sourced(e))&&active(nodes.get(n.parent_standard_id),new Set([...seen,n.id]));
    }
    const subjects=SUBJECTS.filter(([label,re])=>re.test(label==='Arts'?q.replace(/\blanguage arts\b/g,''):label==='Science'?q.replace(/\bcomputer science\b/g,''):q)).map(([label])=>label);
    const names=['Matthew','Eva'].filter(n=>new RegExp('\\b'+n.toLowerCase()+'\\b').test(q));
    let g=null;
    const grades=new Set();
    for(const numeric of q.matchAll(/\bgrade\s+(\d{1,2})(?:st|nd|rd|th)?\b|\b(\d{1,2})(?:st|nd|rd|th)\s+grade\b/g))grades.add(Number(numeric[1]||numeric[2]));
    for(const [word,value] of Object.entries(WORD_GRADES))if(new RegExp('\\b(?:grade '+word+'|'+word+' grade)\\b').test(q)||word==='kindergarten'&&q.includes(word))grades.add(value);
    if(/\bgrade k\b/.test(q))grades.add(0);
    if(grades.size>1)return stop('Ask about one grade','This version answers one grade selection at a time.');
    if(grades.size)g=[...grades][0];
    if(g!==null&&(g<0||g>12))return stop('Outside K–12','The reference pathway covers kindergarten through Grade 12.');
    const band=/\b(middle school|middle-school|band|grades 6-8|grades six through eight)\b/.test(q);
    if(band&&g!==null)return stop('Choose one placement','Ask about one grade or the shared middle-school band. This version does not combine those selections.');
    if(/\bgrades?\b/.test(q)&&g===null&&!band)return stop('Ask about one grade','Use one grade number or the middle-school band. This version does not interpret other grade ranges.');
    // Consume complete placement phrases. Residual grade values are narrowing constraints,
    // not harmless vocabulary (for example "seventh and eighth grade").
    let gradeRemainder=q.replace(/\b(?:grades 6-8|grades six through eight|middle school|middle-school)(?: band)?\b/g,'');
    gradeRemainder=gradeRemainder.replace(/\bgrade\s+\d{1,2}(?:st|nd|rd|th)?\b|\b\d{1,2}(?:st|nd|rd|th)\s+grade\b/g,'');
    for(const word of Object.keys(WORD_GRADES))gradeRemainder=gradeRemainder.replace(new RegExp('\\b(?:grade '+word+'|'+word+' grade)\\b','g'),'');
    gradeRemainder=gradeRemainder.replace(/\b(?:kindergarten|grade k)\b/g,'');
    if(Object.keys(WORD_GRADES).some(word=>new RegExp('\\b'+word+'\\b').test(gradeRemainder)))return stop('Selection is ambiguous','Use one grade or the shared middle-school band. This version does not interpret other grade ranges or record-count limits.');
    if(/\b(?:assigned|assignment)\b/.test(q)&&g===null&&(!band||names.length))return stop('Assignment needs explicit placement','Ask for an assignment to one explicit grade or the shared band. An avatar name alone is not a source assignment.');
    const exactGrade=/\b(?:exact|individually|individual)\b/.test(q)||g!==null&&/\b(?:assigned|assignment)\b/.test(q);
    if(exactGrade&&(g===null||band))return stop('Exact placement needs one grade','Ask for exact assignments to one grade, or ask for shared band context.');
    const statusWords=q.match(/\b(?:source|parsed|provisional|tentative|rejected)\b/g)||[];
    const sourceDisposition=/\bsource (?:expectations?|comparisons?|claims?|standards?)\b/.test(q);
    const requestedStatuses=[...new Set(statusWords.filter(w=>w!=='source'||sourceDisposition).map(w=>w==='tentative'?'PROVISIONAL':w.toUpperCase()))];
    if(requestedStatuses.length>1)return stop('Ask for one disposition','This version does not combine multiple claim-disposition filters.');
    const comparison=/\b(compare|comparison|comparisons|connect|connects|connection|connections|equivalent|equivalence|analogies|analogy|related|same|different|differences|similar|relationships? between)\b/.test(q);
    const lookup=model.nodes.filter(n=>n.type==='Standard'&&new RegExp('(?:^| )'+normal(n.label).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?: |$)').test(q));
    // Limit recognition to the declared record-question vocabulary. Unknown topics must not silently broaden a query.
    const vocabulary=new Set(('what which how where are is do does have has we you our your the a an for of from to in on about between and or with me show list tell say says said asks ask asking expected expect expectations expectation learning learn know able can should would mapped mapping map coverage covered material records record sources source wording support supports evidence textual text claim claims mean means matthew eva both students student fictional reference new york nys state minerva wildcats curriculum standard standards requirements requirement belongs belong assigned assignment assigned individually individual exact broader somewhere within band middle school grade grades not no yes all only currently under at this that it its their them these those same different differences similar compare comparison comparisons connect connects connection connections equivalent equivalence analogies analogy relationship relationships related parsed provisional tentative rejected equation proportional quantities graph point forces motion gravity gravitational investigation arguments argument interpretation infer inferences logical literary informational sixth seventh eighth kindergarten first second third fourth fifth ninth tenth eleventh twelfth one two three four five six seven eight nine ten eleven twelve k through mathematics math english ela language arts reading science social studies history art music dance theater visual media world languages spanish french physical education pe health technology computer digital fluency computing family consumer sciences facs cdos career development occupational available completed complete whole').split(' '));
    vocabulary.add('be');
    if(/\b(not|no|nor|neither|never|except|without|exclude|excluding)\b/.test(q))return stop('Selection is ambiguous','This version does not interpret exclusions. Ask for a subject or grade directly.');
    if((q.match(/\b(?:what|which|how|where)\b/g)||[]).length>1)return stop('Ask one question at a time','Split the question into one record selection or one comparison selection.');
    if(/\b(?:and|or)\s+(?:show|list|tell|ask|compare|mapped|all mapped|expectations?|standards?)\b/.test(q))return stop('Ask one question at a time','Split the question into one record selection or one comparison selection.');
    let remainder=q.replace(/middle-school/g,'middle school').replace(/grades 6-8/g,'grades six through eight');
    for(const n of lookup)remainder=remainder.replace(normal(n.label),'');
    const unplacedNumbers=remainder.replace(/\bgrade\s+\d{1,2}(?:st|nd|rd|th)?\b|\b\d{1,2}(?:st|nd|rd|th)\s+grade\b/g,'');
    if(/\d/.test(unplacedNumbers))return stop('Selection is ambiguous','Use a standard identifier, one grade number or the middle-school band.');
    const unsupportedTopics=new Set('equation proportional quantities graph point forces motion gravity gravitational investigation arguments argument interpretation infer inferences logical literary informational'.split(' '));
    if(remainder.split(/\s+/).some(w=>w&&(unsupportedTopics.has(w)||!vocabulary.has(w)&&!/^\d{1,2}(st|nd|rd|th)?$/.test(w))))return stop('Question is outside the supported patterns','I could not reliably match the whole question to this checkpoint. Ask about mapped expectations, source wording, grade placement or the recorded comparisons.');
    const sourceSubject=n=>model.nodes.find(s=>s.type==='Subject'&&s.source_id===n.source_id&&active(s))?.label;
    const selectedSubject=n=>!subjects.length||subjects.includes(sourceSubject(n));
    function placement(parent){
      return model.edges.filter(e=>e.from===parent.id&&['ASSIGNED_TO_GRADE','ASSIGNED_TO_GRADE_BAND'].includes(e.relation)&&eligible(e)&&sourced(e)&&eligible(nodes.get(e.to))&&sourced(nodes.get(e.to))).map(e=>nodes.get(e.to));
    }
    function item(exp,parent,places){return {node_id:exp.id,standard_id:parent.id,title:exp.label,status:exp.status,subject:sourceSubject(parent),placement:places.map(p=>p.label).join('; '),placement_kind:places.some(p=>p.type==='GradeBand')?'band':'grade',text:exp.action+' · '+exp.object,qualifiers:exp.qualifiers||[],source_quote:parent.original_text,annotations:parent.source_annotations||[],source_id:parent.source_id,pdf_page:parent.pdf_page};}
    const limits=['This is partial map coverage, not the full curriculum. Counts include overlapping parent-heading and subpart interpretations.','Source edition and cohort applicability remain unresolved. An expectation is not demonstrated mastery.'];
    const records=model.nodes.filter(n=>n.type==='Expectation'&&active(n)&&active(nodes.get(n.derived_from))&&model.edges.some(e=>e.relation==='DERIVED_FROM'&&e.from===n.id&&e.to===n.derived_from&&eligible(e)&&sourced(e))).map(n=>{const p=nodes.get(n.derived_from);return item(n,p,placement(p));}).filter(i=>i.placement&&i.source_quote&&i.subject);
    if(comparison){
      if(/\bor\b/.test(q))return stop('Comparison selection is ambiguous','Use one subject or a subject pair joined by “and”. This version does not interpret alternative comparison selections.');
      if(lookup.length)return stop('Standard-specific comparisons are not supported','This version selects comparison records by subject pair. It does not interpret a standard identifier as a comparison filter.');
      if(exactGrade||requestedStatuses.some(s=>!['PROVISIONAL','REJECTED'].includes(s)))return stop('Comparison filter is not supported','Comparison records have PROVISIONAL or REJECTED dispositions. Ask for one of those or omit the filter.');
      if(g!==null||band||names.length)return stop('Comparison placement needs a narrower question','Ask about the subject pair without a grade or student filter. The current comparisons mix Grade 7 expectations with a grades 6–8 science band.');
      if(!subjects.length)return stop('Choose a subject pair','Try: What connects English and science?');
      const matches=comparisons.records.filter(r=>['PROVISIONAL','REJECTED'].includes(r.status)&&(!requestedStatuses.length||requestedStatuses.includes(r.status))&&r.promoted_to_ontology===false&&subjects.every(s=>r.subjects.includes(s))&&r.evidence.length===2&&r.evidence.every((e,i)=>{
        const n=nodes.get(e.node_id),p=nodes.get(e.standard_id),s=sources.get(e.source_id);
        return records.some(item=>item.node_id===n?.id)&&active(p)&&n.derived_from===p.id&&sourceSubject(p)===r.subjects[i]&&e.quotation===p.original_text&&e.source_id===p.source_id&&e.pdf_page===p.pdf_page&&e.source_locator===p.source_locator&&s?.sha256===e.source_sha256;
      }));
      if(!matches.length)return result('unmapped','No eligible comparison mapped','No comparison for this subject selection is available in the current register.',[],limits);
      return result('comparison','Recorded comparisons',`${matches.length} comparison record${matches.length===1?'':'s'} match. No cross-subject equivalence or accepted graph link is established.`,matches.map(r=>({comparison_id:r.id,title:r.title,subjects:r.subjects,status:r.status,text:r.decision,commonality:r.commonality,not_established:r.not_established,next_evidence:r.next_evidence,axes:r.axes,evidence:r.evidence})),limits);
    }
    if(lookup.length){
      if(subjects.length>1||/\b(?:and|or)\b/.test(q))return stop('Source lookup needs one selection','Ask about one standard identifier at a time, without another selection or operation.');
      if(requestedStatuses.length)return stop('Claim-status lookup is not supported','Use the standard identifier to inspect source wording, without a separate claim-status filter.');
      if(lookup.length!==1)return stop('Ask about one standard','Use one standard identifier at a time.');
      const p=lookup[0],places=placement(p);
      if(!selectedSubject(p)||g!==null&&!places.some(x=>x.type==='Grade'&&x.id==='wc:grade:'+g||!exactGrade&&x.type==='GradeBand'&&x.grades.includes(g))||band&&!places.some(x=>x.type==='GradeBand'))return stop('Placement or subject does not match','The named standard does not have the requested placement or subject in this map.');
      if(!active(p)||!places.length||!sourceSubject(p))return result('unmapped','No eligible standard record','This record is not currently eligible for an answer.',[],limits);
      const items=records.filter(i=>i.standard_id===p.id);
      return result('source','What the source says',p.label+' · '+places.map(x=>x.label).join('; '),[{node_id:p.id,standard_id:p.id,title:p.label,status:p.status,source_quote:p.original_text,annotations:p.source_annotations||[],placement:places.map(x=>x.label).join('; '),placement_kind:places.some(x=>x.type==='GradeBand')?'band':'grade',pdf_page:p.pdf_page,source_id:p.source_id,text:p.parsing_rationale||'Original source wording',qualifiers:[],children:items.map(i=>i.node_id)}],limits);
    }
    const expected=/\b(expected|expect|should|expectations|expectation|standards|requirements|learn|learning|know|mapped|mapping|map|coverage|covered|curriculum)\b/.test(q);
    if(requestedStatuses.length)return stop('Expectation-status filtering is not supported','This view answers from eligible SOURCE/PARSED expectation records. It does not retrieve tentative or rejected claims as expected learning. Inspect claim status in the atlas and Crossroads.');
    if(/\b(evidence|textual|support|supports|claims?|relationships?)\b/.test(q))return stop('Topic filtering is not supported','This version selects records by subject and grade, not by a narrower concept or keyword. Use a standard identifier to inspect its wording.');
    if(!expected)return stop('Question is outside the supported patterns','Try an expectation, source-wording, grade-placement or comparison question.');
    if(names.length&&g===null)g=7;
    if(!subjects.length&&g===null&&!band&&!names.length){
      const labels=[...new Set(records.map(i=>i.subject))];
      return result('coverage','Current map coverage',`${records.length} eligible parsed expectations${labels.length?' across '+labels.join(', '):''}: ${records.filter(i=>i.placement_kind==='grade').length} exact-grade and ${records.filter(i=>i.placement_kind==='band').length} shared band records. Band membership is not an individual-grade assignment.`,records,limits);
    }
    const items=records.filter(i=>selectedSubject(nodes.get(i.standard_id))).filter(i=>{
      const places=placement(nodes.get(i.standard_id));
      if(band)return places.some(p=>p.type==='GradeBand'&&(g===null||p.grades.includes(g)));
      return g===null||places.some(p=>p.type==='Grade'&&p.id==='wc:grade:'+g||!exactGrade&&p.type==='GradeBand'&&p.grades.includes(g));
    });
    const label=names.length?names.join(' and ')+' · '+(g===0?'Kindergarten':'Grade '+g):g!==null?(g===0?'Kindergarten':'Grade '+g):band?'Middle-school band':subjects.join(' / ');
    if(!items.length)return result('unmapped',label+' · not yet mapped',`No eligible ${exactGrade?'exact-grade ':''}expectations for this selection have been modeled here. This does not mean New York has no expectations for it.${exactGrade?' Shared band context is a separate selection.':''}`,[],limits);
    return result('expectations',label+' · mapped expectations',`${items.filter(i=>i.placement_kind==='grade').length} parsed exact-grade expectations and ${items.filter(i=>i.placement_kind==='band').length} shared grade-band expectations in this selection. Band records belong somewhere within grades 6–8; they are not additional assignments to an individual grade.`,items,limits);
  }
  const api={answer,EXAMPLES,VERSION};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.MinervaAnswers=api;
})(typeof globalThis!=='undefined'?globalThis:this);
