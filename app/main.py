import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from app.config import TELEGRAM_BOT_TOKEN
from app.bot.handlers import start_command, help_command, news_command


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing. Please check your .env file")
    
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", news_command))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()