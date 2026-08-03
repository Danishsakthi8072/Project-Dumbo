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

    def _build_context(
        self,
        conversation_id: str,
        prompt: str,
    ) -> list[dict]:
        self.conversation_service.add_user_message(
            conversation_id=conversation_id,
            message=prompt,
        )

        conversation = self.conversation_service.get_messages(
            conversation_id=conversation_id,
        )

        return self.context_builder.build(conversation)

    def chat(
        self,
        conversation_id: str,
        prompt: str,
    ) -> str:
        context = self._build_context(
            conversation_id,
            prompt,
        )

        response = self.manager.chat(context)

        self.conversation_service.add_assistant_message(
            conversation_id=conversation_id,
            message=response,
        )

        return response

    def stream_chat(
        self,
        conversation_id: str,
        prompt: str,
    ):
        context = self._build_context(
            conversation_id,
            prompt,
        )

        full_response = ""

        for chunk in self.manager.stream_chat(context):
            full_response += chunk
            yield chunk

        self.conversation_service.add_assistant_message(
            conversation_id=conversation_id,
            message=full_response,
        )

    def clear_memory(
        self,
        conversation_id: str,
    ):
        self.conversation_service.clear(
            conversation_id=conversation_id,
        )