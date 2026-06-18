import requests
from app.config import NEWS_API_KEY, NEWS_KEYWORD, NEWS_LANGUAGE

NEWS_API_URL = "https://eventregistry.org/api/v1/article/getArticles"

IMPORTANT_KEYWORDS = [
    "fed",
    "federal reserve",
    "fomc",
    "interest rate",
    "interest rates",
    "inflation",
    "cpi",
    "ppi",
    "jobs report",
    "unemployment",
    "recession",
    "gdp",
    "treasury",
    "bond",
    "yield",
    "yields",
    "dollar",
    "usd",
    "gold",
    "oil",
    "bitcoin",
    "btc",
    "ethereum",
    "crypto",
    "stocks",
    "nasdaq",
    "s&p 500",
    "dow",
    "earnings",
    "tariff",
    "geopolitical",
    "war",
]

BLOCKED_KEYWORDS = [
    "presale",
    "crypto presale",
    "airdrop",
    "giveaway",
    "sponsored",
    "promotion",
    "promo",
    "bonus",
    "casino",
    "betting",
    "lottery",
    "meme coin",
    "memecoin",
    "price prediction",
    "price forecast",
    "best crypto to buy",
    "next 100x",
    "100x",
    "1000x",
    "moon",
    "altcoin gem",
    "hidden gem",
    "buy now",
    "top crypto",
    "token sale",
    "ico",
    "ido",
    "penny stock",
    "stock to buy",
    "stocks to buy",
    "millionaire",
    "dangerous assumption",
]

PREFERRED_SOURCES = [
    "Reuters",
    "Bloomberg",
    "CNBC",
    "MarketWatch",
    "Financial Times",
    "The Wall Street Journal",
    "Investing.com",
    "Yahoo Finance",
    "CoinDesk",
    "Crypto Briefing",
    "The Block",
    "Decrypt",
    "CNN",
]

BLOCKED_SOURCES = [
    "Paperblog",
    "Coinpedia",
    "CoinGape",
    "The Cryptonomist",
    "Pluang",
    "Coindoo",
    "U.Today",
    "CryptoPotato",
    "BeInCrypto",
    "Watcher Guru",
    "Bitcoinist",
    "Seeking Alpha",
    "NDTV Gadgets 360",
]

MIN_RELEVANCE_PREFERRED_SOURCE = 4
MIN_RELEVANCE_UNKNOWN_SOURCE = 6


def get_article_text(article: dict) -> str:
    title = article.get("title") or ""
    body = article.get("body") or ""
    source = article.get("source", {}).get("title") or ""

    return f"{title} {body} {source}".lower()


def get_article_source(article: dict) -> str:
    return article.get("source", {}).get("title") or ""


def is_blocked_source(article: dict) -> bool:
    source = get_article_source(article).lower()

    return any(
        blocked_source.lower() in source for blocked_source in BLOCKED_SOURCES
    )


def is_preferred_source(article: dict) -> bool:
    source = get_article_source(article).lower()

    return any(
        preferred_source.lower() in source for preferred_source in PREFERRED_SOURCES
    )


def is_relevant_article(article: dict) -> bool:
    if is_blocked_source(article):
        return False
    
    article_text = get_article_text(article)

    has_blocked_keyword = any(
        keyword in article_text for keyword in BLOCKED_KEYWORDS
    )
    if has_blocked_keyword:
        return False
    
    relevance = article.get("relevance") or 0

    if is_preferred_source(article):
        if relevance < MIN_RELEVANCE_PREFERRED_SOURCE:
            return False
    else:
        if relevance < MIN_RELEVANCE_UNKNOWN_SOURCE:
            return False
    
    has_important_keyword = any(
        keyword in article_text for keyword in IMPORTANT_KEYWORDS
    )

    return has_important_keyword


def filter_articles(articles: list[dict]) -> list[dict]:
    return [article for article in articles if is_relevant_article(article)]


def fetch_top_headlines(limit: int = 5, keyword: str |None = None):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is missing. Please check your .env file.")
    
    search_keyword = keyword or NEWS_KEYWORD
    
    payload = {
        "action": "getArticles",
        "apiKey": NEWS_API_KEY,
        "keyword": search_keyword,
        "lang": NEWS_LANGUAGE,
        "articlesPage": 1,
        "articlesCount": limit,
        "articlesSortBy": "date",
        "articlesSortByAsc": False,
        "resultType": "articles",
        "dataType": ["news"],
       # "forceMaxDataTimeWindow": 31,
    }

    response = requests.post(NEWS_API_URL, json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    articles = data.get("articles", {}).get("results", [])
    filtered_articles = filter_articles(articles)
    filtered_articles.sort(
        key=lambda article: (is_preferred_source(article), article.get("relevance") or 0,), reverse=True,
    )

    cleaned_articles = []

    for article in filtered_articles:
        cleaned_articles.append(
            {
            "title": article.get("title"),
            "source": get_article_source(article),
            "url": article.get("url"),
            "published_at": article.get("dateTime"),
            "sentiment": article.get("sentiment"),
            "relevance": article.get("relevance"),
            "is_preferred_source": is_preferred_source(article),
            }
        )
    return cleaned_articles