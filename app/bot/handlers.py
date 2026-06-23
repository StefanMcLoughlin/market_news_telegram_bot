import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.services.news_service import (
    NewsAPIError,
    NewsAPITimeoutError,
    fetch_top_headlines,
    fetch_news_by_keywords,
)
from app.services.ai_service import analyze_article
from app.bot.formatters import format_ai_article, format_news_list


logger = logging.getLogger(__name__)


NEWS_CATEGORIES = {
    "crypto": ["bitcoin", "ethereum", "crypto market"],
    "macro": ["federal reserve", "inflation", "interest rates"],
    "stocks": ["stock market", "nasdaq", "earnings"],
    "gold": ["gold price", "safe haven", "dollar yields"],
}


def get_news_category(context: ContextTypes.DEFAULT_TYPE) -> tuple[str, list[str] | None]:
    if not context.args:
        return "general", None
    
    category = context.args[0].lower()

    if category not in NEWS_CATEGORIES:
        return "unknown", None
    
    return category, NEWS_CATEGORIES[category]


def should_use_ai(context: ContextTypes.DEFAULT_TYPE) -> bool:
    return len(context.args) > 1 and context.args[1].lower() == "ai"


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
        "/news gold - Zeigt Gold-/Dollar-News.\n"
        "/news crypto ai - Analysiert die wichtigste Crypto-News mit AI.\n"
        "/news macro ai - Analysiert die wichtigste Makro-News mit AI.\n"
        "/news stocks ai - Analysiert die wichtigste Aktienmarkt-News mit AI.\n"
        "/news gold ai - Analysiert die wichtigste Gold-/Dollar-News mit AI."
    )


async def send_or_edit_error_message(
        update: Update,
        status_message,
        error_message = (
            "Beim Laden der News ist ein Fehler aufgetreten. "
            "Bitte versuch es später erneut."
        ),
    ) -> None:
        if status_message is not None:
            await status_message.edit_text(error_message)
        else:
            await update.message.reply_text(error_message)


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = None

    try:
        category, keywords = get_news_category(context)

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
        
        is_ai_mode = should_use_ai(context)

        if is_ai_mode:
            status_message = await update.message.reply_text(
                "🤖 AI analysis is running...\n\n"
                "Fetching market news and analyzing the top article."
            )
        
        if keywords is None:
            articles = fetch_top_headlines(limit=50)
        else:
            articles = fetch_news_by_keywords(
                keywords=keywords,
                limit_per_keyword=50,
            )
        if not articles:
            no_articles_message = "Aktuell wurden keine passenden Markt-News gefunden."

            if status_message is not None:
                await status_message.edit_text(no_articles_message)
            else:
                await update.message.reply_text(no_articles_message)

            return
        
        if is_ai_mode:
            await status_message.edit_text(
                "📰 Market news found.\n\n"
                "🤖 Running AI analysis..."
            )

            analyzed_article = analyze_article(articles[0])
            message = format_ai_article(analyzed_article)

            await status_message.edit_text(
                message,
                disable_web_page_preview=True,
            )
            return
        
        message = format_news_list(articles, category)
        await update.message.reply_text(message, disable_web_page_preview=True)

    except NewsAPITimeoutError:
        logger.warning("News command failed because News API timed out")
        await send_or_edit_error_message(
            update,
            status_message,
            "Die News-API hat nicht rechtzeitig geantwortet. Bitte versuche es gleich nochmal.",
    )

    except NewsAPIError:
        logger.exception("News command failed because News API request failed")
        await send_or_edit_error_message(
            update,
            status_message,
            "Die News-API ist aktuell nicht erreichbar. Bitte versuche es später erneut.",
    )

    except Exception:
        logger.exception("Error while handling news command")
        await send_or_edit_error_message(update, status_message)