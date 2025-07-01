from pydantic import BaseModel
from typing import Optional

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
    finalized: bool

class NoteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
