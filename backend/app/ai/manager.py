from app.ai.models import AIModel


class AIManager:
    def __init__(self):
        self.current_model: AIModel | None = None

    def load_model(self, model: AIModel):
        self.current_model = model

    def unload_model(self):
        self.current_model = None

    def get_current_model(self):
        return self.current_model

    def is_loaded(self):
        return self.current_model is not None
