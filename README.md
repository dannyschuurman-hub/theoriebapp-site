# Theorie B website

Statische site voor de iPhone-app Theorie B (App Store id 6834047508). Gemodelleerd op notecord-site, bedoeld voor GitHub Pages. Alleen lokaal gebouwd, niets gepubliceerd.

- Pagina's: `index.html` (NL), `en/index.html` (EN), `support.html`, `support-en.html`, `privacy.html`, `privacy-en.html`, `sitemap.xml`, `robots.txt`.
- Pagina's worden gegenereerd door `python3 build.py` (leest support en privacy uit `appstore/web/` van het app-project; support uit `klaar-voor-1.0.1/`). Tekst blijft identiek, alleen de opmaak is van deze site.
- Lokaal bekijken: `python3 -m http.server 8000` in deze map.

## Nog te doen vóór livegang
- **CNAME**: nog geen domein gekozen. Zet straks een bestand `CNAME` in de root met alleen het domein (bijvoorbeeld `theorieb.nl`), zoals in notecord-site.
- In `build.py` staat `BASE = "https://theorieb.example"` als plaatsvervanger. Vervang door het echte domein en draai `python3 build.py` opnieuw (canonical, hreflang, og:image, sitemap, robots).
- Links zijn absoluut vanaf de root (`/style.css`), dus de site moet op een eigen domein staan, niet onder een subpad.
- Support- en privacy-URL's in App Store Connect bijwerken zodra het domein bekend is.
