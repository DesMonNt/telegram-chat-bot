from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def get_active_personality(update: Update, context: CallbackContext):
    await db.init_db()

    user_id = update.effective_user.id
    active_personality = await db.get_active_personality(user_id)

    if active_personality:
        await update.message.reply_text(f"Ваша активная личность: {active_personality}")
    else:
        await update.message.reply_text("Активная личность не установлена.")


def register_get_active_personality_handler(application):
    application.add_handler(CommandHandler("active_persona", get_active_personality))
