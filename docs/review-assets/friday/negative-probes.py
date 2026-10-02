import copy,hashlib,json,sys
from pathlib import Path
root=Path(__file__).parent/'candidate';sys.path.insert(0,str(root/'scripts'))
import validate_release_candidate as v
results=[]
def trial(label,mutate,expected='rejected'):
 changes={}
 def put(name,value):
  p=root/name;changes.setdefault(name,p.read_bytes() if p.exists() else None);p.parent.mkdir(parents=True,exist_ok=True)
  if value is None:p.unlink()
  else:p.write_bytes(value if isinstance(value,bytes) else v.encoded(value))
 try:
  mutate(put)
  try:v.verify(root);outcome='accepted'
  except (ValueError,OSError,KeyError) as e:outcome='rejected'
  results.append({'case':label,'expected':expected,'observed':outcome,'pass':outcome==expected})
 finally:
  for name,raw in changes.items():
   p=root/name
   if raw is None:p.unlink(missing_ok=True)
   else:p.write_bytes(raw)
load=lambda name:json.loads((root/name).read_bytes())
trial('added served asset expands inventory',lambda p:p('dist/audit-extra.js',b'unreviewed'))
trial('missing asset changes inventory',lambda p:p('dist/ask-engine.js',None))
trial('archive byte mutation',lambda p:p('sources/originals/nys-math-standards-grade-7-crosswalk.pdf',b'bad archive'))
trial('dependency pin mutation',lambda p:p('package.json',{**load('package.json'),'devDependencies':{'jsdom':'27.5.0','vite':'8.3.1'}}))
trial('source annotation loss',lambda p:p('data/ontology.json',{**load('data/ontology.json'),'nodes':[]}))
trial('release freeze promotion',lambda p:p('dist/release.json',{**load('dist/release.json'),'freeze_status':'frozen'}))
trial('manifest omitted asset',lambda p:p(v.MANIFEST,{**load(v.MANIFEST),'artifacts_sha256':{k:x for k,x in load(v.MANIFEST)['artifacts_sha256'].items() if k!='dist/ask-engine.js'}}))
trial('public export mutation',lambda p:p(v.EXPORT,b'{}'))
trial('missing command evidence',lambda p:p(v.RECORD,{**load(v.RECORD),'checks':[]}))
trial('nonzero command evidence',lambda p:p(v.RECORD,{**load(v.RECORD),'checks':[{'exit_code':1}]}))
trial('changed successful evidence bytes',lambda p:p(v.RECORD,{**load(v.RECORD),'completed_at':'invented'}))
trial('research pointer excluded by declared boundary',lambda p:p('dist/release.json',{**load('dist/release.json'),'research_commit':'0'*40}),expected='accepted')
trial('postpublication receipt excluded by declared boundary',lambda p:p('data/publications/reviewer-negative.json',{'research_commit':'false'}),expected='accepted')
def reissue_minimal(put):
 record={'result':'pass-builder-validation-with-recorded-limits','checks':[{'exit_code':0}]}
 put(v.RECORD,record)
 manifest=v.make_manifest(root,record)
 put(v.MANIFEST,manifest);put(v.EXPORT,manifest)
trial('reissued manifest admits incomplete evidence: robustness follow-up',reissue_minimal,expected='accepted')
print(json.dumps({'checks':results,'failed':sum(not x['pass'] for x in results)},indent=2));assert all(x['pass'] for x in results)
