from app.ai.rag.chunker import TextChunker
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)


class DocumentChunkService:
    def __init__(
        self,
        repository: DocumentChunkRepository,
    ):
        self.repository = repository
        self.chunker = TextChunker()

    def create_chunks(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        """
        Split a document into chunks and store them.
        """

        chunks = self.chunker.chunk(
            document.extracted_text
        )

        document_chunks = []

        for index, chunk in enumerate(chunks):
            document_chunks.append(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                )
            )

        return self.repository.create_many(
            document_chunks
        )

    def get_chunks(
        self,
        document_id: int,
    ) -> list[DocumentChunk]:
        return self.repository.get_by_document_id(
            document_id
        )

    def delete_chunks(
        self,
        document_id: int,
    ):
        self.repository.delete_by_document_id(
            document_id
        )