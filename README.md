# Market News Telegram Bot

Ein Python-basierter Telegram Bot, der aktuelle marktbezogene News abruft, filtert, nach Relevanz sortiert und direkt in Telegram ausgibt.

Das Projekt wurde im Rahmen meiner AI-/Backend-Ausbildung gebaut, um praktische Erfahrung mit APIs, Telegram Bots, Projektstruktur, externer Datenverarbeitung und AI-gestützter Analyse zu sammeln.

---

## Ziel des Projekts

Ziel ist es, einen Telegram Bot zu entwickeln, der relevante Markt-News aus verschiedenen Bereichen sammelt und übersichtlich ausgibt.

Der Bot soll langfristig ähnlich wie ein kleiner Market-News-Assistent funktionieren:

* aktuelle News abrufen
* unrelevante Quellen und Clickbait filtern
* News nach Kategorien ausgeben
* Relevance und Sentiment anzeigen
* wichtige News mit AI zusammenfassen
* mögliche Markt-Auswirkungen analysieren

---

## Aktueller Funktionsumfang

Der Bot kann aktuell:

* auf Telegram Commands reagieren
* aktuelle News über die NewsAPI.ai / EventRegistry API abrufen
* News nach Kategorien filtern
* mehrere Keywords pro Kategorie abfragen
* doppelte Artikel entfernen
* Quellenqualität bewerten
* schlechte Quellen blockieren
* Clickbait-Keywords blockieren
* News nach Relevance sortieren
* Sentiment anzeigen
* Relevance Score anzeigen
* Link-Previews in Telegram deaktivieren
* einen AI-Analyse-Modus als Placeholder ausgeben

---

## Telegram Commands

| Command           | Beschreibung                                             |
| ----------------- | -------------------------------------------------------- |
| `/start`          | Startet den Bot                                          |
| `/help`           | Zeigt alle verfügbaren Commands                          |
| `/news`           | Zeigt allgemeine Markt-News                              |
| `/news crypto`    | Zeigt Crypto-News                                        |
| `/news macro`     | Zeigt Makro-News                                         |
| `/news stocks`    | Zeigt Aktienmarkt-News                                   |
| `/news gold`      | Zeigt Gold-/Dollar-News                                  |
| `/news crypto ai` | Analysiert die wichtigste Crypto-News mit AI-Placeholder |

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

## Filterlogik

Der Bot nutzt mehrere Filter, um die Qualität der News zu verbessern.

Aktuell werden Artikel gefiltert nach:

* blockierten Quellen
* bevorzugten Quellen
* blockierten Keywords
* Relevance Score
* wichtigen Markt-Keywords

Zusätzlich werden mehrere Suchergebnisse zusammengeführt und doppelte Artikel anhand der URL entfernt.

---

## Beispiel-Ausgabe

```text
Top Market News (crypto):

1. Bitcoin slides as investors reassess rate cut expectations
Source: Crypto Briefing
Relevance: 8/10
Sentiment: Bearish
Link: https://example.com/article
```

AI-Modus:

```text
AI Market News Analysis:

Title: Bitcoin slides as investors reassess rate cut expectations
Source: Crypto Briefing
Relevance: 8/10
Sentiment: Bearish

Summary:
AI summary placeholder

Market Impact:
Market impact placeholder

Link: https://example.com/article
```

---

## Tech Stack

* Python
* python-telegram-bot
* requests
* python-dotenv
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

* professionelle Projektstruktur
* virtuelle Umgebung
* Environment Variables
* Telegram Bot Commands
* externe API-Anbindung
* API Response Verarbeitung
* Service Layer
* Filterlogik
* Sortierung nach Relevance
* Duplikat-Entfernung
* einfache Source Quality Bewertung
* AI-ready Datenstruktur
* AI-Service Placeholder
* Git & GitHub Workflow mit sinnvollen Commits

---

## Roadmap

Geplante nächste Schritte:

* echte OpenAI-Anbindung
* AI-Zusammenfassung pro Artikel
* AI Market Impact Analyse
* bessere Kategorie-Logik
* Logging statt `print`
* Tests mit pytest
* Docker
* Deployment
* Scheduler für automatische News-Updates
* Datenbank zur Speicherung relevanter News
* optionales Dashboard

---

## Status

Aktueller Status:

```text
MVP in Entwicklung
```

Der Bot ist lokal lauffähig und kann bereits echte Markt-News abrufen, filtern und in Telegram ausgeben.

Die AI-Analyse ist vorbereitet, nutzt aktuell aber noch einen Placeholder.
