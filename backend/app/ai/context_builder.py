from app.ai.prompt_engine import PromptEngine


class ContextBuilder:
    def __init__(
        self,
        prompt_engine: PromptEngine,
    ):
        self.prompt_engine = prompt_engine

    def build(
        self,
        conversation: list[dict],
    ) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": self.prompt_engine.get_system_prompt(),
            }
        ]

        messages.extend(conversation)

        return messages