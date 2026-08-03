from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository

        project_root = Path(__file__).resolve().parents[3]
        self.upload_dir = project_root / "uploads"

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload_document(
        self,
        file: UploadFile,
    ) -> Document:
        extension = Path(file.filename).suffix.lower()

        unique_filename = f"{uuid4().hex}{extension}"

        file_path = self.upload_dir / unique_filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_type=extension.replace(".", ""),
            file_path=str(file_path),
        )

        return self.repository.create(document)

    def list_documents(self):
        return self.repository.list_documents()

    def get_document(
        self,
        document_id: int,
    ):
        return self.repository.get_by_id(document_id)

    def delete_document(
        self,
        document: Document,
    ):
        file_path = Path(document.file_path)

        if file_path.exists():
            file_path.unlink()

        self.repository.delete(document)