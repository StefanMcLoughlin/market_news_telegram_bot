import logging
import json

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL


logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

def build_article_analysis_prompt(article: dict) -> str:
    title = article.get("title") or ""
    source = article.get("source") or ""
    sentiment = article.get("sentiment")
    relevance = article.get("relevance")
    url = article.get("url") or ""

    return f"""
You are a financial market news analyst.

Analyze the following market news article for a trader/investor.

Return ONLY valid JSON with this exact structure:
{{
    "summary": "short summary in 1-2 sentences",
    "market_impact": "short explanation of the possible market impact",
    "key_points": ["point 1", "point 2", "point 3"]
}}

Article:
Title: {title}
Source: {source}
Sentiment score: {sentiment}
Relevance score: {relevance}
URL: {url}

Rules:
- Be concise.
- Do not give financial advice.
- Focus on possible impact on crypto, stocks, gold, USD, bonds or risk sentiment.
- If the article is not market relevant, say that in market_impact.
"""


def normalize_key_points(key_points) -> list[str]:
    if not isinstance(key_points, list):
        return []
    
    return [str(point) for point in key_points if point]


def analyze_article(article: dict) -> dict:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Please check your .env file.")
    
    prompt = build_article_analysis_prompt(article)

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            temperature=0.2,
        )

        content = response.output_text

        if not content:
            raise ValueError("OpenAI response was empty.")

        analysis = json.loads(content)

    except json.JSONDecodeError:
        logger.warning("OpenAI response could not be parsed as JSON")
        analysis = {
            "summary": "The AI response could not be parsed correctly.",
            "market_impact": "Market impact analysis is currently unavailable.",
            "key_points": [],
        }

    except Exception:
        logger.exception("Error while analyzing article with OpenAI")
    
        analysis = {
            "summary": "AI analysis is currently unavailable.",
            "market_impact": "The article could not be analyzed at this time.",
            "key_points": [],
        }

    return {
        **article,
        "summary": analysis.get("summary") or "No summary available",
        "market_impact": analysis.get("market_impact") or "No market impact available",
        "key_points": normalize_key_points(analysis.get("key_points")),
    }