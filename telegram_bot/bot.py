# telegram_bot/bot.py

import logging
from telegram.ext import Application
from config import BOT_TOKEN
from handlers import register_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    application = Application.builder().token(BOT_TOKEN).concurrent_updates(True).build()
    register_handlers(application)
    application.run_polling()


if __name__ == "__main__":
    main()
