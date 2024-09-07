import pytest
from telegram import Update, Message, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from telegram_bot.handlers.personality.create_personality import (
    start_create_personality, process_name, process_description, cancel_creation
)


WAITING_FOR_NAME, WAITING_FOR_DESCRIPTION = range(2)


@pytest.mark.asyncio
async def test_start_create_personality(mocker):
    mock_db = mocker.patch("telegram_bot.handlers.personality.create_personality.db")
    mock_db.init_db = mocker.AsyncMock()

    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)

    result = await start_create_personality(update, context)

    assert result == WAITING_FOR_NAME
    message.reply_text.assert_called_once_with(
        "To create a new personality, write her name.",
        reply_markup=mocker.ANY
    )


@pytest.mark.asyncio
async def test_process_name_existing_personality(mocker):
    message = mocker.Mock(spec=Message)
    message.text = "TestPersona"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message
    update.effective_user = mocker.Mock(spec=User)
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}

    mock_db = mocker.patch("telegram_bot.handlers.personality.create_personality.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[("TestPersona", "description")])

    result = await process_name(update, context)

    assert result == WAITING_FOR_NAME
    message.reply_text.assert_called_once_with("A personality with that name already exists. Please choose a different name.")


@pytest.mark.asyncio
async def test_process_name_valid(mocker):
    message = mocker.Mock(spec=Message)
    message.text = "NewPersona"
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message
    update.effective_user = mocker.Mock(spec=User)
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}

    mock_db = mocker.patch("telegram_bot.handlers.personality.create_personality.db")
    mock_db.get_personalities = mocker.AsyncMock(return_value=[])

    result = await process_name(update, context)

    assert result == WAITING_FOR_DESCRIPTION
    message.reply_text.assert_called_once_with(
        "Now write a description of your personality.",
        reply_markup=mocker.ANY
    )


@pytest.mark.asyncio
async def test_process_description(mocker):
    message = mocker.Mock(spec=Message)
    message.text = "This is a new personality."
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message
    update.effective_user = mocker.Mock(spec=User)
    update.effective_user.id = 1234

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {"name": "NewPersona"}

    mock_db = mocker.patch("telegram_bot.handlers.personality.create_personality.db")
    mock_db.add_personality = mocker.AsyncMock()

    result = await process_description(update, context)

    assert result == ConversationHandler.END
    mock_db.add_personality.assert_called_once_with(1234, "NewPersona", "This is a new personality.")
    message.reply_text.assert_called_once_with(
        "The personality is created:\n\n*Name:* NewPersona\n*Description:* This is a new personality.",
        parse_mode=ParseMode.MARKDOWN
    )
    assert context.user_data == {}


@pytest.mark.asyncio
async def test_cancel_creation(mocker):
    message = mocker.Mock(spec=Message)
    message.reply_text = mocker.AsyncMock()

    update = mocker.Mock(spec=Update)
    update.message = message

    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {"name": "NewPersona"}

    result = await cancel_creation(update, context)

    assert result == ConversationHandler.END
    message.reply_text.assert_called_once_with(
        "The creation of a personality has been canceled.",
        reply_markup=mocker.ANY
    )
    assert context.user_data == {}
