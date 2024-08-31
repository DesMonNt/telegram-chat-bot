from .start import register_start_handler
from .create_personality import register_create_personality_handlers
from .personalities_list import register_personalities_list
from .edit_personality import register_edit_personality
from .delete_personality import register_delete_personality

__all__ = [
    'register_handlers',
    'register_start_handler',
    'register_create_personality_handlers',
    'register_personalities_list',
    'register_edit_personality',
    'register_delete_personality'
]


def register_handlers(app):
    register_start_handler(app)
    register_create_personality_handlers(app)
    register_personalities_list(app)
    register_edit_personality(app)
    register_delete_personality(app)
