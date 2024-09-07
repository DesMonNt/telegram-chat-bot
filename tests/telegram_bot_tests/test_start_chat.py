import pytest
from telegram import Update, Message, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from telegram_bot.handlers.chat.start_chat import handle_user_message, end_chat


@pytest.mark.asyncio
async def test_handle_user_message(mocker):
    mock_chat = mocker.Mock()
    mock_chat.chat = mocker.AsyncMock(return_value="TestBot's response")

    message = mocker.Mock(spec=Message)
    message.text = "Hello, TestBot"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.chat_data = {"chat": mock_chat}

    result = await handle_user_message(update, context)

    assert result is None
    message.reply_text.assert_called_once_with("TestBot's response")


@pytest.mark.asyncio
async def test_handle_stop_chat(mocker):
    message = mocker.Mock(spec=Message)
    message.text = "stop chat"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.chat_data = {"chat": mocker.Mock()}

    result = await handle_user_message(update, context)

    assert result == ConversationHandler.END
    message.reply_text.assert_called_once_with("The chat is over.", reply_markup=ReplyKeyboardRemove())


@pytest.mark.asyncio
async def test_end_chat(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.chat_data = {"chat": mocker.Mock()}

    result = await end_chat(update, context)

    assert result == ConversationHandler.END
    message.reply_text.assert_called_once_with("The chat is over.", reply_markup=ReplyKeyboardRemove())
    assert context.chat_data == {}
