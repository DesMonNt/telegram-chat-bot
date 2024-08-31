from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from .edit_personality import edit_personality
from .delete_personality import delete_personality, confirm_delete, cancel_delete
from .set_active_personality import set_active_personality
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def list_personalities(update: Update, context: CallbackContext):
    await db.init_db()

    user_id = update.effective_user.id
    personalities = await db.get_personalities(user_id)

    if not personalities:
        await update.message.reply_text("Нет сохраненных личностей.")
        return

    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)]
        for name, _ in personalities
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите личность:", reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data
    user_id = update.effective_user.id

    if name.startswith("edit_"):
        await edit_personality(update, context)
        return
    elif name.startswith("delete_"):
        await delete_personality(update, context)
        return
    elif name.startswith("confirm_delete_"):
        await confirm_delete(update, context)
        return
    elif name.startswith("cancel_delete_"):
        await cancel_delete(update, context)
        return
    elif name.startswith("set_active_"):
        await set_active_personality(update, context)
        return

    personalities = await db.get_personalities(user_id)
    description = next((desc for n, desc in personalities if n == name), "Описание не найдено")

    keyboard = [
        [InlineKeyboardButton("Выбрать активной", callback_data=f"set_active_{name}")],
        [InlineKeyboardButton("Изменить", callback_data=f"edit_{name}")],
        [InlineKeyboardButton("Удалить", callback_data=f"delete_{name}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"Имя: {name}\nОписание: {description}", reply_markup=reply_markup)


def register_personalities_list_handler(application):
    application.add_handler(CommandHandler("manage_personas", list_personalities))
    application.add_handler(CallbackQueryHandler(button_handler))
