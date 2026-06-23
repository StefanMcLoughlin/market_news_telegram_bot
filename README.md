# Market News Telegram Bot

Ein Python-basierter Telegram Bot, der aktuelle marktbezogene News abruft, filtert, nach Relevanz sortiert und direkt in Telegram ausgibt.

Zusätzlich kann der Bot die wichtigste News einer Kategorie mit OpenAI analysieren und eine kurze AI Market Analysis mit Summary, möglichem Market Impact und Key Points ausgeben.

Das Projekt wurde im Rahmen meiner AI-/Backend-Ausbildung gebaut, um praktische Erfahrung mit APIs, Telegram Bots, externer Datenverarbeitung, AI-Integration, Projektstruktur, Testing, Logging, Fehlerbehandlung, Linting, Formatting und GitHub-Workflow zu sammeln.

---

## Ziel des Projekts

Ziel ist es, einen Telegram Bot zu entwickeln, der relevante Markt-News aus verschiedenen Bereichen sammelt, filtert und verständlich aufbereitet.

Der Bot soll langfristig ähnlich wie ein kleiner Market-News-Assistent funktionieren:

* aktuelle News abrufen
* irrelevante Quellen und Clickbait filtern
* News nach Kategorien ausgeben
* Relevance und Sentiment anzeigen
* wichtige News mit AI zusammenfassen
* mögliche Markt-Auswirkungen analysieren
* Usern eine schnelle Einschätzung zu marktbewegenden News liefern

---

## Aktueller Funktionsumfang

Der Bot kann aktuell:

* auf Telegram Commands reagieren
* aktuelle News über die NewsAPI.ai / EventRegistry API abrufen
* News nach Kategorien filtern
* mehrere Keywords pro Kategorie abfragen
* doppelte Artikel anhand der URL entfernen
* Quellenqualität bewerten
* schlechte Quellen blockieren
* Clickbait-Keywords blockieren
* News nach Relevance sortieren
* Sentiment anzeigen
* Relevance Score anzeigen
* Link-Previews in Telegram deaktivieren
* OpenAI zur Analyse eines Top-Artikels verwenden
* eine AI Market Analysis mit Summary, Market Impact und Key Points ausgeben
* während der AI-Verarbeitung eine Status-Nachricht anzeigen
* AI-Antworten robuster verarbeiten und Fehlerfälle abfangen
* Timeouts und Fehler der News-API gezielt behandeln
* verständliche User-Meldungen bei API-Problemen anzeigen
* Fehler mit Python Logging protokollieren
* Unit Tests mit pytest ausführen
* Codequalität mit Ruff prüfen
* Codeformatierung mit Ruff sicherstellen
* Tests, Linting und Formatting automatisch über GitHub Actions prüfen lassen

---

## Telegram Commands

| Command           | Beschreibung                                       |
| ----------------- | -------------------------------------------------- |
| `/start`          | Startet den Bot                                    |
| `/help`           | Zeigt alle verfügbaren Commands                    |
| `/news`           | Zeigt allgemeine Markt-News                        |
| `/news crypto`    | Zeigt Crypto-News                                  |
| `/news macro`     | Zeigt Makro-News                                   |
| `/news stocks`    | Zeigt Aktienmarkt-News                             |
| `/news gold`      | Zeigt Gold-/Dollar-News                            |
| `/news crypto ai` | Analysiert die wichtigste Crypto-News mit AI       |
| `/news macro ai`  | Analysiert die wichtigste Makro-News mit AI        |
| `/news stocks ai` | Analysiert die wichtigste Aktienmarkt-News mit AI  |
| `/news gold ai`   | Analysiert die wichtigste Gold-/Dollar-News mit AI |

---

## Kategorien

Der Bot unterstützt aktuell folgende News-Kategorien:

### Crypto

Keywords:

* bitcoin
* ethereum
* crypto market

### Macro

Keywords:

* federal reserve
* inflation
* interest rates

### Stocks

Keywords:

* stock market
* nasdaq
* earnings

### Gold

Keywords:

* gold price
* safe haven
* dollar yields

---

## News-Filterlogik

Der Bot nutzt mehrere Filter, um die Qualität der News zu verbessern.

Aktuell werden Artikel gefiltert nach:

* blockierten Quellen
* bevorzugten Quellen
* blockierten Keywords
* Relevance Score
* wichtigen Markt-Keywords

Zusätzlich werden mehrere Suchergebnisse zusammengeführt und doppelte Artikel anhand der URL entfernt.

Die News werden anschließend nach Quellenqualität und Relevance Score sortiert.

---

## News API Fehlerbehandlung

Da der Bot auf eine externe News-API zugreift, können gelegentlich Netzwerkfehler, Timeouts oder API-Probleme auftreten.

Dafür wurden eigene Fehlerklassen eingeführt:

```text
NewsAPIError
NewsAPITimeoutError
```

Wenn die News-API nicht rechtzeitig antwortet, erhält der User eine spezifische Meldung:

```text
Die News-API hat nicht rechtzeitig geantwortet. Bitte versuche es gleich nochmal.
```

Wenn die News-API allgemein nicht erreichbar ist oder ein Request fehlschlägt, erhält der User:

```text
Die News-API ist aktuell nicht erreichbar. Bitte versuche es später erneut.
```

Technische Details werden nicht an den User weitergegeben, sondern sauber über Python Logging protokolliert.

Die Fehlerbehandlung der News-API wird zusätzlich mit Unit Tests geprüft. Dabei werden externe API-Calls mit Mocking simuliert, damit die Tests stabil, schnell und unabhängig von EventRegistry laufen.

---

## AI-Analyse

Für den AI-Modus wird nur der relevanteste Artikel einer Kategorie analysiert.

Beispiel:

```text
/news crypto ai
```

Ablauf:

```text
1. Kategorie erkennen
2. News zur Kategorie abrufen
3. Artikel filtern
4. Artikel nach Relevance sortieren
5. Top-Artikel auswählen
6. Artikel an OpenAI übergeben
7. AI-Antwort als strukturierte Analyse ausgeben
```

Die AI-Analyse enthält aktuell:

* Titel
* Quelle
* Relevance Score
* Sentiment
* Summary
* möglichen Market Impact
* Key Points
* Link zum Artikel

Der OpenAI Client wird erst während der Analyse erstellt und nicht bereits beim Import des Moduls. Dadurch bleiben Unit Tests und GitHub Actions unabhängig von einem lokalen OpenAI API Key.

---

## User Experience

Bei AI-Commands dauert die Antwort einige Sekunden, da zuerst News abgerufen und anschließend ein OpenAI API Call ausgeführt wird.

Damit der User direkt Feedback bekommt, sendet der Bot zuerst eine Status-Nachricht:

```text
🤖 AI analysis is running...

Fetching market news and analyzing the top article.
```

Danach wird die Status-Nachricht aktualisiert:

```text
📰 Market news found.

🤖 Running AI analysis...
```

Anschließend wird dieselbe Nachricht durch die finale AI Market Analysis ersetzt.

Dadurch bleibt der Chat sauber und der User sieht jederzeit, dass der Bot arbeitet.

Falls während des AI-Flows ein Fehler auftritt und bereits eine Status-Nachricht existiert, wird diese Status-Nachricht durch eine Fehlermeldung ersetzt, anstatt eine zusätzliche Nachricht zu senden.

---
## Demo Screenshot

![Telegram AI Market News Analysis](assets/telegram-ai-analysis.png)


## Beispiel-Ausgabe

Normale News-Ausgabe:

```text
Top Market News (crypto):

1. Bitcoin slides as investors reassess rate cut expectations
Source: Crypto Briefing
Relevance: 8/10
Sentiment: Bearish
Link: https://example.com/article
```

AI-Ausgabe:

```text
🤖 AI Market News Analysis

📰 Title:
Bitcoin slides as investors reassess rate cut expectations

🏦 Source:
Crypto Briefing

📊 Relevance:
8/10

📈 Sentiment:
Bearish

🧠 Summary:
Bitcoin declined as investors reduced exposure to risk assets.

🌍 Possible Market Impact:
The article may indicate weaker short-term risk appetite, which could pressure crypto and equity markets.

🔑 Key Points:
• Bitcoin moved lower amid broader market weakness
• Risk sentiment remains under pressure
• Traders may watch USD, yields and equity markets

🔗 Link:
https://example.com/article
```

---

## Tech Stack

* Python
* python-telegram-bot
* requests
* python-dotenv
* OpenAI API
* NewsAPI.ai / EventRegistry API
* Telegram Bot API
* pytest
* Ruff
* GitHub Actions
* Git
* GitHub

---

## Projektstruktur

```text
market_news_telegram_bot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── formatters.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── news_service.py
│       └── ai_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_formatters.py
│   ├── test_ai_service.py
│   └── test_news_service.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Installation

Repository klonen:

```bash
git clone https://github.com/StefanMcLoughlin/market_news_telegram_bot.git
cd market_news_telegram_bot
```

Virtuelle Umgebung erstellen:

```bash
python -m venv .venv
```

Virtuelle Umgebung aktivieren:

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Dependencies installieren:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Erstelle eine `.env` Datei im Hauptverzeichnis.

Beispiel:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NEWS_API_KEY=your_news_api_key
NEWS_KEYWORD=bitcoin
NEWS_LANGUAGE=eng
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Die Datei `.env` wird nicht auf GitHub gespeichert.

Als Vorlage dient:

```text
.env.example
```

---

## Bot starten

```bash
python -m app.main
```

Wenn der Bot erfolgreich startet, erscheint im Terminal eine Log-Ausgabe:

```text
app.main - INFO - Bot is running...
```

Danach kann der Bot in Telegram verwendet werden.

---

## Tests

Das Projekt enthält Unit Tests für testbare Funktionen ohne echte externe API-Calls.

Aktuell werden unter anderem getestet:

* Sentiment-Formatierung
* normale News-Formatierung
* AI-Analyse-Formatierung
* Normalisierung von Key Points
* News API Timeout Handling
* News API Request Error Handling
* erfolgreiche Verarbeitung einer simulierten News API Response

Tests lokal ausführen:

```bash
python -m pytest
```

Erwartung:

```text
all tests passed
```

---

## Ruff: Linting & Formatting

Das Projekt nutzt Ruff für Codequalität und Formatierung.

Linting ausführen:

```bash
python -m ruff check .
```

Formatierung prüfen:

```bash
python -m ruff format --check .
```

Code automatisch formatieren:

```bash
python -m ruff format .
```

Automatisch fixbare Ruff-Probleme beheben:

```bash
python -m ruff check . --fix
```

Die Ruff-Konfiguration liegt in:

```text
pyproject.toml
```

---

## GitHub Actions / CI

Das Projekt nutzt GitHub Actions, um Codequalität und Tests automatisch bei jedem Push und Pull Request zu prüfen.

Workflow-Datei:

```text
.github/workflows/tests.yml
```

Der Workflow führt folgende Schritte aus:

```text
1. Repository auschecken
2. Python installieren
3. Dependencies installieren
4. Ruff Lint Check ausführen
5. Ruff Format Check ausführen
6. pytest ausführen
```

Dadurch wird automatisch geprüft, ob neue Änderungen bestehende Tests brechen oder gegen die Codequalitätsregeln verstoßen.

---

## Logging

Das Projekt nutzt Python Logging statt einfacher `print()` Ausgaben.

Aktuell werden unter anderem geloggt:

* Bot-Start
* Fehler im Telegram Handler
* OpenAI-Fehler
* JSON Parsing Probleme bei AI-Antworten
* News-API Timeouts
* News-API Request-Fehler

Zusätzlich wurden laute Drittanbieter-Logs reduziert, damit das Terminal übersichtlich bleibt.

---

## Bisherige Lerninhalte in diesem Projekt

In diesem Projekt wurden folgende Themen praktisch umgesetzt:

* professionelle Python-Projektstruktur
* virtuelle Umgebung
* Environment Variables
* Telegram Bot Commands
* externe API-Anbindung
* API Response Verarbeitung
* Service Layer
* eigene Exceptions
* News-Filterlogik
* Sortierung nach Relevance
* Duplikat-Entfernung
* Source Quality Bewertung
* AI-ready Datenstruktur
* OpenAI API Integration
* Prompt Engineering für strukturierte JSON-Antworten
* JSON Parsing
* Fehlerbehandlung für externe API Calls
* Timeout Handling
* User Experience durch Status Messages
* Telegram Message Formatting
* Refactoring in Formatter-Modul
* Python Logging
* Unit Tests mit pytest
* Mocking externer API-Calls in Tests
* Ruff Linting & Formatting
* GitHub Actions CI Workflow
* Git & GitHub Workflow mit sinnvollen Commits

---

## Roadmap

Mögliche nächste Schritte:

* finaler Portfolio-Review
* kompaktere AI-Ausgabe bei langen Antworten
* Mock-Tests für OpenAI API Calls
* Kategorien aus dem Handler auslagern
* optional: mehrere Top-News analysieren
* optional: automatische News-Updates per Scheduler
* optional: Datenbank zur Speicherung relevanter News
* optional: Docker
* optional: Deployment
* optional: Dashboard

---

## Status

Aktueller Status:

```text
MVP v1 abgeschlossen
```

Der Bot ist lokal lauffähig und kann echte Markt-News abrufen, filtern und in Telegram ausgeben.

Die OpenAI-Anbindung funktioniert und kann die wichtigste News einer Kategorie analysieren.

Lokale Tests, Ruff Checks und GitHub Actions laufen erfolgreich.

Externe API-Fehler wie Timeouts werden gezielt behandelt und für User verständlich ausgegeben.
