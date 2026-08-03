from typing import List


class TextChunker:
    """
    Splits text into overlapping chunks.

    Example:
        chunk_size = 1000
        overlap = 200

        Chunk 1:
        0 -------- 1000

        Chunk 2:
              800 -------- 1800
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        """

        text = text.strip()

        if not text:
            return []

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(
                start + self.chunk_size,
                text_length,
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - self.overlap

        return chunks