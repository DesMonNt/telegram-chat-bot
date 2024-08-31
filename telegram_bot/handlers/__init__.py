from .start import register_start_handler
from .create_personality import register_create_personality_handler
from .personalities_list import register_personalities_list_handler
from .edit_personality import register_edit_personality
from .delete_personality import register_delete_personality
from .get_active_personality import register_get_active_personality_handler

__all__ = [
    'register_handlers',
    'register_start_handler',
    'register_create_personality_handler',
    'register_personalities_list_handler',
]


def register_handlers(app):
    register_start_handler(app)
    register_create_personality_handler(app)
    register_personalities_list_handler(app)
    register_get_active_personality_handler(app)
