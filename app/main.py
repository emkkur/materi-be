from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from .models import DocumentCreate, DocumentResponse, DocumentUpdate
from .services import DocumentService

app = FastAPI()
document_service = DocumentService()


@app.post("/document", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(document: DocumentCreate):
    return document_service.create_document(document)


@app.get("/documents", response_model=List[DocumentResponse])
async def list_documents():
    return document_service.list_documents()


@app.get("/document/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: UUID):
    document = document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.patch("/document/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: UUID, document_update: DocumentUpdate):
    document = document_service.update_document(document_id, document_update)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.delete("/document/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: UUID):
    if not document_service.delete_document(document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return
