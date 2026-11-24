#!/bin/zsh
# Theorie B · dagelijkse blog (16-11). Bouwt de site; artikelen met DATUM <= vandaag komen erbij.
# Commit alleen blog-uitvoer en sitebestanden die de build raakt, nooit CNAME of het Google-bestand.
set -e
cd "$(dirname "$0")"
git pull -q --rebase --autostash origin main
python3 build.py https://theoriebapp.nl > /dev/null
python3 -m unittest -q tests/test_integration.py 2>&1 | tail -1
git diff --quiet CNAME google8d2a8cb9065b448d.html || { echo "CNAME of Google-bestand gewijzigd, stop"; exit 1; }
git add blog en/blog sitemap.xml llms.txt index.html en/index.html assets/blog
if git diff --cached --quiet; then echo "niets nieuws vandaag"; exit 0; fi
nieuw=$(git diff --cached --name-only -- 'blog/*/index.html' 'en/blog/*/index.html' | grep -v 'blog/index.html$\|onderwerp\|/topic/' | sed 's#blog/\(.*\)/index.html#\1#' | tr '\n' ' ')
git commit -q -m "Blog $(date +%d-%m): ${nieuw:-bijwerken}" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin main
echo "live: $nieuw"
