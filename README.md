# Theorie B website

Statische site voor de iPhone-app Theorie B (App Store id 6834047508). Gemodelleerd op notecord-site, bedoeld voor GitHub Pages. Alleen lokaal gebouwd, niets gepubliceerd.

- Pagina's worden gegenereerd door `python3 build.py` (leest support en privacy uit `appstore/web/` van het app-project; support uit `klaar-voor-1.0.1/`). Tekst blijft identiek, alleen de opmaak is van deze site.
- Lokaal bekijken: `python3 -m http.server 8000` in deze map.

## Nog te doen vóór livegang
- **Domein**: nog niet gekozen. Bouw met `python3 build.py https://<domein>`: dat zet canonical, hreflang, og:image, sitemap, robots, llms.txt en schrijft dan ook `CNAME`. Zonder argument blijft de plaatsvervanger `https://theorieb.example` staan en komt er geen CNAME.
- TODO: `sameAs` (Instagram en Facebook) in de JSON-LD toevoegen zodra de socialaccounts af zijn.
- Pagina's: `/`, `/en/`, `/support/`, `/en/support/`, `/privacy/`, `/en/privacy/`, `404.html`.
- Links zijn absoluut vanaf de root (`/style.css`), dus de site moet op een eigen domein staan, niet onder een subpad.
- Support- en privacy-URL's in App Store Connect bijwerken zodra het domein bekend is.
