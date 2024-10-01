from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from databases import BotDB

db = BotDB()


async def delete_bot(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 2)[2]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)
    if not any(n == name for _, n, _ in personalities):
        await query.message.reply_text("You cannot delete this bot.")
        return

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=f"confirm_delete_bot_{name}")],
        [InlineKeyboardButton("No", callback_data=f"cancel_delete_bot_{name}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(f"Are you sure you want to delete the bot '{name}'?", reply_markup=reply_markup)


async def confirm_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    name = query.data.split("_", 3)[3]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)
    if not any(n == name for _, n, _ in personalities):
        await query.message.reply_text("Couldn't find a bot to delete.")
        return

    personality_id = next((id for id, n, _ in personalities if n == name), None)
    if personality_id is not None:
        await db.delete_bot_info(personality_id)
        await db.delete_personality(personality_id)
        await query.message.reply_text(f"Bot '{name}' it was successfully deleted.")
    else:
        await query.message.reply_text("An error occurred while deleting the bot.")


async def cancel_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.message.reply_text("The removal of the bot has been canceled.")


def register_delete_bot_handler(application):
    application.add_handler(CallbackQueryHandler(delete_bot, pattern="^delete_bot_"))
    application.add_handler(CallbackQueryHandler(confirm_delete, pattern="^confirm_delete_bot_"))
    application.add_handler(CallbackQueryHandler(cancel_delete, pattern="^cancel_delete_bot_"))
