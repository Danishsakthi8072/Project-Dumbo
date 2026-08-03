from app.ai.context_builder import ContextBuilder
from app.ai.manager import AIManager
from app.ai.prompt_engine import PromptEngine
from app.services.conversation_service import ConversationService


class ChatService:
    def __init__(
        self,
        manager: AIManager,
        conversation_service: ConversationService,
    ):
        self.manager = manager
        self.conversation_service = conversation_service

        prompt_engine = PromptEngine()
        self.context_builder = ContextBuilder(prompt_engine)

    def chat(
        self,
        conversation_id: str,
        prompt: str,
    ) -> str:
        self.conversation_service.add_user_message(
            conversation_id=conversation_id,
            message=prompt,
        )

        conversation = self.conversation_service.get_messages(
            conversation_id=conversation_id,
        )

        context = self.context_builder.build(conversation)

        response = self.manager.chat(context)

        self.conversation_service.add_assistant_message(
            conversation_id=conversation_id,
            message=response,
        )

        return response

    def clear_memory(
        self,
        conversation_id: str,
    ):
        self.conversation_service.clear(
            conversation_id=conversation_id,
        )