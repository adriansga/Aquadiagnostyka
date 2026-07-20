# -*- coding: utf-8 -*-
"""
Generator podstron lokalnych AquaDiagnostyka (programmatic SEO).
Tworzy badanie-wody-<slug>.html dla kazdego miasta + krzyzowe linkowanie wewnetrzne.
Uruchom z katalogu projektu:  python seo/generate_city_pages.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sitemap as shared_sitemap

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://aquadiagnostyka.pl"

# name = mianownik (do title), loc = miejscownik (do "w ..."), lat/lon, oraz unikalne tresci
CITIES = [
    {
        "slug": "stary-sacz", "name": "Stary Sącz", "loc": "Starym Sączu",
        "lat": "49.5618", "lon": "20.6347",
        "intro": "Masz studnię, własne ujęcie albo chcesz mieć pewność, że woda z kranu jest bezpieczna dla rodziny? Przyjeżdżamy do Ciebie w Starym Sączu, pobieramy próbkę zgodnie z procedurą i dostarczamy wyniki z czytelną interpretacją.",
        "why": "Stary Sącz i okoliczne sołectwa to w dużej mierze zabudowa korzystająca z własnych studni i ujęć. Woda studzienna bywa narażona na zanieczyszczenia bakteriologiczne (bakterie grupy coli, <em>E. coli</em> z nieszczelnych szamb i pól) oraz przekroczenia azotanów, żelaza, manganu czy twardości.",
        "note": "Tych zagrożeń nie widać i nie czuć, a mają realny wpływ na zdrowie — szczególnie dzieci i osób starszych.",
    },
    {
        "slug": "gorlice", "name": "Gorlice", "loc": "Gorlicach",
        "lat": "49.6553", "lon": "21.1601",
        "intro": "Mieszkasz w Gorlicach lub okolicznych wsiach i chcesz wiedzieć, co naprawdę pijesz? Dojeżdżamy pod wskazany adres, pobieramy próbkę i dostarczamy wynik z interpretacją — bez dzwonienia, wszystko zamawiasz online.",
        "why": "Część Gorlic korzysta z wodociągu, ale obrzeża miasta i okoliczne miejscowości w dużej mierze opierają się na własnych studniach. W regionie z historią przemysłu naftowego warto kontrolować nie tylko bakteriologię, ale też parametry fizykochemiczne — żelazo, mangan i ogólny stan wody gruntowej.",
        "note": "Badanie to jedyny sposób, by obiektywnie ocenić, czy woda nadaje się do spożycia — szczególnie po remoncie studni lub w nowym domu.",
    },
    {
        "slug": "limanowa", "name": "Limanowa", "loc": "Limanowej",
        "lat": "49.7058", "lon": "20.4231",
        "intro": "W Limanowej i okolicy duża część gospodarstw stoi na własnych ujęciach w górzystym, rozproszonym terenie. Przyjeżdżamy do Ciebie, pobieramy próbkę zgodnie z procedurą i przekazujemy czytelny wynik.",
        "why": "Górzysty teren i studnie kopane sprzyjają sezonowym wahaniom jakości wody — po roztopach i intensywnych opadach rośnie ryzyko zanieczyszczeń mikrobiologicznych spływających z powierzchni.",
        "note": "Jeśli woda zmienia smak, barwę lub mętność po deszczu, to wyraźny sygnał, żeby ją przebadać.",
    },
    {
        "slug": "krynica-zdroj", "name": "Krynica-Zdrój", "loc": "Krynicy-Zdroju",
        "lat": "49.4220", "lon": "20.9590",
        "intro": "Krynica-Zdrój słynie z wód mineralnych, ale woda użytkowa w domach, pensjonatach i kwaterach to zupełnie inna sprawa. Badamy wodę pod kątem bezpieczeństwa zdrowotnego i wymogów formalnych — z dojazdem na miejsce.",
        "why": "W miejscowości uzdrowiskowej działa wiele pensjonatów, kwater i obiektów agroturystycznych, które potrzebują badań wody honorowanych przez Sanepid. Niezależnie od słynnych źródeł, woda z sieci czy własnego ujęcia w obiekcie powinna być regularnie kontrolowana.",
        "note": "Prowadzisz wynajem lub gastronomię? Aktualne badanie wody to podstawa przy kontroli sanitarnej.",
    },
    {
        "slug": "muszyna", "name": "Muszyna", "loc": "Muszynie",
        "lat": "49.3536", "lon": "20.8908",
        "intro": "Muszyna to uzdrowisko pełne pensjonatów i kwater — a każdy obiekt świadczący usługi noclegowe czy gastronomiczne potrzebuje pewności co do jakości wody. Badamy z dojazdem i czytelnym sprawozdaniem.",
        "why": "Obok słynnych wód mineralnych, woda użytkowa w obiektach i prywatnych domach w Muszynie wymaga osobnej kontroli — szczególnie tam, gdzie korzysta się z własnych ujęć obok sieci wodociągowej.",
        "note": "Dla kwater i pensjonatów wykonujemy pełny pakiet wymagany przy kontrolach Sanepidu.",
    },
    {
        "slug": "piwniczna-zdroj", "name": "Piwniczna-Zdrój", "loc": "Piwnicznej-Zdroju",
        "lat": "49.4186", "lon": "20.7136",
        "intro": "W Piwnicznej-Zdroju i dolinie Popradu zabudowa jest rozproszona, a wiele domów korzysta z własnych studni. Przyjeżdżamy, pobieramy próbkę i dostarczamy wynik z interpretacją — zamawiasz online.",
        "why": "Rozproszona, górska zabudowa i własne ujęcia oznaczają, że jakość wody potrafi się różnić dom w dom. Bez badania nie da się stwierdzić, czy woda spełnia normy mikrobiologiczne i fizykochemiczne.",
        "note": "Pensjonaty i kwatery w Piwnicznej obsługujemy w zakresie wymaganym przez Sanepid.",
    },
    {
        "slug": "grybow", "name": "Grybów", "loc": "Grybowie",
        "lat": "49.6147", "lon": "20.9483",
        "intro": "Grybów i okoliczne wsie to w dużej mierze tereny rolnicze, gdzie woda pochodzi z własnych studni. Badamy ją pod kątem bezpieczeństwa zdrowotnego — z dojazdem na miejsce i wynikiem w 48h.",
        "why": "Na terenach rolniczych z hodowlą i nawożeniem rośnie ryzyko zanieczyszczeń bakteriologicznych oraz podwyższonych azotanów w wodzie ze studni. To parametry, które realnie wpływają na zdrowie, a zwłaszcza na niemowlęta.",
        "note": "Jeśli w gospodarstwie jest mała dzieci lub przygotowujesz wodę do picia ze studni — badanie jest szczególnie zalecane.",
    },
    {
        "slug": "lacko", "name": "Łącko", "loc": "Łącku",
        "lat": "49.5556", "lon": "20.4344",
        "intro": "Łącko to region sadowniczy z intensywnym rolnictwem — a to bezpośrednio przekłada się na jakość wody gruntowej. Badamy wodę ze studni i ujęć z dojazdem pod wskazany adres.",
        "why": "Intensywne uprawy i nawożenie zwiększają ryzyko przedostawania się azotanów oraz pozostałości środków ochrony roślin do wód gruntowych. Studnie w rejonie sadowniczym warto kontrolować regularnie, nie tylko jednorazowo.",
        "note": "Podwyższone azotany są szczególnie groźne dla niemowląt — dlatego w rejonach rolniczych badanie wody to konieczność, nie formalność.",
    },
    {
        "slug": "podegrodzie", "name": "Podegrodzie", "loc": "Podegrodziu",
        "lat": "49.5800", "lon": "20.5500",
        "intro": "Podegrodzie to gmina wiejska, gdzie większość gospodarstw korzysta z własnych studni. Przyjeżdżamy, pobieramy próbkę zgodnie z procedurą i dostarczamy wynik z jasną interpretacją.",
        "why": "W zabudowie wiejskiej studnie często sąsiadują z szambami, oborami i polami uprawnymi, co zwiększa ryzyko zanieczyszczeń mikrobiologicznych i azotanowych. Tego nie wykryją zmysły — tylko badanie laboratoryjne.",
        "note": "Po wykopaniu nowej studni lub jej remoncie badanie wody jest pierwszą rzeczą, którą warto zrobić przed użytkowaniem.",
    },
]


# dopelniacz (po "do ...") - polska gramatyka
GEN = {
    "stary-sacz": "Starego Sącza",
    "gorlice": "Gorlic",
    "limanowa": "Limanowej",
    "krynica-zdroj": "Krynicy-Zdroju",
    "muszyna": "Muszyny",
    "piwniczna-zdroj": "Piwnicznej-Zdroju",
    "grybow": "Grybowa",
    "lacko": "Łącka",
    "podegrodzie": "Podegrodzia",
}


def towns_links(current_slug):
    out = ['<a href="%s/">Nowy Sącz</a>' % DOMAIN]
    for c in CITIES:
        if c["slug"] == current_slug:
            continue
        out.append('<a href="%s/badanie-wody-%s.html">%s</a>' % (DOMAIN, c["slug"], c["name"]))
    return "\n                    ".join(out)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">

    <title>Badanie Wody %%NAME%% od 150 zł | AquaDiagnostyka® | Dojazd GRATIS</title>
    <meta name="description" content="Badanie wody w %%LOC%% — akredytowane laboratorium, dojazd i pobranie próbki GRATIS, wyniki w 48h. Studnia, woda pitna, basen, Sanepid. Zamów online od 150 zł.">
    <meta name="keywords" content="badanie wody %%NAME%%, badanie wody ze studni %%NAME%%, laboratorium wody %%NAME%%, analiza wody %%NAME%%, badanie wody pitnej %%NAME%%, badanie wody do Sanepidu %%NAME%%">
    <meta name="author" content="AquaDiagnostyka - Laboratorium Badania Wody">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="language" content="Polish">

    <meta name="geo.region" content="PL-MA">
    <meta name="geo.placename" content="%%NAME%%">
    <meta name="geo.position" content="%%LAT%%;%%LON%%">
    <meta name="ICBM" content="%%LAT%%, %%LON%%">

    <meta property="og:type" content="website">
    <meta property="og:url" content="%%DOMAIN%%/badanie-wody-%%SLUG%%.html">
    <meta property="og:site_name" content="AquaDiagnostyka">
    <meta property="og:title" content="Badanie Wody %%NAME%% | AquaDiagnostyka® | Dojazd GRATIS">
    <meta property="og:description" content="Akredytowane badanie wody w %%LOC%% od 150 zł. Dojazd GRATIS, wyniki w 48h. Zamów online.">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:image" content="%%DOMAIN%%/baner_gmb.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="628">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Badanie Wody %%NAME%% | AquaDiagnostyka®">
    <meta name="twitter:description" content="Akredytowane badanie wody w %%LOC%% od 150 zł. Dojazd GRATIS, wyniki w 48h.">
    <meta name="twitter:image" content="%%DOMAIN%%/baner_gmb.png">

    <link rel="canonical" href="%%DOMAIN%%/badanie-wody-%%SLUG%%.html">

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
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-7HN31380S5');
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Badanie wody",
        "provider": {
            "@type": "LocalBusiness",
            "name": "AquaDiagnostyka",
            "email": "kontakt@aquadiagnostyka.pl",
            "url": "https://aquadiagnostyka.pl",
            "image": "https://aquadiagnostyka.pl/baner_gmb.png",
            "priceRange": "od 150 zł",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Nowy Sącz",
                "postalCode": "33-300",
                "addressRegion": "małopolskie",
                "addressCountry": "PL"
            }
        },
        "areaServed": { "@type": "City", "name": "%%NAME%%" },
        "description": "Akredytowane badanie wody w %%LOC%%: woda ze studni, woda pitna, woda basenowa, badania do Sanepidu. Dojazd i pobranie próbki gratis, wyniki w 48h.",
        "offers": { "@type": "Offer", "price": "150", "priceCurrency": "PLN", "url": "https://aquadiagnostyka.pl/#kontakt" }
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            { "@type": "Question", "name": "Ile kosztuje badanie wody w %%LOC%%?", "acceptedAnswer": { "@type": "Answer", "text": "Badanie wody w %%LOC%% zaczyna się od 150 zł. Cena zależy od zakresu — od podstawowego badania fizykochemicznego, przez mikrobiologiczne, po pełny pakiet wymagany m.in. przez Sanepid. Dojazd i pobranie próbki są gratis." } },
            { "@type": "Question", "name": "Czy dojeżdżacie do %%GEN%% po próbkę wody?", "acceptedAnswer": { "@type": "Answer", "text": "Tak. Przyjeżdżamy pod wskazany adres w %%LOC%% i okolicach, sami pobieramy próbkę zgodnie z procedurą i dostarczamy ją do laboratorium. Dojazd jest bezpłatny." } },
            { "@type": "Question", "name": "Jak szybko otrzymam wyniki badania wody?", "acceptedAnswer": { "@type": "Answer", "text": "Standardowo wyniki dostarczamy w ciągu 48 godzin wraz z czytelną interpretacją oraz zaleceniami, co zrobić, jeśli woda przekracza normy." } },
            { "@type": "Question", "name": "Czy badanie wody nadaje się do Sanepidu?", "acceptedAnswer": { "@type": "Answer", "text": "Tak. Wykonujemy badania akredytowanymi metodami, honorowanymi przez Sanepid (odbiory budynków, agroturystyka, gastronomia, studnie do spożycia)." } }
        ]
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "https://aquadiagnostyka.pl/"},
            {"@type": "ListItem", "position": 2, "name": "Badanie wody %%NAME%%", "item": "%%DOMAIN%%/badanie-wody-%%SLUG%%.html"}
        ]
    }
    </script>

    <style>
        :root { --primary:#147fa8; --primary-glow:rgba(20,127,168,0.18); --primary-dark:#0e6282; --secondary:#2fa36b; --bg:#f5fafc; --card-bg:#ffffff; --text:#173040; --text-gray:#526675; --muted:#7d909d; --border:rgba(16,37,50,0.10); --soft:#e7f6fb; --transition:all 0.25s ease; }
        * { margin:0; padding:0; box-sizing:border-box; }
        html { scroll-behavior:smooth; }
        body { font-family:'Montserrat',sans-serif; background:var(--bg); color:var(--text); line-height:1.65; -webkit-font-smoothing:antialiased; }
        a { color:inherit; text-decoration:none; }
        .container { max-width:1080px; margin:0 auto; padding:0 22px; }
        .accent { color:var(--primary); }
        header.topbar { position:sticky; top:0; z-index:100; background:rgba(255,255,255,0.94); backdrop-filter:blur(10px); border-bottom:1px solid var(--border); padding:14px 0; box-shadow:0 8px 28px rgba(16,37,50,0.05); }
        .topbar-inner { display:flex; align-items:center; justify-content:space-between; }
        .logo { font-weight:800; font-size:1.25rem; letter-spacing:-0.5px; }
        .topbar a.back { color:var(--text-gray); font-size:0.9rem; }
        .topbar a.back:hover { color:var(--primary); }
        .breadcrumb { font-size:0.82rem; color:var(--text-gray); padding:18px 0 0; }
        .breadcrumb a:hover { color:var(--primary); }
        .hero { padding:56px 0 44px; background:linear-gradient(180deg,var(--soft),rgba(245,250,252,0)); }
        .badges { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:22px; }
        .badge { background:var(--card-bg); border:1px solid var(--border); border-radius:50px; padding:7px 16px; font-size:0.8rem; color:var(--primary); box-shadow:0 10px 26px rgba(16,37,50,0.05); }
        h1 { font-size:clamp(1.9rem,5vw,3rem); line-height:1.15; font-weight:800; margin-bottom:18px; }
        .lead { font-size:1.12rem; color:var(--text-gray); max-width:760px; }
        .cta-row { display:flex; gap:14px; flex-wrap:wrap; margin-top:28px; }
        .btn-primary { background:var(--primary); color:#fff; padding:15px 32px; border-radius:50px; font-weight:600; box-shadow:0 10px 24px var(--primary-glow); transition:var(--transition); }
        .btn-primary:hover { transform:translateY(-2px); box-shadow:0 14px 34px var(--primary-glow); }
        .btn-secondary { background:#fff; border:1px solid var(--border); color:var(--text); padding:15px 32px; border-radius:50px; font-weight:600; transition:var(--transition); }
        .btn-secondary:hover { border-color:var(--primary); color:var(--primary); }
        .micro { color:var(--text-gray); font-size:0.85rem; margin-top:14px; }
        section { padding:42px 0; border-top:1px solid var(--border); }
        h2 { font-size:clamp(1.5rem,3.5vw,2.1rem); font-weight:800; margin-bottom:22px; }
        h3 { font-size:1.15rem; font-weight:600; margin-bottom:8px; }
        .prose p { color:var(--text-gray); margin-bottom:14px; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:18px; }
        .card { background:var(--card-bg); border:1px solid var(--border); border-radius:14px; padding:24px; transition:var(--transition); box-shadow:0 12px 34px rgba(16,37,50,0.06); }
        .card:hover { transform:translateY(-3px); border-color:rgba(20,127,168,0.28); }
        .card p { color:var(--text-gray); font-size:0.95rem; }
        .price { color:var(--primary); font-weight:800; font-size:1.05rem; margin-top:10px; }
        .faq-item { border:1px solid var(--border); border-radius:14px; padding:20px 22px; margin-bottom:12px; background:var(--card-bg); box-shadow:0 10px 26px rgba(16,37,50,0.05); }
        .faq-item p { color:var(--text-gray); margin-top:6px; }
        .cta-band { text-align:center; background:#fff; border:1px solid var(--border); border-radius:14px; padding:44px 24px; box-shadow:0 14px 38px rgba(16,37,50,0.07); }
        .cta-band h2 { margin-bottom:12px; }
        .cta-band p { color:var(--text-gray); margin-bottom:24px; }
        .towns { display:flex; gap:10px; flex-wrap:wrap; }
        .towns a { background:var(--card-bg); border:1px solid var(--border); border-radius:50px; padding:8px 16px; font-size:0.85rem; color:var(--text-gray); transition:var(--transition); }
        .towns a:hover { color:var(--primary); border-color:var(--primary); }
        footer { border-top:1px solid var(--border); padding:30px 0; color:var(--text-gray); font-size:0.85rem; text-align:center; background:#eef7fa; }
        footer a { color:var(--primary); }
    </style>
    <script defer src="/aqua-tracking.js"></script>
</head>
<body>
    <header class="topbar">
        <div class="container topbar-inner">
            <a href="%%DOMAIN%%/" class="logo">Aqua<span class="accent">Diagnostyka</span></a>
            <a href="%%DOMAIN%%/" class="back">← Strona główna</a>
        </div>
    </header>

    <div class="container">
        <nav class="breadcrumb">
            <a href="%%DOMAIN%%/">Strona główna</a> &nbsp;›&nbsp; Badanie wody %%NAME%%
        </nav>
    </div>

    <main>
        <section class="hero" style="border-top:none;">
            <div class="container">
                <div class="badges">
                    <span class="badge">Akredytowane metody</span>
                    <span class="badge">Wyniki w 48h</span>
                    <span class="badge">Dojazd GRATIS</span>
                </div>
                <h1>Badanie wody w <span class="accent">%%LOC%%</span> — sprawdzamy to za Ciebie</h1>
                <p class="lead">%%INTRO%%</p>
                <div class="cta-row">
                    <a href="%%DOMAIN%%/#kontakt" class="btn-primary">Zamów badanie wody</a>
                    <a href="#uslugi" class="btn-secondary">Zobacz zakres badań</a>
                </div>
                <p class="micro">Badanie od 150 zł &nbsp;·&nbsp; Dojazd i pobranie próbki GRATIS w %%LOC%% &nbsp;·&nbsp; Wyniki w 48h</p>
            </div>
        </section>

        <section>
            <div class="container prose">
                <h2>Dlaczego warto zbadać wodę w %%LOC%%?</h2>
                <p>%%WHY%%</p>
                <p>%%NOTE%% Regularne badanie wody to jedyny sposób, żeby wiedzieć na pewno, co pijesz — a często jest też wymagane formalnie, m.in. przy odbiorze domu, agroturystyce czy gastronomii (badanie honorowane przez Sanepid).</p>
            </div>
        </section>

        <section id="uslugi">
            <div class="container">
                <h2>Zakres badań wody w <span class="accent">%%LOC%%</span></h2>
                <div class="grid">
                    <div class="card"><h3>Woda ze studni</h3><p>Najczęstszy wybór — sprawdzenie, czy woda z własnego ujęcia nadaje się do picia.</p><div class="price">od 150 zł</div></div>
                    <div class="card"><h3>Badanie mikrobiologiczne</h3><p>Bakterie coli, <em>E. coli</em>, ogólna liczba mikroorganizmów — kluczowe dla bezpieczeństwa zdrowotnego.</p><div class="price">od 150 zł</div></div>
                    <div class="card"><h3>Badanie fizykochemiczne</h3><p>Azotany, azotyny, żelazo, mangan, twardość, pH, mętność i inne parametry jakości wody.</p><div class="price">od 150 zł</div></div>
                    <div class="card"><h3>Pełny pakiet (Sanepid)</h3><p>Mikrobiologia + fizykochemia w jednym — zakres wymagany m.in. przy odbiorach i działalności.</p><div class="price">pakiet</div></div>
                    <div class="card"><h3>Woda basenowa</h3><p>Kontrola jakości wody w przydomowych basenach i obiektach rekreacyjnych.</p><div class="price">wycena</div></div>
                    <div class="card"><h3>Doradztwo</h3><p>Nie wiesz, jaki zakres wybrać? Zaznacz „proszę o doradztwo" w formularzu — dobierzemy badanie do Twojej sytuacji.</p><div class="price">gratis</div></div>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <h2>Jak to działa?</h2>
                <div class="grid">
                    <div class="card"><h3>1. Formularz</h3><p>Wypełniasz krótki formularz online — adres w %%LOC%%, zakres badań, dane kontaktowe. Zajmuje minutę.</p></div>
                    <div class="card"><h3>2. Dojazd i pobranie</h3><p>Przyjeżdżamy pod wskazany adres i sami pobieramy próbkę zgodnie z procedurą. Dojazd gratis.</p></div>
                    <div class="card"><h3>3. Wyniki w 48h</h3><p>Otrzymujesz sprawozdanie z czytelną interpretacją i zaleceniami, jeśli woda przekracza normy.</p></div>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <h2>Najczęstsze pytania — badanie wody %%NAME%%</h2>
                <div class="faq-item"><h3>Ile kosztuje badanie wody w %%LOC%%?</h3><p>Od 150 zł. Cena zależy od zakresu — od fizykochemicznego, przez mikrobiologiczne, po pełny pakiet wymagany m.in. przez Sanepid. Dojazd i pobranie próbki są gratis.</p></div>
                <div class="faq-item"><h3>Czy dojeżdżacie do %%GEN%% po próbkę?</h3><p>Tak. Przyjeżdżamy pod wskazany adres w %%LOC%% i okolicach, sami pobieramy próbkę zgodnie z procedurą i dostarczamy do laboratorium. Dojazd jest bezpłatny.</p></div>
                <div class="faq-item"><h3>Jak szybko otrzymam wyniki?</h3><p>Standardowo w ciągu 48 godzin, wraz z interpretacją i zaleceniami.</p></div>
                <div class="faq-item"><h3>Czy badanie nadaje się do Sanepidu?</h3><p>Tak — wykonujemy badania akredytowanymi metodami, honorowanymi przez Sanepid.</p></div>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="cta-band">
                    <h2>Zamów badanie wody w <span class="accent">%%LOC%%</span></h2>
                    <p>Wypełnij formularz online — oddzwaniamy, doradzamy zakres i umawiamy dogodny termin pobrania próbki.</p>
                    <a href="%%DOMAIN%%/#kontakt" class="btn-primary">Wypełnij formularz zlecenia</a>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <h2>Obsługujemy też okoliczne miejscowości</h2>
                <div class="towns">
                    %%TOWNS%%
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>© 2026 AquaDiagnostyka — akredytowane laboratorium badania wody, Nowy Sącz i okolice.<br>
            Kontakt: <a href="mailto:kontakt@aquadiagnostyka.pl">kontakt@aquadiagnostyka.pl</a> &nbsp;·&nbsp; <a href="%%DOMAIN%%/#kontakt">Zamów badanie online</a></p>
        </div>
    </footer>
</body>
</html>
"""


def render(city):
    html = TEMPLATE
    repl = {
        "%%NAME%%": city["name"],
        "%%LOC%%": city["loc"],
        "%%SLUG%%": city["slug"],
        "%%LAT%%": city["lat"],
        "%%LON%%": city["lon"],
        "%%INTRO%%": city["intro"],
        "%%WHY%%": city["why"],
        "%%NOTE%%": city["note"],
        "%%GEN%%": GEN[city["slug"]],
        "%%DOMAIN%%": DOMAIN,
        "%%TOWNS%%": towns_links(city["slug"]),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


if __name__ == "__main__":
    for c in CITIES:
        path = os.path.join(OUT_DIR, "badanie-wody-%s.html" % c["slug"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(c))
        print("OK:", os.path.basename(path))
    shared_sitemap.build()
