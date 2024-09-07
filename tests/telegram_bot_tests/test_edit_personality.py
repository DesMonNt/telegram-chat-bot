import pytest
from telegram import Update, Message, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram_bot.handlers.personality.edit_personality import handle_edit_description, cancel_edit


@pytest.mark.asyncio
async def test_handle_edit_description(mocker):
    message = mocker.Mock(spec=Message)
    message.text = "New description"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {'edit_personality': {'name': 'TestPersona', 'user_id': 1234}}

    mock_db = mocker.patch("telegram_bot.handlers.personality.edit_personality.db")
    mock_db.update_personality = mocker.AsyncMock()

    result = await handle_edit_description(update, context)

    mock_db.update_personality.assert_called_once_with(1234, 'TestPersona', 'New description')
    message.reply_text.assert_called_once_with("Description for the personality 'TestPersona' updated.")
    assert 'edit_personality' not in context.user_data
    assert result == -1


@pytest.mark.asyncio
async def test_cancel_edit(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {'edit_personality': {'name': 'TestPersona', 'user_id': 1234}}

    result = await cancel_edit(update, context)

    message.reply_text.assert_called_once_with(
        "Personality editing has been canceled.", reply_markup=ReplyKeyboardRemove()
    )
    assert context.user_data == {}
    assert result == -1 
