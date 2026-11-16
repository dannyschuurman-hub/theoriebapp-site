import unittest, subprocess, pathlib, re, json
from pathlib import Path
class Build(unittest.TestCase):
 def test_build_contract(self):
  cname=pathlib.Path('CNAME'); before=(cname.read_bytes(),cname.stat().st_mtime_ns)
  subprocess.run(['python3','build.py','https://theoriebapp.nl'],check=True)
  self.assertEqual(before,(cname.read_bytes(),cname.stat().st_mtime_ns),'CNAME must remain untouched')
  for lang,path in [('nl','index.html'),('en','en/index.html')]:
   s=pathlib.Path(path).read_text()
   self.assertIn('class="exam"',s)
   self.assertIn('/assets/home/site.js',s)
   self.assertIn('class="card featured"',s)
   self.assertNotIn('topic-screen',s)
   self.assertIn("script-src 'self'",s)
   if lang=='en':
    q=json.loads(pathlib.Path('/Users/dannyschuurman/Developer/theorie-b-app/Theorie/Resources/vragen.json').read_text())
    for x in q:
     if x['id'] in ['q142','q10','q04']: self.assertIn(x['question']['en'],s)
  for p in ['support/index.html','privacy/index.html','en/support/index.html','en/privacy/index.html','404.html']:
   s=pathlib.Path(p).read_text();self.assertIn('class="mag-nav"',s);self.assertIn("script-src 'self'",s)
 def test_links_and_seo(self):
  from html.parser import HTMLParser
  from urllib.parse import urlsplit,unquote
  class Links(HTMLParser):
   def __init__(self): super().__init__();self.links=[]
   def handle_starttag(self,tag,attrs):
    for k,v in attrs:
     if k in ('src','href') and v: self.links.append(v)
  pages=[Path('index.html'),Path('404.html'),*Path('en').rglob('*.html'),*Path('support').rglob('*.html'),*Path('privacy').rglob('*.html'),*Path('blog').rglob('*.html')]
  for p in pages:
   text=p.read_text();parser=Links();parser.feed(text)
   self.assertIn("script-src 'self'",text,str(p))
   self.assertIn('rel="canonical"',text,str(p))
   for link in parser.links:
    u=urlsplit(link)
    if u.scheme or u.netloc or not u.path: continue
    target=Path(unquote(u.path).lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
    if target.is_dir(): target/= 'index.html'
    self.assertTrue(target.is_file(),f'{p}: missing {link}')
  for p in [Path('index.html'),Path('en/index.html')]:
   text=p.read_text()
   for lang in ['nl','en','x-default']: self.assertIn(f'hreflang="{lang}"',text)
   ld=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text)]
   app=next(x for x in ld if x['@type']=='MobileApplication')
   self.assertTrue(app['url'].startswith('https://theoriebapp.nl/'))
 def test_document_text_unchanged(self):
  from html.parser import HTMLParser
  class Text(HTMLParser):
   def __init__(self):super().__init__();self.active=False;self.words=[]
   def handle_starttag(self,t,a):
    if t=='main':self.active=True
   def handle_endtag(self,t):
    if t=='main':self.active=False
   def handle_data(self,d):
    if self.active:self.words.extend(d.split())
  for p in ['support/index.html','privacy/index.html','en/support/index.html','en/privacy/index.html']:
   before=subprocess.run(['git','show','HEAD:'+p],capture_output=True,text=True,check=True).stdout
   a=Text();a.feed(before);b=Text();b.feed(pathlib.Path(p).read_text())
   self.assertEqual(a.words,b.words,p)
 def test_new_article_is_rendered_from_data(self):
  import runpy, sys, home_v2
  previous=sys.argv
  try:
   sys.argv=['build.py','https://theoriebapp.nl']
   ns=runpy.run_path('build.py')
  finally: sys.argv=previous
  article=dict(ns['BLOGS'][0],slug='nieuw-artikel-test',titel='Een nieuw artikel uit de bron')
  output=home_v2.render(ns['T']['nl'],'/','/en/',ns['head'],[article]+ns['BLOGS'])
  self.assertIn('/blog/nieuw-artikel-test/',output)
  self.assertIn('Een nieuw artikel uit de bron',output)
  self.assertIn('/assets/blog/cover/',output)
  self.assertEqual(output.count('class="card featured"'),1)
if __name__=='__main__': unittest.main()
