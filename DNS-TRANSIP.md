# DNS voor theoriebapp.nl (TransIP, klaar 15-11)

In TransIP: Domeinen, theoriebapp.nl, DNS. Bestaande regels voor `@` en `www` vervangen door:

| Naam | Type | Waarde |
|---|---|---|
| @ | A | 185.199.108.153 |
| @ | A | 185.199.109.153 |
| @ | A | 185.199.110.153 |
| @ | A | 185.199.111.153 |
| @ | AAAA | 2606:50c0:8000::153 |
| @ | AAAA | 2606:50c0:8001::153 |
| @ | AAAA | 2606:50c0:8002::153 |
| @ | AAAA | 2606:50c0:8003::153 |
| www | CNAME | dannyschuurman-hub.github.io. |

Mailregels (MX, SPF) niet aanraken; die komen pas bij het inrichten van mail.
Daarna: GitHub Pages, custom domain theoriebapp.nl, wachten op het certificaat, dan "Enforce HTTPS". Stilstand na 2 uur melden.
theoriebapp.online: later doorsturen naar theoriebapp.nl (niet nodig voor livegang).
