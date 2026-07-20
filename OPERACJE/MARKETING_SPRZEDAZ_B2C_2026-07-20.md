# AquaDiagnostyka — promocja i sprzedaż B2C 20.07.2026

## Decyzja strategiczna

AquaDiagnostyka idzie teraz głównie w prywatnych klientów: domy, studnie, działki, zakup nieruchomości, prywatne baseny i rodziny z dziećmi. Firmy/Sanepid zostają jako dostępny zakres, ale nie dominują komunikacji.

## Oferta wejściowa

1. Badanie podstawowe od 150 zł — szybki zakup, niski próg decyzji.
2. Pakiet studnia bezpieczna — fizykochemia + mikrobiologia, rekomendowany domyślnie.
3. Badanie przed zakupem domu/działki — komunikacja pod ryzyko kosztownej niespodzianki.
4. Kontrola po awarii/ulewie — komunikacja pod pilną potrzebę.
5. Basen/jacuzzi prywatne — sezonowo, reklamy maj-sierpień.

## Lejek

1. Wejście: Google Maps, lokalne SEO, poradniki, katalogi, polecenia.
2. Strona: rozpoznanie sytuacji klienta, CTA do formularza, kalkulator ceny.
3. Formularz: źródło, pierwszy landing, UTM i `session_id` zapisują się automatycznie.
4. Odpowiedź: potwierdzenie zakresu, terminu pobrania i ceny.
5. Po wyniku: wysyłka dokumentu + prośba o opinię Google.
6. Po 6-12 miesiącach: przypomnienie o badaniu kontrolnym.

## Kanały na start

### Google Business Profile

- Uzupełnić profil według `WIZYTOWKA_GOOGLE_PAKIET.md`.
- Link z UTM: `utm_source=google&utm_medium=organic&utm_campaign=gbp`.
- Co tydzień 1 post.
- Po każdym kliencie prośba o opinię.

### Lokalny SEO

- Utrzymać 10 stron miast i 12 poradników.
- Każdy nowy artykuł ma odpowiadać na prywatną sytuację klienta, np. "czy woda ze studni nadaje się do picia", "badanie wody przed kupnem domu".
- Mierzyć leady z `first_landing_path`.

### Katalogi i marketplace

- Dodać katalogi z `KATALOGI_NAP.md`.
- Każdy katalog dostaje własny UTM.
- Oferteo/Fixly testować tylko wtedy, gdy można szybko odpowiedzieć na zapytania.

### Reklamy płatne

- Nie startować szeroko bez baseline z organic.
- Pierwszy test: Google Search, tylko frazy intencyjne:
  - badanie wody ze studni Nowy Sącz
  - badanie wody Nowy Sącz
  - badanie wody do sanepidu Nowy Sącz
  - badanie wody przed kupnem domu
- Budżet testowy: mały, 7 dni, mierzyć koszt formularza.

## Sprzedaż

### Skrypt oddzwonienia / odpowiedzi

1. "Jaki jest typ wody: studnia, kran, basen, inne?"
2. "Do czego wynik jest potrzebny: bezpieczeństwo domowe, filtr, Sanepid, zakup domu?"
3. "Czy są objawy: zapach, kolor, osad, problemy po ulewie?"
4. "Czy ktoś pije tę wodę na co dzień, dzieci/niemowlęta?"
5. "Proponuję zakres X, cena Y, pobranie próbki w terminie Z."

### Reguły handlowe

- Nie sprzedawać najtańszego badania, jeśli sytuacja wymaga mikrobiologii.
- Nie obiecywać "woda jest dobra" przed wynikiem.
- Tłumaczyć wynik prostym językiem, bo to zwiększa zaufanie i polecenia.
- Po wysłaniu wyniku zawsze prosić o opinię Google.

## KPI tygodniowe

- Wejścia z GBP.
- Wejścia z SEO pages.
- Formularze łącznie.
- Formularze z `first_source_kind=google_organic`.
- Formularze z katalogów/marketplace.
- Klienci zapłaceni.
- Opinie Google pozyskane.
- Najlepszy landing według `first_landing_path`.

## Najbliższe zadania

1. Dokończyć deploy trackingu i jasnego motywu.
2. Uzupełnić Google Business Profile po zalogowaniu do konta właściciela.
3. Dodać pierwsze 3 katalogi: Bing Places, Panorama Firm, pkt.pl.
4. Po 5-10 leadach sprawdzić, z których landingów przychodzą prywatni klienci.
5. Dopiero potem uruchomić mały test Google Ads.
