from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class TenantCreate(BaseModel):
    slug: str = Field(..., description="URL-friendly identifier for the tenant")
    name: str = Field(..., description="Display name of the tenant")


class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    slug: str
    name: str
    created_at: datetime
    is_active: bool


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
