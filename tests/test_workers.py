import importlib.util, subprocess, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('pipeline',Path(__file__).resolve().parents[1]/'workers/pipeline.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class AnalysisTest(unittest.TestCase):
 def test_diff_and_production_dependencies(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   def git(*a):return subprocess.check_output(['git','-C',temp,*a],text=True).strip()
   git('init','-q');git('config','user.name','Test');git('config','user.email','test@example.invalid')
   crate=root/'crates/astro-demo';(crate/'src').mkdir(parents=True)
   (crate/'Cargo.toml').write_text('[package]\nname = "astro-demo"\n[dependencies]\nastro-db.workspace = true\n[dev-dependencies]\nastro-core.workspace = true\n')
   f=crate/'src/lib.rs';f.write_text('// Nostr already existed\n')
   git('add','.');git('commit','-qm','base');base=git('rev-parse','HEAD')
   f.write_text('// Nostr already existed\n// WebDAV added <script>alert(1)</script>\n')
   git('add','.');git('commit','-qm','new WebDAV');head=git('rev-parse','HEAD')
   report=p.analyze(root,base,head)
   self.assertEqual(report['modules'][0]['dependencies'],['astro-db'])
   self.assertEqual(report['modules'][0]['changed_files'],1)
   self.assertEqual([m['protocol'] for m in report['protocol_mentions']],['WebDAV'])
   self.assertEqual(report['protocol_mentions'][0]['line'],2)
   (root/'figure.html').write_text('<svg></svg>')
   p.render(report,root)
   rendered=(root/'index.html').read_text()
   self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',rendered)
   self.assertNotIn('<script>alert(1)</script>',rendered)
   self.assertIn(head+'/crates/astro-demo/src/lib.rs#L2',rendered)
if __name__=='__main__':unittest.main()
