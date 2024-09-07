import os

import pytest
from unittest.mock import AsyncMock
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from telegram_bot.handlers.bot import start_create_bot, process_bot_name, process_description,process_scenario



@pytest.mark.asyncio
async def test_start_create_bot(mocker):
    mock_update = mocker.MagicMock(Update)
    mock_update.message.reply_text = AsyncMock()

    await start_create_bot(mock_update, mocker.MagicMock(CallbackContext))

    mock_update.message.reply_text.assert_called_once_with(
        "To create a new bot, write its name.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Cancel")]], resize_keyboard=True)
    )

    if os.path.exists('bots.db'):
        os.remove('bots.db')


@pytest.mark.asyncio
async def test_process_bot_name(mocker):
    mock_update = mocker.MagicMock(Update)
    mock_update.message.text = "TestBot"
    mock_update.message.reply_text = AsyncMock()

    context = mocker.MagicMock(CallbackContext)
    await process_bot_name(mock_update, context)

    context.user_data['bot_name'] = "TestBot"
    mock_update.message.reply_text.assert_called_once_with(
        "Now write a description for the bot. Specify all the important characteristics (for example, character traits) so that the bot knows how to behave.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Cancel")]], resize_keyboard=True)
    )

    if os.path.exists('bots.db'):
        os.remove('bots.db')


@pytest.mark.asyncio
async def test_process_description(mocker):
    mock_update = mocker.MagicMock(Update)
    mock_update.message.text = "A friendly bot."
    mock_update.message.reply_text = AsyncMock()

    context = mocker.MagicMock(CallbackContext)
    context.user_data = {'bot_name': 'TestBot'}
    await process_description(mock_update, context)

    context.user_data['bot_description'] = "A friendly bot."
    mock_update.message.reply_text.assert_called_once_with(
        "Now write a script for the bot. It is intended to give him the context of what is happening.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Cancel")]], resize_keyboard=True)
    )

    if os.path.exists('bots.db'):
        os.remove('bots.db')


@pytest.mark.asyncio
async def test_process_scenario(mocker):
    mock_update = mocker.MagicMock(Update)
    mock_update.message.text = "Bot scenario details."
    mock_update.message.reply_text = AsyncMock()

    context = mocker.MagicMock(CallbackContext)
    context.user_data = {'bot_name': 'TestBot', 'bot_description': 'A friendly bot.'}
    await process_scenario(mock_update, context)

    context.user_data['bot_scenario'] = "Bot scenario details."
    mock_update.message.reply_text.assert_called_once_with(
        "Now write the initial message for the bot.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Cancel")]], resize_keyboard=True)
    )

    if os.path.exists('bots.db'):
        os.remove('bots.db')
