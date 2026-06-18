from telegram import Update
from telegram.ext import ContextTypes
from app.services.news_service import fetch_top_headlines


NEWS_CATEGORIES = {
    "crypto": "bitcoin",
    "macro": "federal reserve",
    "stocks": "stock market",
    "gold": "gold",
}


def get_news_category(context: ContextTypes.DEFAULT_TYPE) -> tuple[str, str | None]:
    if not context.args:
        return "general", None
    
    category = context.args[0].lower()

    if category not in NEWS_CATEGORIES:
        return "unknown", None
    
    return category, NEWS_CATEGORIES[category]


def format_sentiment(sentiment: float | None) -> str:
    if sentiment is None:
        return "Unknown"
    
    if sentiment > 0.1:
        return "Bullish"
    
    if sentiment < -0.1:
        return "Bearish"
    
    return "Neutral"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Willkommen beim Market News Bot\n\n"
        "Nutze /news, um aktuelle Market-News abzurufen.\n"
        "Nutze /help, um alle verfügbaren Commands zu sehen."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Verfügbare Commands:\n\n"
        "/start - Startet den Bot.\n"
        "/help - Zeigt diese Hilfe.\n"
        "/news - Zeigt allgemeine Markt-News.\n"
        "/news crypto - Zeigt Crypto-News.\n"
        "/news macro - Zeigt Makro-News.\n"
        "/news stocks - Zeigt Aktienmarkt-News.\n"
        "/news gold - Zeigt Gold-/Dollar-News."
    )


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        category, keyword = get_news_category(context)

        if category == "unknown":
            await update.message.reply_text(
                "Unbekannte Kategorie.\n\n"
                "Verfügbare Kategorien:\n"
                "/news crypto\n"
                "/news macro\n"
                "/news stocks\n"
                "/news gold"
            )
            return
        
        articles = fetch_top_headlines(limit=50, keyword=keyword)
        if not articles:
            await update.message.reply_text(
                "Aktuell wurden keine passenden Markt-News gefunden."
            )
            return
    
        message = f"Top Market News ({category}):\n\n"

        for index, article in enumerate(articles[:5], start=1):
            title = article.get("title") or "No title"
            source = article.get("source") or "Unknown source"
            url = article.get("url") or "No URL"
            relevance = article.get("relevance")
            sentiment = format_sentiment(article.get("sentiment"))

            if relevance is not None:
                display_relevance = min(relevance, 10)
                relevance_text = f"{display_relevance}/10"
            else:
                relevance_text = "Unknown"

            message += (
                f"{index}. {title}\n"
                f"Source: {source}\n"
                f"Relevance: {relevance_text}\n"
                f"Sentiment: {sentiment}\n"
                f"Link: {url}\n\n"
            )

        await update.message.reply_text(message, disable_web_page_preview=True)

    except Exception as error:
        print(f"Error while fetching news: {error}")
        await update.message.reply_text(
            "Beim Laden der News ist ein Fehler aufgetreten. Bitte versuche es später erneut."
        )