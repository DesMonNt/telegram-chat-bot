import pytest
from telegram import Update, CallbackQuery, Message, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.handlers.personality.delete_personality import delete_personality, confirm_delete, cancel_delete

@pytest.mark.asyncio
async def test_delete_personality_exists(mocker):
    query = mocker.Mock(spec=CallbackQuery)
    query.data = "delete_personality_TestPersona"
    query.message = mocker.Mock(spec=Message)
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = mocker.Mock()
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    mock_db = mocker.patch("telegram_bot.handlers.personality.delete_personality.db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_personalities = mocker.AsyncMock(return_value=[("TestPersona", "description")])

    await delete_personality(update, context)

    query.message.reply_text.assert_called_once_with(
        "Are you sure you want to delete the personality 'TestPersona'?",
        reply_markup=mocker.ANY
    )
    assert isinstance(query.message.reply_text.call_args[1]["reply_markup"], InlineKeyboardMarkup)


@pytest.mark.asyncio
async def test_delete_personality_not_exists(mocker):
    query = mocker.Mock(spec=CallbackQuery)
    query.data = "delete_personality_NonExistentPersona"
    query.message = mocker.Mock(spec=Message)
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = mocker.Mock()
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    mock_db = mocker.patch("telegram_bot.handlers.personality.delete_personality.db")
    mock_db.init_db = mocker.AsyncMock()
    mock_db.get_personalities = mocker.AsyncMock(return_value=[("TestPersona", "description")])

    await delete_personality(update, context)

    query.message.reply_text.assert_called_once_with("You cannot delete this personality.")


@pytest.mark.asyncio
async def test_confirm_delete(mocker):
    query = mocker.Mock(spec=CallbackQuery)
    query.data = "confirm_delete_personality_TestPersona"
    query.message = mocker.Mock(spec=Message)
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query
    update.effective_user = mocker.Mock()
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    mock_db = mocker.patch("telegram_bot.handlers.personality.delete_personality.db")
    mock_db.delete_personality = mocker.AsyncMock()

    await confirm_delete(update, context)

    mock_db.delete_personality.assert_called_once_with(1234, "TestPersona")
    query.message.reply_text.assert_called_once_with("Personality 'TestPersona' it was deleted.")


@pytest.mark.asyncio
async def test_cancel_delete(mocker):
    query = mocker.Mock(spec=CallbackQuery)
    query.message = mocker.Mock(spec=Message)
    query.message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.callback_query = query

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    await cancel_delete(update, context)

    query.message.reply_text.assert_called_once_with("The deletion of the personality has been canceled.")
