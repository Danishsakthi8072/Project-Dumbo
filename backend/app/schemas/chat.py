from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    document_id: int | None = None


class ChatResponse(BaseModel):
    response: str