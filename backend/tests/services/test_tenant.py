import pytest
from unittest.mock import MagicMock
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import uuid
from api.services import tenant as sut
from api.schemas.tenant import TenantCreate, TenantUpdate


class DummyTenant:
    def __init__(self, id, slug, name, created_at=None, is_active=True):
        self.id = id
        self.slug = slug
        self.name = name
        self.created_at = created_at or datetime.now()
        self.is_active = is_active


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    db.rollback = MagicMock()
    return db


# ===== CREATE TENANT TESTS =====

def test_create_tenant_success(mock_db):
    # Arrange
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    dummy_id = uuid.uuid4()
    dummy_created_at = datetime.now()
    dummy_tenant = DummyTenant(
        id=dummy_id,
        slug=tenant_data.slug,
        name=tenant_data.name,
        created_at=dummy_created_at,
        is_active=True
    )
    mock_db.refresh.side_effect = lambda obj: None
    # Patch Tenant constructor to return dummy_tenant
    original_Tenant = sut.Tenant
    sut.Tenant = lambda slug, name: dummy_tenant

    # Act
    result = sut.create_tenant(tenant_data, db=mock_db)

    # Restore
    sut.Tenant = original_Tenant

    # Assert
    assert result["id"] == dummy_id
    assert result["slug"] == tenant_data.slug
    assert result["name"] == tenant_data.name
    assert result["created_at"] == dummy_created_at
    assert result["is_active"] is True
    mock_db.add.assert_called_once_with(dummy_tenant)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(dummy_tenant)


def test_create_tenant_duplicate_slug_raises_409(mock_db):
    # Arrange
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    mock_db.commit.side_effect = IntegrityError("duplicate key", {}, None)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.create_tenant(tenant_data, db=mock_db)
    assert exc_info.value.status_code == 409
    assert "already exists" in str(exc_info.value.detail).lower()
    mock_db.rollback.assert_called_once()


def test_create_tenant_database_error_raises_500(mock_db):
    # Arrange
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    mock_db.commit.side_effect = SQLAlchemyError("Database connection failed")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.create_tenant(tenant_data, db=mock_db)
    assert exc_info.value.status_code == 500
    assert "Database error" in str(exc_info.value.detail)
    mock_db.rollback.assert_called_once()


# ===== GET TENANT BY SLUG TESTS =====

def test_get_tenant_by_slug_success(mock_db):
    # Arrange
    dummy_id = uuid.uuid4()
    dummy_tenant = DummyTenant(
        id=dummy_id,
        slug="acme",
        name="Acme Corporation",
        created_at=datetime.now(),
        is_active=True
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant

    # Act
    result = sut.get_tenant_by_slug("acme", db=mock_db)

    # Assert
    assert isinstance(result, dict)
    assert result["id"] == dummy_id
    assert result["slug"] == "acme"
    assert result["name"] == "Acme Corporation"
    assert result["is_active"] is True


def test_get_tenant_by_slug_not_found_raises_404(mock_db):
    # Arrange
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.get_tenant_by_slug("nonexistent", db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Tenant not found" in str(exc_info.value.detail)


def test_get_tenant_by_slug_database_error_raises_500(mock_db):
    # Arrange
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.get_tenant_by_slug("acme", db=mock_db)
    assert exc_info.value.status_code == 500
    assert "Database error" in str(exc_info.value.detail)


# ===== GET TENANT BY ID TESTS =====

def test_get_tenant_by_id_success(mock_db):
    # Arrange
    dummy_id = uuid.uuid4()
    dummy_tenant = DummyTenant(
        id=dummy_id,
        slug="acme",
        name="Acme Corporation",
        created_at=datetime.now(),
        is_active=True
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant

    # Act
    result = sut.get_tenant_by_id(dummy_id, db=mock_db)

    # Assert
    assert isinstance(result, dict)
    assert result["id"] == dummy_id
    assert result["slug"] == "acme"
    assert result["name"] == "Acme Corporation"
    assert result["is_active"] is True


def test_get_tenant_by_id_not_found_raises_404(mock_db):
    # Arrange
    dummy_id = uuid.uuid4()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.get_tenant_by_id(dummy_id, db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Tenant not found" in str(exc_info.value.detail)


def test_get_tenant_by_id_database_error_raises_500(mock_db):
    # Arrange
    dummy_id = uuid.uuid4()
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.get_tenant_by_id(dummy_id, db=mock_db)
    assert exc_info.value.status_code == 500
    assert "Database error" in str(exc_info.value.detail)


# ===== LIST TENANTS TESTS =====

def test_list_tenants_success(mock_db):
    # Arrange
    dummy_tenants = [
        DummyTenant(id=uuid.uuid4(), slug="acme", name="Acme Corporation"),
        DummyTenant(id=uuid.uuid4(), slug="demo", name="Demo Company"),
    ]
    # Store original Tenant class
    original_Tenant = sut.Tenant
    # Create a mock Tenant class with created_at attribute for order_by
    mock_tenant_class = MagicMock()
    mock_tenant_class.created_at = MagicMock()
    mock_tenant_class.created_at.asc = MagicMock(return_value="created_at_asc")
    sut.Tenant = mock_tenant_class
    
    mock_db.query.return_value.order_by.return_value.all.return_value = dummy_tenants

    # Act
    result = sut.list_tenants(db=mock_db)
    
    # Restore
    sut.Tenant = original_Tenant

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["slug"] == "acme"
    assert result[0]["name"] == "Acme Corporation"
    assert result[1]["slug"] == "demo"
    assert result[1]["name"] == "Demo Company"


def test_list_tenants_empty(mock_db):
    # Arrange
    original_Tenant = sut.Tenant
    mock_tenant_class = MagicMock()
    mock_tenant_class.created_at = MagicMock()
    mock_tenant_class.created_at.asc = MagicMock(return_value="created_at_asc")
    sut.Tenant = mock_tenant_class
    
    mock_db.query.return_value.order_by.return_value.all.return_value = []

    # Act
    result = sut.list_tenants(db=mock_db)
    
    # Restore
    sut.Tenant = original_Tenant

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0


def test_list_tenants_filters_inactive(mock_db):
    # Arrange
    dummy_tenants = [
        DummyTenant(id=uuid.uuid4(), slug="acme", name="Acme Corporation", is_active=True),
    ]
    original_Tenant = sut.Tenant
    mock_tenant_class = MagicMock()
    mock_tenant_class.created_at = MagicMock()
    mock_tenant_class.created_at.asc = MagicMock(return_value="created_at_asc")
    sut.Tenant = mock_tenant_class
    
    # Create mock chain for query with filter_by
    mock_query = MagicMock()
    mock_query.filter_by.return_value.order_by.return_value.all.return_value = dummy_tenants
    mock_db.query.return_value = mock_query

    # Act
    result = sut.list_tenants(db=mock_db, include_inactive=False)
    
    # Restore
    sut.Tenant = original_Tenant

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["is_active"] is True
    # Verify filter_by was called with is_active=True
    mock_query.filter_by.assert_called_once_with(is_active=True)


def test_list_tenants_database_error_raises_500(mock_db):
    # Arrange
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.list_tenants(db=mock_db)
    assert exc_info.value.status_code == 500
    assert "Database error" in str(exc_info.value.detail)


# ===== UPDATE TENANT TESTS =====

def test_update_tenant_success(mock_db):
    # Arrange
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Old Name",
        created_at=datetime.now(),
        is_active=True
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    update = TenantUpdate(name="New Name", is_active=False)

    # Act
    result = sut.update_tenant("acme", update, db=mock_db)

    # Assert
    assert result["slug"] == "acme"
    assert result["name"] == "New Name"
    assert result["is_active"] is False
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(dummy_tenant)


def test_update_tenant_partial_update(mock_db):
    # Arrange
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Old Name",
        created_at=datetime.now(),
        is_active=True
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    update = TenantUpdate(name="New Name")  # Only update name

    # Act
    result = sut.update_tenant("acme", update, db=mock_db)

    # Assert
    assert result["name"] == "New Name"
    assert result["is_active"] is True  # Should remain unchanged


def test_update_tenant_not_found_raises_404(mock_db):
    # Arrange
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    update = TenantUpdate(name="New Name")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.update_tenant("nonexistent", update, db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Tenant not found" in str(exc_info.value.detail)


def test_update_tenant_database_error_raises_500(mock_db):
    # Arrange
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Old Name",
        created_at=datetime.now(),
        is_active=True
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    mock_db.commit.side_effect = SQLAlchemyError("Database connection failed")
    update = TenantUpdate(name="New Name")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.update_tenant("acme", update, db=mock_db)
    assert exc_info.value.status_code == 500
    assert "Database error" in str(exc_info.value.detail)
    mock_db.rollback.assert_called_once()
