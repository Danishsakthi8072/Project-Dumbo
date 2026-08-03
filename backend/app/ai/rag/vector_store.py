from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection


class VectorStore:
    """
    Handles storing and retrieving embeddings
    from ChromaDB.
    """

    def __init__(
        self,
        path: str = "./chroma_db",
        collection_name: str = "document_chunks",
    ):
        self.client = PersistentClient(path=path)

        self.collection: Collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add(
        self,
        chunk_id: str,
        embedding: list[float],
        text: str,
        metadata: dict,
    ):
        self.collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )

    def add_many(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        texts: list[str],
        metadatas: list[dict],
    ):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
        )

    def delete(
        self,
        chunk_id: str,
    ):
        self.collection.delete(
            ids=[chunk_id],
        )

    def delete_many(
        self,
        ids: list[str],
    ):
        self.collection.delete(
            ids=ids,
        )

    def count(
        self,
    ) -> int:
        return self.collection.count()