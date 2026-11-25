"""Twee gidspagina's voor zoekers die net beginnen (SEO-ronde 25-11), gebouwd in de stijl van het magazine.

NL  /theorie-examen-auto/
EN  /en/dutch-car-theory-exam-in-english/
Alleen tekst die hier staat komt op de pagina. Geen bedragen. Examenfeiten: zie _seo-concepten-2511/.
"""
import json
from pathlib import Path
import blog

PADEN = {'nl': '/theorie-examen-auto/', 'en': '/en/dutch-car-theory-exam-in-english/'}
ARTIKELEN = {'nl': ['stilstaan-na-zebrapad', 'rechts-inhalen-in-de-file', 'fietser-van-rechts-voorrang'],
             'en': ['stopping-after-a-zebra-crossing', 'passing-on-right-in-queues', 'cyclist-from-right-priority']}

G = {
 'nl': dict(
  titel='Theorie-examen auto: zo werkt het en zo oefen je',
  meta='Wat je moet weten over het theorie-examen auto: aantal vragen, hoeveel je goed moet hebben, de tijd en hoe je oefent met uitleg bij elk antwoord.',
  kicker='Gids', h1='Theorie-examen auto: zo werkt het',
  intro='Het theorie-examen auto is het eerste deel van je rijbewijs B. Hier staat kort wat je kunt verwachten en hoe je je voorbereidt. Controleer de actuele regels altijd bij het CBR; Theorie B is onafhankelijk van het CBR.',
  secties=[
   ('wat', 'Wat is het theorie-examen?', [
     'Het theorie-examen auto is een computerexamen van het CBR over verkeersregels en verkeerssituaties. Je krijgt 50 examenvragen en 2 testvragen die niet meetellen. Je hebt 30 minuten, of 45 minuten met extra tijd. Je slaagt met minimaal 44 goede antwoorden van de 50.',
     'Je vraagt het examen aan via Mijn CBR, met DigiD. Het CBR past het examen soms aan, dus kijk voor je boekt nog even op de actuele examenpagina.']),
   ('onderwerpen', 'Waar gaan de vragen over?', [
     'Over verkeersregels en situaties onderweg. Theorie B verdeelt dat in negen onderwerpen met samen 225 eigen oefenvragen: gebruik van de weg, voorrang en voor laten gaan, bijzondere wegen en manoeuvres, veilig rijden en noodsituaties, verkeerstekens, verantwoord rijden, wetgeving, voertuigkennis en rijhulpsystemen.']),
   ('oefenen', 'Zo oefen je slim', [
     '1. Begin met losse vragen en lees bij elk antwoord waarom het klopt. Dan leer je de regel, niet alleen het antwoord.',
     '2. Doe daarna een proefexamen van 50 vragen en bekijk je fouten terug.',
     '3. Lees regels die je blijft missen na in het magazine. Een paar voorbeelden staan onderaan deze pagina.']),
   ('engels', 'Oefenen in het Nederlands of Engels', [
     'Je kunt in de app wisselen tussen Nederlands en Engels, of alleen de vraag omzetten. Welke taal je voor het examen zelf kunt kiezen, controleer je bij het CBR voor je aanvraagt. Onze <a href="/en/dutch-car-theory-exam-in-english/" hreflang="en" lang="en">gids in het Engels</a> legt uit hoe je in het Engels oefent.']),
   ('proberen', 'Theorie B proberen', [
     '10 oefenvragen en je eerste proefexamen zijn gratis. Je hebt geen account nodig, er is geen reclame en je voortgang blijft op je iPhone.'])],
  faq_kop='Veelgestelde vragen',
  faq=[('Hoeveel vragen heeft het theorie-examen auto?', 'Het examen heeft 50 examenvragen, plus 2 testvragen die niet meetellen. Controleer de actuele opzet bij het CBR.'),
       ('Hoeveel vragen moet ik goed hebben?', 'Je slaagt met minstens 44 goede antwoorden van de 50.'),
       ('In welke taal kan ik het theorie-examen doen?', 'Dat controleer je bij het CBR voor je het examen aanvraagt. In de app kun je wel in het Nederlands en in het Engels oefenen.'),
       ('Is Theorie B van het CBR?', 'Nee. Theorie B is onafhankelijk en heeft eigen oefenvragen. Je score in de app zegt niets over je CBR-uitslag.')],
  verder='Lees ook', aside='Op deze pagina', home='Home', magazine='Magazine',
  back='← Magazine'),
 'en': dict(
  titel='Dutch car theory exam in English: how it works',
  meta='What to know about the Dutch car theory exam if Dutch is not your first language: how it works, how to practise in English, and how Theorie B helps.',
  kicker='Guide', h1='The Dutch car theory exam in English',
  intro='If you are learning to drive in the Netherlands and Dutch is not your first language, you can prepare in English. This page explains what to expect and how to practise. Always check the current rules with the CBR; Theorie B is independent of the CBR.',
  secties=[
   ('english', 'Which language is the exam in?', [
     'Which languages you can choose for the exam itself is something to check with the CBR before you apply. This guide makes no promises about it. What you can do now is learn the rules in English, so you understand them whichever language the exam is in.',
     'You apply for the exam through Mijn CBR, with DigiD. The CBR changes the exam from time to time, so check the current exam page before you apply.']),
   ('format', 'What the exam looks like', [
     'The car theory exam is a computer exam about traffic rules and traffic situations. It has 50 exam questions and 2 test questions that do not count. You have 30 minutes, or 45 minutes with extra time. You pass with at least 44 correct answers out of 50.']),
   ('covers', 'What the exam covers', [
     'Traffic rules and situations by topic. Theorie B covers nine topics with 225 original practice questions: using the road, priority and giving way, special roads and manoeuvres, safe driving and emergencies, traffic signs, responsible driving, legislation, vehicle knowledge and driver assistance systems.']),
   ('practise', 'How to practise in English', [
     'Switch the whole app to English, or turn only the question into English when you want to compare it with Dutch. Every answer has an explanation and a source, so you learn the rule and not only the answer.',
     'A mock exam in the app has 50 questions in 30 minutes, and you need 44 correct. Read the rules you keep missing in the magazine. A few examples are at the bottom of this page.']),
   ('try', 'Try Theorie B', [
     '10 practice questions and your first mock exam are free. There is no account, there are no ads, and your progress stays on your iPhone.'])],
  faq_kop='Frequently asked questions',
  faq=[('Is the exam itself available in English?', 'Check this with the CBR before you apply. Theorie B lets you practise in English or Dutch.'),
       ('Do I need to know Dutch road signs?', 'Yes, the signs are the Dutch ones. In the app, the explanations can be in English.'),
       ('How many questions do I need to get right?', 'You pass with at least 44 correct answers out of 50.'),
       ('Is Theorie B affiliated with the CBR?', 'No. Theorie B is independent and has its own practice questions. Your score in the app says nothing about your CBR result.')],
  verder='Read next', aside='On this page', home='Home', magazine='Magazine',
  back='← Magazine'),
}


def _alinea(tekst):
    # lijstregels "1. ..." blijven gewone alinea's; links in de tekst zijn al HTML
    return '<p>' + tekst + '</p>'


def bouw(head, T, BASE, alle):
    """Schrijf beide gidsen. `alle` = {taal: lijst artikelen}. Geeft de paden terug."""
    uit = []
    for taal in blog.TALEN:
        g = G[taal]; t = blog.L[taal]; pad = PADEN[taal]
        andere = 'en' if taal == 'nl' else 'nl'; alt = PADEN[andere]
        bij = [b for slug in ARTIKELEN[taal] for b in alle[taal] if b['slug'] == slug]
        aside = f'<p class="kicker">{g["aside"]}</p>' + ''.join(f'<a href="#{i}">{blog.esc(k)}</a>' for i, k, _ in g['secties']) + f'<a href="#faq">{blog.esc(g["faq_kop"])}</a>'
        body = ''.join(f'<h2 id="{i}">{blog.esc(k)}</h2>' + ''.join(_alinea(p) for p in ps) for i, k, ps in g['secties'])
        body += f'<h2 id="faq">{blog.esc(g["faq_kop"])}</h2>' + ''.join(f'<h3>{blog.esc(q)}</h3><p>{blog.esc(a)}</p>' for q, a in g['faq'])
        content = (f'<section class="wrap hub-heading"><a class="back" href="{blog.BASIS[taal]}">{g["back"]}</a><p class="kicker">{g["kicker"]}</p>'
                   f'<h1>{blog.esc(g["h1"])}</h1><p class="hub-intro">{blog.esc(g["intro"])}</p></section>'
                   f'<div class="reading-layout wrap"><aside class="article-aside">{aside}</aside><div class="reading"><div class="prose guide">{body}</div></div></div>')
        if bij:
            content += (f'<section class="wrap articles related"><div class="section-heading"><h2>{g["verder"]}</h2><a href="{blog.BASIS[taal]}">{t["alle_art"]}</a></div>'
                        '<div class="card-grid">' + ''.join(blog.card(b) for b in bij) + '</div></section>')
        content += blog.cta(T[taal]['store'], taal)
        org = {'@type': 'Organization', 'name': 'Theorie B', 'url': BASE + T[taal]['home']}
        ld = [{'@type': 'FAQPage', 'inLanguage': taal, 'url': BASE + pad, 'name': g['titel'], 'publisher': org,
               'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]},
              {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': j + 1, 'name': n, 'item': BASE + p}
                                                              for j, (n, p) in enumerate([(g['home'], T[taal]['home']), (g['magazine'], blog.BASIS[taal]), (g['h1'], pad)])]}]
        s = blog.shell(taal, g['titel'], g['meta'], pad, alt, ld, content, head, T)
        p = Path('.' + pad + 'index.html'); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s)
        uit.append(pad)
    return uit


def sitemap(base, datum):
    x = ''
    for taal in blog.TALEN:
        nl, en = PADEN['nl'], PADEN['en']
        x += (f'<url><loc>{base + PADEN[taal]}</loc><lastmod>{datum}</lastmod><xhtml:link rel="alternate" hreflang="nl" href="{base + nl}"/>'
              f'<xhtml:link rel="alternate" hreflang="en" href="{base + en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{base + nl}"/></url>\n')
    return x


def llms(base):
    return (f'- [{G["nl"]["h1"]} (Nederlands)]({base}{PADEN["nl"]}): {G["nl"]["meta"]}\n'
            f'- [{G["en"]["h1"]} (English)]({base}{PADEN["en"]}): {G["en"]["meta"]}\n')
