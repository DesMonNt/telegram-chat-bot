from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from telegram_bot.databases import PersonalityDB

db = PersonalityDB()


async def list_personalities(update: Update, context: CallbackContext):
    await db.init_db()

    user_id = update.effective_user.id
    personalities = await db.get_personalities(user_id)

    if not personalities:
        await update.message.reply_text("There are no saved personalities.")
        return

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'manage_personality_{name}')]
        for name, _ in personalities
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose a personality:", reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split('_', 2)[2]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)
    description = next((desc for n, desc in personalities if n == name), "Description not found")

    keyboard = [
        [InlineKeyboardButton("Select Active", callback_data=f"set_active_personality_{name}")],
        [InlineKeyboardButton("Change", callback_data=f"edit_personality_{name}")],
        [InlineKeyboardButton("Delete", callback_data=f"delete_personality_{name}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"Name: {name}\nDescription: {description}", reply_markup=reply_markup)


def register_personalities_list_handler(application):
    application.add_handler(CommandHandler("manage_personas", list_personalities))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^manage_personality_"))
