from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from databases import PersonalityDB

db = PersonalityDB()

WAITING_FOR_EDIT_DESCRIPTION = range(1)


async def edit_personality(update: Update, context: CallbackContext):
    await db.init_db()

    query = update.callback_query
    name = query.data.split("_", 2)[2]
    user_id = update.effective_user.id

    personalities = await db.get_personalities(user_id)

    if not any(n == name for n, _ in personalities):
        await query.message.reply_text("You cannot edit this personality.")
        return

    await query.message.reply_text(f"Enter a new description for the personality '{name}':")
    context.user_data['edit_personality'] = {'name': name, 'user_id': user_id}

    return WAITING_FOR_EDIT_DESCRIPTION


async def handle_edit_description(update: Update, context: CallbackContext):
    if 'edit_personality' not in context.user_data:
        return

    name = context.user_data['edit_personality']['name']
    new_description = update.message.text
    user_id = context.user_data['edit_personality']['user_id']

    await db.update_personality(user_id, name, new_description)
    await update.message.reply_text(f"Description for the personality '{name}' updated.")

    del context.user_data['edit_personality']

    return ConversationHandler.END


async def cancel_edit(update: Update, context: CallbackContext):
    await update.message.reply_text("Personality editing has been canceled.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

    return ConversationHandler.END


def register_edit_personality(application):
    edit_personality_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_personality, pattern="^edit_personality_")],
        states={
            WAITING_FOR_EDIT_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_description),
                MessageHandler(filters.Regex('^Cancel$'), cancel_edit)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel_edit)]
    )
    application.add_handler(edit_personality_handler)
