import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_COUNTRY = os.getenv("NEWS COUNTRY", "us")
NEWS_CATEGORY = os.getenv("NEWS_CATEGORY", "business")