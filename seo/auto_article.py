# -*- coding: utf-8 -*-
"""
Autopilot tresci: bierze nastepny temat z seo/topics.md, generuje artykul przez Anthropic API,
renderuje strone (generate_article.py), oznacza temat jako zrobiony.
NIE robi git push - to robi workflow GitHub Actions.

Wymaga zmiennej srodowiskowej ANTHROPIC_API_KEY.
  python seo/auto_article.py
"""
import os, re, json, subprocess, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS = os.path.join(ROOT, "seo", "topics.md")
BODY_TMP = os.path.join(ROOT, "seo", "_body_tmp.html")
MODEL = "claude-sonnet-4-6"

SYSTEM = (
    "Jesteś ekspertem SEO i copywriterem laboratorium badania wody AquaDiagnostyka "
    "(Nowy Sącz i okolice). Piszesz po polsku, rzeczowo, bez lania wody, z realną wiedzą. "
    "Zwracasz WYŁĄCZNIE poprawny JSON."
)

PROMPT = """Napisz artykuł na bloga (poradnik) dla strony aquadiagnostyka.pl.

Temat: {title}
Główna fraza SEO: {kw}

Wymagania:
- 700-1000 słów, język polski, ton ekspercki i pomocny.
- Treść jako czysty HTML: akapity <p>, nagłówki <h2>/<h3>, listy <ul>/<li>/<ol>, <strong>. BEZ <html>, <head>, <h1>, <style>.
- Naturalnie wpleć główną frazę oraz lokalność (Nowy Sącz i okolice, studnie, Sanepid) — bez przesady.
- Konkretna wiedza (normy, liczby, przyczyny, rozwiązania), nie ogólniki.
- NIE podawaj numeru telefonu. CTA: zamówienie przez formularz online.
- Zakończ akapitem podsumowującym z zachętą do zamówienia badania przez formularz.

Zwróć JSON o polach:
{{"desc": "<meta description 150-160 znaków>", "keywords": "<5-7 fraz po przecinku>", "body": "<HTML treści>"}}"""


def next_topic():
    with open(TOPICS, encoding="utf-8") as f:
        lines = f.readlines()
    for i, ln in enumerate(lines):
        m = re.match(r"- \[ \] (\S+) \| (.+?) \| (.+)", ln.strip())
        if m:
            return i, lines, m.group(1), m.group(2).strip(), m.group(3).strip()
    return None, lines, None, None, None


def call_api(title, kw):
    key = os.environ["ANTHROPIC_API_KEY"]
    payload = {
        "model": MODEL,
        "max_tokens": 4000,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": PROMPT.format(title=title, kw=kw)}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    text = "".join(b.get("text", "") for b in resp["content"])
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(json)?\s*|\s*```$", "", text)
    return json.loads(text)


def main():
    idx, lines, slug, title, kw = next_topic()
    if slug is None:
        print("Kolejka pusta - brak nowych tematow.")
        return 0
    print("Temat:", slug, "|", title)
    data = call_api(title, kw)
    with open(BODY_TMP, "w", encoding="utf-8") as f:
        f.write(data["body"].strip())

    subprocess.run([sys.executable, os.path.join(ROOT, "seo", "generate_article.py"),
                    "--slug", slug, "--title", title,
                    "--desc", data["desc"], "--keywords", data["keywords"],
                    "--body", BODY_TMP], check=True)

    if os.path.exists(BODY_TMP):
        os.remove(BODY_TMP)
    # oznacz temat jako zrobiony
    lines[idx] = lines[idx].replace("- [ ]", "- [x]", 1)
    with open(TOPICS, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Gotowe:", slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
