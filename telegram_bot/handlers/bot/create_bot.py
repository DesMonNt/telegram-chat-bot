from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from telegram_bot.databases import BotDB

WAITING_FOR_NAME, WAITING_FOR_DESCRIPTION, WAITING_FOR_SCENARIO, WAITING_FOR_INITIAL_MESSAGE = range(4)

db = BotDB()

cancel_button = KeyboardButton("Отмена")
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)


async def start_create_bot(update: Update, context: CallbackContext):
    await db.init_db()
    await update.message.reply_text(
        "Для создания нового бота напишите его имя.",
        reply_markup=cancel_keyboard
    )
    return WAITING_FOR_NAME


async def process_bot_name(update: Update, context: CallbackContext):
    context.user_data['bot_name'] = update.message.text

    await update.message.reply_text(
        "Теперь напишите описание для бота.",
        reply_markup=cancel_keyboard
    )
    return WAITING_FOR_DESCRIPTION


async def process_description(update: Update, context: CallbackContext):
    context.user_data['bot_description'] = update.message.text

    await update.message.reply_text(
        "Теперь напишите сценарий для бота.",
        reply_markup=cancel_keyboard
    )

    return WAITING_FOR_SCENARIO


async def process_scenario(update: Update, context: CallbackContext):
    context.user_data['bot_scenario'] = update.message.text

    await update.message.reply_text(
        "Теперь напишите начальное сообщение для бота.",
        reply_markup=cancel_keyboard
    )

    return WAITING_FOR_INITIAL_MESSAGE


async def process_initial_message(update: Update, context: CallbackContext):
    bot_name = context.user_data.get('bot_name')
    description = context.user_data.get('bot_description')
    scenario = context.user_data.get('bot_scenario')
    initial_message = update.message.text
    creator_id = update.effective_user.id

    await db.add_personality(creator_id, bot_name, description)
    personalities = await db.get_personalities(creator_id)
    personality_id = personalities[-1][0]

    await db.add_bot_info(personality_id, scenario, initial_message)

    await update.message.reply_text(f"Бот создан:\nИмя: {bot_name}\nОписание: {description}\nСценарий: {scenario}\nНачальное сообщение: {initial_message}")

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_creation(update: Update, context: CallbackContext):
    await update.message.reply_text("Создание бота отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

    return ConversationHandler.END


def register_create_bot_handler(application):
    create_bot_handler = ConversationHandler(
        entry_points=[CommandHandler("create_bot", start_create_bot)],
        states={
            WAITING_FOR_NAME: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_bot_name)
            ],
            WAITING_FOR_DESCRIPTION: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_description)
            ],
            WAITING_FOR_SCENARIO: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_scenario)
            ],
            WAITING_FOR_INITIAL_MESSAGE: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_initial_message)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex('^Отмена$'), cancel_creation)],
    )
    application.add_handler(create_bot_handler)
