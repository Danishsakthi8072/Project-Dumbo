from app.ai.manager import AIManager


class ChatService:
    def __init__(self, manager: AIManager):
        self.manager = manager

    def chat(self, prompt: str) -> str:
        return self.manager.generate(prompt)