from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def set_active_personality(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 2)[-1]
    user_id = update.effective_user.id

    await db.set_active_personality(user_id, name)
    await query.message.reply_text(f"Активная личность изменена на '{name}'.")


def register_set_active_personality(application):
    application.add_handler(CommandHandler("set_active_personality", set_active_personality))
