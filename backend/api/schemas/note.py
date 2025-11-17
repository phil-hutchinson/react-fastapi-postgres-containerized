from pydantic import BaseModel
from typing import Optional
import uuid

# Default tenant UUID constant
DEFAULT_TENANT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")

class NoteCreate(BaseModel):
    name: str
    description: Optional[str] = None

class NoteSummary(BaseModel):
    uuid: str
    name: str

class NoteDetail(BaseModel):
    uuid: str
    name: str
    description: Optional[str] = None
    locked: bool  # Expose as locked for API

class NoteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
