from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.tenant import TenantCreate, TenantRead, TenantUpdate
from api.services import tenant as tenant_service
from typing import List
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=TenantRead, status_code=201)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    """Create a new tenant."""
    logger.info(f"API: Creating new tenant with slug: {tenant.slug}")
    result = tenant_service.create_tenant(tenant, db=db)
    return result


@router.get("/{slug}", response_model=TenantRead)
def get_tenant_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a tenant by slug."""
    logger.info(f"API: Fetching tenant by slug: {slug}")
    result = tenant_service.get_tenant_by_slug(slug, db=db)
    return result


@router.get("/id/{tenant_id}", response_model=TenantRead)
def get_tenant_by_id(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a tenant by ID."""
    logger.info(f"API: Fetching tenant by ID: {tenant_id}")
    result = tenant_service.get_tenant_by_id(tenant_id, db=db)
    return result


@router.get("/", response_model=List[TenantRead])
def list_tenants(include_inactive: bool = False, db: Session = Depends(get_db)):
    """List all tenants, optionally including inactive ones."""
    logger.info(f"API: Listing tenants (include_inactive={include_inactive})")
    result = tenant_service.list_tenants(db=db, include_inactive=include_inactive)
    return result


@router.put("/{slug}", response_model=TenantRead)
def update_tenant(slug: str, update: TenantUpdate, db: Session = Depends(get_db)):
    """Update a tenant."""
    logger.info(f"API: Updating tenant with slug: {slug}")
    result = tenant_service.update_tenant(slug, update, db=db)
    return result
