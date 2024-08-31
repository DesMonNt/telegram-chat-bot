from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from telegram_bot.databases import PersonalityDB

WAITING_FOR_NAME, WAITING_FOR_DESCRIPTION = range(2)

db = PersonalityDB()

cancel_button = KeyboardButton("Отмена")
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)


async def start_create_personality(update: Update, context: CallbackContext):
    await db.init_db()
    await update.message.reply_text(
        "Для создания новой личности напишите ее имя.",
        reply_markup=cancel_keyboard
    )
    return WAITING_FOR_NAME


async def process_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text

    user_id = update.effective_user.id
    existing_personalities = await db.get_personalities(user_id)

    if any(name == context.user_data['name'] for name, _ in existing_personalities):
        await update.message.reply_text("Личность с таким именем уже существует. Пожалуйста, выберите другое имя.")
        return WAITING_FOR_NAME

    await update.message.reply_text(
        "Теперь напишите описание личности.",
        reply_markup=cancel_keyboard
    )

    return WAITING_FOR_DESCRIPTION


async def process_description(update: Update, context: CallbackContext):
    name = context.user_data.get('name')
    description = update.message.text
    user_id = update.effective_user.id

    await db.add_personality(user_id, name, description)
    await update.message.reply_text(f"Личность создана:\nИмя: {name}\nОписание: {description}")

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_creation(update: Update, context: CallbackContext):
    await update.message.reply_text("Создание личности отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

    return ConversationHandler.END


def register_create_personality_handler(application):
    create_personality_handler = ConversationHandler(
        entry_points=[CommandHandler("create_persona", start_create_personality)],
        states={
            WAITING_FOR_NAME: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT, process_name)
            ],
            WAITING_FOR_DESCRIPTION: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_creation),
                MessageHandler(filters.TEXT, process_description)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex('^Отмена$'), cancel_creation)]
    )
    application.add_handler(create_personality_handler)
