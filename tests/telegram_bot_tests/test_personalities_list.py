import pytest
from telegram import Update, Message
from telegram.ext import CallbackContext
from telegram_bot.handlers.personality.personalities_list import list_personalities, button_handler


@pytest.mark.asyncio
async def test_list_personalities(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()
    update = mocker.Mock(spec=Update)
    update.effective_user.id = 1234
    update.message = message

    context = mocker.Mock(spec=CallbackContext)

    mock_db = mocker.patch("telegram_bot.handlers.personality.personalities_list.db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_personalities = mocker.AsyncMock(return_value=[("Persona1", "Description1"), ("Persona2", "Description2")])

    await list_personalities(update, context)

    message.reply_text.assert_called_once()
    assert "Choose a personality:" in message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_button_handler(mocker):
    query = mocker.Mock()
    query.data = "manage_personality_Persona1"
    query.message.reply_text = mocker.AsyncMock()
    update = mocker.Mock(spec=Update)
    update.effective_user.id = 1234
    update.callback_query = query

    context = mocker.Mock(spec=CallbackContext)

    mock_db = mocker.patch("telegram_bot.handlers.personality.personalities_list.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[("Persona1", "Description1")])

    await button_handler(update, context)

    query.message.reply_text.assert_called_once()
    assert "Name: Persona1" in query.message.reply_text.call_args[0][0]
