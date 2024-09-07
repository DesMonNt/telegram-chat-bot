import pytest
from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.handlers.personality.set_active_personality import set_active_personality


@pytest.mark.asyncio
async def test_set_active_personality(mocker):
    query = mocker.Mock()
    query.data = "set_active_personality_Persona1"
    query.message.reply_text = mocker.AsyncMock()
    update = mocker.Mock(spec=Update)
    update.effective_user.id = 1234
    update.callback_query = query

    context = mocker.Mock(spec=CallbackContext)

    mock_db = mocker.patch("telegram_bot.handlers.personality.set_active_personality.db")
    mock_db.set_active_personality = mocker.AsyncMock()

    await set_active_personality(update, context)

    mock_db.set_active_personality.assert_called_once_with(1234, "Persona1")
    query.message.reply_text.assert_called_once_with("The active personality has been changed to 'Persona1'.")
