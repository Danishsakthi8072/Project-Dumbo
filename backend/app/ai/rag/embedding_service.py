import ollama


class EmbeddingService:
    """
    Generates embeddings using Ollama.
    """

    def __init__(
        self,
        model: str = "nomic-embed-text",
    ):
        self.model = model

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = ollama.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        response = ollama.embed(
            model=self.model,
            input=texts,
        )

        return response["embeddings"]