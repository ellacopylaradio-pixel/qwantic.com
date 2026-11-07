import hashlib, importlib.util, json, subprocess, unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('anatomy_catalog',ROOT/'workers/anatomy_catalog.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.errors=[];self.ids=set();self.anchors=[];self.files=[];self.script=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:
   if d['id'] in self.ids:self.errors.append('duplicate id '+d['id'])
   self.ids.add(d['id'])
  if 'style' in d or tag=='style':self.errors.append('inline style')
  if any(k.lower().startswith('on') for k in d):self.errors.append('handler inline')
  if tag=='script':
   if not d.get('src'):self.errors.append('inline script')
  for key in ['href','src']:
   value=d.get(key,'')
   if value.startswith('#'):self.anchors.append(value[1:])
   elif value and not value.startswith(('https:','data:','http:')):self.files.append(value)
class Contract(unittest.TestCase):
 def test_source_drift_disables_validation(self):
  text='fn a() {}';catalog=[{'sources':[{'file':'a.rs','sha256':hashlib.sha256(text.encode()).hexdigest()}]}]
  self.assertFalse(m.resolve(catalog,lambda _:text)[0]['review_required'])
  self.assertTrue(m.resolve(catalog,lambda _:text+' changed')[0]['review_required'])
  def missing(_):raise subprocess.CalledProcessError(128,'git')
  self.assertTrue(m.resolve(catalog,missing)[0]['review_required'])
 def test_generated_pages_have_no_inline_code_or_style_and_resolve_links(self):
  folder=ROOT/'dist/observatoire'
  for name in ['index.html','anatomies.html']:
   page=Page();page.feed((folder/name).read_text());self.assertEqual(page.errors,[],name)
   self.assertTrue(all(a in page.ids for a in page.anchors))
   self.assertTrue(all((folder/f).exists() for f in page.files),page.files)
  catalog=json.loads((folder/'anatomies.json').read_text());self.assertEqual(len(catalog),7);self.assertFalse(any(v['review_required'] for v in catalog))
if __name__=='__main__':unittest.main()
