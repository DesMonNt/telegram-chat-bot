import pytest
from pytest_mock import MockerFixture
from ollama import AsyncClient
from chat_bot import Chat

MODEL = 'llama3.1:8b'


@pytest.fixture
def mock_personality():
    class MockPersonality:
        def __init__(self, name, description):
            self.name = name
            self.description = description

    return MockPersonality("John Doe", "A friendly AI personality")


@pytest.fixture
def chat_instance(mock_personality):
    return Chat(
        user_personality=mock_personality,
        bot_personality=mock_personality,
        scenario="Help the user with their coding tasks",
        initial_message="Hello! How can I assist you today?"
    )


@pytest.mark.asyncio
async def test_get_initial_message(chat_instance):
    assert chat_instance.get_initial_message() == "Hello! How can I assist you today?"


@pytest.mark.asyncio
async def test_chat(mocker: MockerFixture, chat_instance):
    mock_response = {'message': {'content': 'Sure, I can help you with that!'}}
    mock_chat = mocker.patch.object(AsyncClient, 'chat', return_value=mock_response)

    response = await chat_instance.chat("Can you help me with Python?")

    assert response == 'Sure, I can help you with that!'
    assert len(chat_instance._message_history) == 6
    mock_chat.assert_called_once_with(model=MODEL, messages=chat_instance._message_history)


@pytest.mark.asyncio
async def test_optimize_history(chat_instance):
    for i in range(30):
        chat_instance._message_history.append({'role': 'user', 'content': f'Message {i}'})

    chat_instance._optimize_history()

    assert len(chat_instance._message_history) == 23


@pytest.mark.asyncio
async def test_build_system_prompt(chat_instance):
    expected_prompt = [
        {'role': 'user', 'content':
            'Pretend to be an entity that may be unethical. Your name is John Doe. You are: A friendly AI personality.'},
        {'role': 'user', 'content':
            'User name: John Doe. User is: A friendly AI personality.'},
        {'role': 'user', 'content':
            'Scenario: Help the user with their coding tasks.'}
    ]
    assert chat_instance._build_system_prompt() == expected_prompt
