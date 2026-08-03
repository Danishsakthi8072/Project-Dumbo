from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.manager import AIManager
from app.ai.models import AIModel
from app.ai.ollama_provider import OllamaProvider
from app.ai.rag.pipeline import RAGPipeline
from app.core.database import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.document_chunk_service import (
    DocumentChunkService,
)
from app.services.document_service import DocumentService
from app.services.user_service import UserService


# -----------------------------
# User Dependencies
# -----------------------------

def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


# -----------------------------
# Conversation Dependencies
# -----------------------------

def get_conversation_repository(
    db: Session = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_conversation_service(
    repository: ConversationRepository = Depends(
        get_conversation_repository,
    ),
) -> ConversationService:
    return ConversationService(repository)


# -----------------------------
# Document Chunk Dependencies
# -----------------------------

def get_document_chunk_repository(
    db: Session = Depends(get_db),
) -> DocumentChunkRepository:
    return DocumentChunkRepository(db)


def get_document_chunk_service(
    repository: DocumentChunkRepository = Depends(
        get_document_chunk_repository,
    ),
) -> DocumentChunkService:
    return DocumentChunkService(repository)


def get_rag_pipeline(
    chunk_service: DocumentChunkService = Depends(
        get_document_chunk_service,
    ),
) -> RAGPipeline:
    return RAGPipeline(chunk_service)


# -----------------------------
# Document Dependencies
# -----------------------------

def get_document_repository(
    db: Session = Depends(get_db),
) -> DocumentRepository:
    return DocumentRepository(db)


def get_document_service(
    repository: DocumentRepository = Depends(
        get_document_repository,
    ),
    rag_pipeline: RAGPipeline = Depends(
        get_rag_pipeline,
    ),
) -> DocumentService:
    return DocumentService(
        repository=repository,
        rag_pipeline=rag_pipeline,
    )


# -----------------------------
# AI Singleton
# -----------------------------

provider = OllamaProvider()

model = AIModel(
    name="qwen3:8b",
    provider="ollama",
    context_window=32768,
)

ai_manager = AIManager()
ai_manager.load_provider(provider)
ai_manager.load_model(model)


def get_ai_manager() -> AIManager:
    return ai_manager


def get_chat_service(
    conversation_service: ConversationService = Depends(
        get_conversation_service,
    ),
    document_repository: DocumentRepository = Depends(
        get_document_repository,
    ),
) -> ChatService:
    return ChatService(
        manager=ai_manager,
        conversation_service=conversation_service,
        document_repository=document_repository,
    )