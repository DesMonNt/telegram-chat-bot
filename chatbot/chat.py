from ollama import AsyncClient

MODEL = 'llama3.1:8b'


class Chat:
    def __init__(self, user_personality, bot_personality, scenario, initial_message):
        self._user_personality = user_personality
        self._bot_personality = bot_personality
        self._scenario = scenario
        self._initial_message = initial_message
        self._system_prompt = self._build_system_prompt()
        self._message_history = self._system_prompt + [{'role': 'assistant', 'content': initial_message}]
        self._client = AsyncClient()

    def get_initial_message(self):
        return self._initial_message

    async def chat(self, message_text):
        message = {'role': 'user', 'content': message_text}
        self._message_history.append(message)

        response = await self._get_response()

        if response:
            self._message_history.append({'role': 'assistant', 'content': response})

        self._optimize_history()

        return response

    def _optimize_history(self, history_length=20):
        if len(self._message_history) <= history_length + 3:
            return

        self._message_history = self._message_history[-history_length:]
        self._message_history = self._system_prompt + self._message_history

    async def _get_response(self):
        response = await self._client.chat(model=MODEL, messages=self._message_history)
        return response['message']['content']

    def _build_system_prompt(self):
        return [
            {'role': 'user', 'content':
                f'Now you will participate with the user in a role-playing game. '
                f'Your name {self._bot_personality.name}. '
                f'You are: {self._bot_personality.description}.'},

            {'role': 'user', 'content':
                f'User name: {self._user_personality.name}. '
                f'User are: {self._user_personality.description}.'},

            {'role': 'user', 'content':
                f'Scenario: {self._scenario}.'}
        ]
