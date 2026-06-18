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
]

MIN_RELEVANCE = 5

def get_article_text(article: dict) -> str:
    title = article.get("title") or ""
    body = article.get("body") or ""
    source = article.get("source", {}).get("title") or ""

    return f"{title} {body} {source}".lower()

def is_relevant_article(article: dict) -> bool:
    article_text = get_article_text(article)

    has_blocked_keyword = any(
        keyword in article_text for keyword in BLOCKED_KEYWORDS
    )
    if has_blocked_keyword:
        return False
    
    relevance = article.get("relevance")

    if relevance is not None and relevance < MIN_RELEVANCE:
        return False
    
    has_important_keyword = any(
        keyword in article_text for keyword in IMPORTANT_KEYWORDS
    )

    return has_important_keyword

def filter_articles(articles: list[dict]) -> list[dict]:
    return[article for article in articles if is_relevant_article(article)]


def fetch_top_headlines(limit: int = 5):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is missing. Please check your .env file.")
    
    payload = {
        "action": "getArticles",
        "apiKey": NEWS_API_KEY,
        "keyword": NEWS_KEYWORD,
        "lang": NEWS_LANGUAGE,
        "articlesPage": 1,
        "articlesCount": limit,
        "articlesSortBy": "date",
        "articlesSortByAsc": False,
        "resultType": "articles",
        "dataType": ["news"],
        "forceMaxDataTimeWindow": 31,
    }

    response = requests.post(NEWS_API_URL, json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    articles = data.get("articles", {}).get("results", [])
    filtered_articles = filter_articles(articles)
    filtered_articles.sort(
        key=lambda article: article.get("relevance") or 0, reverse=True,
    )

    cleaned_articles = []

    for article in filtered_articles:
        cleaned_articles.append(
            {
            "title": article.get("title"),
            "source": article.get("source", {}).get("title"),
            "url": article.get("url"),
            "published_at": article.get("dateTime"),
            "sentiment": article.get("sentiment"),
            "relevance": article.get("relevance"),
            }
        )
    return cleaned_articles