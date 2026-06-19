from telegram import Update
from telegram.ext import ContextTypes
from app.services.news_service import fetch_top_headlines, fetch_news_by_keywords
from app.services.ai_service import analyze_article


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


def format_sentiment(sentiment: float | None) -> str:
    if sentiment is None:
        return "Unknown"
    
    if sentiment > 0.1:
        return "Bullish"
    
    if sentiment < -0.1:
        return "Bearish"
    
    return "Neutral"


def format_ai_article(article: dict) -> str:
    title = article.get("title") or "No title"
    source = article.get("source") or "Unknown source"
    url = article.get("url") or "No URL"
    relevance = article.get("relevance")
    sentiment = format_sentiment(article.get("sentiment"))
    summary = article.get("summary") or "No summary available"
    market_impact = article.get("market_impact") or "No market impact available"
    key_points = article.get("key_points") or []

    relevance_text = f"{min(relevance, 10)}/10" if relevance is not None else "Unknown"

    message = (
        "🤖 AI Market News Analysis\n\n"
        "📰 Title:\n"
        f"{title}\n\n"
        "🏦 Source:\n"
        f"{source}\n\n"
        "📊 Relevance:\n"
        f"{relevance_text}\n\n"
        "📈 Sentiment:\n"
        f"{sentiment}\n\n"
        "🧠 Summary:\n"
        f"{summary}\n\n"
        "🌍 Possible Market Impact:\n"
        f"{market_impact}\n\n"
    )

    if key_points:
        message += "🔑 Key Points:\n"
        for point in key_points:
            message += f"• {point}\n"

        message += "\n"

    message += (
        "🔗 Link:\n"
        f"{url}"
    )

    return message


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


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        status_message = None

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