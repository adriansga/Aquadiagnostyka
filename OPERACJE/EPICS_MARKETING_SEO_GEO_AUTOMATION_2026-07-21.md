# AquaDiagnostyka — epiki marketing/SEO/GEO/automation 21.07.2026

## Zasada wykonania

Każdy epik robimy end-to-end: diagnoza -> backup -> wdrożenie -> lokalny test -> produkcja/test zewnętrzny -> log. Nie kończyć na "planie". Dla publikacji zewnętrznych, płatnych reklam i OAuth potrzebny może być dostęp do konta właściciela, ale wszystko inne agent przygotowuje sam.

## Decyzja operacyjna 21.07.2026

Główna ścieżka AquaDiagnostyki = B2C i mikrobiologiczne badanie wody dla prywatnych studni/domów/działek. Fizykochemia zostaje jako rozszerzenie, gdy sytuacja klienta tego wymaga. Przemysł, ścieki, duże obiekty, aquaparki i ogólne B2B nie są komunikatem frontowym strony ani contentu.

## EPIC 01 — Incognito content pack i publikacja V1

**Cel:** mieć gotowe treści do publikacji jako marka `Zespół AquaDiagnostyka`, bez ekspozycji Adriana.

**Zakres:**
- 10 postów Facebook lokalne grupy/strona,
- 8 postów Google Business Profile,
- odpowiedzi na komentarze,
- linki UTM,
- harmonogram 7 dni,
- QA antyhalucynacyjne.

**Done/dowód:**
- Plik `CONTENT_PACK_INCOGNITO_B2C_2026-07-21.md` istnieje.
- Każdy post ma CTA i UTM.
- Żaden post nie używa imienia Adriana ani nie udaje opinii.

**Self-check:**
- `rg "Adrian|127 opinii|Promocja|-20|opinia klienta"` na paczce postów.
- Ręczne sprawdzenie 3 losowych postów pod kątem tonu i zgodności B2C.

## EPIC 02 — Google Business Profile manual sprint

**Cel:** uzupełnić istniejącą wizytówkę i zacząć zbierać ruch z intencji lokalnej.

**Zakres:**
- ustawić link strony z UTM,
- uzupełnić kategorie, opis, usługi, obszar działania,
- dodać pierwszy post z paczki,
- przygotować/prosić o link do opinii,
- zapisać publiczny status i prywatne ograniczenia.

**Done/dowód:**
- Screenshot lub eksport pól profilu po zmianie.
- Link z profilu prowadzi do `utm_campaign=gbp`.
- Pierwszy post opublikowany albo zapisany jako gotowy do publikacji, jeśli brak dostępu.

**Bloker fizyczny:**
- Dostęp do konta Google właściciela profilu i ewentualne OAuth/2FA.

**Self-check:**
- Otworzyć publiczną wizytówkę.
- Kliknąć link strony i potwierdzić UTM.
- Sprawdzić w GA4/Formspree po testowym wejściu, czy `utm_campaign=gbp` jest widoczny.

## EPIC 03 — Automatyzacja publikacji postów

**Cel:** zbudować automat, który generuje, waliduje i publikuje posty do kanałów, gdzie API jest legalnie dostępne.

**Zakres V1:**
- generator postów z szablonów i kalendarza,
- kolejka `draft -> qa_pass -> ready -> published`,
- tryb `dry-run` bez publikacji,
- zapis UTM, kanału i daty,
- eksport CSV/JSON dla ręcznej publikacji.

**Zakres V2:**
- publikacja do Google Business Profile przez Business Profile API po autoryzacji,
- publikacja na Facebook Page przez Meta Pages API po dostępie do strony,
- pobieranie statusu i linku opublikowanego posta,
- raport tygodniowy.

**Ważne ograniczenia:**
- Facebook Page można automatyzować przez Pages API po uzyskaniu tokena i uprawnień.
- Facebook Groups traktować jako manual/semi-manual, dopóki nie ma oficjalnej i bezpiecznej ścieżki dla konkretnej grupy.
- Google Business Profile wymaga dostępu do profilu i OAuth.

**Done/dowód:**
- `dry-run` generuje paczkę 7 dni bez publikacji.
- Walidator blokuje post bez UTM, z imieniem Adriana, z fałszywą promocją lub niezweryfikowaną opinią.
- Po OAuth: post testowy opublikowany i publicznie widoczny.

**Self-check:**
- Test jednostkowy walidatora treści.
- Test `dry-run` na 7 postów.
- Test publikacji tylko na koncie testowym albo po jawnej zgodzie właściciela.

## EPIC 04 — SEO/GEO audit techniczny

**Status 21.07.2026:** P0 wykonane dla lokalnych podstron miast i sitemap. Generator `seo/generate_city_pages.py` przepisany z szerokiego/starego przekazu (`150 zł`, `Dojazd GRATIS`, Sanepid, basen, B2B) na B2C mikrobiologię prywatnych studni/domów/działek. Wygenerowano 9 podstron miast i `sitemap.xml` z 23 URL. Naprawiono techniczny slug poradnika `poradnik-woda-mętna-przyczyny.html` → `poradnik-woda-metna-przyczyny.html`, wraz z linkami wewnętrznymi i canonical/OG/schema. QA lokalne: HTML parse + JSON-LD OK dla 16 plików, sitemap bez nie-ASCII w URL, lokalne HTTP 200, screenshot desktop/mobile strony miasta OK.

**Cel:** sprawdzić, czy strona jest czytelna dla Google i modeli AI jako lokalna usługa badania wody.

**Zakres:**
- meta title/description,
- nagłówki H1-H3,
- LocalBusiness JSON-LD,
- usługi i obszary działania,
- sitemap/robots,
- canonical,
- internal linking między miastami, poradnikiem i stroną główną,
- treści pod zapytania lokalne i AI answers,
- spójność NAP bez niepotwierdzonych danych,
- brak fake ratings i fake reviews.

**Done/dowód:**
- Raport `SEO_GEO_AUDIT_YYYY-MM-DD.md` z priorytetami P0/P1/P2.
- Walidacja: sitemap HTTP 200, wszystkie publiczne URL HTTP 200.
- Rich Results Test lub lokalna walidacja JSON-LD, jeśli nie ma dostępu do narzędzia webowego.

**Self-check:**
- `curl -I` dla strony głównej, sitemap i 3 podstron.
- Parser HTML dla title/meta/H1/schema.
- `rg` na zakazane claims: `aggregateRating`, `127 opinii`, `Promocja`.

## EPIC 05 — GEO/content pod AI answers

**Status 21.07.2026:** P0 wdrożone na stronie głównej. Dodano sekcję `#odpowiedzi` z 6 krótkimi odpowiedziami dla prywatnego właściciela studni: co wykrywa mikrobiologia, kiedy badać, czy filtr wystarczy, co oznacza E. coli, kiedy rozszerzyć o fizykochemię i jak zamówić. Rozszerzono `FAQPage` JSON-LD o 4 dodatkowe pytania pod AI/Google answers.

**Cel:** zwiększyć szansę, że Google/AI odpowiadający na pytania lokalne rozumie, że Aqua robi badanie wody w Nowym Sączu i okolicach.

**Zakres:**
- sekcja Q&A na stronie pod naturalne pytania,
- krótkie definicje usług,
- tabele: kiedy badać, jaki zakres, co oznaczają objawy,
- jasne odpowiedzi na pytania "czy badanie do Sanepidu", "ile kosztuje", "czy dojeżdżacie",
- spójny język B2C.

**Done/dowód:**
- Strona ma sekcję Q&A 6-8 pytań dla prywatnych klientów.
- Każda odpowiedź ma konkretny kontekst lokalny i CTA.
- Brak przesadnych obietnic i brak medyczno-prawnych gwarancji.

**Self-check:**
- Manual read-through całej ścieżki klienta.
- Sprawdzenie, czy każda odpowiedź kończy niepewność klienta albo kieruje do formularza.

## EPIC 06 — Formularz/dropdowny i kalkulator B2C

**Problem teraz:** aktualne opcje formularza/kalkulatora nadal zawierają B2B/przemysł/ścieki i są mniej zgodne z prywatnym klientem.

**Wstępny audyt 21.07.2026:**
- `calcSource` ma opcję `Woda przemyslowa / scieki`, która nie pasuje do głównej ścieżki B2C.
- `calcScope` zaczyna od terminologii laboratoryjnej, zanim klient opisze sytuację.
- `contactForm` ma `Badanie przemyslowe / scieki` obok studni/basenu, przez co rozmywa przekaz prywatny.
- Brakuje opcji sytuacyjnych: zakup domu/działki, po ulewach/awarii, kontrola po dezynfekcji, "nie wiem, dobierzcie".
- Wniosek: P0 do wdrożenia przed reklamami i większą publikacją postów.

**Status 21.07.2026 07:xx:**
- P0 wdrożone na `index.html`: hero, usługi, przypadki, kalkulator, FAQ, formularz i stopka ustawione pod mikrobiologię/B2C.
- Usunięto z głównej ścieżki przemysł, ścieki, aquaparki, przykłady OSiR oraz B2B social proof.
- Pozostały do sprawdzenia lokalnie/produkcyjnie: render, tracking formularza, schema, brak zakazanych fraz.

**Cel:** uprościć wybór tak, żeby klient nie musiał znać terminologii laboratoryjnej.

**Zakres:**
- zmienić `Typ źródła wody` na wybór sytuacji klienta:
  - Własna studnia przy domu,
  - Woda z kranu / instalacja domowa,
  - Zakup domu lub działki,
  - Prywatny basen / jacuzzi,
  - Po ulewach, awarii albo długiej przerwie,
  - Nie wiem, chcę doradztwa.
- zmienić `Zakres badania` na:
  - Nie wiem, dobierzcie zakres,
  - Podstawowe fizykochemiczne,
  - Mikrobiologiczne,
  - Pełne: fizykochemia + mikrobiologia,
  - Do Sanepidu / formalne,
  - Kontrola po dezynfekcji.
- usunąć `przemysłowe / ścieki` z głównej ścieżki B2C albo przenieść niżej.
- formularz kontaktowy ma pytać najpierw o sytuację, nie o specjalistyczny zakres.

**Done/dowód:**
- HTML wdrożony i produkcyjnie zweryfikowany.
- Formularz wysyła nowe wartości do Formspree.
- GA4/Formspree nadal dostają UTM i `first_landing_path`.

**Self-check:**
- Playwright desktop/mobile screenshot.
- Test submit do Formspree tylko jeśli nie spamuje produkcyjnego maila; inaczej test pól hidden lokalnie.
- `node --check` i brak błędów konsoli.

## EPIC 07 — UX simplification strony

**Cel:** sprawdzić, czy strona nie jest zagmatwana i skrócić drogę do formularza.

**Zakres:**
- analiza kolejności sekcji,
- sprawdzenie, czy kalkulator pomaga czy rozprasza,
- uproszczenie nawigacji,
- jasne CTA w hero i po sekcjach,
- usunięcie elementów B2B z głównej ścieżki,
- mobile first.

**Done/dowód:**
- Raport `UX_CONVERSION_AUDIT_YYYY-MM-DD.md`.
- Lista zmian P0/P1/P2.
- Wdrożone P0.

**Self-check:**
- 5-sekundowy test: użytkownik ma wiedzieć co firma robi, dla kogo i co kliknąć.
- Mobile screenshot 390x844.
- Brak overlapów i tekstów wychodzących z przycisków.

## EPIC 08 — Katalogi i lokalne cytowania

**Cel:** zwiększyć lokalne zaufanie i źródła wejść bez ekspozycji osobistej.

**Zakres:**
- Bing Places,
- Apple Business Connect,
- Panorama Firm,
- pkt.pl,
- Aleo,
- ewentualnie Oferteo/Fixly po decyzji o obsłudze zapytań.

**Done/dowód:**
- Każdy wpis ma spójny NAP.
- Każdy możliwy link ma UTM.
- Status wpisany w `KATALOGI_NAP.md`.

**Self-check:**
- Otworzyć publiczny wpis.
- Kliknąć link i potwierdzić UTM.

## EPIC 09 — Lead tracking i tygodniowy raport

**Cel:** połączyć marketing z realnymi pieniędzmi.

**Zakres:**
- tabela leadów,
- źródło deklarowane przez klienta,
- źródło techniczne z formularza,
- status: nowy / kontakt / wycena / pobranie / zapłacone / utracone,
- kwota,
- następny krok.

**Done/dowód:**
- Jeden plik CSV/Sheet jako SSOT leadów.
- Tygodniowy raport: kanał -> formularze -> klienci -> przychód.

**Self-check:**
- Każdy nowy klient ma źródło albo `nieustalone`.
- Brak pustych kwot przy statusie `zapłacone`.

## EPIC 10 — Google Ads mini-test

**Cel:** sprawdzić, czy płatny intent search może tanio dowozić formularze.

**Warunek wejścia:**
- GBP i formularz gotowe.
- Minimum podstawowy raport organic/GBP.
- Landing i dropdowny B2C poprawione.

**Zakres:**
- kampania Search tylko exact/phrase lokalne,
- mały budżet 7 dni,
- konwersja = formularz,
- frazy negatywne,
- brak broad match na start.

**Done/dowód:**
- Koszt kliknięcia, koszt formularza, liczba formularzy.
- Decyzja: skalować / poprawić landing / zatrzymać.

**Self-check:**
- Nie uruchamiać bez pomiaru konwersji.
- Nie uruchamiać bez limitu budżetu.

## Kolejność autonomiczna

1. EPIC 06 — DONE: QA/deploy formularza i dropdownów B2C mikrobiologia.
2. EPIC 04 — DONE P0: lokalne podstrony miast + sitemap pod mikrobiologię B2C.
3. EPIC 05 — DONE P0: sekcja AI/GEO answers + dodatkowe FAQ schema.
4. EPIC 02 — GBP manual sprint pod mikrobiologię prywatnych studni.
5. EPIC 01 — publikacja pierwszych postów, po aktualizacji treści pod mikrobiologię.
6. EPIC 08 — katalogi z opisem mikrobiologia/studnia/dom.
7. EPIC 09 — raport leadów.
8. EPIC 03 — automatyzacja po ustaleniu dostępu do kont.
9. EPIC 10 — Google Ads mini-test tylko na frazy mikrobiologiczne/studnia.

## Źródła techniczne do automatyzacji

- Google Business Profile API: https://developers.google.com/my-business/reference/rest
- Meta Pages API Posts: https://developers.facebook.com/documentation/pages-api/posts
- Google LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
