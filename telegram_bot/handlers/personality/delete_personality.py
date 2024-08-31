from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def delete_personality(update: Update, context: CallbackContext):
    await db.init_db()

    query = update.callback_query
    name = query.data.split("_", 2)[2]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)

    if not any(n == name for n, _ in personalities):
        await query.message.reply_text("You cannot delete this personality.")
        return

    keyboard = [[InlineKeyboardButton("Yes", callback_data=f"confirm_delete_personality_{name}")],
                [InlineKeyboardButton("No", callback_data=f"cancel_delete_personality_{name}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"Are you sure you want to delete the personality '{name}'?", reply_markup=reply_markup)


async def confirm_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 3)[3]
    user_id = update.effective_user.id

    await db.delete_personality(user_id, name)
    await query.message.reply_text(f"Personality '{name}' it was deleted.")


async def cancel_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.message.reply_text("The deletion of the personality has been canceled.")


def register_delete_personality(application):
    application.add_handler(CallbackQueryHandler(delete_personality, pattern="^delete_personality_"))
    application.add_handler(CallbackQueryHandler(confirm_delete, pattern="^confirm_delete_personality_"))
    application.add_handler(CallbackQueryHandler(cancel_delete, pattern="^cancel_delete_personality_"))
