from app.ai.rag.embedding_service import EmbeddingService
from app.ai.rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant document chunks
    for a user query.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Retrieve the top matching chunks.
        """

        query_embedding = self.embedding_service.embed(
            query
        )

        results = self.vector_store.search(
            embedding=query_embedding,
            limit=limit,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        retrieved_chunks = []

        for chunk_id, text, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_chunks