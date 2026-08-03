from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.core.dependencies import (
    get_chat_service,
    get_document_service,
    get_user_service,
)
from app.core.security import get_current_user_id
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.document import DocumentResponse
from app.schemas.user import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "status": "running",
    }


@router.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Users
# -----------------------------

@router.get("/users", response_model=list[UserResponse])
def list_users(
    service: UserService = Depends(get_user_service),
):
    return service.list_users()


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(user)


@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    service: UserService = Depends(get_user_service),
):
    return service.login(user.email, user.password)


@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: int = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return service.get_current_user(user_id)


# -----------------------------
# Chat
# -----------------------------

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    response = service.chat(
        conversation_id=request.conversation_id,
        prompt=request.message,
    )

    return ChatResponse(
        response=response,
    )


@router.post("/chat/stream")
def stream_chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    return StreamingResponse(
        service.stream_chat(
            conversation_id=request.conversation_id,
            prompt=request.message,
        ),
        media_type="text/plain",
    )


# -----------------------------
# Documents
# -----------------------------

@router.post(
    "/documents/upload",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    return service.upload_document(file)


@router.get(
    "/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    service: DocumentService = Depends(get_document_service),
):
    return service.list_documents()