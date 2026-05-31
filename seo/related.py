# -*- coding: utf-8 -*-
"""
Cross-linking artykulow poradnika: w kazdym poradnik-*.html wstawia/odswieza
blok 'Zobacz tez' z linkami do innych artykulow + huba + formularza.
Idempotentne (marker RELATED:START/END). Wolane automatycznie przez generate_article.py.
  python seo/related.py
"""
import os, glob, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_LINKS = 5


def articles():
    out = []
    for p in glob.glob(os.path.join(ROOT, "poradnik-*.html")):
        t = open(p, encoding="utf-8").read()
        m = re.search(r"<h1>(.*?)</h1>", t, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else os.path.basename(p)
        out.append({"path": p, "name": os.path.basename(p), "title": title,
                    "mtime": os.path.getmtime(p)})
    out.sort(key=lambda a: a["mtime"], reverse=True)
    return out


def block_for(current, arts):
    others = [a for a in arts if a["path"] != current["path"]][:MAX_LINKS]
    lis = "\n".join(
        '                    <li><a href="/%s" style="color:var(--primary);">%s</a></li>'
        % (a["name"], html.escape(a["title"])) for a in others)
    return (
        "<!-- RELATED:START -->\n"
        '            <div style="border-top:1px solid var(--border); margin-top:36px; padding-top:24px;">\n'
        '                <h2 style="font-size:1.3rem; margin:0 0 14px;">Zobacz też</h2>\n'
        "                <ul>\n" + lis + "\n                </ul>\n"
        '                <p style="margin-top:14px;"><a href="/poradnik.html" style="color:var(--primary);">→ Wszystkie artykuły w poradniku</a></p>\n'
        "            </div>\n"
        "            <!-- RELATED:END -->")


def rebuild_related():
    arts = articles()
    if len(arts) < 2:
        print("related: za malo artykulow (%d) - pomijam" % len(arts))
        return
    n = 0
    for a in arts:
        t = open(a["path"], encoding="utf-8").read()
        blk = block_for(a, arts)
        if "<!-- RELATED:START -->" in t:
            t2 = re.sub(r"<!-- RELATED:START -->.*?<!-- RELATED:END -->", blk, t, flags=re.S)
        else:
            # wstaw przed sekcja CTA
            t2 = t.replace('            <div class="cta-band">', blk + '\n            <div class="cta-band">', 1)
        if t2 != t:
            open(a["path"], "w", encoding="utf-8").write(t2)
            n += 1
    print("related: zaktualizowano %d artykulow" % n)


if __name__ == "__main__":
    rebuild_related()
