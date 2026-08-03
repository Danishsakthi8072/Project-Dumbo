from app.ai.rag.embedding_service import EmbeddingService
from app.ai.rag.vector_store import VectorStore
from app.models.document import Document
from app.services.document_chunk_service import (
    DocumentChunkService,
)


class RAGPipeline:
    """
    Complete RAG indexing pipeline.

    Document
        ↓
    Chunk
        ↓
    Store Chunks
        ↓
    Generate Embeddings
        ↓
    Store in ChromaDB
    """

    def __init__(
        self,
        chunk_service: DocumentChunkService,
    ):
        self.chunk_service = chunk_service
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def process_document(
        self,
        document: Document,
    ):
        """
        Index a document for semantic search.
        """

        chunks = self.chunk_service.create_chunks(
            document
        )

        for chunk in chunks:
            embedding = self.embedding_service.embed(
                chunk.content
            )

            self.vector_store.add(
                chunk_id=str(chunk.id),
                embedding=embedding,
                text=chunk.content,
                metadata={
                    "document_id": document.id,
                    "chunk_index": chunk.chunk_index,
                },
            )