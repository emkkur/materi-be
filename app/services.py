from typing import List, Optional
from uuid import UUID

from .models import DocumentCreate, DocumentResponse, DocumentUpdate


class DocumentService:
    def __init__(self):
        # In-memory storage for simplicity
        self.documents: dict[UUID, DocumentResponse] = {}

    def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        document = DocumentResponse(**document_data.model_dump())
        self.documents[document.id] = document
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
        return updated_document

    def delete_document(self, document_id: UUID) -> bool:
        if document_id in self.documents:
            del self.documents[document_id]
            return True
        return False
