"""Render the shared v2 home template in Dutch and English."""
import html, json, re, shutil
from pathlib import Path
import blog

def nav(t, other_href=None):
 en=t['lang']=='en'
 return f'''<header class="mag-nav"><a class="brand" href="{t['home']}"><img src="/assets/icon-192.webp" width="34" height="34" alt="">Theorie B</a><nav aria-label="{'Main navigation' if en else 'Hoofdnavigatie'}"><a href="/blog/">Magazine</a><a class="lang" href="{other_href or t['other']}" lang="{'nl' if en else 'en'}">{t['otherlab']}</a><a class="nav-app" href="{t['store']}">{'Practise in the app' if en else 'Oefen in de app'} ↗</a></nav></header>'''

def foot(t):
 return f'''<footer class="mag-footer"><a class="footer-word" href="{t['home']}">Theorie B<span>↗</span></a><div><p>{'Understand the rules. Pay attention to the road.' if t['lang']=='en' else 'Verkeersregels begrijpen. Met aandacht voor de weg.'}</p><p>{t['foot']}</p></div><nav aria-label="Footer"><a href="/blog/">Magazine</a><a href="{t['sup']}">Support</a><a href="{t['pri']}">Privacy</a><a href="/blog/feed.xml">RSS</a></nav></footer>'''

def assets():
 dest=Path('assets/home');dest.mkdir(exist_ok=True)
 for p in Path('_v2/assets').iterdir():
  if p.suffix in ['.webp','.woff2','.svg','.png']: shutil.copyfile(p,dest/p.name)
 shutil.copyfile('_v2/site.js',dest/'site.js')
 (dest/'style.css').write_text(Path('_v2/style.css').read_text().replace('url(assets/','url(/assets/home/'))

def render(t,path,alt,head,blogs):
 s=Path('_v2/home.html').read_text()
 s=re.sub(r'(?<=["\'])assets/', '/assets/home/',s).replace('src="site.js"','src="/assets/home/site.js"')
 if t['lang']=='en':
  # Translate exact question/option/explanation strings from the app's source.
  pairs={}
  for q in json.loads(blog.VRAGEN.read_text()):
   for key in ['question','explanation']:
    pairs[q[key]['nl']]=q[key]['en']
   pairs.update(zip(q['options']['nl'],q['options']['en']))
  pairs.update(EN)
  def vertaal(m):
   t=html.unescape(m[1]); kern=t.strip(); voor=t[:len(t)-len(t.lstrip())]; na=t[len(t.rstrip()):]
   return '>'+voor+html.escape(pairs.get(kern,kern),quote=False)+na+'<' if kern in pairs else m[0]
  s=re.sub(r'>([^<>]+)<',vertaal,s)
  s=s.replace('<div class="question-card" lang="nl"','<div class="question-card" lang="en"')
  # Question language is independent of app language. Restore both language-demo
  # cards, while retaining translated app navigation, progress and bottom bar.
  original=Path('_v2/home.html').read_text()
  for lang in ['nl','en']:
   pattern=r'(<article class="question language-'+lang+r'".*?)(<div class="question-card".*?)(?=</div><div class="app-bottom">)'
   card=re.search(pattern,original)[2]
   card=card.replace('Vraag in het Engels','Question in English').replace('Vraag in het Nederlands','Question in Dutch')
   s=re.sub(pattern,lambda m:m[1]+card,s)
  s=s.replace('appstore-nl.svg','appstore-en.svg').replace('Download in de App Store','Download on the App Store').replace('https://apps.apple.com/nl/','https://apps.apple.com/')
  s=s.replace('lang="nl"><div class="app-nav"','lang="en"><div class="app-nav"')
  s=s.replace('Vanachter het stuur in de schemering: natte straat, bakstenen huizen, grachtbrug met witte leuningen, brandende lantaarns, geel verkeerslicht en stopstreep.','Driver’s view at dusk: wet street, brick houses, white-railed canal bridge, lit streetlights, amber traffic light and stop line.').replace('Het kruispunt in het blauwe uur.','The junction at dusk.').replace('Taal van de voorbeeldvraag','Language of the sample question')
 cards=''
 if blogs:
  cards=blog.card(blogs[0],True)+'<div class="card-grid">'+''.join(blog.card(b) for b in blogs[1:4])+'</div>'
 magazine='<section class="home-magazine wrap"><p class="kicker">'+('THE MAGAZINE · ARTICLES IN DUTCH' if t['lang']=='en' else 'VOOR DAT ENE TWIJFELMOMENT')+'</p><h2>'+('Understand the road.' if t['lang']=='en' else 'Verkeersregels uitgelegd.')+'</h2>'+cards+'<a class="text-link" href="/blog/">'+('Explore the magazine' if t['lang']=='en' else 'Naar het magazine')+' ↗</a></section>'
 s=s.replace('/assets/home/appstore-en.svg','/assets/appstore-en.svg').replace('/assets/home/appstore-nl.svg','/assets/appstore-nl.svg')
 s=s.replace('{{MAGAZINE}}',magazine).replace('{{HEADER}}',nav(t)).replace('{{FOOTER}}',foot(t))
 ld={'@context':'https://schema.org','@type':'MobileApplication','name':'Theorie B','operatingSystem':'iOS','applicationCategory':'EducationalApplication','inLanguage':['nl','en'],'url':path,'downloadUrl':t['store'],'description':t['desc']}
 # Canonical absolute URL also identifies the application.
 h=head(t,t['title'],t['desc'],path,alt,'<link rel="stylesheet" href="/assets/home/style.css"><script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
 base=re.search(r'rel="canonical" href="([^"]+)"',h)[1]
 h=h.replace('"url": "'+path+'"','"url": "'+base+'"')
 return h+'<body class="home-v2">'+s+'</body></html>'

EN = {
'OEFENEN. MET UITLEG.':'PRACTISE. WITH EXPLANATIONS.',
'Vraag 1 van 10':'Question 1 of 10','Kies een antwoord':'Choose an answer',
'Goed':'Correct','Niet goed':'Incorrect','Fout melden':'Report an error',
'Vraag in het Engels':'Question in Dutch','Vraag in het Nederlands':'Question in English',
'Haal jij 44?':'Can you get 44?',
'Oefen voor je theorie-examen auto. Je hebt 44 van de 50 vragen goed nodig.':'Practise for your car theory test. You need 44 out of 50 correct.',
'Start gratis proefexamen':'Start free mock exam',
'50 vragen · 30 minuten · 44 goed nodig':'50 questions · 30 minutes · 44 correct needed',
'Vul je examendatum in':'Add your exam date','Oefen per onderwerp':'Practise by topic',
'Alle 225 oefenvragen':'All 225 practice questions','Eenmalig betalen.':'One-time purchase.',
'Theorie B heeft eigen oefenvragen en geen band met het CBR. Je score zegt niets over je CBR-uitslag en geeft geen garantie dat je slaagt.':'Theorie B uses its own practice questions and has no link to the CBR. Your score says nothing about your CBR result and does not guarantee that you will pass.',
'Over deze app':'About this app',
'Naar de inhoud':'Skip to content','JE THEORIE-EXAMEN BEGINT HIER.':'YOUR THEORY TEST STARTS HERE.', 'Haal jij ':'Can you get ', 'Haal jij':'Can you get',
'Het licht wordt geel.':'The light turns amber.','Jij weet wat je doet.':'You know what to do.','Theorie B voor iPhone':'Theorie B for iPhone','Oefenen. Begrijpen. Door.':'Practise. Understand. Move on.',
'50 vragen. 30 minuten.':'50 questions. 30 minutes.','Even alleen jij.':'Just you and the road.','Start proefexamen ↗':'Start mock test ↗',
'EEN PROEFEXAMEN. JIJ AAN HET STUUR.':'A MOCK TEST. YOU AT THE WHEEL.','Geel.':'Amber.','En nu?':'What now?', 'Een antwoord kiezen is één ding.':'Choosing an answer is one thing.','Weten waarom is alles.':'Understanding why makes the difference.',
'Jij slaat af.':'You are turning.','Wie gaat voor?':'Who goes first?','Even twijfelen.':'A moment of doubt.','Dan valt het op zijn plek.':'Then it all makes sense.','De file':'The traffic','beweegt. Jij ook?':'moves. Can you?', 'Vraag voor vraag.':'Question by question.','Tot je het ziet.':'Until you see it.','Een kijkje in de app · scroll om te oefenen':'Inside the app · scroll to practise',
'VERKEERSTEKENS':'TRAFFIC SIGNS','VOORRANG EN VOOR LATEN GAAN':'PRIORITY AND GIVING WAY','GEBRUIK VAN DE WEG':'USE OF THE ROAD','✓ Goed':'✓ Correct','× Fout':'× Incorrect','Volgende vraag':'Next question',
'Vraag 1 van 50':'Question 1 of 50','Vraag 2 van 50':'Question 2 of 50','Vraag 3 van 50':'Question 3 of 50','DE GRENS VAN 44':'THE 44 PASS MARK','Nog één.':'One more.','En dan ':'And then ', 'adem uit.':'breathe out.','44 goed nodig.':'44 correct to pass.','Voorbeelduitslag van een proefexamen.':'Sample mock test result.','JE PROEFEXAMEN':'YOUR MOCK TEST','Grens van 44 gehaald.':'44 pass mark reached.','● Goed':'● Correct','44 nodig':'44 to pass','Je ziet wat goed ging.':'See what went well.','En waar je nog kunt groeien.':'And where you can improve.',
'225 EIGEN OEFENVRAGEN':'225 ORIGINAL PRACTICE QUESTIONS','Elke bocht.':'Every turn.','Elk onderwerp.':'Every topic.','9 onderwerpen. Elk 25 vragen.':'9 topics. 25 questions each.','25 VRAGEN':'25 QUESTIONS','25 vragen':'25 questions','Oefen in je eigen tempo.':'Practise at your own pace.',
'Gebruik van de weg':'Use of the road','Voorrang en voor laten gaan':'Priority and giving way','Bijzondere wegen en manoeuvres':'Special roads and manoeuvres','Veilig rijden en noodsituaties':'Safe driving and emergencies','Verkeerstekens':'Traffic signs','Verantwoord rijden':'Responsible driving','Wetgeving':'Legislation','Voertuigkennis':'Vehicle knowledge','Rijhulpsystemen':'Driver assistance',
'Ken de regels rond je rijbewijs en deelname aan het verkeer.':'Know the rules for your licence and the road.','Leer je auto kennen en ga veilig op weg.':'Know your car and prepare for a safe journey.','Begrijp wat je rijhulpsystemen voor je doen.':'Understand how driver assistance supports you.',
'HETZELFDE INZICHT':'THE SAME UNDERSTANDING','In de taal':'In the language','die bij je past.':'that suits you.','Nederlands of Engels.':'Dutch or English.','Wissel de app. Of alleen de vraag.':'Switch the app. Or just the question.',
'KLAAR VOOR JE EERSTE RONDE?':'READY FOR YOUR FIRST ROUND?','Begin met tien.':'Start with ten.','Ga voor 44.':'Go for 44.','10 oefenvragen en je eerste proefexamen zijn gratis.':'10 practice questions and your first mock test are free.','Inclusief uitleg en je fouten terugkijken.':'With explanations and a review of your mistakes.','Daarna alle 225 vragen?':'Ready for all 225 questions?','Eén aankoop. Onbeperkt oefenen.':'One purchase. Unlimited practice.','Eenmalig € 7,99':'One-off € 7.99','Geen abonnement. Geen reclame. Geen account.':'No subscription. No ads. No account.','Je voortgang blijft op je iPhone.':'Your progress stays on your iPhone.','Jouw volgende stap.':'Your next step.','Op groen.':'Go on green.'}
