from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from telegram.constants import ParseMode
from telegram_bot.databases import PersonalityDB

WAITING_FOR_NAME, WAITING_FOR_DESCRIPTION = range(2)

db = PersonalityDB()

cancel_button = KeyboardButton("Cancel")
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)


async def start_create_personality(update: Update, context: CallbackContext):
    await db.init_db()
    await update.message.reply_text(
        "To create a new personality, write her name.",
        reply_markup=cancel_keyboard
    )
    return WAITING_FOR_NAME


async def process_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text

    user_id = update.effective_user.id
    existing_personalities = await db.get_personalities(user_id)

    if any(name == context.user_data['name'] for name, _ in existing_personalities):
        await update.message.reply_text("A personality with that name already exists. Please choose a different name.")
        return WAITING_FOR_NAME

    await update.message.reply_text(
        "Now write a description of your personality.",
        reply_markup=cancel_keyboard
    )

    return WAITING_FOR_DESCRIPTION


async def process_description(update: Update, context: CallbackContext):
    name = context.user_data.get('name')
    description = update.message.text
    user_id = update.effective_user.id

    await db.add_personality(user_id, name, description)
    await update.message.reply_text(f"The personality is created:\n\n*Name:* {name}\n*Description:* {description}",
                                    parse_mode=ParseMode.MARKDOWN)

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_creation(update: Update, context: CallbackContext):
    await update.message.reply_text("The creation of a personality has been canceled.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

    return ConversationHandler.END


def register_create_personality_handler(application):
    create_personality_handler = ConversationHandler(
        entry_points=[CommandHandler("create_persona", start_create_personality)],
        states={
            WAITING_FOR_NAME: [
                MessageHandler(filters.Regex('^Cancel$'), cancel_creation),
                MessageHandler(filters.TEXT, process_name)
            ],
            WAITING_FOR_DESCRIPTION: [
                MessageHandler(filters.Regex('^Cancel$'), cancel_creation),
                MessageHandler(filters.TEXT, process_description)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel_creation)],
    )
    application.add_handler(create_personality_handler)
