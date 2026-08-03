from app.ai.context_builder import ContextBuilder
from app.ai.manager import AIManager
from app.ai.prompt_engine import PromptEngine
from app.ai.rag.context_formatter import ContextFormatter
from app.ai.rag.retriever import Retriever
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

        self.retriever = Retriever()
        self.context_formatter = ContextFormatter()

    def _build_context(
        self,
        conversation_id: str,
        prompt: str,
    ) -> tuple[list[dict], list[dict]]:
        self.conversation_service.add_user_message(
            conversation_id=conversation_id,
            message=prompt,
        )

        conversation = self.conversation_service.get_messages(
            conversation_id=conversation_id,
        )

        context = self.context_builder.build(conversation)

        retrieved_chunks = self.retriever.retrieve(
            query=prompt,
            limit=5,
        )

        rag_context, sources = self.context_formatter.format(
            retrieved_chunks
        )

        if rag_context:
            context.insert(
                1,
                {
                    "role": "system",
                    "content": (
                        "You are Project Dumbo.\n\n"
                        "Answer ONLY using the retrieved document "
                        "context whenever possible.\n\n"
                        "Retrieved Document Context:\n\n"
                        f"{rag_context}"
                    ),
                },
            )

        return context, sources

    def chat(
        self,
        conversation_id: str,
        prompt: str,
    ) -> str:
        context, sources = self._build_context(
            conversation_id,
            prompt,
        )

        response = self.manager.chat(context)

        self.conversation_service.add_assistant_message(
            conversation_id=conversation_id,
            message=response,
        )

        if sources:
            response += "\n\nSources:\n"

            for source in sources:
                response += (
                    f"- Document ID: {source['document_id']}, "
                    f"Chunk: {source['chunk_index']}\n"
                )

        return response

    def stream_chat(
        self,
        conversation_id: str,
        prompt: str,
    ):
        context, sources = self._build_context(
            conversation_id,
            prompt,
        )

        full_response = ""

        for chunk in self.manager.stream_chat(context):
            full_response += chunk
            yield chunk

        if sources:
            citation_text = "\n\nSources:\n"

            for source in sources:
                citation_text += (
                    f"- Document ID: {source['document_id']}, "
                    f"Chunk: {source['chunk_index']}\n"
                )

            full_response += citation_text
            yield citation_text

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