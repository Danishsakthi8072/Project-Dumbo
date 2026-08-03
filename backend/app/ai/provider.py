from abc import ABC, abstractmethod

from app.ai.models import AIModel


class AIProvider(ABC):
    @abstractmethod
    def load_model(self, model: AIModel):
        pass

    @abstractmethod
    def unload_model(self):
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        pass

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
    ) -> str:
        pass

    @abstractmethod
    def stream_chat(
        self,
        messages: list[dict],
    ):
        """
        Stream the model response chunk by chunk.
        """
        pass

    @abstractmethod
    def embeddings(
        self,
        text: str,
    ):
        pass