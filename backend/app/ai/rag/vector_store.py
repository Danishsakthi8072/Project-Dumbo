from pathlib import Path

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection


class VectorStore:
    def __init__(
        self,
        collection_name: str = "document_chunks",
    ):
        project_root = Path(__file__).resolve().parents[4]
        chroma_path = project_root / "backend" / "chroma_db"

        chroma_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = PersistentClient(
            path=str(chroma_path),
        )

        self.collection: Collection = (
            self.client.get_or_create_collection(
                name=collection_name,
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
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
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

    def count(self) -> int:
        return self.collection.count()