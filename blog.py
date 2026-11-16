"""Blog: verkeersregels uitgelegd (16-11, Danny: 'zet die er ook op').
Bron: App-niches/03_theorie/marketing/blog-concepten/NN_slug.md (tekst Codex, gekeurd door de Theorie B-manager).
Beeld: echt app-scherm per blog in assets/blog/<slug>.webp (uit de simulatoropnames, maak met beelden())."""
import os, re, html, json, glob

BRON = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/App-niches/03_theorie/marketing/blog-concepten")
DATUM = "2026-11-16"
ALT = {
    "telefoon-vasthouden-tijdens-rijden": "Theorie B: oefenvraag over telefoon vasthouden tijdens het rijden, antwoord Nee met uitleg en RVV 1990, art. 61a",
    "rechtsaf-fietser-rechtdoor": "Theorie B: oefenvraag over rechtsaf slaan met een fietser naast je, fout antwoord en goed antwoord De fietser met uitleg",
    "rechts-inhalen-in-de-file": "Theorie B: oefenvraag over rechts inhalen in de file, antwoord Ja met uitleg en RVV 1990, art. 13 lid 2",
    "parkeerschijf-tijd-afronden": "Theorie B: oefenvraag over de parkeerschijf in een blauwe zone, antwoord 10.30 uur met uitleg",
    "geel-verkeerslicht-stoppen": "Theorie B: oefenvraag over een geel verkeerslicht, antwoord Stoppen met uitleg en wetsartikel",
    "groot-licht-fietser-tegemoet": "Theorie B: oefenvraag over groot licht bij een tegemoetkomende fietser, met uitleg en wetsartikel",
    "uitrit-verlaten-voetganger": "Theorie B: oefenvraag over een uitrit en een hardloper op het trottoir, met uitleg en RVV 1990, art. 54",
}

def lees():
    uit = []
    for f in sorted(glob.glob(os.path.join(BRON, "[0-9][0-9]_*.md"))):
        t = open(f, encoding="utf-8").read().strip()
        kop = dict(re.findall(r"^(SLUG|ZOEKVRAAG|TITEL|META): (.+)$", t, re.M))
        body = re.sub(r"^(SLUG|ZOEKVRAAG|TITEL|META): .+\n", "", t, flags=re.M).strip()
        uit.append(dict(slug=kop["SLUG"], vraag=kop["ZOEKVRAAG"], titel=kop["TITEL"], meta=kop["META"], body=body))
    return uit

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)

def md(body, beeld):
    out, lijst, para_n, gezet = [], [], 0, False
    def sluit():
        if lijst: out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lijst) + "</ul>"); lijst.clear()
    for blok in re.split(r"\n\s*\n", body):
        regels = [r.strip() for r in blok.strip().split("\n") if r.strip()]
        if not regels: continue
        if all(r.startswith("- ") for r in regels):
            lijst.extend(r[2:] for r in regels); sluit(); continue
        sluit()
        if regels[0].startswith("## "):
            out.append(f"<h2>{inline(regels[0][3:])}</h2>")
            if len(regels) > 1: out.append(f"<p>{inline(' '.join(regels[1:]))}</p>")
            continue
        out.append(f"<p>{inline(' '.join(regels))}</p>"); para_n += 1
        if para_n == 2 and not gezet:   # beeld direct na het korte antwoord
            out.append(beeld); gezet = True
    sluit()
    return "\n".join(out)

def pagina(b, head, nav, foot, T, BASE, STORE):
    t = T["nl"]; path = f"/blog/{b['slug']}/"
    img = f"/assets/blog/{b['slug']}.webp"
    heeft = os.path.exists("." + img)
    beeld = (f'<figure class="scherm"><img src="{img}" width="600" height="1305" loading="lazy" alt="{html.escape(ALT.get(b["slug"], b["titel"]))}">'
             f'<figcaption>Zo staat deze vraag in Theorie B.</figcaption></figure>') if heeft else ""
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": b["titel"], "description": b["meta"],
           "datePublished": DATUM, "dateModified": DATUM, "inLanguage": "nl", "mainEntityOfPage": BASE + path,
           "author": {"@type": "Organization", "name": "Theorie B", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Theorie B", "logo": {"@type": "ImageObject", "url": BASE + "/assets/apple-touch-icon.png"}},
           **({"image": BASE + img} if heeft else {})},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Theorie B", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Verkeersregels uitgelegd", "item": BASE + "/blog/"},
              {"@type": "ListItem", "position": 3, "name": b["titel"], "item": BASE + path}]}]
    extra = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    s = head(t, f"{b['titel']} | Theorie B", b["meta"], path, None, extra, ogtype="article")
    s += '<body class="doc">\n<a class="skip" href="#main">Naar de inhoud</a>\n' + nav(t)
    s += (f'<main id="main" class="doc-main blog"><p class="kruimel"><a href="/blog/">Verkeersregels uitgelegd</a></p>'
          f'<article><h1>{inline(b["titel"])}</h1>\n{md(b["body"], beeld)}\n'
          f'<p><a class="badge" href="{STORE}"><img src="/assets/{t["badge"]}" width="150" height="50" alt="{t["badgealt"]}"></a></p></article></main>\n')
    return s + foot(t) + "</body>\n</html>\n"

def overzicht(blogs, head, nav, foot, T, BASE):
    t = T["nl"]; titel = "Verkeersregels uitgelegd | Theorie B"
    desc = "Korte uitleg over verkeersregels die vaak fout gaan op het theorie-examen auto, elk met het wetsartikel en een oefenvraag."
    s = head(t, titel, desc, "/blog/", None)
    s += '<body class="doc">\n<a class="skip" href="#main">Naar de inhoud</a>\n' + nav(t)
    s += '<main id="main" class="doc-main blog"><h1>Verkeersregels uitgelegd</h1><p>' + desc + '</p><ul class="bloglijst">'
    s += "".join(f'<li><a href="/blog/{b["slug"]}/">{inline(b["titel"])}</a><span>{inline(b["vraag"])}</span></li>' for b in blogs)
    return s + "</ul></main>\n" + foot(t) + "</body>\n</html>\n"

def bouw(head, nav, foot, T, BASE, STORE):
    blogs = lees()
    os.makedirs("blog", exist_ok=True)
    for b in blogs:
        os.makedirs(f"blog/{b['slug']}", exist_ok=True)
        open(f"blog/{b['slug']}/index.html", "w", encoding="utf-8").write(pagina(b, head, nav, foot, T, BASE, STORE))
    open("blog/index.html", "w", encoding="utf-8").write(overzicht(blogs, head, nav, foot, T, BASE))
    return blogs

def beelden(bronnen):
    """bronnen: {slug: pad naar 1206x2622 png}. Schrijft assets/blog/<slug>.webp (600 breed)."""
    from PIL import Image
    os.makedirs("assets/blog", exist_ok=True)
    for slug, p in bronnen.items():
        im = Image.open(p).convert("RGB").resize((600, 1305), Image.LANCZOS)
        im.save(f"assets/blog/{slug}.webp", quality=82, method=6)
