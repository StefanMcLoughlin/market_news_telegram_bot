from telegram import Update
from telegram.ext import ContextTypes
from app.services.news_service import fetch_top_headlines


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

            message += (
                f"{index}. {title}\n"
                f"Source: {source}\n"
                f"Link: {url}\n\n"
            )

        await update.message.reply_text(message)

    except Exception as error:
        print(f"Error while fetching news: {error}")
        await update.message.reply_text(
            "Beim Laden der News ist ein Fehler aufgetreten. Bitte versuche es später erneut."
        )