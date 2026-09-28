"""Regenerate page text from archived PDF bytes. Does not parse standards semantics."""
import hashlib,json
from pathlib import Path
import pymupdf
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'data/sources.json').read_text())
for source in manifest['sources']:
    if source.get('acquisition_status')!='full-document-acquired':continue
    path=root/source['archive_path'];digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==source['sha256'], 'Archived source changed'
    doc=pymupdf.open(path)
    output=dict(source_id=source['id'],sha256=digest,method='PyMuPDF '+pymupdf.VersionBind+' plain text; reading order is not semantic structure',pages=[dict(pdf_page=i+1,text=page.get_text()) for i,page in enumerate(doc)])
    (root/'sources/extracted'/f'{path.stem}.pages.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
