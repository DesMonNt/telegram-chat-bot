# telegram_bot/handlers/start.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


async def start(update: Update, context: CallbackContext):
    welcome_message = (
         "👋 Hello! Welcome to our chat bot. I can help you create and manage various personalities and bots. Here’s what you can do:\n\n"
        "🔹 **Create and customize personalities** — set names and descriptions for different personalities that will be used in chats.\n"
        "🔹 **Create and customize bots** — set up bots with unique scenarios and initial messages to interact with.\n\n"
        "To get started, select a bot to chat with and we'll begin. If you'd like to create or customize a personality or bot, use the corresponding commands.\n\n"
    )
    await update.message.reply_text(welcome_message)


def register_start_handler(application):
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
