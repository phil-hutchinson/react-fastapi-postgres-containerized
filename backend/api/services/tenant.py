from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.tenant import Tenant
from api.schemas.tenant import TenantCreate, TenantRead, TenantUpdate
from typing import List
import logging
import uuid

logger = logging.getLogger(__name__)


def get_tenant_by_slug(slug: str, db: Session) -> dict:
    """Look up tenant by slug.
    
    Args:
        slug: The tenant slug to look up
        db: Database session
        
    Returns:
        Dictionary with tenant data
        
    Raises:
        HTTPException: 404 if tenant not found, 500 for database errors
    """
    logger.info(f"Fetching tenant by slug: {slug}")
    try:
        tenant = db.query(Tenant).filter_by(slug=slug).first()
        if not tenant:
            logger.warning(f"Tenant not found for slug: {slug}")
            raise HTTPException(status_code=404, detail="Tenant not found")
        logger.info(f"Successfully retrieved tenant: {tenant.name}")
        return {
            "id": tenant.id,
            "slug": tenant.slug,
            "name": tenant.name,
            "created_at": tenant.created_at,
            "is_active": tenant.is_active
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching tenant by slug {slug}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching tenant by slug {slug}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_tenant_by_id(tenant_id: uuid.UUID, db: Session) -> dict:
    """Get tenant by ID.
    
    Args:
        tenant_id: The tenant UUID to look up
        db: Database session
        
    Returns:
        Dictionary with tenant data
        
    Raises:
        HTTPException: 404 if tenant not found, 500 for database errors
    """
    logger.info(f"Fetching tenant by ID: {tenant_id}")
    try:
        tenant = db.query(Tenant).filter_by(id=tenant_id).first()
        if not tenant:
            logger.warning(f"Tenant not found for ID: {tenant_id}")
            raise HTTPException(status_code=404, detail="Tenant not found")
        logger.info(f"Successfully retrieved tenant: {tenant.name}")
        return {
            "id": tenant.id,
            "slug": tenant.slug,
            "name": tenant.name,
            "created_at": tenant.created_at,
            "is_active": tenant.is_active
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching tenant by ID {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching tenant by ID {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def create_tenant(tenant_data: TenantCreate, db: Session) -> dict:
    """Create new tenant.
    
    Args:
        tenant_data: Tenant creation data (slug, name)
        db: Database session
        
    Returns:
        Dictionary with created tenant data
        
    Raises:
        HTTPException: 409 if slug already exists, 500 for database errors
    """
    logger.info(f"Creating new tenant with slug: {tenant_data.slug}")
    try:
        db_tenant = Tenant(
            slug=tenant_data.slug,
            name=tenant_data.name
        )
        db.add(db_tenant)
        db.commit()
        db.refresh(db_tenant)
        logger.info(f"Successfully created tenant with ID: {db_tenant.id}")
        return {
            "id": db_tenant.id,
            "slug": db_tenant.slug,
            "name": db_tenant.name,
            "created_at": db_tenant.created_at,
            "is_active": db_tenant.is_active
        }
    except IntegrityError as e:
        logger.error(f"Integrity error while creating tenant: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=409, detail="Tenant with this slug already exists")
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating tenant: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while creating tenant: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def list_tenants(db: Session, include_inactive: bool = True) -> List[dict]:
    """Get all tenants.
    
    Args:
        db: Database session
        include_inactive: Whether to include inactive tenants (default: True)
        
    Returns:
        List of dictionaries with tenant data
        
    Raises:
        HTTPException: 500 for database errors
    """
    logger.info("Fetching all tenants")
    try:
        query = db.query(Tenant)
        if not include_inactive:
            query = query.filter_by(is_active=True)
        tenants = query.order_by(Tenant.created_at.asc()).all()
        logger.info(f"Successfully retrieved {len(tenants)} tenants")
        return [
            {
                "id": tenant.id,
                "slug": tenant.slug,
                "name": tenant.name,
                "created_at": tenant.created_at,
                "is_active": tenant.is_active
            }
            for tenant in tenants
        ]
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching tenants: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching tenants: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def update_tenant(slug: str, update_data: TenantUpdate, db: Session) -> dict:
    """Update tenant.
    
    Args:
        slug: The tenant slug to update
        update_data: Data to update (name, is_active)
        db: Database session
        
    Returns:
        Dictionary with updated tenant data
        
    Raises:
        HTTPException: 404 if tenant not found, 500 for database errors
    """
    logger.info(f"Updating tenant with slug: {slug}")
    try:
        tenant = db.query(Tenant).filter_by(slug=slug).first()
        if not tenant:
            logger.warning(f"Tenant not found for update, slug: {slug}")
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        if update_data.name is not None:
            tenant.name = update_data.name
        if update_data.is_active is not None:
            tenant.is_active = update_data.is_active
            
        db.commit()
        db.refresh(tenant)
        logger.info(f"Successfully updated tenant: {tenant.name}")
        return {
            "id": tenant.id,
            "slug": tenant.slug,
            "name": tenant.name,
            "created_at": tenant.created_at,
            "is_active": tenant.is_active
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating tenant {slug}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while updating tenant {slug}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
