from collections import defaultdict

from app.ai.context_builder import ContextBuilder
from app.ai.manager import AIManager
from app.ai.prompt_engine import PromptEngine
from app.ai.rag.context_formatter import ContextFormatter
from app.ai.rag.retriever import Retriever
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.services.conversation_service import ConversationService


class ChatService:
    def __init__(
        self,
        manager: AIManager,
        conversation_service: ConversationService,
        document_repository: DocumentRepository,
    ):
        self.manager = manager
        self.conversation_service = conversation_service
        self.document_repository = document_repository

        prompt_engine = PromptEngine()
        self.context_builder = ContextBuilder(prompt_engine)

        self.retriever = Retriever()
        self.context_formatter = ContextFormatter()

    def _build_context(
        self,
        conversation_id: str,
        prompt: str,
        document_id: int | None = None,
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
            document_id=document_id,
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
                        "Answer using ONLY the retrieved document "
                        "context whenever possible.\n\n"
                        "Retrieved Context:\n\n"
                        f"{rag_context}"
                    ),
                },
            )

        return context, sources

    def _format_sources(
        self,
        sources: list[dict],
    ) -> str:
        if not sources:
            return ""

        grouped = defaultdict(list)

        for source in sources:
            document = self.document_repository.get_by_id(
                source["document_id"]
            )

            filename = (
                document.original_filename
                if document
                else f"Document {source['document_id']}"
            )

            grouped[filename].append(
                source["chunk_index"]
            )

        output = "\n\nSources:\n"

        for filename, chunks in grouped.items():
            chunks = sorted(set(chunks))

            output += (
                f"- {filename} "
                f"(Chunks: {', '.join(map(str, chunks))})\n"
            )

        return output

    def chat(
        self,
        conversation_id: str,
        prompt: str,
        document_id: int | None = None,
    ) -> str:
        context, sources = self._build_context(
            conversation_id,
            prompt,
            document_id,
        )

        response = self.manager.chat(context)

        self.conversation_service.add_assistant_message(
            conversation_id,
            response,
        )

        return response + self._format_sources(sources)

    def stream_chat(
        self,
        conversation_id: str,
        prompt: str,
        document_id: int | None = None,
    ):
        context, sources = self._build_context(
            conversation_id,
            prompt,
            document_id,
        )

        full_response = ""

        for chunk in self.manager.stream_chat(context):
            full_response += chunk
            yield chunk

        source_text = self._format_sources(sources)

        if source_text:
            full_response += source_text
            yield source_text

        self.conversation_service.add_assistant_message(
            conversation_id,
            full_response,
        )

    def clear_memory(
        self,
        conversation_id: str,
    ):
        self.conversation_service.clear(
            conversation_id,
        )