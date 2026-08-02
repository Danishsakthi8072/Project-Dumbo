from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(
        self,
        repository: ConversationRepository,
    ):
        self.repository = repository

    def add_user_message(
        self,
        conversation_id: str,
        message: str,
    ):
        return self.repository.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        message: str,
    ):
        return self.repository.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=message,
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict]:
        messages = self.repository.get_messages(
            conversation_id
        )

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    def clear(
        self,
        conversation_id: str,
    ):
        self.repository.clear(conversation_id)