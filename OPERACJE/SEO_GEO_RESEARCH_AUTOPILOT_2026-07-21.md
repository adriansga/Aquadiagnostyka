# AquaDiagnostyka — SEO/GEO research + autopilot 21.07.2026

## Wnioski z aktualnego researchu

1. Google nie traktuje GEO/AEO jako osobnej sztuczki. Dla widocznosci w AI Overviews/AI Mode dalej liczy sie fundament SEO: dostepna strona, dobra struktura, pomocna tresc, zgodne dane strukturalne i realna wartosc dla uzytkownika.
2. Lokalne wyniki Google Business Profile opieraja sie glownie o relevance, distance i prominence. Dla Aqua oznacza to: profil GBP musi miec kategorie, opis, uslugi, obszar, zdjecia, posty i opinie spojne z fraza „badanie wody / mikrobiologia / studnia / Nowy Sacz”.
3. LocalBusiness JSON-LD pomaga Google zrozumiec firme, ale structured data musi zgadzac sie z widoczna trescia. Nie wolno dodawac fake ratingow/opinii ani danych, ktorych nie ma na stronie.
4. Indexing API Google nie sluzy do zwyklych artykulow ani stron uslugowych. Dla Aqua poprawna sciezka to sitemap + Search Console URL Inspection / recrawl, nie Indexing API.
5. Automatyczne tresci AI sa dopuszczalne tylko wtedy, gdy sa dokladne, pomocne i nie powstaja wylacznie do manipulowania rankingiem. Dlatego autopilot musi miec walidator i zakazane claimy.

## Co juz jest wdrozone

- Lokalne strony miast B2C mikrobiologia + sitemap.
- Sekcja odpowiedzi AI/GEO na stronie glownej.
- LocalBusiness/FAQ/Article JSON-LD.
- Tracking UTM, first landing, source kind i session id.
- GBP/FB publish queue gotowa, ale publikacja czeka na dostep do kont.

## Autopilot V1

Workflow: `.github/workflows/seo-content.yml`

Harmonogram:
- poniedzialek/sroda/piatek 06:00 UTC,
- mozliwe reczne uruchomienie przez GitHub Actions.

Kroki:
1. `python seo/seo_guard.py` przed generowaniem.
2. `python seo/auto_article.py` generuje pierwszy niezaznaczony temat z `seo/topics.md`.
3. Generator tworzy `poradnik-*.html`, aktualizuje `poradnik.html`, related links i `sitemap.xml`.
4. `python seo/seo_guard.py` po generowaniu.
5. Workflow commituje tylko: `seo/topics.md`, `sitemap.xml`, `poradnik.html`, `poradnik-*.html`.

## Guard blokuje

- techniczne etykiety na stronie typu `NAJWAŻNIEJSZA ŚCIEŻKA B2C`,
- stare claimy: `od 150`, `Dojazd GRATIS`, `dojazd i pobranie próbki gratis`,
- fake social proof: `127 opinii`, `aggregateRating`,
- promocje i urgency timer,
- bledny JSON-LD,
- brak title/meta description/H1/canonical,
- nie-ASCII albo duplikaty w sitemap,
- URL w sitemap bez lokalnego pliku.

## Kolejka tematyczna

Od 21.07.2026 nowe tematy sa tylko pod:
- prywatne studnie,
- mikrobiologie wody,
- E. coli, enterokoki, bakterie grupy coli,
- kontrole po dezynfekcji,
- ulewy/podtopienia,
- filtracje po wyniku, nie przed wynikiem.

Tematy basenowe, przemyslowe, scieki, gastronomia i ogolne B2B nie sa juz frontem ani kolejka autopilota.

## Zrodla

- Google Search Central — AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Business Profile Help — local ranking: https://support.google.com/business/answer/7091
- Google Search Central — LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google Search Central — structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google Search Central — generative AI content: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Google Search Central — Indexing API: https://developers.google.com/search/apis/indexing-api/v3/quickstart
