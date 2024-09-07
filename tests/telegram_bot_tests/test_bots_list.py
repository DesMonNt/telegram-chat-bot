import os.path

import pytest
from unittest.mock import AsyncMock
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram_bot.handlers.bot import list_bots, button_handler


@pytest.mark.asyncio
async def test_list_bots_no_bots(mocker):
    mock_db = mocker.patch('telegram_bot.databases.BotDB', autospec=True)
    mock_db_instance = mock_db.return_value
    mock_db_instance.get_personalities = AsyncMock(return_value=[])

    mock_update = mocker.MagicMock(Update)
    mock_update.effective_user.id = 12345
    mock_update.message.reply_text = AsyncMock()

    await list_bots(mock_update, mocker.MagicMock(CallbackContext))

    mock_update.message.reply_text.assert_called_once_with("You don't have any bots created.")

    if os.path.exists('bots.db'):
        os.remove('bots.db')


@pytest.mark.asyncio
async def test_button_handler(mocker):
    mock_update = mocker.Mock(spec=Update)
    mock_context = mocker.Mock(spec=CallbackContext)
    mock_query = mocker.Mock()
    mock_query.data = "manage_bot_Bot1"

    mock_query.message.reply_text = AsyncMock()

    mock_update.callback_query = mock_query

    await button_handler(mock_update, mock_context)

    keyboard = [
        [InlineKeyboardButton("Start chat", callback_data="chat_start_Bot1")],
        [InlineKeyboardButton("Change", callback_data="edit_bot_Bot1")],
        [InlineKeyboardButton("Delete", callback_data="delete_bot_Bot1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    mock_query.message.reply_text.assert_called_once_with("Name: Bot1", reply_markup=reply_markup)
