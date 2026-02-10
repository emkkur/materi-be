from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class DocumentBase(BaseModel):
    title: str = Field(..., description="The title of the document")
    content: str = Field(..., description="The content of the document")


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, description="The title of the document")
    content: Optional[str] = Field(None, description="The content of the document")


class DocumentResponse(DocumentBase):
    id: UUID = Field(default_factory=uuid4, description="The unique identifier of the document")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="The creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="The last update timestamp")

    model_config = ConfigDict(from_attributes=True)
