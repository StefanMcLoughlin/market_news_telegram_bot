# Market News Telegram Bot

Ein Python-basierter Telegram Bot, der aktuelle marktbezogene News abruft, filtert, nach Relevanz sortiert und direkt in Telegram ausgibt.

Zusätzlich kann der Bot die wichtigste News einer Kategorie mit OpenAI analysieren und eine kurze AI Market Analysis mit Summary, möglichem Market Impact und Key Points ausgeben.

Das Projekt wurde im Rahmen meiner AI-/Backend-Ausbildung gebaut, um praktische Erfahrung mit APIs, Telegram Bots, externer Datenverarbeitung, AI-Integration, Projektstruktur und GitHub-Workflow zu sammeln.

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

---

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
│   │   └── handlers.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── news_service.py
│       └── ai_service.py
│
├── .env.example
├── .gitignore
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

Wenn der Bot erfolgreich startet, erscheint im Terminal:

```text
Bot is running...
```

Danach kann der Bot in Telegram verwendet werden.

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
* News-Filterlogik
* Sortierung nach Relevance
* Duplikat-Entfernung
* Source Quality Bewertung
* AI-ready Datenstruktur
* OpenAI API Integration
* Prompt Engineering für strukturierte JSON-Antworten
* JSON Parsing
* Fehlerbehandlung für externe API Calls
* User Experience durch Status Messages
* Telegram Message Formatting
* Git & GitHub Workflow mit sinnvollen Commits

---

## Roadmap

Geplante nächste Schritte:

* Logging statt `print`
* Refactoring der Formatter-Logik
* Tests mit pytest
* bessere Fehlerbehandlung im Telegram Handler
* kompaktere AI-Ausgabe bei langen Antworten
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
MVP in Entwicklung
```

Der Bot ist lokal lauffähig und kann echte Markt-News abrufen, filtern und in Telegram ausgeben.

Die OpenAI-Anbindung funktioniert und kann die wichtigste News einer Kategorie analysieren.
