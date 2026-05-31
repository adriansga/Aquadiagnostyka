# -*- coding: utf-8 -*-
"""
Buduje sitemap.xml skanujac katalog projektu.
Wspolny dla podstron miast i artykulow poradnika - uruchamiaj po kazdej zmianie tresci.
  python seo/build_sitemap.py
"""
import os, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://aquadiagnostyka.pl"
TODAY = datetime.date.today().isoformat()


def url_entry(loc, priority, changefreq):
    return ('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n'
            '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
            % (loc, TODAY, changefreq, priority))


def build():
    entries = [url_entry(DOMAIN + "/", "1.0", "weekly")]

    # poradnik (hub)
    if os.path.exists(os.path.join(ROOT, "poradnik.html")):
        entries.append(url_entry(DOMAIN + "/poradnik.html", "0.7", "weekly"))

    # podstrony miast
    for p in sorted(glob.glob(os.path.join(ROOT, "badanie-wody-*.html"))):
        entries.append(url_entry(DOMAIN + "/" + os.path.basename(p), "0.8", "monthly"))

    # artykuly poradnika
    for p in sorted(glob.glob(os.path.join(ROOT, "poradnik-*.html"))):
        entries.append(url_entry(DOMAIN + "/" + os.path.basename(p), "0.6", "monthly"))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(entries) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("sitemap.xml: %d URL" % len(entries))


if __name__ == "__main__":
    build()
