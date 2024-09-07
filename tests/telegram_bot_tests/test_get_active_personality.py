import pytest
from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram_bot.handlers.personality.get_active_personality import get_active_personality


@pytest.mark.asyncio
async def test_get_active_personality_exists(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.effective_user.id = 1234
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    mock_db = mocker.patch("telegram_bot.handlers.personality.get_active_personality.db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_active_personality = mocker.AsyncMock(return_value="TestPersona")

    await get_active_personality(update, context)

    message.reply_text.assert_called_once_with("Your active personality: TestPersona")


@pytest.mark.asyncio
async def test_get_active_personality_none(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.effective_user.id = 1234
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    mock_db = mocker.patch("telegram_bot.handlers.personality.get_active_personality.db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_active_personality = mocker.AsyncMock(return_value=None)

    await get_active_personality(update, context)

    message.reply_text.assert_called_once_with("No active identity has been established.")
