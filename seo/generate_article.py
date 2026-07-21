# -*- coding: utf-8 -*-
"""
Generator artykulow poradnika AquaDiagnostyka.
Renderuje poradnik-<slug>.html z brandem + schema Article, wstawia kafelek do poradnik.html
i przebudowuje sitemap.xml.

Uzycie:
  python seo/generate_article.py --slug jak-zbadac-wode-ze-studni \
      --title "Jak zbadać wodę ze studni? Poradnik krok po kroku" \
      --desc "Opis pod meta description (150-160 znakow)." \
      --keywords "badanie wody ze studni, jak zbadac wode" \
      --body sciezka/do/body.html

Plik --body to czysty HTML tresci (akapity <p>, naglowki <h2>/<h3>, listy <ul>).
"""
import os, sys, argparse, datetime, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://aquadiagnostyka.pl"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sitemap  # noqa: E402

CSS = """:root { --primary:#147fa8; --primary-glow:rgba(20,127,168,0.18); --primary-dark:#0e6282; --secondary:#2fa36b; --bg:#f5fafc; --card-bg:#ffffff; --text:#173040; --text-gray:#526675; --muted:#7d909d; --border:rgba(16,37,50,0.10); --soft:#e7f6fb; --transition:all 0.25s ease; }
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { font-family:'Montserrat',sans-serif; background:var(--bg); color:var(--text); line-height:1.7; -webkit-font-smoothing:antialiased; }
a { color:inherit; text-decoration:none; }
.container { max-width:820px; margin:0 auto; padding:0 22px; }
.accent { color:var(--primary); }
header.topbar { position:sticky; top:0; z-index:100; background:rgba(255,255,255,0.94); backdrop-filter:blur(10px); border-bottom:1px solid var(--border); padding:14px 0; box-shadow:0 8px 28px rgba(16,37,50,0.05); }
.topbar-inner { max-width:820px; margin:0 auto; padding:0 22px; display:flex; align-items:center; justify-content:space-between; }
.logo { font-weight:800; font-size:1.25rem; }
.topbar a.back { color:var(--text-gray); font-size:0.9rem; }
.topbar a.back:hover { color:var(--primary); }
.breadcrumb { font-size:0.82rem; color:var(--text-gray); padding:18px 0 0; }
.breadcrumb a:hover { color:var(--primary); }
article { padding:34px 0 10px; }
.meta { color:var(--text-gray); font-size:0.85rem; margin-bottom:18px; }
h1 { font-size:clamp(1.7rem,4.5vw,2.6rem); line-height:1.2; font-weight:800; margin-bottom:18px; }
article h2 { font-size:clamp(1.3rem,3vw,1.7rem); font-weight:800; margin:34px 0 14px; }
article h3 { font-size:1.15rem; font-weight:600; margin:22px 0 8px; }
article p { color:var(--text-gray); margin-bottom:16px; }
article ul, article ol { color:var(--text-gray); margin:0 0 16px 22px; }
article li { margin-bottom:8px; }
article strong { color:var(--text); }
.cta-band { text-align:center; background:#fff; border:1px solid var(--border); border-radius:14px; padding:38px 24px; margin:40px 0; box-shadow:0 14px 38px rgba(16,37,50,0.07); }
.cta-band h2 { margin:0 0 12px; }
.cta-band p { color:var(--text-gray); margin-bottom:22px; }
.btn-primary { background:var(--primary); color:#fff; padding:15px 32px; border-radius:50px; font-weight:600; box-shadow:0 10px 24px var(--primary-glow); transition:var(--transition); display:inline-block; }
.btn-primary:hover { transform:translateY(-2px); }
footer { border-top:1px solid var(--border); padding:30px 0; color:var(--text-gray); font-size:0.85rem; text-align:center; margin-top:30px; background:#eef7fa; }
footer a { color:var(--primary); }"""

PAGE = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{title} | AquaDiagnostyka®</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="AquaDiagnostyka - Laboratorium Badania Wody">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="language" content="Polish">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{domain}/poradnik-{slug}.html">
    <meta property="og:site_name" content="AquaDiagnostyka">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:image" content="{domain}/baner_gmb.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{domain}/baner_gmb.png">
    <link rel="canonical" href="{domain}/poradnik-{slug}.html">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7HN31380S5"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-7HN31380S5');
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title_json}",
        "description": "{desc_json}",
        "datePublished": "{date}",
        "dateModified": "{date}",
        "image": "{domain}/baner_gmb.png",
        "author": {{ "@type": "Organization", "name": "AquaDiagnostyka" }},
        "publisher": {{ "@type": "Organization", "name": "AquaDiagnostyka", "logo": {{ "@type": "ImageObject", "url": "{domain}/favicon-512x512.png" }} }},
        "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{domain}/poradnik-{slug}.html" }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "{domain}/"}},
            {{"@type": "ListItem", "position": 2, "name": "Poradnik", "item": "{domain}/poradnik.html"}},
            {{"@type": "ListItem", "position": 3, "name": "{title_json}", "item": "{domain}/poradnik-{slug}.html"}}
        ]
    }}
    </script>
    <style>{css}</style>
    <script defer src="/aqua-tracking.js"></script>
</head>
<body>
    <header class="topbar">
        <div class="topbar-inner">
            <a href="{domain}/" class="logo">Aqua<span class="accent">Diagnostyka</span></a>
            <a href="{domain}/poradnik.html" class="back">← Poradnik</a>
        </div>
    </header>
    <div class="container">
        <nav class="breadcrumb"><a href="{domain}/">Strona główna</a> &nbsp;›&nbsp; <a href="{domain}/poradnik.html">Poradnik</a> &nbsp;›&nbsp; {title}</nav>
    </div>
    <main class="container">
        <article>
            <h1>{title}</h1>
            <p class="meta">AquaDiagnostyka · {date_pl} · badanie wody Nowy Sącz i okolice</p>
            {body}
            <div class="cta-band">
                <h2>Chcesz zbadać swoją wodę?</h2>
                <p>Mikrobiologiczne badanie wody ze studni zaczyna się od ok. 180 zł. Zakres, pobranie próbki i termin potwierdzamy po opisie sytuacji w formularzu.</p>
                <a href="{domain}/#kontakt" class="btn-primary">Zamów badanie przez formularz</a>
            </div>
        </article>
    </main>
    <footer>
        <div class="container">
            <p>© 2026 AquaDiagnostyka — akredytowane laboratorium badania wody, Nowy Sącz i okolice.<br>
            Kontakt: <a href="mailto:kontakt@aquadiagnostyka.pl">kontakt@aquadiagnostyka.pl</a> &nbsp;·&nbsp; <a href="{domain}/#kontakt">Zamów badanie online</a></p>
        </div>
    </footer>
</body>
</html>
"""

MONTHS_PL = ["", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
             "lipca", "sierpnia", "września", "października", "listopada", "grudnia"]


def date_pl(d):
    return "%d %s %d" % (d.day, MONTHS_PL[d.month], d.year)


def update_index(slug, title, desc, d):
    idx_path = os.path.join(ROOT, "poradnik.html")
    if not os.path.exists(idx_path):
        return
    with open(idx_path, encoding="utf-8") as f:
        content = f.read()
    card = ('<a class="post-card" href="/poradnik-%s.html">\n'
            '                <span class="post-date">%s</span>\n'
            '                <h3>%s</h3>\n'
            '                <p>%s</p>\n'
            '            </a>' % (slug, date_pl(d), html.escape(title), html.escape(desc)))
    marker = "<!-- ARTICLES:START -->"
    if marker in content and ("/poradnik-%s.html" % slug) not in content:
        content = content.replace(marker, marker + "\n            " + card)
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("poradnik.html: dodano kafelek")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", required=True)
    ap.add_argument("--keywords", required=True)
    ap.add_argument("--body", required=True, help="sciezka do pliku HTML z trescia")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    d = datetime.date.fromisoformat(a.date)
    with open(a.body, encoding="utf-8") as f:
        body = f.read().strip()

    page = PAGE.format(
        title=a.title, title_json=a.title.replace('"', '\\"'),
        desc=a.desc, desc_json=a.desc.replace('"', '\\"'),
        keywords=a.keywords, slug=a.slug, domain=DOMAIN,
        date=a.date, date_pl=date_pl(d), css=CSS, body=body,
    )
    out = os.path.join(ROOT, "poradnik-%s.html" % a.slug)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("OK:", os.path.basename(out))

    update_index(a.slug, a.title, a.desc, d)
    import related
    related.rebuild_related()
    build_sitemap.build()


if __name__ == "__main__":
    main()
