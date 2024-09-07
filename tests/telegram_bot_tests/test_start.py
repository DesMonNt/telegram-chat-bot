import pytest
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from telegram_bot.handlers.start import start

@pytest.mark.asyncio
async def test_start_handler(mocker):
    update = mocker.Mock(spec=Update)
    update.message.reply_text = mocker.AsyncMock()

    context = mocker.Mock(spec=CallbackContext)

    await start(update, context)

    expected_message = (
        "👋 Hello! Welcome to our chat bot. I can help you create and manage various personalities and bots. Here’s what you can do:\n\n"
        "🔹 *Create and customize personalities* — set names and descriptions for different personalities that will be used in chats.\n"
        "🔹 *Create and customize bots* — set up bots with unique scenarios and initial messages to interact with.\n\n"
        "To get started, select a bot to chat with and we'll begin. If you'd like to create or customize a personality or bot, use the corresponding commands.\n\n"
    )
    update.message.reply_text.assert_called_once_with(expected_message, parse_mode=ParseMode.MARKDOWN)
