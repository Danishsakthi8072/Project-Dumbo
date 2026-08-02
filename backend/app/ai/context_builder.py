from app.ai.prompts import SYSTEM_PROMPT


class ContextBuilder:
    def build(
        self,
        messages: list[dict],
    ) -> list[dict]:
        context = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        context.extend(messages)

        return context