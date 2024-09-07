from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from telegram_bot.databases import BotDB

db = BotDB()


async def list_bots(update: Update, context: CallbackContext):
    await db.init_db()

    user_id = update.effective_user.id
    bots = await db.get_personalities(user_id)

    if not bots:
        await update.message.reply_text("You don't have any bots created.")
        return

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"manage_bot_{name}")]
        for _, name, _ in bots
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a bot to manage:", reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split('_', 2)[2]

    keyboard = [
        [InlineKeyboardButton("Start chat", callback_data=f"chat_start_{name}")],
        [InlineKeyboardButton("Change", callback_data=f"edit_bot_{name}")],
        [InlineKeyboardButton("Delete", callback_data=f"delete_bot_{name}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"*Name:* {name}", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


def register_bots_list_handler(application):
    application.add_handler(CommandHandler("manage_bots", list_bots))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^manage_bot_"))
