import pytest
from telegram import Update, Message, CallbackQuery, User
from telegram.ext import CallbackContext, ConversationHandler
from telegram_bot.handlers.bot.edit_bot import (
    edit_bot, process_edit_scenario, process_edit_initial_message, cancel_edit, WAITING_FOR_EDIT_SCENARIO,
    WAITING_FOR_EDIT_INITIAL_MESSAGE
)


@pytest.mark.asyncio
async def test_edit_bot_not_found(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.edit_bot.bot_db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_personalities = mocker.AsyncMock(return_value=[])

    query = mocker.Mock(spec=CallbackQuery)
    query.data = "edit_bot_non_existent_bot"
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user.id = 1234

    context = mocker.Mock(spec=CallbackContext)

    state = await edit_bot(update, context)

    assert state is None
    query.message.reply_text.assert_called_once_with("You cannot edit this bot.")


@pytest.mark.asyncio
async def test_process_edit_scenario(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.edit_bot.bot_db")
    mock_db.update_bot_scenario = mocker.AsyncMock()

    message = mocker.Mock(spec=Message)
    message.text = "New bot scenario"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=CallbackContext)
    context.user_data = {'edit_bot': {'bot_id': 1}}

    state = await process_edit_scenario(update, context)

    assert state == WAITING_FOR_EDIT_INITIAL_MESSAGE
    mock_db.update_bot_scenario.assert_called_once_with(1, "New bot scenario")
    message.reply_text.assert_called_once_with(
        "Now enter the initial message for the bot.",
        reply_markup=mocker.ANY
    )


@pytest.mark.asyncio
async def test_process_edit_initial_message(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.edit_bot.bot_db")
    mock_db.update_bot_initial_message = mocker.AsyncMock()

    message = mocker.Mock(spec=Message)
    message.text = "Initial message"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=CallbackContext)
    context.user_data = {'edit_bot': {'bot_id': 1}}

    state = await process_edit_initial_message(update, context)

    assert state == ConversationHandler.END
    mock_db.update_bot_initial_message.assert_called_once_with(1, "Initial message")
    message.reply_text.assert_called_once_with("The initial message for the bot has been updated.")
    assert context.user_data == {}


@pytest.mark.asyncio
async def test_cancel_edit(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=CallbackContext)
    context.user_data = {}

    state = await cancel_edit(update, context)

    assert state == ConversationHandler.END
    message.reply_text.assert_called_once_with(
        "Bot editing has been canceled.", reply_markup=mocker.ANY
    )
    assert context.user_data == {}
