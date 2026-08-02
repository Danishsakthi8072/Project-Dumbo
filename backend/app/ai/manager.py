from app.ai.models import AIModel
from app.ai.provider import AIProvider


class AIManager:
    def __init__(self):
        self.current_provider: AIProvider | None = None
        self.current_model: AIModel | None = None

    def load_provider(self, provider: AIProvider):
        self.current_provider = provider

    def load_model(self, model: AIModel):
        if self.current_provider is None:
            raise RuntimeError("No AI provider loaded.")

        self.current_provider.load_model(model)
        self.current_model = model

    def unload_model(self):
        if self.current_provider is not None:
            self.current_provider.unload_model()

        self.current_model = None

    def get_current_provider(self):
        return self.current_provider

    def get_current_model(self):
        return self.current_model

    def is_loaded(self):
        return (
            self.current_provider is not None
            and self.current_model is not None
        )

    def generate(self, prompt: str) -> str:
        if not self.is_loaded():
            raise RuntimeError("No AI model loaded.")

        return self.current_provider.generate(prompt)

    def chat(self, messages: list[dict]) -> str:
        if not self.is_loaded():
            raise RuntimeError("No AI model loaded.")

        return self.current_provider.chat(messages)

    def embeddings(self, text: str):
        if not self.is_loaded():
            raise RuntimeError("No AI model loaded.")

        return self.current_provider.embeddings(text)