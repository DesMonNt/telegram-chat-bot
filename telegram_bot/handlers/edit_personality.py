from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def edit_personality(update: Update, context: CallbackContext):
    await db.init_db()

    query = update.callback_query
    name = query.data.split("_", 1)[-1]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)

    if not any(n == name for n, _ in personalities):
        await query.message.reply_text("Вы не можете редактировать эту личность.")
        return

    await query.message.reply_text(f"Введите новое описание для личности '{name}':")
    context.user_data['edit_personality'] = name
    context.user_data['edit_user_id'] = user_id


async def handle_edit_description(update: Update, context: CallbackContext):
    if 'edit_personality' not in context.user_data or 'edit_user_id' not in context.user_data:
        return

    name = context.user_data['edit_personality']
    new_description = update.message.text
    user_id = context.user_data['edit_user_id']

    await db.update_personality(user_id, name, new_description)
    await update.message.reply_text(f"Описание для личности '{name}' обновлено.")

    del context.user_data['edit_personality']
    del context.user_data['edit_user_id']


def register_edit_personality(application):
    application.add_handler(CallbackQueryHandler(edit_personality, pattern="^edit_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_description))
