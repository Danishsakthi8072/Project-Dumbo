class ContextFormatter:
    """
    Formats retrieved document chunks into
    a structured context for the LLM.
    """

    def format(
        self,
        chunks: list[dict],
    ) -> tuple[str, list[dict]]:
        """
        Returns:
            context: str
            sources: list[dict]
        """

        if not chunks:
            return "", []

        sections = []
        sources = []

        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk.get("metadata", {})

            document_id = metadata.get("document_id")
            chunk_index = metadata.get("chunk_index")

            sections.append(
                f"""Document Chunk {index}

Document ID: {document_id}
Chunk Index: {chunk_index}

Content:
{chunk["text"]}"""
            )

            sources.append(
                {
                    "document_id": document_id,
                    "chunk_index": chunk_index,
                }
            )

        context = "\n\n-----------------------------\n\n".join(
            sections
        )

        return context, sources