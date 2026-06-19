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

def format_news_list(articles: list[dict], category: str) -> str:
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
        
    return message