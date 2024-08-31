# telegram_bot/handlers/start.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я твой бот. Чем могу помочь?")


def register_start_handler(application):
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
