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
        document_id: int | None = None,
    ) -> list[dict]:
        """
        Retrieve the top matching chunks.

        If document_id is provided, only search
        within that document.
        """

        query_embedding = self.embedding_service.embed(
            query
        )

        where = None

        if document_id is not None:
            where = {
                "document_id": document_id,
            }

        results = self.vector_store.search(
            embedding=query_embedding,
            limit=limit,
            where=where,
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