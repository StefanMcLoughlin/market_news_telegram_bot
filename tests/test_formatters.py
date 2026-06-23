from app.bot.formatters import format_ai_article, format_news_list, format_sentiment


def test_format_sentiment_returns_unknown_for_none():
    result = format_sentiment(None)

    assert result == "Unknown"


def test_format_sentiment_returns_bullish_for_positive_value():
    result = format_sentiment(0.2)

    assert result == "Bullish"


def test_format_sentiment_returns_bearish_for_negative_value():
    result = format_sentiment(-0.2)

    assert result == "Bearish"


def test_format_sentiment_returns_neutral_for_small_value():
    result = format_sentiment(0.05)

    assert result == "Neutral"


def test_format_news_list_contains_article_data():
    articles = [
        {
            "title": "Bitcoin rises after Fed decision",
            "source": "Reuters",
            "url": "https://example.com/bitcoin",
            "relevance": 8,
            "sentiment": 0.3,
        }
    ]

    result = format_news_list(articles, "crypto")

    assert "Top Market News (crypto)" in result
    assert "Bitcoin rises after Fed decision" in result
    assert "Reuters" in result
    assert "8/10" in result
    assert "Bullish" in result
    assert "https://example.com/bitcoin" in result


def test_format_ai_article_contains_analysis_data():
    article = {
        "title": "Gold rises as dollar weakens",
        "source": "MarketWatch",
        "url": "https://example.com/gold",
        "relevance": 7,
        "sentiment": 0.1,
        "summary": "Gold moved higher as the dollar weakened",
        "market_impact": "This could support save-haven demand",
        "key_points": [
            "Gold moved higher",
            "Dollar weakened",
            "Safe-haven demand increased",
        ],
    }

    result = format_ai_article(article)

    assert "🤖 AI Market News Analysis" in result
    assert "Gold rises as dollar weakens" in result
    assert "MarketWatch" in result
    assert "7/10" in result
    assert "Neutral" in result
    assert "Gold moved higher as the dollar weakened" in result
    assert "This could support save-haven demand" in result
    assert "• Gold moved higher" in result
    assert "https://example.com/gold" in result
