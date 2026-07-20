# AquaDiagnostyka - atrybucja kontaktow 2026-07-20

## Stan faktyczny

- Aktualna strona glowna dziala glownie przez formularz Formspree `https://formspree.io/f/mdawepne`.
- GA4 jest podpiete jako `G-7HN31380S5`.
- Na stronie glownej nie ma aktywnego linku `tel:` ani plywajacego widgetu telefonu. W kodzie jest komentarz, ze telefon/WhatsApp zostal usuniety, a zamowienia ida przez formularz.
- Historyczny numer `696 053 282` wystepuje w backupach, ulotkach i banerach. To moglo generowac telefony poza obecnym trackingiem strony.
- W samym HTML nie ma danych, ktore pozwalaja pewnie odtworzyc, skad dzwonili klienci.

## Co mozna sprawdzic dla historycznych telefonow

1. Google Business Profile Insights, jezeli wizytowka byla aktywna i miala numer telefonu.
2. GA4 / Search Console: wejscia organiczne na strone, frazy, miasta, landing pages.
3. Historia polaczen w telefonie: daty/godziny numerow i reczne dopasowanie do zlecen.
4. Formspree: maile/zlecenia z pola `zrodlo`, jesli lead przyszedl formularzem.

## Co zostalo wdrozone na przyszlosc

- Formularze wysylaja teraz osobne pola: `landing_url`, `landing_path`, `query_string`, `referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `gclid`.
- Pole `zrodlo` ma czytelny skrót atrybucji dla maila z Formspree.
- GA4 `generate_lead` dostaje etykiete formularza i podstawowe parametry atrybucji.
- Reczny rejestr telefonow: `OPERACJE/LEADY_AQUA_2026.csv`.

## Zasada od dzisiaj

Przy kazdym telefonie zadac jedno neutralne pytanie:

> Skad Pan/Pani trafila na AquaDiagnostyke - Google, polecenie, ulotka, Facebook czy inaczej?

Odpowiedz wpisac do `OPERACJE/LEADY_AQUA_2026.csv`.
