import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_KEYWORD = os.getenv("NEWS_KEYWORD", "bitcoin")
NEWS_LANGUAGE = os.getenv("NEWS_LANGUAGE", "eng")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")