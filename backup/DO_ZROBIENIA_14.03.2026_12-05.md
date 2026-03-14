# 📋 AQUADIAGNOSTYKA - DO ZROBIENIA (USER TASKS)

**Data:** 14.03.2026  
**Status:** Strona gotowa do publikacji ✅  
**Czas realizacji:** ~30-40 minut

---

## 🎯 PRIORYTET 1: KONFIGURACJA NARZĘDZI (15 minut)

### 1. GOOGLE ANALYTICS 4 ⭐⭐⭐
**Czas:** 5 minut  
**Priorytet:** KRYTYCZNY

**Kroki:**
1. Wejdź na [analytics.google.com](https://analytics.google.com)
2. Zaloguj się Google
3. Kliknij **"Rozpocznij pomiar"**
4. Wypełnij:
   - Nazwa konta: `AquaDiagnostyka`
   - Nazwa właściwości: `aquadiagnostyka.pl`
   - Strefa czasowa: `Polska`
   - Waluta: `PLN`
5. Kliknij **"Dalej"** → **"Utwórz"**
6. Wybierz **"Sieć"** → **"Strona internetowa"**
7. Wpisz:
   - Nazwa strumienia: `aquadiagnostyka.pl`
   - URL: `https://aquadiagnostyka.pl`
8. **SKOPIUJ Measurement ID** (zaczyna się od `G-`)
9. Otwórz plik `index.html`
10. Znajdź linię ~66 (komentarz `<!-- Google Analytics 4 -->`)
11. Zamień `G-XXXXXXXXXX` na swoje ID
12. Zapisz plik

**Przykład:**
```html
<!-- BYŁO: -->
gtag('config', 'G-XXXXXXXXXX');

<!-- BĘDZIE: -->
gtag('config', 'G-ABC123XYZ456');
```

---

### 2. FACEBOOK PIXEL ⭐⭐
**Czas:** 5 minut  
**Priorytet:** WAŻNY (jeśli planujesz reklamy na FB)

**Kroki:**
1. Wejdź na [Facebook Events Manager](https://www.facebook.com/events_manager)
2. Kliknij **"Połącz źródło danych"** → **"Sieć"** → **"Pixel Facebooka"**
3. Nazwij pixel: `AquaDiagnostyka Pixel`
4. Kliknij **"Utwórz"**
5. **SKOPIUJ Pixel ID** (same cyfry)
6. Otwórz plik `index.html`
7. Znajdź linię ~79 (komentarz `<!-- Facebook Pixel -->`)
8. Zamień `XXXXXXXXXXXXX` na swoje Pixel ID (w 2 miejscach!)

**Przykład:**
```html
<!-- BYŁO: -->
fbq('init', 'XXXXXXXXXXXXX');
src="https://www.facebook.com/tr?id=XXXXXXXXXXXXX&ev=PageView

<!-- BĘDZIE: -->
fbq('init', '123456789012345');
src="https://www.facebook.com/tr?id=123456789012345&ev=PageView
```

---

### 3. CRISP LIVE CHAT ⭐⭐⭐
**Czas:** 10 minut  
**Priorytet:** KRYTYCZNY

**Kroki:**
1. Wejdź na [crisp.chat](https://crisp.chat)
2. Kliknij **"Wypróbuj za darmo"**
3. Zarejestruj się (email + hasło)
4. Wypełnij profil firmy:
   - Nazwa: `AquaDiagnostyka`
   - Email: `kontakt@aquadiagnostyka.pl`
   - Telefon: `696 053 282`
5. Kliknij **"Dalej"** → **"Dodaj stronę"**
6. Wpisz: `aquadiagnostyka.pl`
7. Wybierz **"Inna"** (nie WordPress/Shopify)
8. **SKOPIUJ Website ID** (format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`)
9. Otwórz plik `index.html`
10. Znajdź linię ~88 (komentarz `<!-- Crisp Live Chat -->`)
11. Zamień `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` na swoje ID
12. Zapisz plik

**Przykład:**
```html
<!-- BYŁO: -->
window.CRISP_WEBSITE_ID="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX";

<!-- BĘDZIE: -->
window.CRISP_WEBSITE_ID="abc12345-6789-0xyz-abcd-ef1234567890";
```

**Po konfiguracji:**
- Zainstaluj aplikację Crisp na telefonie (iOS/Android)
- Będziesz dostawać powiadomienia o nowych wiadomościach
- Odpowiadaj w ciągu 5 minut (szybka reakcja = więcej konwersji!)

---

## 🎨 PRIORYTET 2: GRAFIKI (15 minut)

### 4. OG-IMAGE.JPG ⭐⭐⭐
**Czas:** 15 minut  
**Priorytet:** KRYTYCZNY (do social media)

**Opcja A: Canva (najłatwiej)**
1. Wejdź na [canva.com](https://canva.com)
2. Wyszukaj: **"Facebook Post"** (1200x630px)
3. Stwórz grafikę:
   - **Tło:** Ciemne (#050508) z niebieskim akcentem (#0099ff)
   - **Tekst główny:** `Badanie Wody Nowy Sącz`
   - **Tekst mniejszy:** `od 150zł | Wynik 24h`
   - **Telefon:** `696 053 282`
   - **Logo:** Napisz "AD" lub dodaj logo jeśli masz
4. Kliknij **"Pobierz"** → **JPG**
5. Zapisz jako: `og-image.jpg`
6. Wrzuć na serwer obok `index.html`

**Opcja B: AI Generator (szybciej)**
1. Wejdź na [looka.com](https://looka.com) lub [hatchful.shopify.com](https://hatchful.shopify.com)
2. Wygeneruj logo/branding
3. Eksportuj jako 1200x630px
4. Zapisz jako `og-image.jpg`

**Wymagania techniczne:**
- Wymiary: **1200x630 pikseli**
- Format: **JPG** (max 200KB)
- Kolory: Ciemne tło + niebieski akcent (#0099ff)
- Tekst: Czytelny, duży, kontrastowy

---

## 🚀 PRIORYTET 3: PUBLIKACJA (10 minut)

### 5. WRZUCENIE NA SERWER ⭐⭐⭐
**Czas:** 10 minut  
**Priorytet:** KRYTYCZNY

**Kroki:**
1. Podłącz się do serwera (FTP/cPanel/SSH)
2. Przejdź do folderu strony (zazwyczaj `public_html` lub `www`)
3. **Zrób backup starej strony** (jeśli była):
   - Pobierz wszystkie pliki na komputer
   - Lub zmień nazwę folderu na `public_html_OLD`
4. Wgraj nowe pliki:
   - `index.html` (zmieniony)
   - `og-image.jpg` (nowy plik)
5. Sprawdź czy strona działa: `https://aquadiagnostyka.pl`

**Alternatywa: GitHub Pages (darmowy hosting)**
1. Wejdź na [GitHub](https://github.com)
2. Utwórz nowe repozytorium: `aquadiagnostyka`
3. Wrzuć pliki: `index.html` + `og-image.jpg`
4. Wejdź w **Settings** → **Pages**
5. Włącz: **Deploy from branch: main**
6. Strona będzie pod: `twoj-user.github.io/aquadiagnostyka`
7. Podłącz domenę (opcjonalnie)

---

## ✅ CHECKLIST PO KONFIGURACJI

### Testy (10 minut):
- [ ] Strona ładuje się poprawnie
- [ ] Wszystkie sekcje są widoczne
- [ ] CTA przyciski działają
- [ ] Formularz wysyła (test wyślij)
- [ ] Phone FAB przycisk działa
- [ ] Exit popup się pojawia (wyjedź myszką nad pasek adresu)
- [ ] Urgency timer odlicza (72h)
- [ ] Floating CTA pojawia się po scrollu
- [ ] Opinie są widoczne (12 sztuk)
- [ ] Badge "NAJCZĘŚCIEJ WYBIERANY" widoczny

### Testy narzędzi:
- [ ] Google Analytics: Wejdź na stronę → Sprawdź Real-Time w GA4
- [ ] Facebook Pixel: Zainstaluj [Facebook Pixel Helper](https://chrome.google.com/webstore/detail/facebook-pixel-helper/) → Sprawdź czy wykrywa
- [ ] Crisp Chat: Wejdź na stronę → Czy widget jest widoczny?

### Testy SEO:
- [ ] Title wyświetla się w Google (sprawdź podgląd linku)
- [ ] OG image wyświetla się na Facebooku (udostępnij link)
- [ ] Strona jest responsywna (sprawdź na telefonie)

---

## 📞 KONTAKT DO POMOCY

Jeśli utkniesz:
- **Email:** kontakt@aquadiagnostyka.pl
- **Telefon:** 696 053 282
- **Godziny:** Pon-Pt 7:30-16:00

---

## 🎯 NASTĘPNE KROKI (PO PUBLIKACJI)

### Tydzień 1:
- [ ] Skonfiguruj Google Analytics 4
- [ ] Skonfiguruj Facebook Pixel
- [ ] Włącz Crisp Live Chat
- [ ] Wrzuć og-image.jpg
- [ ] Przetestuj formularz kontaktowy

### Tydzień 2:
- [ ] Uruchom Google Ads (budżet 20zł/dzień)
- [ ] Uruchom Facebook Ads (budżet 15zł/dzień)
- [ ] Dodaj 3 artykuły na bloga
- [ ] Poproś 5 klientów o opinie w Google

### Miesiąc 1:
- [ ] Analiza konwersji w Google Analytics
- [ ] Optymalizacja reklam (A/B testy)
- [ ] Dodaj case study klientów
- [ ] Rozszerz ofertę o nowe badania

---

## 📊 METRYKI SUKCESU

**Cel na miesiąc 1:**
- 500+ odwiedzin miesięcznie
- 20+ leadów z formularza
- 5+ telefonów z kliknięcia w numer
- 3+ konwersji z Live Chat

**Cel na miesiąc 3:**
- 1500+ odwiedzin miesięcznie
- 50+ leadów z formularza
- 15+ telefonów z kliknięcia
- 10+ konwersji z Live Chat

---

**Powodzenia! Strona jest gotowa do działania!** 🚀

**Wersja:** 1.0  
**Ostatnia aktualizacja:** 14.03.2026 12:00
