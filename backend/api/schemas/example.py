from pydantic import BaseModel
from typing import Optional

class ExampleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleSummary(BaseModel):
    uuid: str
    name: str

class ExampleDetail(BaseModel):
    uuid: str
    name: str
    description: Optional[str] = None

class ExampleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
