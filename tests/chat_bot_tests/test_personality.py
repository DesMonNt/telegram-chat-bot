import pytest
from chat_bot import Personality


def test_personality_initialization():
    name = "  John Doe  "
    description = "  A friendly AI personality.  "

    personality = Personality(name, description)

    assert personality.name == "John Doe"
    assert personality.description == "A friendly AI personality."


def test_personality_empty_strings():
    name = "   "
    description = "   "

    personality = Personality(name, description)

    assert personality.name == ""
    assert personality.description == ""


def test_personality_no_whitespace():
    name = "Jane Doe"
    description = "An enthusiastic AI."

    personality = Personality(name, description)

    assert personality.name == "Jane Doe"
    assert personality.description == "An enthusiastic AI."
