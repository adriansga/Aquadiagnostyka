# -*- coding: utf-8 -*-
"""
Lokalny guard SEO/GEO dla AquaDiagnostyki.

Blokuje publikacje, jesli publiczne HTML-e maja stare claimy, bledne schema,
nie-ASCII w sitemap albo podstawowe braki title/meta/H1/canonical.
Uzycie:
  python seo/seo_guard.py
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://aquadiagnostyka.pl"

PUBLIC_PATTERNS = [
    "index.html",
    "poradnik.html",
    "badanie-wody-*.html",
    "poradnik-*.html",
]

HARD_BANNED = [
    r"NAJWAŻNIEJSZA\s+ŚCIEŻKA\s+B2C",
    r"NAJWAZNIEJSZA\s+SCIEZKA\s+B2C",
    r"Dojazd\s+GRATIS",
    r"dojazd i pobranie próbki gratis",
    r"dojazd i pobranie probki gratis",
    r"Akredytowane badanie od 150",
    r"Badanie od 150",
    r"zaczyna się od 150",
    r"zaczyna sie od 150",
    r"127 opinii",
    r"Promocja",
    r"urgencyTimer",
    r"aggregateRating",
]

REQUIRED_MAIN_MARKERS = [
    "Mikrobiologiczne badanie wody",
    "prywatnych studni",
    "priceGridMicro",
    "pakiet_cena_brutto",
    "formPackagePreview",
    "utm_campaign",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1 = []
        self.meta_desc = ""
        self.canonical = ""
        self.jsonld = []
        self._tag = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._tag = "title"
            self._buf = []
        elif tag == "h1":
            self._tag = "h1"
            self._buf = []
        elif tag == "meta" and attrs.get("name") == "description":
            self.meta_desc = attrs.get("content", "")
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._tag = "jsonld"
            self._buf = []

    def handle_data(self, data):
        if self._tag:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._tag == "title" and tag == "title":
            self.title = "".join(self._buf).strip()
            self._tag = None
        elif self._tag == "h1" and tag == "h1":
            self.h1.append(re.sub(r"\s+", " ", "".join(self._buf)).strip())
            self._tag = None
        elif self._tag == "jsonld" and tag == "script":
            self.jsonld.append("".join(self._buf).strip())
            self._tag = None


def public_files():
    files = []
    for pattern in PUBLIC_PATTERNS:
        files.extend(glob.glob(os.path.join(ROOT, pattern)))
    return sorted(set(files))


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def fail(errors, msg):
    errors.append(msg)


def check_html(errors):
    for path in public_files():
        text = open(path, encoding="utf-8").read()
        r = rel(path)
        for pattern in HARD_BANNED:
            if re.search(pattern, text, re.I):
                fail(errors, "%s: zakazany/stary claim: %s" % (r, pattern))

        parser = PageParser()
        parser.feed(text)
        if not parser.title:
            fail(errors, "%s: brak <title>" % r)
        if not parser.meta_desc:
            fail(errors, "%s: brak meta description" % r)
        if not parser.h1:
            fail(errors, "%s: brak H1" % r)
        if r != "index.html" and not parser.canonical.startswith(DOMAIN + "/"):
            fail(errors, "%s: brak poprawnego canonical" % r)
        for raw in parser.jsonld:
            try:
                json.loads(raw)
            except Exception as exc:
                fail(errors, "%s: bledny JSON-LD: %s" % (r, exc))

    index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    for marker in REQUIRED_MAIN_MARKERS:
        if marker not in index:
            fail(errors, "index.html: brak markera glownej sciezki: %s" % marker)


def check_sitemap(errors):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        fail(errors, "brak sitemap.xml")
        return
    data = open(path, encoding="utf-8").read()
    if any(ord(ch) > 127 for ch in data):
        fail(errors, "sitemap.xml: zawiera nie-ASCII w URL lub XML")
    root = ET.fromstring(data)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [el.text for el in root.findall("sm:url/sm:loc", ns)]
    if len(urls) < 10:
        fail(errors, "sitemap.xml: podejrzanie malo URL: %d" % len(urls))
    seen = set()
    for url in urls:
        if url in seen:
            fail(errors, "sitemap.xml: duplikat URL: %s" % url)
        seen.add(url)
        if not url.startswith(DOMAIN):
            fail(errors, "sitemap.xml: obcy domain: %s" % url)
        suffix = url.replace(DOMAIN + "/", "")
        if suffix and not os.path.exists(os.path.join(ROOT, suffix)):
            fail(errors, "sitemap.xml: URL bez pliku lokalnego: %s" % url)


def main():
    errors = []
    check_html(errors)
    check_sitemap(errors)
    if errors:
        print("SEO_GUARD_FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("SEO_GUARD_OK files=%d" % len(public_files()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
