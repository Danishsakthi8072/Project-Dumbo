from collections import defaultdict


class ConversationMemory:
    def __init__(self):
        self._conversations = defaultdict(list)

    def add_user_message(
        self,
        conversation_id: str,
        message: str,
    ):
        self._conversations[conversation_id].append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        message: str,
    ):
        self._conversations[conversation_id].append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict]:
        return self._conversations[conversation_id]

    def clear(
        self,
        conversation_id: str,
    ):
        self._conversations[conversation_id].clear()