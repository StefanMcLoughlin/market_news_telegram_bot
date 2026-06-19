import json
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL

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
    "market_impact": "short explanation of the possible market impact"
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
- Do not give financial advice
- Focus on possible impact on crypto, stocks, gold, USD, bonds or risk sentiment
- If the article is not market relevant, sat that in market_impact
"""


def analyze_article(article: dict) -> dict:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing, Please check your .env file.")
    
    prompt = build_article_analysis_prompt(article)

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0.2,
    )

    content = response.output_text

    try:
        analysis = json.loads(content)
    except json.JSONDecodeError:
        analysis = {
            "summary": content,
            "market_impact": "Could not parse structured market impact",
            "key points": [],
        }

    return {
        **article,
        "summary": analysis.get("summary"),
        "market_impact": analysis.get("market_impact"),
        "key_points": analysis.get("key_points", []),
    }