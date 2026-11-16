#!/usr/bin/env python3
"""Genereert alle pagina's. Run: python3 build.py"""
import re, os, html, sys
SRC = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/App-niches/03_theorie/appstore/web")
STORE = "https://apps.apple.com/nl/app/id6834047508"
BASE = sys.argv[1].rstrip("/") if len(sys.argv)>1 else "https://theorieb.example"  # python3 build.py https://domein.nl
REAL = len(sys.argv)>1
FONT = '<link rel="preload" href="/assets/fonts/inter-tight-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>'

T = {
 "nl": dict(lang="nl", home="/", other="/en/", otherlab="English", sup="/support/", pri="/privacy/", badge="appstore-nl.svg", store=STORE, badgealt="Download in de App Store",
  title="Theorie B: auto examen oefenen", desc="Oefen voor je theorie-examen auto en begrijp waarom een antwoord klopt, met uitleg en bron bij elke vraag. Proefexamen met 50 vragen in 30 minuten, in het Nederlands en Engels.",
  h1="Haal jij 44?", sub="Oefen voor je theorie-examen auto en begrijp waarom een antwoord klopt, met uitleg en bron bij elke vraag.",
  btn="Download in de App Store", chips=["Geen abonnement","Geen reclame","Ook in het Engels"], alt_hero="Theorie B uitslagscherm: 49 van 50 goed, grens van 44 gehaald",
  secs=[("Oefen met uitleg","225 zelfgeschreven oefenvragen op basis van de Nederlandse verkeerswetten, in 9 onderwerpen met elk 25 vragen. Bij elk antwoord staat uitleg met een wetsverwijzing, zoals RVV 1990, art. 15 lid 1.","nl-02-uitleg.webp","Theorie B toont een goed antwoord met uitleg en bron"),
        ("Proefexamen in 30 minuten","Doe een proefexamen met 50 vragen in 30 minuten. Je hebt 44 goede antwoorden nodig. Na afloop zie je je uitslag in 50 stippen en je score per onderwerp.","nl-03-proefexamen.webp","Theorie B proefexamen: 50 vragen, 44 goed nodig"),
        ("Nederlands of Engels","Wissel de taal van de hele app of lees per vraag de andere taal.","nl-04-engels.webp","Theorie B in het Nederlands en het Engels"),
        ("225 vragen, 9 onderwerpen","Oefen per onderwerp, in je eigen tempo. Je ziet je voortgang per onderwerp.","nl-05-onderwerpen.webp","Theorie B onderwerpenoverzicht met voortgang")],
  cta_h="Gratis proberen", cta_p="Gratis: één ronde van 10 oefenvragen en je eerste proefexamen, inclusief uitleg, fouten terugkijken en je scorekaart. Met één aankoop krijg je alle 225 vragen en kun je onbeperkt oefenen en proefexamens doen. Geen abonnement of advertenties. Een account of login is niet nodig.",
  price="Eenmalig € 7,99", privacy_line="Je voortgang blijft op je iPhone. Er worden geen gegevens verzameld.",
  foot="Onafhankelijk van het CBR.", suplab="Support", prilab="Privacy", share="/assets/share.jpg", shalt="Theorie B: Haal jij 44? Oefen voor je theorie-examen auto", hero="hero-nl.webp"),
 "en": dict(lang="en", home="/en/", other="/", otherlab="Nederlands", sup="/en/support/", pri="/en/privacy/", badge="appstore-en.svg", store="https://apps.apple.com/app/id6834047508", badgealt="Download on the App Store",
  title="Theorie B: Dutch theory test", desc="Practise for your Dutch car theory test and understand each answer, with an explanation and a source for every question. Mock test with 50 questions in 30 minutes, in English or Dutch.",
  h1="Can you get 44?", sub="Practise for your Dutch car theory test and understand each answer, with an explanation and a source for every question.",
  btn="Download on the App Store", chips=["No subscription","No ads","Dutch or English"], alt_hero="Theorie B result screen: 49 out of 50 correct, the 44 pass mark reached",
  secs=[("Know why","225 questions written by the maker, based on Dutch traffic law, in 9 topics with 25 questions each. Every answer includes an explanation and a source, such as RVV 1990, art. 15 lid 1.","en-02-uitleg.webp","Theorie B shows a correct answer with an explanation and source"),
        ("Mock test: 30 minutes","Take a mock test with 50 questions in 30 minutes. You need 44 correct answers. See all 50 answers as dots, plus your score by topic.","en-03-proefexamen.webp","Theorie B mock test: 50 questions, 44 correct to pass"),
        ("English or Dutch","Switch the language of the whole app, or read an individual question in the other language.","en-04-engels.webp","Theorie B in English and Dutch"),
        ("225 questions, 9 topics","Practise by topic, at your own pace. See your progress by topic.","en-05-onderwerpen.webp","Theorie B topic overview with progress")],
  cta_h="Try it free", cta_p="Free: one round of 10 practice questions and your first mock test, including explanations, mistake review and your scorecard. A one-off purchase gives you all 225 questions and unlimited practice and mock tests. There is no subscription or advertising. You do not need an account or login.",
  price="One-off € 7.99", privacy_line="Your progress stays on your iPhone. No data is collected.",
  foot="Independent of the CBR.", suplab="Support", prilab="Privacy", share="/assets/share-en.jpg", shalt="Theorie B: Can you get 44? Dutch car theory test, in English", hero="hero-en.webp"),
}

def head(t, title, desc, path, alt_path, extra="", ogtype="website"):
    nlp, enp = (path, alt_path) if t["lang"]=="nl" else (alt_path, path)
    alts = "" if alt_path is None else f'''<link rel="alternate" hreflang="nl" href="{BASE}{nlp}">
<link rel="alternate" hreflang="en" href="{BASE}{enp}">
<link rel="alternate" hreflang="x-default" href="{BASE}{nlp}">
'''
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; font-src 'self'; script-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="color-scheme" content="light">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="apple-itunes-app" content="app-id=6834047508">
<meta name="theme-color" content="#F4FA58">
<link rel="canonical" href="{BASE}{path}">
{alts}<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Theorie B">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}{t['share']}">
<meta property="og:image:alt" content="{html.escape(t['shalt'])}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{'nl_NL' if t['lang']=='nl' else 'en_GB'}">
{'' if alt_path is None else '<meta property="og:locale:alternate" content="' + ('en_GB' if t['lang']=='nl' else 'nl_NL') + '">'}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{FONT}
<link rel="stylesheet" href="/style.css">
{extra}</head>
'''

def nav(t, other_href=None):
    return f'''<header class="top"><a class="brand" href="{t['home']}"><img src="/assets/icon-192.webp" width="32" height="32" alt="" ><span>Theorie B</span></a>
<a class="lang" href="{other_href or t['other']}" lang="{'en' if t['lang']=='nl' else 'nl'}">{t['otherlab']}</a></header>
'''

def foot(t):
    return f'''<footer class="foot"><p>{t['foot']}</p><nav aria-label="Footer">{'<a href="/blog/">Verkeersregels uitgelegd</a>' if t['lang']=='nl' else ''}<a href="{t['sup']}">{t['suplab']}</a><a href="{t['pri']}">{t['prilab']}</a></nav></footer>
'''

def home(t, path, alt):
    ld = '{"@context":"https://schema.org","@type":"MobileApplication","name":"Theorie B","operatingSystem":"iOS","applicationCategory":"EducationalApplication","inLanguage":["nl","en"],"url":"%s%s","downloadUrl":"%s","description":%s}' % (BASE, path, t["store"], '"%s"' % t['desc'].replace('"','\\"'))
    s = head(t, t['title'], t['desc'], path, alt, f'<script type="application/ld+json">{ld}</script>\n')
    s += '<body class="home">\n<a class="skip" href="#main">Skip to content</a>\n'
    s += nav(t)
    s += f'''<main id="main">
<section class="hero"><div class="hero-t"><h1>{t['h1']}</h1><p class="lead">{t['sub']}</p>
<ul class="chips">{''.join(f'<li>{c}</li>' for c in t['chips'])}</ul>
<p><a class="badge" href="{t['store']}"><img src="/assets/{t['badge']}" width="150" height="50" alt="{t['badgealt']}"></a></p></div>
<img class="hero-img" src="/assets/{t['hero']}" width="640" height="1354" alt="{t['alt_hero']}" fetchpriority="high"></section>
'''
    for i,(h,p,img,alt) in enumerate(t['secs']):
        s += f'''<section class="row{' rev' if i%2 else ''}"><div class="row-t"><h2>{h}</h2><p>{p}</p></div><img src="/assets/{img}" width="640" height="1391" loading="lazy" alt="{alt}"></section>
'''
    if t['lang']=='nl' and BLOGS:
        s += '<section class="uitleg"><h2>Verkeersregels uitgelegd</h2><ul class="bloglijst">' + ''.join(f'<li><a href="/blog/{b["slug"]}/">{html.escape(b["titel"])}</a></li>' for b in BLOGS) + '</ul><p><a href="/blog/">Alle uitleg</a></p></section>\n'
    s += f'''<section class="cta"><h2>{t['cta_h']}</h2><p>{t['cta_p']}</p><p class="price">{t['price']}</p><p><a class="badge" href="{t['store']}"><img src="/assets/{t['badge']}" width="150" height="50" alt="{t['badgealt']}"></a></p><p class="small">{t['privacy_line']}</p></section>
</main>
'''
    s += foot(t) + '</body>\n</html>\n'
    return s

def page(src, out, lang, other_out):
    t = T[lang]
    raw = open(os.path.join(SRC, src), encoding="utf-8").read()
    m = re.search(r'<title>(.*?)</title>', raw, re.S)
    title = m.group(1)
    body = re.search(r'<body><main>(.*)</main></body>', raw, re.S).group(1)
    # strip old brand bar, keep rest of text identical
    body = re.sub(r'<div class="merk">.*?</div>', '', body, count=1, flags=re.S)
    body = body.replace('href="privacy.html"', 'href="/privacy/"').replace('href="privacy-en.html"', 'href="/en/privacy/"')
    body = body.replace('href="support.html"', 'href="/support/"').replace('href="support-en.html"', 'href="/en/support/"')
    path = "/" + out.replace("index.html","")
    alt = "/" + other_out.replace("index.html","")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    s = head(t, title, title, path, alt)
    s += '<body class="doc">\n<a class="skip" href="#main">Skip to content</a>\n'
    s += nav(t, alt)
    s += f'<main id="main" class="doc-main">{body}</main>\n' + foot(t) + '</body>\n</html>\n'
    open(out, "w", encoding="utf-8").write(s)

import blog
BLOGS = blog.lees()
blog.bouw(head, nav, foot, T, BASE, STORE)
open("index.html","w").write(home(T["nl"], "/", "/en/"))
open("en/index.html","w").write(home(T["en"], "/en/", "/"))
page("klaar-voor-1.0.1/support.html","support/index.html","nl","en/support/index.html")
page("klaar-voor-1.0.1/support-en.html","en/support/index.html","en","support/index.html")
page("privacy.html","privacy/index.html","nl","en/privacy/index.html")
page("privacy-en.html","en/privacy/index.html","en","privacy/index.html")

pages = ["/","/en/","/support/","/en/support/","/privacy/","/en/privacy/"]
pair = {"/":("/","/en/"),"/en/":("/","/en/"),"/support/":("/support/","/en/support/"),"/en/support/":("/support/","/en/support/"),"/privacy/":("/privacy/","/en/privacy/"),"/en/privacy/":("/privacy/","/en/privacy/")}
x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for p in pages:
    a,b = pair[p]
    x += f' <url><loc>{BASE}{p}</loc><xhtml:link rel="alternate" hreflang="nl" href="{BASE}{a}"/><xhtml:link rel="alternate" hreflang="en" href="{BASE}{b}"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{a}"/></url>\n'
x += f' <url><loc>{BASE}/blog/</loc><lastmod>{blog.DATUM}</lastmod></url>\n' + ''.join(f' <url><loc>{BASE}/blog/{b["slug"]}/</loc><lastmod>{blog.DATUM}</lastmod></url>\n' for b in BLOGS)
open("sitemap.xml","w").write(x+'</urlset>\n')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(".nojekyll","w").write("")
if REAL: open("CNAME","w").write(BASE.split("://")[-1]+"\n")

n=T["nl"]; e=T["en"]
doc = f"""{head(n,"Theorie B: pagina niet gevonden / page not found","Pagina niet gevonden. Page not found.","/404.html","/404.html")}<body class="doc">
{nav(n)}<main id="main" class="doc-main"><h1>404</h1><p>Deze pagina bestaat niet. <a href="/">Terug naar Theorie B</a></p><p lang="en">This page does not exist. <a href="/en/">Back to Theorie B</a></p></main>
{foot(n)}</body>
</html>
"""
open("404.html","w").write(doc)
open("llms.txt","w").write(f"""# Theorie B

> Theorie B is an iPhone app to practise for the Dutch car theory test (category B), in Dutch or English, with an explanation and a source for every answer. 225 original practice questions, mock test of 50 questions in 30 minutes, 44 correct needed. Independent of the CBR.

## Pages

- [Theorie B (Nederlands)]({BASE}/): Oefen voor je theorie-examen auto met uitleg en bron bij elke vraag.
- [Theorie B (English)]({BASE}/en/): Practise for your Dutch car theory test with an explanation and a source for every question.
- [Support (Nederlands)]({BASE}/support/)
- [Support (English)]({BASE}/en/support/)
- [Privacy (Nederlands)]({BASE}/privacy/)
- [Privacy (English)]({BASE}/en/privacy/)
- [Verkeersregels uitgelegd (Nederlands)]({BASE}/blog/): korte uitleg per verkeersregel met wetsartikel en oefenvraag.
- [App Store]({STORE})
""")
