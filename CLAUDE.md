# AquaDiagnostyka - instrukcje projektu

## Poczta i wysylka wynikow

- Nadawca dla wynikow: `Zespół AquaDiagnostyka <kontakt@aquadiagnostyka.pl>`.
- Reply-To: `kontakt@aquadiagnostyka.pl`.
- Podpis w mailach do klientow: `Zespół AquaDiagnostyka`.
- Nie podpisywac maili imieniem i nazwiskiem.
- Nie uzywac w nadawcy ani podpisie `Adrian Wieloch`.
- Wyniki wysylac jako PDF, nie jako edytowalny DOCX, chyba ze Adrian wprost poprosi inaczej.
- Sekrety i parametry techniczne poczty sa w `SEJF/KLUCZE_API/AQUADIAGNOSTYKA_SECRETS.md`.
- Po bounce sprawdzic status w Resend. Jesli adres trafi na suppression list, nie ponawiac bez usuniecia suppression w panelu Resend.

## Aktualna infrastruktura

- Strona: GitHub Pages, rekordy A root + CNAME `www`.
- Odbior `kontakt@aquadiagnostyka.pl`: ForwardEmail.net przez MX root.
- Wysylka `kontakt@aquadiagnostyka.pl`: Resend, domena `aquadiagnostyka.pl`, region `eu-west-1`, status verified.

## Atrybucja leadow i telefonow

- Formularze na stronie maja wysylac pola trackingowe do Formspree: `zrodlo`, `landing_url`, `landing_path`, `query_string`, `referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `gclid`.
- GA4 event formularza: `generate_lead`, z `event_label` rownym ID formularza (`contactForm` albo `leadForm`).
- Telefonow historycznych nie da sie pewnie odtworzyc z samej strony, jesli klient nie kliknal sledzonego `tel:`. Do analizy trzeba miec Google Business Profile Insights, GA4/Search Console albo reczny zapis rozmowy.
- Reczny rejestr rozmow i zlecen: `OPERACJE/LEADY_AQUA_2026.csv`.
- Przy kazdym telefonie dopisuj w rejestrze: data, imie/nazwa, miejscowosc, temat, kwota/status, odpowiedz klienta na pytanie "Skad Pan/Pani trafila na AquaDiagnostyke?", notatka.
