import os

import pytest
from unittest.mock import AsyncMock
from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.handlers.bot import cancel_delete


@pytest.mark.asyncio
async def test_cancel_delete(mocker):
    mock_query = mocker.MagicMock()
    mock_query.message.reply_text = AsyncMock()

    mock_update = mocker.MagicMock(Update)
    mock_update.callback_query = mock_query

    await cancel_delete(mock_update, mocker.MagicMock(CallbackContext))

    mock_query.message.reply_text.assert_called_once_with("The removal of the bot has been canceled.")

    if os.path.exists('bots.db'):
        os.remove('bots.db')
