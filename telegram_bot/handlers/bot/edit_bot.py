from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from telegram_bot.databases import BotDB

WAITING_FOR_EDIT_SCENARIO, WAITING_FOR_EDIT_INITIAL_MESSAGE = range(2)

bot_db = BotDB()

cancel_button = KeyboardButton("Отмена")
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)


async def edit_bot(update: Update, context: CallbackContext):
    await bot_db.init_db()

    query = update.callback_query
    bot_name = query.data.split("_", 2)[2]
    user_id = update.effective_user.id

    bots = await bot_db.get_personalities(user_id)

    bot_id = None

    for name, id in bots:
        if name == bot_name:
            bot_id = id
            break

    if bot_id is None:
        await query.message.reply_text("Вы не можете редактировать этого бота.")
        return

    context.user_data['edit_bot'] = {'name': bot_name, 'bot_id': bot_id}
    bot_info = await bot_db.get_bot_info(bot_id)

    if bot_info:
        await query.message.reply_text(
            f"Введите новый сценарий для бота '{bot_name}':",
            reply_markup=cancel_keyboard
        )
        return WAITING_FOR_EDIT_SCENARIO
    else:
        await query.message.reply_text("Информация о боте не найдена.")
        return ConversationHandler.END


async def process_edit_scenario(update: Update, context: CallbackContext):
    if 'edit_bot' not in context.user_data:
        return

    bot_id = context.user_data['edit_bot']['bot_id']
    new_scenario = update.message.text

    await bot_db.update_bot_info(bot_id, scenario=new_scenario, initial_message=None)

    await update.message.reply_text(f"Сценарий для бота обновлен.")

    await update.message.reply_text(
        "Теперь введите начальное сообщение для бота.",
        reply_markup=cancel_keyboard
    )

    return WAITING_FOR_EDIT_INITIAL_MESSAGE


async def process_edit_initial_message(update: Update, context: CallbackContext):
    if 'edit_bot' not in context.user_data:
        return

    bot_id = context.user_data['edit_bot']['bot_id']
    initial_message = update.message.text

    await bot_db.update_bot_info(bot_id, scenario=None, initial_message=initial_message)

    await update.message.reply_text(f"Начальное сообщение для бота обновлено.")

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_edit(update: Update, context: CallbackContext):
    await update.message.reply_text("Редактирование бота отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

    return ConversationHandler.END


def register_edit_bot_handler(application):
    edit_bot_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_bot, pattern="^edit_bot_")],
        states={
            WAITING_FOR_EDIT_SCENARIO: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_edit),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_edit_scenario),
            ],
            WAITING_FOR_EDIT_INITIAL_MESSAGE: [
                MessageHandler(filters.Regex('^Отмена$'), cancel_edit),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_edit_initial_message),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex('^Отмена$'), cancel_edit)]
    )
    application.add_handler(edit_bot_handler)
