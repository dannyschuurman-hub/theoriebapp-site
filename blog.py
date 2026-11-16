"""Bronbestanden vormen het magazine, de hubs, RSS en zoekmachinegegevens."""
import re, html, json, os, math
from pathlib import Path
from datetime import date, datetime
from email.utils import format_datetime
from xml.etree import ElementTree as ET
BRON = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/App-niches/03_theorie/marketing/blog-concepten'
VRAGEN = Path.home() / 'Developer/theorie-b-app/Theorie/Resources/vragen.json'
DATUM = date.today().isoformat()
TOPICS = {
1: ('gebruik-van-de-weg','Gebruik van de weg','Van je plek op de rijbaan tot parkeren. Begrijp hoe je de ruimte op de weg gebruikt.'),
2: ('voorrang','Voorrang en voor laten gaan','Wie gaat eerst? Leer kijken naar de situatie, de richting en de andere weggebruiker.'),
3: ('bijzondere-wegen-en-manoeuvres','Bijzondere wegen en manoeuvres','Wegrijden, afslaan en bijzondere situaties. We leggen uit waar je op let.'),
4: ('veilig-rijden','Veilig rijden en noodsituaties','Goed zicht en aandacht voor elkaar. De regels achter veilige keuzes onderweg.'),
5: ('verkeerstekens','Verkeerstekens','Lichten, borden en tekens op de weg. Ontdek wat ze van je vragen.'),
6: ('verantwoord-rijden','Verantwoord rijden','Houd je aandacht bij de weg. Lees de regels achter verantwoord rijgedrag.'),
7: ('wetgeving','Wetgeving','De regels achter je rijbewijs en je deelname aan het verkeer.'),
8: ('voertuigkennis','Voertuigkennis','Ken je auto en begrijp wat er nodig is om veilig op weg te gaan.'),
9: ('rijhulpsystemen','Rijhulpsystemen','Begrijp hoe rijhulpsystemen je ondersteunen tijdens het rijden.')}
HUB_META = {"1": "Leer hoe je de weg gebruikt met de artikelen van Theorie B. Lees over je plaats op de weg, rijstroken en de ruimte die je andere weggebruikers geeft.", "2": "Wanneer geef je voorrang en wie laat je voorgaan? Lees de artikelen van Theorie B over kruispunten, afslaan en omgaan met andere weggebruikers.", "3": "Lees in de artikelen van Theorie B hoe je rijdt op bijzondere wegen. Leer waar je op let bij invoegen, uitrijden, keren en andere manoeuvres.", "4": "Leer met de artikelen van Theorie B hoe je veilig rijdt en reageert op noodsituaties. Lees over afstand houden, gevaar herkennen en handelen bij pech.", "5": "Wat betekenen verkeersborden, verkeerslichten en tekens op de weg? De artikelen van Theorie B leggen uit hoe je ze herkent en wat je moet doen.", "6": "Lees hoe je verantwoord deelneemt aan het verkeer. De artikelen van Theorie B leggen uit wat vermoeidheid, alcohol en afleiding doen met je rijgedrag.", "7": "Welke wetten en regels moet je als automobilist kennen? Lees de artikelen van Theorie B over je rijbewijs, verplichte documenten en verkeersregels.", "8": "Leer je auto kennen met de artikelen van Theorie B. Lees over banden, remmen, verlichting en onderhoud, zodat je weet waar je voor vertrek op let.", "9": "Lees hoe rijhulpsystemen werken in de artikelen van Theorie B. Leer wat systemen doen bij remmen en sturen en waar je als bestuurder zelf op blijft letten."}
def esc(s): return html.escape(str(s), quote=True)
def lees():
    blogs=[]
    for f in sorted(BRON.glob('[0-9][0-9]_*.md')):
        header,body=f.read_text().strip().split('\n\n',1)
        k=dict(line.split(': ',1) for line in header.splitlines())
        if date.fromisoformat(k['DATUM']) > date.today(): continue
        b=dict(slug=k['SLUG'],titel=k['TITEL'],vraag=k['ZOEKVRAAG'],meta=k['META'],body=body,topic=int(k['ONDERWERP']),qid=k['VRAAG'],datum=k['DATUM'],kort=k['KORT'],cover=k['COVER'])
        b['minuten']=max(1,math.ceil(len(body.split())/220))
        # Een volledige beschrijving, zonder afgekapt woord of losse punt.
        if len(b['meta'])<140: b['meta']=b['meta'].rstrip('.')+'. Met een oefenvraag en uitleg bij het antwoord.'
        if len(b['meta'])>160: b['meta']=b['meta'][:157].rsplit(' ',1)[0]+'.'
        blogs.append(b)
    return sorted(blogs,key=lambda b:b['datum'],reverse=True)
def onderwerpen(blogs): return [i for i in TOPICS if any(b['topic']==i for b in blogs)]
def hub(i): return '/blog/onderwerp/'+TOPICS[i][0]+'/'
def url(b): return '/blog/'+b['slug']+'/'
def cover(b): return '/assets/blog/cover/'+b['cover']+'.webp'
def datum(b):
    d=date.fromisoformat(b['datum']); return f'{d.day} '+['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december'][d.month-1]+f' {d.year}'
def inline(s):
    s=esc(s); s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'(?<!\*)\*([^*]+)\*',r'<em>\1</em>',s)
def md(body):
    body=body.split('## Test jezelf')[0]
    out=[]
    for index,b in enumerate(re.split(r'\n\s*\n',body)):
        if index == 1: continue  # Het korte antwoord staat al boven de leeskolom.
        if b.startswith('## '): out.append('<h2>'+inline(b[3:])+'</h2>')
        elif b.startswith('De wettelijke basis'): continue
        else: out.append('<p>'+inline(' '.join(b.splitlines()))+'</p>')
    return '\n'.join(out)
def card(b, featured=False):
    return f'''<article class="card {'featured' if featured else ''}"><a class="card-image" href="{url(b)}"><img src="{cover(b)}" width="1600" height="900" {'fetchpriority="high"' if featured else 'loading="lazy"'} alt="{esc(b['vraag'])}"><span class="image-arrow" aria-hidden="true">↗</span></a><div class="card-copy"><a class="kicker" href="{hub(b['topic'])}">{esc(TOPICS[b['topic']][1])}</a><h2><a href="{url(b)}">{esc(b['titel'])}</a></h2><p class="intro">{esc(b['kort'])}</p><p class="meta"><time datetime="{b['datum']}">{datum(b)}</time><span>{b['minuten']} min lezen</span></p></div></article>'''
def cta(store,topic=None):
    return f'''<section class="mag-cta"><div><p class="kicker">Van begrijpen naar oefenen</p><h2>{'Oefen dit onderwerp in de app' if topic else 'Neem de volgende afslag met vertrouwen.'}</h2><p>225 oefenvragen met uitleg en wetsartikel.</p><p class="cta-small">Gratis proberen · Geen abonnement · Geen account</p></div><a href="{store}"><img src="/assets/appstore-nl.svg" width="180" height="60" alt="Download in de App Store"></a></section>'''
def shell(title,desc,path,ld,content,head,T,BASE,image=None,published=None):
    t=dict(T['nl']); t['share']=image or '/assets/blog/og/geel-verkeerslicht-stoppen.jpg'; t['shalt']=title
    extra='<link rel="stylesheet" href="/blog.css"><link rel="alternate" type="application/rss+xml" title="Theorie B magazine" href="/blog/feed.xml"><script src="/blog.js" defer></script>'
    if published: extra+=f'<meta property="article:published_time" content="{published}">'
    extra+=''.join('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**x},ensure_ascii=False).replace('<','\\u003c')+'</script>' for x in ld)
    s=head(t,title,desc,path,None,extra,ogtype='article' if published else 'website').replace("script-src 'none'","script-src 'self'").replace('<link rel="stylesheet" href="/style.css">','')
    from home_v2 import nav, foot
    return s+'<body class="magazine"><a class="skip" href="#main">Naar de inhoud</a>'+nav(T['nl'])+'<main id="main">'+content+'</main>'+foot(T['nl'])+'</body></html>'

def quiz(q):
    options=''.join(f'<button type="button" class="answer" aria-pressed="false" data-correct="{str(i==q["correct"]).lower()}"><span>{chr(65+i)}</span>{esc(o)}</button>' for i,o in enumerate(q['options']['nl']))
    answer=q['options']['nl'][q['correct']]
    return f'''<section class="quiz" aria-labelledby="quiz-title"><p class="kicker">Even proberen / Oefenvraag</p><h2 id="quiz-title">{esc(q['question']['nl'])}</h2><div class="answers">{options}</div><div class="feedback" role="status" hidden><strong class="verdict"></strong><p>{esc(q['explanation']['nl'])}</p><p class="law">{esc(q['law'])}</p></div><noscript><details><summary>Bekijk het antwoord</summary><p>{esc(answer)} {esc(q['explanation']['nl'])}</p><p>{esc(q['law'])}</p></details></noscript></section>'''
def bouw(head,nav,foot,T,BASE,STORE):
    blogs=lees()
    active={b['slug'] for b in blogs}
    for source in BRON.glob('[0-9][0-9]_*.md'):
        slug=re.search(r'^SLUG: (.+)$',source.read_text(),re.M).group(1)
        if slug not in active:
            Path('blog',slug,'index.html').unlink(missing_ok=True)
    for i in TOPICS:
        if i not in onderwerpen(blogs):
            Path('.'+hub(i)+'index.html').unlink(missing_ok=True)
    questions={q['id']:q for q in json.loads(VRAGEN.read_text())}
    def write(path,s):
        p=Path('.'+path+'index.html'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s)
    chips='<nav class="topic-chips" aria-label="Onderwerpen">'+''.join(f'<a href="{hub(i)}">{esc(TOPICS[i][1])}<span>{sum(b["topic"]==i for b in blogs)}</span></a>' for i in onderwerpen(blogs))+'</nav>'
    featured=next((b for b in blogs if b['qid']=='q142'),blogs[0]) if blogs else None
    content='<section class="mag-heading wrap"><p class="kicker">Het Theorie B magazine</p><h1>Begrijp de weg.</h1><div class="heading-bottom"><p>De regels achter alledaagse verkeerssituaties.<br>Helder uitgelegd, zodat je weet waarom.</p><span class="edition">VERKEERSREGELS / UITGELEGD</span></div>'+chips+'</section>'
    if featured: content+='<section class="wrap feature-section" aria-label="Uitgelicht">'+card(featured,True)+'</section>'
    content+='<section class="wrap articles"><div class="section-heading"><h2>Verder op weg</h2><span>'+str(len(blogs))+' artikelen</span></div><div class="card-grid">'+''.join(card(b) for b in blogs if b!=featured)+'</div></section>'+cta(STORE)
    write('/blog/',shell('Verkeersregels uitgelegd | Theorie B magazine','Begrijp de regels op de Nederlandse weg. Lees heldere uitleg per onderwerp, ontdek herkenbare verkeerssituaties en test jezelf met een oefenvraag.','/blog/',[{'@type':'Blog','name':'Theorie B magazine','url':BASE+'/blog/','blogPost':[{'@type':'BlogPosting','headline':b['titel'],'url':BASE+url(b)} for b in blogs]}],content,head,T,BASE))
    for i in onderwerpen(blogs):
        subset=[b for b in blogs if b['topic']==i]; name=TOPICS[i][1]
        content=f'<section class="wrap hub-heading"><a class="back" href="/blog/">← Alle onderwerpen</a><p class="kicker">Onderwerp / {i:02d}</p><h1>{esc(name)}</h1><p class="hub-intro">{esc(TOPICS[i][2])}</p><span class="edition">{len(subset)} artikelen</span></section><section class="wrap articles"><div class="card-grid">'+''.join(card(b) for b in subset)+'</div></section>'+cta(STORE,i)
        write(hub(i),shell(name+' | Theorie B',HUB_META.get(str(i),TOPICS[i][2]),hub(i),[{'@type':'CollectionPage','name':name,'url':BASE+hub(i),'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':j+1,'url':BASE+url(b),'name':b['titel']} for j,b in enumerate(subset)]}}],content,head,T,BASE))
    for b in blogs:
        q=questions[b['qid']]; related=sorted([a for a in blogs if a!=b],key=lambda a:a['topic']!=b['topic'])[:3]
        content=f'''<article><header class="article-hero"><img src="{cover(b)}" width="1600" height="900" alt="" fetchpriority="high"><div class="article-title wrap"><a class="back" href="/blog/">← Magazine</a><a class="kicker" href="{hub(b['topic'])}">{esc(TOPICS[b['topic']][1])}</a><h1>{esc(b['titel'])}</h1><p class="meta">Redactie Theorie B · <time datetime="{b['datum']}">{datum(b)}</time> · {b['minuten']} min lezen</p></div></header><div class="reading-layout wrap"><aside class="article-aside"><p class="kicker">In dit artikel</p><a href="{hub(b['topic'])}">{esc(TOPICS[b['topic']][1])} ↗</a><a href="#oefenen">Test je kennis ↓</a></aside><div class="reading"><section class="short-answer"><p class="kicker">Kort antwoord</p><p>{esc(b['kort'])}</p></section><div class="prose">{md(b['body'])}<aside class="rule"><span>De regel</span><strong>{esc(q['law'])}</strong></aside></div><div id="oefenen">{quiz(q)}</div></div></div></article><section class="wrap articles related"><div class="section-heading"><h2>Lees ook</h2><a href="/blog/">Alle artikelen ↗</a></div><div class="card-grid">{''.join(card(a) for a in related)}</div></section>'''+cta(STORE)
        org={'@type':'Organization','name':'Theorie B','url':BASE+'/'}
        ld=[{'@type':'BlogPosting','headline':b['titel'],'description':b['meta'],'image':BASE+'/assets/blog/og/'+b['cover']+'.jpg','datePublished':b['datum'],'dateModified':b['datum'],'author':org,'publisher':org,'inLanguage':'nl','mainEntityOfPage':BASE+url(b)}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':j+1,'name':n,'item':BASE+p} for j,(n,p) in enumerate([('Home','/'),('Magazine','/blog/'),(TOPICS[b['topic']][1],hub(b['topic'])),(b['titel'],url(b))])]}]
        write(url(b),shell(b['titel']+' | Theorie B',b['meta'],url(b),ld,content,head,T,BASE,'/assets/blog/og/'+b['cover']+'.jpg',b['datum']))
    rss=ET.Element('rss',version='2.0'); channel=ET.SubElement(rss,'channel')
    for k,v in [('title','Theorie B magazine'),('link',BASE+'/blog/'),('description','Verkeersregels helder uitgelegd'),('language','nl-nl')]: ET.SubElement(channel,k).text=v
    for b in blogs:
        item=ET.SubElement(channel,'item')
        for k,v in [('title',b['titel']),('link',BASE+url(b)),('guid',BASE+url(b)),('description',b['kort']),('pubDate',format_datetime(datetime.fromisoformat(b['datum']+'T09:00:00+01:00')))]: ET.SubElement(item,k).text=v
    ET.ElementTree(rss).write('blog/feed.xml',encoding='utf-8',xml_declaration=True)
    return blogs

def sitemap(blogs,base):
    last=max((b['datum'] for b in blogs),default=DATUM)
    pages=[('/blog/',last)]+[(hub(i),max(b['datum'] for b in blogs if b['topic']==i)) for i in onderwerpen(blogs)]+[(url(b),b['datum']) for b in blogs]
    return ''.join(f'<url><loc>{esc(base+p)}</loc><lastmod>{d}</lastmod></url>\n' for p,d in pages)
def llms(blogs,base):
    return '\n## Magazine\n\n'+''.join(f'- [{TOPICS[i][1]}]({base}{hub(i)})\n' for i in onderwerpen(blogs))+''.join(f'- [{b["titel"]}]({base}{url(b)}): {b["kort"]}\n' for b in blogs)
