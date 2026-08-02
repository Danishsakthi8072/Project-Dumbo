from app.ai.models import AIModel
from app.ai.ollama_provider import OllamaProvider

model = AIModel(
    name="qwen3:8b",
    provider="ollama",
    context_window=32768,
)

provider = OllamaProvider()
provider.load_model(model)

print("Sending prompt...")

response = provider.generate(
    "Say hello to Project Dumbo in one sentence."
)

print()
print(response)
