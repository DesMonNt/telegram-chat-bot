from .start import register_start_handler
from telegram_bot.handlers.personality.create_personality import register_create_personality_handler
from telegram_bot.handlers.personality.personalities_list import register_personalities_list_handler
from telegram_bot.handlers.personality.edit_personality import register_edit_personality
from telegram_bot.handlers.personality.delete_personality import register_delete_personality
from telegram_bot.handlers.personality.get_active_personality import register_get_active_personality_handler
from telegram_bot.handlers.personality.set_active_personality import register_set_active_personality_handler
from telegram_bot.handlers.bot.bots_list import register_bots_list_handler
from telegram_bot.handlers.bot.create_bot import register_create_bot_handler
from telegram_bot.handlers.bot.delete_bot import register_delete_bot_handler
from telegram_bot.handlers.bot.edit_bot import register_edit_bot_handler
from telegram_bot.handlers.chat.start_chat import register_chat_handlers

__all__ = [
    'register_handlers',
]


def register_handlers(app):
    register_create_bot_handler(app)
    register_start_handler(app)
    register_create_personality_handler(app)
    register_personalities_list_handler(app)
    register_edit_personality(app)
    register_set_active_personality_handler(app)
    register_get_active_personality_handler(app)
    register_delete_personality(app)
    register_bots_list_handler(app)
    register_delete_bot_handler(app)
    register_edit_bot_handler(app)
    register_chat_handlers(app)
