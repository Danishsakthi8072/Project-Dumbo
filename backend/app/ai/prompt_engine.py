from app.ai.prompts import SYSTEM_PROMPT


class PromptEngine:
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def get_system_prompt(self) -> str:
        """
        Return the default system prompt for Project Dumbo.
        """
        return self.system_prompt