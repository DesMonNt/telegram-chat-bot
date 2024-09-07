import pytest
from telegram import Update, CallbackQuery, User
from telegram.ext import CallbackContext
from telegram_bot.handlers.bot.delete_bot import delete_bot, confirm_delete, cancel_delete

@pytest.mark.asyncio
async def test_delete_bot(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.delete_bot.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[(1, "test_bot", "description")])

    query = mocker.Mock(spec=CallbackQuery)
    query.data = "delete_bot_test_bot"
    query.message.reply_text = mocker.AsyncMock()

    user = mocker.Mock(spec=User)
    user.id = 1234

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = user

    context = mocker.Mock(spec=CallbackContext)

    await delete_bot(update, context)

    query.message.reply_text.assert_called_once_with(
        "Are you sure you want to delete the bot 'test_bot'?",
        reply_markup=mocker.ANY
    )


@pytest.mark.asyncio
async def test_delete_bot_not_found(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.delete_bot.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[])

    query = mocker.Mock(spec=CallbackQuery)
    query.data = "delete_bot_non_existent_bot"
    query.message.reply_text = mocker.AsyncMock()

    user = mocker.Mock(spec=User)
    user.id = 1234

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = user

    context = mocker.Mock(spec=CallbackContext)

    await delete_bot(update, context)

    query.message.reply_text.assert_called_once_with("You cannot delete this bot.")


@pytest.mark.asyncio
async def test_confirm_delete(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.delete_bot.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[(1, "test_bot", "description")])
    mock_db.delete_bot_info = mocker.AsyncMock()
    mock_db.delete_personality = mocker.AsyncMock()

    query = mocker.Mock(spec=CallbackQuery)
    query.data = "confirm_delete_bot_test_bot"
    query.message.reply_text = mocker.AsyncMock()

    user = mocker.Mock(spec=User)
    user.id = 1234

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = user

    context = mocker.Mock(spec=CallbackContext)

    await confirm_delete(update, context)

    query.message.reply_text.assert_called_once_with("Bot 'test_bot' it was successfully deleted.")
    mock_db.delete_bot_info.assert_called_once_with(1)
    mock_db.delete_personality.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_confirm_delete_not_found(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.bot.delete_bot.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[])

    query = mocker.Mock(spec=CallbackQuery)
    query.data = "confirm_delete_bot_non_existent_bot"
    query.message.reply_text = mocker.AsyncMock()

    user = mocker.Mock(spec=User)
    user.id = 1234

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = user

    context = mocker.Mock(spec=CallbackContext)

    await confirm_delete(update, context)

    query.message.reply_text.assert_called_once_with("Couldn't find a bot to delete.")
    mock_db.delete_bot_info.assert_not_called()
    mock_db.delete_personality.assert_not_called()


@pytest.mark.asyncio
async def test_cancel_delete(mocker):
    query = mocker.Mock(spec=CallbackQuery)
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query

    context = mocker.Mock(spec=CallbackContext)

    await cancel_delete(update, context)

    query.message.reply_text.assert_called_once_with("The removal of the bot has been canceled.")
