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
        await query.message.reply_text("Вы не можете удалить эту личность.")
        return

    keyboard = [[InlineKeyboardButton("Да", callback_data=f"confirm_delete_personality_{name}")],
                [InlineKeyboardButton("Нет", callback_data=f"cancel_delete_personality_{name}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"Вы уверены, что хотите удалить личность '{name}'?", reply_markup=reply_markup)


async def confirm_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 3)[3]
    user_id = update.effective_user.id

    await db.delete_personality(user_id, name)
    await query.message.reply_text(f"Личность '{name}' была удалена.")


async def cancel_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.message.reply_text("Удаление личности отменено.")


def register_delete_personality(application):
    application.add_handler(CallbackQueryHandler(delete_personality, pattern="^delete_personality_"))
    application.add_handler(CallbackQueryHandler(confirm_delete, pattern="^confirm_delete_personality_"))
    application.add_handler(CallbackQueryHandler(cancel_delete, pattern="^cancel_delete_personality_"))
