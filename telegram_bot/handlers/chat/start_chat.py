from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, CallbackContext

from chat_bot import Personality, Chat
from telegram_bot.databases import PersonalityDB, BotDB

cancel_button = KeyboardButton("Stop chat")
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)

personality_db = PersonalityDB()
bot_db = BotDB()

WAITING_FOR_USER_MESSAGE = range(1)


async def start_chat(update: Update, context: CallbackContext):
    await personality_db.init_db()
    await bot_db.init_db()

    user_id = update.effective_user.id

    user_name = await personality_db.get_active_personality(user_id)
    user = await personality_db.get_description(user_id, user_name)

    if user is None:
        user = [update.effective_user.first_name, '']

    user_personality = Personality(name=user[0], description=user[1])

    query = update.callback_query
    bot_name = query.data.split('_', 2)[2]

    bot_personalities = await bot_db.get_personalities(user_id)
    bot_personality_entry = next((entry for entry in bot_personalities if entry[1] == bot_name), None)

    if bot_personality_entry is None:
        await update.callback_query.message.reply_text("Information about the selected bot was not found.")
        return ConversationHandler.END

    bot_id = bot_personality_entry[0]
    bot_description = bot_personality_entry[2]
    bot_personality = Personality(name=bot_name, description=bot_description)

    scenario = await bot_db.get_bot_scenario(bot_id)
    initial_message = await bot_db.get_bot_initial_message(bot_id)

    chat = Chat(user_personality, bot_personality, scenario, initial_message)
    context.chat_data['chat'] = chat

    await update.callback_query.message.reply_text(f'{initial_message}', reply_markup=cancel_keyboard)

    return WAITING_FOR_USER_MESSAGE


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'chat' not in context.chat_data:
        await update.message.reply_text("The chat has not been started.")
        return ConversationHandler.END

    chat = context.chat_data['chat']
    user_message = update.message.text

    if user_message.lower() == "stop chat":
        return await end_chat(update, context)

    bot_response = await chat.chat(user_message)
    await update.message.reply_text(bot_response)


async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'chat' not in context.chat_data:
        await update.message.reply_text("The chat has not been started.")
        return ConversationHandler.END

    context.chat_data.clear()
    await update.message.reply_text("The chat is over.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def register_chat_handlers(application):
    chat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_chat, pattern="^chat_start_")],
        states={
            WAITING_FOR_USER_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message),
                CallbackQueryHandler(end_chat, pattern="^end_chat_"),
            ],
        },
        fallbacks=[CallbackQueryHandler(end_chat, pattern="^end_chat_")]
    )
    application.add_handler(chat_handler)
