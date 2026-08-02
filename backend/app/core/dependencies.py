from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.chat import ChatService
from app.ai.manager import AIManager
from app.ai.models import AIModel
from app.ai.ollama_provider import OllamaProvider
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
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
    manager: AIManager = Depends(get_ai_manager),
) -> ChatService:
    return ChatService(manager)