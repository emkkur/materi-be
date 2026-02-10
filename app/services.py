import json
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from .models import DocumentCreate, DocumentResponse, DocumentUpdate

DATA_FILE = Path("data.json")


class DocumentService:
    def __init__(self):
        self.documents: dict[UUID, DocumentResponse] = {}
        self._load_documents()

    def _load_documents(self):
        if not DATA_FILE.exists():
            return

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    doc = DocumentResponse(**item)
                    self.documents[doc.id] = doc
        except (json.JSONDecodeError, ValueError):
            # If file is empty or corrupted, start fresh
            pass

    def _save_documents(self):
        data = [doc.model_dump(mode="json") for doc in self.documents.values()]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        document = DocumentResponse(**document_data.model_dump())
        self.documents[document.id] = document
        self._save_documents()
        return document

    def get_document(self, document_id: UUID) -> Optional[DocumentResponse]:
        return self.documents.get(document_id)

    def list_documents(self) -> List[DocumentResponse]:
        return list(self.documents.values())

    def update_document(
        self, document_id: UUID, document_data: DocumentUpdate
    ) -> Optional[DocumentResponse]:
        existing_document = self.documents.get(document_id)
        if not existing_document:
            return None

        update_data = document_data.model_dump(exclude_unset=True)
        updated_document = existing_document.model_copy(update=update_data)
        self.documents[document_id] = updated_document
        self._save_documents()
        return updated_document

    def delete_document(self, document_id: UUID) -> bool:
        if document_id in self.documents:
            del self.documents[document_id]
            self._save_documents()
            return True
        return False
