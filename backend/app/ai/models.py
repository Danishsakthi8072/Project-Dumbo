from dataclasses import dataclass


@dataclass
class AIModel:
    name: str
    provider: str
    context_window: int
    supports_chat: bool = True
    supports_vision: bool = False
    supports_tools: bool = False
    supports_embeddings: bool = False
