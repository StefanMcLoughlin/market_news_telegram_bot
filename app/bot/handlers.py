from telegram import Update
from telegram.ext import ContextTypes
from app.services.news_service import fetch_top_headlines


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
        "/news - Zeigt aktuelle Markt-News."
    )

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        articles = fetch_top_headlines(limit=10)
        if not articles:
            await update.message.reply_text(
                "Aktuell wurden keine passenden Markt-News gefunden."
        )
            return
    
        message = "Top Market News:\n\n"

        for index, article in enumerate(articles[:5], start=1):
            title = article.get("title") or "No title"
            source = article.get("source") or "Unknown source"
            url = article.get("url") or "No URL"
            relevance = article.get("relevance")
            sentiment = format_sentiment(article.get("sentiment"))

            relevance_text = f"{relevance}/10" if relevance is not None else "Unknown"

            message += (
                f"{index}. {title}\n"
                f"Source: {source}\n"
                f"Relevance: {relevance_text}\n"
                f"Sentiment: {sentiment}\n"
                f"Link: {url}\n\n"
            )

        await update.message.reply_text(message)

    except Exception as error:
        print(f"Error while fetching news: {error}")
        await update.message.reply_text(
            "Beim Laden der News ist ein Fehler aufgetreten. Bitte versuche es später erneut."
        )