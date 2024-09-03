from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def set_active_personality(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 3)[3]
    user_id = update.effective_user.id

    await db.set_active_personality(user_id, name)
    await query.message.reply_text(f"*The active personality has been changed to* '{name}'.",
                                   parse_mode=ParseMode.MARKDOWN)


def register_set_active_personality_handler(application):
    application.add_handler(CallbackQueryHandler(set_active_personality, pattern="^set_active_personality_"))
