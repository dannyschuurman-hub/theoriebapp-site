"""Theorie B magazine in NL en EN, gebouwd uit blogs.json en blog-hubs.json (WEBSITE-RECEPT 1b).

Bron: iCloud App-niches/03_theorie/marketing/blog-concepten/. Een artikel komt online vanaf zijn datum.
Een taal wordt alleen gebouwd als die taal een slug heeft; hreflang koppelt alleen bestaande paren.
"""
import re, html, json, math
from pathlib import Path
from datetime import date, datetime
from email.utils import format_datetime
from xml.etree import ElementTree as ET
BRON = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/App-niches/03_theorie/marketing/blog-concepten'
VRAGEN = Path.home() / 'Developer/theorie-b-app/Theorie/Resources/vragen.json'
DATUM = date.today().isoformat()
TALEN = ('nl', 'en')
BASIS = {'nl': '/blog/', 'en': '/en/blog/'}
HUBMAP = {'nl': 'onderwerp', 'en': 'topic'}
L = {
 'nl': dict(maanden=['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december'],
  lezen='min lezen', kicker_mag='Het Theorie B magazine', h1_mag='Begrijp de weg.',
  lead_mag='De regels achter alledaagse verkeerssituaties.<br>Helder uitgelegd, zodat je weet waarom.', editie='VERKEERSREGELS / UITGELEGD',
  chips='Onderwerpen', uitgelicht='Uitgelicht', verder='Verder op weg', artikelen='artikelen', alle='← Alle onderwerpen', onderwerp='Onderwerp',
  terug='← Magazine', redactie='Redactie Theorie B', in_artikel='In dit artikel', test='Test je kennis ↓', kort='Kort antwoord', regel='De regel',
  lees_ook='Lees ook', alle_art='Alle artikelen ↗', quiz='Even proberen / Oefenvraag', bekijk='Bekijk het antwoord', goed='Goed gezien.',
  fout='Nog niet goed. Dit is de regel:', cta_kicker='Van begrijpen naar oefenen', cta_h_topic='Oefen dit onderwerp in de app',
  cta_h='Neem de volgende afslag met vertrouwen.', cta_p='225 oefenvragen met uitleg en wetsartikel.',
  cta_small='Gratis proberen · Geen abonnement · Geen account', badge='/assets/appstore-nl.svg', badge_alt='Download in de App Store',
  mag_title='Verkeersregels uitgelegd | Theorie B magazine',
  mag_desc='Begrijp de regels op de Nederlandse weg. Lees heldere uitleg per onderwerp, ontdek herkenbare verkeerssituaties en test jezelf met een oefenvraag.',
  rss_desc='Verkeersregels helder uitgelegd', rss_lang='nl-nl', meta_extra='. Met een oefenvraag en uitleg bij het antwoord.',
  skip='Naar de inhoud', test_kop='## Test jezelf', wet='De wettelijke basis'),
 'en': dict(maanden=['January','February','March','April','May','June','July','August','September','October','November','December'],
  lezen='min read', kicker_mag='The Theorie B magazine', h1_mag='Understand the road.',
  lead_mag='The rules behind everyday traffic situations in the Netherlands.<br>Clearly explained, so you know why.', editie='DUTCH TRAFFIC RULES / EXPLAINED',
  chips='Topics', uitgelicht='Featured', verder='More to read', artikelen='articles', alle='← All topics', onderwerp='Topic',
  terug='← Magazine', redactie='Theorie B editorial team', in_artikel='In this article', test='Test yourself ↓', kort='Short answer', regel='The rule',
  lees_ook='Read next', alle_art='All articles ↗', quiz='Try it / Practice question', bekijk='Show the answer', goed='Well spotted.',
  fout='Not quite. This is the rule:', cta_kicker='From understanding to practising', cta_h_topic='Practise this topic in the app',
  cta_h='Take the next turn with confidence.', cta_p='225 practice questions with explanations and the law article.',
  cta_small='Try it free · No subscription · No account', badge='/assets/appstore-en.svg', badge_alt='Download on the App Store',
  mag_title='Dutch traffic rules explained | Theorie B magazine',
  mag_desc='Understand the rules of the road in the Netherlands. Clear explanations by topic for your Dutch car theory test, each with a practice question.',
  rss_desc='Dutch traffic rules, clearly explained', rss_lang='en-gb', meta_extra='. With a practice question and an explained answer.',
  skip='Skip to content', test_kop='## Test yourself', wet='The legal basis'),
}
_HUBS = json.loads((BRON / 'blog-hubs.json').read_text())['hubs']
HUBS = {h['onderwerp']: h for h in _HUBS}
TOPICS = {i: (h['nl']['slug'], h['nl']['naam'], h['nl']['intro']) for i, h in HUBS.items()}  # oude vorm, voor NL-code elders


def esc(s): return html.escape(str(s), quote=True)


def _bronnen():
    return json.loads((BRON / 'blogs.json').read_text())['blogs']


def lees(taal='nl', alles=False):
    """Artikelen in één taal, nieuwste eerst. Zonder `alles` alleen met datum tot en met vandaag."""
    uit = []
    for a in _bronnen():
        x = a.get(taal) or {}
        if not x.get('slug') or (not alles and date.fromisoformat(a['datum']) > date.today()):
            continue
        andere = 'en' if taal == 'nl' else 'nl'
        b = dict(taal=taal, slug=x['slug'], titel=x['titel'], vraag=x['zoekvraag'], meta=x['meta'], body=x['tekst'],
                 topic=a['onderwerp'], qid=a['vraag'], datum=a['datum'], kort=x['kort'], cover=a['cover'],
                 paar=(a.get(andere) or {}).get('slug') or None)
        b['minuten'] = max(1, math.ceil(len(b['body'].split()) / 220))
        if len(b['meta']) < 140: b['meta'] = b['meta'].rstrip('.') + L[taal]['meta_extra']
        b['meta'] = kort_meta(b['meta'])
        uit.append(b)
    return sorted(uit, key=lambda b: b['datum'], reverse=True)


def onderwerpen(blogs): return [i for i in sorted(HUBS) if any(b['topic'] == i for b in blogs)]
def hubnaam(i, taal): return HUBS[i][taal]['naam'] or HUBS[i]['nl']['naam']
def hub(i, taal='nl'): return BASIS[taal] + HUBMAP[taal] + '/' + (HUBS[i][taal]['slug'] or HUBS[i]['nl']['slug']) + '/'
def url(b): return BASIS[b['taal']] + b['slug'] + '/'
def paar_url(b):
    if not b['paar']: return None
    return BASIS['en' if b['taal'] == 'nl' else 'nl'] + b['paar'] + '/'
def cover(b): return '/assets/blog/cover/' + b['cover'] + '.webp'


def datum(b):
    d = date.fromisoformat(b['datum']); m = L[b['taal']]['maanden'][d.month - 1]
    return f'{d.day} {m} {d.year}'


def inline(s):
    s = esc(s); s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub(r'(?<!\*)\*([^*]+)\*', r'<em>\1</em>', s)


def md(body, taal='nl'):
    body = body.split(L[taal]['test_kop'])[0]
    out = []
    for index, blok in enumerate(re.split(r'\n\s*\n', body.strip())):
        # Een los kort antwoord als tweede blok staat al boven de leeskolom; een kopje nooit overslaan.
        if index == 1 and not blok.startswith('## '): continue
        if blok.startswith('## '): out.append('<h2>' + inline(blok[3:]) + '</h2>')
        elif blok.startswith(L[taal]['wet']): continue
        else: out.append('<p>' + inline(' '.join(blok.splitlines())) + '</p>')
    return '\n'.join(out)


def kort_meta(m, grens=155):
    # SEO 22-11: meta-description max 155 tekens, afkappen op een woordgrens
    if len(m) <= grens: return m
    return m[:grens - 2].rsplit(' ', 1)[0].rstrip(',;:') .rstrip('.') + '.'


def kort_titel(t, merk=' | Theorie B', grens=60):
    # SEO 22-11: titel max 60 tekens; past het merk er niet bij, dan blijft de pure titel staan
    return t + merk if len(t) + len(merk) <= grens else t


def card(b, featured=False):
    t = L[b['taal']]
    return f'''<article class="card {'featured' if featured else ''}"><a class="card-image" href="{url(b)}"><img src="{cover(b)}" width="1600" height="900" {'fetchpriority="high"' if featured else 'loading="lazy"'} alt="{esc(b['vraag'])}"><span class="image-arrow" aria-hidden="true">↗</span></a><div class="card-copy"><a class="kicker" href="{hub(b['topic'], b['taal'])}">{esc(hubnaam(b['topic'], b['taal']))}</a><h2><a href="{url(b)}">{esc(b['titel'])}</a></h2><p class="intro">{esc(b['kort'])}</p><p class="meta"><time datetime="{b['datum']}">{datum(b)}</time><span>{b['minuten']} {t['lezen']}</span></p></div></article>'''


def cta(store, taal, topic=None):
    t = L[taal]
    return f'''<section class="mag-cta"><div><p class="kicker">{t['cta_kicker']}</p><h2>{t['cta_h_topic'] if topic else t['cta_h']}</h2><p>{t['cta_p']}</p><p class="cta-small">{t['cta_small']}</p></div><a href="{store}"><img src="{t['badge']}" width="180" height="60" alt="{t['badge_alt']}"></a></section>'''


def shell(taal, title, desc, path, alt, ld, content, head, T, image=None, published=None):
    t = dict(T[taal]); t['share'] = image or '/assets/blog/og/geel-verkeerslicht-stoppen.jpg'; t['shalt'] = title
    feed = BASIS[taal] + 'feed.xml'
    extra = f'<link rel="stylesheet" href="/blog.css"><link rel="alternate" type="application/rss+xml" title="Theorie B magazine" href="{feed}"><script src="/blog.js" defer></script>'
    if published: extra += f'<meta property="article:published_time" content="{published}">'
    extra += ''.join('<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', **x}, ensure_ascii=False).replace('<', '\\u003c') + '</script>' for x in ld)
    s = head(t, title, desc, path, alt, extra, ogtype='article' if published else 'website').replace("script-src 'none'", "script-src 'self'").replace('<link rel="stylesheet" href="/style.css">', '')
    from home_v2 import nav, foot
    return s + f'<body class="magazine"><a class="skip" href="#main">{L[taal]["skip"]}</a>' + nav(T[taal], alt) + '<main id="main">' + content + '</main>' + foot(T[taal]) + '</body></html>'


def quiz(q, taal):
    t = L[taal]
    options = ''.join(f'<button type="button" class="answer" aria-pressed="false" data-correct="{str(i == q["correct"]).lower()}"><span>{chr(65 + i)}</span>{esc(o)}</button>' for i, o in enumerate(q['options'][taal]))
    answer = q['options'][taal][q['correct']]
    return f'''<section class="quiz" aria-labelledby="quiz-title" data-goed="{esc(t['goed'])}" data-fout="{esc(t['fout'])}"><p class="kicker">{t['quiz']}</p><h2 id="quiz-title">{esc(q['question'][taal])}</h2><div class="answers">{options}</div><div class="feedback" role="status" hidden><strong class="verdict"></strong><p>{esc(q['explanation'][taal])}</p><p class="law">{esc(q['law'])}</p></div><noscript><details><summary>{t['bekijk']}</summary><p>{esc(answer)} {esc(q['explanation'][taal])}</p><p>{esc(q['law'])}</p></details></noscript></section>'''


def _opruimen(actief):
    """Haal gebouwde pagina's weg van artikelen of onderwerpen die (nog) niet online horen."""
    for taal in TALEN:
        wortel = Path('.' + BASIS[taal])
        if not wortel.is_dir(): continue
        for p in wortel.rglob('index.html'):
            rel = '/' + p.parent.as_posix().strip('./') + '/'
            if rel != BASIS[taal] and rel not in actief:
                p.unlink()


def bouw(head, nav, foot, T, BASE, STORE):
    questions = {q['id']: q for q in json.loads(VRAGEN.read_text())}
    alle = {taal: lees(taal) for taal in TALEN}
    actief = set()

    def write(path, s):
        actief.add(path)
        p = Path('.' + path + 'index.html'); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s)

    for taal in TALEN:
        blogs = alle[taal]; t = L[taal]; store = T[taal]['store']; andere = 'en' if taal == 'nl' else 'nl'
        if not blogs: continue
        tel = lambda i: sum(b['topic'] == i for b in blogs)
        chips = f'<nav class="topic-chips" aria-label="{t["chips"]}">' + ''.join(f'<a href="{hub(i, taal)}">{esc(hubnaam(i, taal))}<span>{tel(i)}</span></a>' for i in onderwerpen(blogs)) + '</nav>'
        featured = next((b for b in blogs if b['qid'] == 'q142'), blogs[0])
        content = f'<section class="mag-heading wrap"><p class="kicker">{t["kicker_mag"]}</p><h1>{t["h1_mag"]}</h1><div class="heading-bottom"><p>{t["lead_mag"]}</p><span class="edition">{t["editie"]}</span></div>' + chips + '</section>'
        content += f'<section class="wrap feature-section" aria-label="{t["uitgelicht"]}">' + card(featured, True) + '</section>'
        content += f'<section class="wrap articles"><div class="section-heading"><h2>{t["verder"]}</h2><span>{len(blogs)} {t["artikelen"]}</span></div><div class="card-grid">' + ''.join(card(b) for b in blogs if b is not featured) + '</div></section>' + cta(store, taal)
        mag_alt = BASIS[andere] if alle[andere] else None
        write(BASIS[taal], shell(taal, t['mag_title'], t['mag_desc'], BASIS[taal], mag_alt, [{'@type': 'Blog', 'name': 'Theorie B magazine', 'inLanguage': taal, 'url': BASE + BASIS[taal], 'blogPost': [{'@type': 'BlogPosting', 'headline': b['titel'], 'url': BASE + url(b)} for b in blogs]}], content, head, T))
        for i in onderwerpen(blogs):
            subset = [b for b in blogs if b['topic'] == i]; name = hubnaam(i, taal)
            hub_alt = hub(i, andere) if any(b['topic'] == i for b in alle[andere]) else None
            meta = kort_meta(HUBS[i][taal]['meta'] or HUBS[i][taal]['intro'] or HUBS[i]['nl']['meta'])
            content = f'<section class="wrap hub-heading"><a class="back" href="{BASIS[taal]}">{t["alle"]}</a><p class="kicker">{t["onderwerp"]} / {i:02d}</p><h1>{esc(name)}</h1><p class="hub-intro">{esc(HUBS[i][taal]["intro"])}</p><span class="edition">{len(subset)} {t["artikelen"]}</span></section><section class="wrap articles"><div class="card-grid">' + ''.join(card(b) for b in subset) + '</div></section>' + cta(store, taal, i)
            write(hub(i, taal), shell(taal, kort_titel(name), meta, hub(i, taal), hub_alt, [{'@type': 'CollectionPage', 'name': name, 'inLanguage': taal, 'url': BASE + hub(i, taal), 'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': j + 1, 'url': BASE + url(b), 'name': b['titel']} for j, b in enumerate(subset)]}}], content, head, T))
        for b in blogs:
            q = questions[b['qid']]; related = sorted([a for a in blogs if a is not b], key=lambda a: a['topic'] != b['topic'])[:3]
            alt = paar_url(b) if b['paar'] and any(a['slug'] == b['paar'] for a in alle[andere]) else None
            content = f'''<article><header class="article-hero"><img src="{cover(b)}" width="1600" height="900" alt="" fetchpriority="high"><div class="article-title wrap"><a class="back" href="{BASIS[taal]}">{t['terug']}</a><a class="kicker" href="{hub(b['topic'], taal)}">{esc(hubnaam(b['topic'], taal))}</a><h1>{esc(b['titel'])}</h1><p class="meta">{t['redactie']} · <time datetime="{b['datum']}">{datum(b)}</time> · {b['minuten']} {t['lezen']}</p></div></header><div class="reading-layout wrap"><aside class="article-aside"><p class="kicker">{t['in_artikel']}</p><a href="{hub(b['topic'], taal)}">{esc(hubnaam(b['topic'], taal))} ↗</a><a href="#oefenen">{t['test']}</a></aside><div class="reading"><section class="short-answer"><p class="kicker">{t['kort']}</p><p>{esc(b['kort'])}</p></section><div class="prose">{md(b['body'], taal)}<aside class="rule"><span>{t['regel']}</span><strong>{esc(q['law'])}</strong></aside></div><div id="oefenen">{quiz(q, taal)}</div></div></div></article><section class="wrap articles related"><div class="section-heading"><h2>{t['lees_ook']}</h2><a href="{BASIS[taal]}">{t['alle_art']}</a></div><div class="card-grid">{''.join(card(a) for a in related)}</div></section>''' + cta(store, taal)
            org = {'@type': 'Organization', 'name': 'Theorie B', 'url': BASE + T[taal]['home']}
            kruimels = [('Home', T[taal]['home']), ('Magazine', BASIS[taal]), (hubnaam(b['topic'], taal), hub(b['topic'], taal)), (b['titel'], url(b))]
            ld = [{'@type': 'BlogPosting', 'headline': b['titel'], 'description': b['meta'], 'image': BASE + '/assets/blog/og/' + b['cover'] + '.jpg', 'datePublished': b['datum'], 'dateModified': b['datum'], 'author': org, 'publisher': org, 'inLanguage': taal, 'mainEntityOfPage': BASE + url(b)},
                  {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': j + 1, 'name': n, 'item': BASE + p} for j, (n, p) in enumerate(kruimels)]}]
            write(url(b), shell(taal, kort_titel(b['titel']), b['meta'], url(b), alt, ld, content, head, T, '/assets/blog/og/' + b['cover'] + '.jpg', b['datum']))
        rss = ET.Element('rss', version='2.0'); channel = ET.SubElement(rss, 'channel')
        for k, v in [('title', 'Theorie B magazine'), ('link', BASE + BASIS[taal]), ('description', t['rss_desc']), ('language', t['rss_lang'])]: ET.SubElement(channel, k).text = v
        for b in blogs:
            item = ET.SubElement(channel, 'item')
            for k, v in [('title', b['titel']), ('link', BASE + url(b)), ('guid', BASE + url(b)), ('description', b['kort']), ('pubDate', format_datetime(datetime.fromisoformat(b['datum'] + 'T09:00:00+01:00')))]: ET.SubElement(item, k).text = v
        ET.ElementTree(rss).write('.' + BASIS[taal] + 'feed.xml', encoding='utf-8', xml_declaration=True)
    _opruimen(actief)
    return alle['nl']


def sitemap(_blogs, base):
    """Alle magazinepagina's in beide talen, met hreflang waar een paar bestaat."""
    alle = {taal: lees(taal) for taal in TALEN}
    regels = []

    def regel(p, d, alt=None, taal='nl'):
        x = f'<url><loc>{esc(base + p)}</loc><lastmod>{d}</lastmod>'
        if alt:
            nl, en = (p, alt) if taal == 'nl' else (alt, p)
            x += f'<xhtml:link rel="alternate" hreflang="nl" href="{esc(base + nl)}"/><xhtml:link rel="alternate" hreflang="en" href="{esc(base + en)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{esc(base + nl)}"/>'
        regels.append(x + '</url>\n')

    for taal in TALEN:
        blogs = alle[taal]; andere = 'en' if taal == 'nl' else 'nl'
        if not blogs: continue
        regel(BASIS[taal], max(b['datum'] for b in blogs), BASIS[andere] if alle[andere] else None, taal)
        for i in onderwerpen(blogs):
            regel(hub(i, taal), max(b['datum'] for b in blogs if b['topic'] == i), hub(i, andere) if any(b['topic'] == i for b in alle[andere]) else None, taal)
        for b in blogs:
            alt = paar_url(b) if b['paar'] and any(a['slug'] == b['paar'] for a in alle[andere]) else None
            regel(url(b), b['datum'], alt, taal)
    return ''.join(regels)


def llms(_blogs, base):
    uit = ''
    for taal, kop in [('nl', 'Magazine (Nederlands)'), ('en', 'Magazine (English)')]:
        blogs = lees(taal)
        if not blogs: continue
        uit += f'\n## {kop}\n\n' + ''.join(f'- [{hubnaam(i, taal)}]({base}{hub(i, taal)})\n' for i in onderwerpen(blogs)) + ''.join(f'- [{b["titel"]}]({base}{url(b)}): {b["kort"]}\n' for b in blogs)
    return uit
