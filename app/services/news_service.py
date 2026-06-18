import requests
from app.config import NEWS_API_KEY, NEWS_KEYWORD, NEWS_LANGUAGE

NEWS_API_URL = "https://eventregistry.org/api/v1/article/getArticles"

def fetch_top_headlines(limit: int = 5):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is missing. Please check your .env file.")
    
    payload = {
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

    cleaned_articles = []

    for article in articles:
        cleaned_articles.append(
            {
            "title": article.get("title"),
            "source": article.get("source", {}).get("title"),
            "url": article.get("url"),
            "published_at": article.get("dateTime"),
            }
        )
    return cleaned_articles