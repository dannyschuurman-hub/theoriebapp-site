from pathlib import Path
import unittest,json,re
class Homepage(unittest.TestCase):
 def test_truth_and_delivery(self):
  p=Path('_v2/index.html'); self.assertTrue(p.exists(),'Homepage ontbreekt')
  s=p.read_text()
  for q in json.loads(Path('/Users/dannyschuurman/Developer/theorie-b-app/Theorie/Resources/vragen.json').read_text()):
   if q['id'] in ['q142','q10','q04']:
    self.assertIn(q['question']['nl'],s)
    self.assertIn(q['explanation']['nl'],s)
    self.assertIn(q['law'],s)
    for option in q['options']['nl']: self.assertIn(option,s)
  self.assertEqual(len(re.findall('class="result-dot',s)),50)
  self.assertNotIn('—',s)
  self.assertIn("script-src 'self'",s)
  for name in ['style.css','site.js']: self.assertTrue(Path('_v2',name).exists())
if __name__=='__main__': unittest.main()
