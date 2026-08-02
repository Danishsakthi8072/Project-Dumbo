from ollama import Client

from app.ai.models import AIModel
from app.ai.provider import AIProvider


class OllamaProvider(AIProvider):
    def __init__(self):
        self.client = Client(host="http://localhost:11434")
        self.model: AIModel | None = None

    def load_model(self, model: AIModel):
        self.model = model

    def unload_model(self):
        self.model = None

    def generate(self, prompt: str) -> str:
        if self.model is None:
            raise RuntimeError("No AI model loaded.")

        response = self.client.generate(
            model=self.model.name,
            prompt=prompt,
        )

        return response["response"]

    def chat(self, messages: list[dict]) -> str:
        if self.model is None:
            raise RuntimeError("No AI model loaded.")

        response = self.client.chat(
            model=self.model.name,
            messages=messages,
        )

        return response["message"]["content"]

    def embeddings(self, text: str):
        if self.model is None:
            raise RuntimeError("No AI model loaded.")

        return self.client.embeddings(
            model=self.model.name,
            prompt=text,
        )
