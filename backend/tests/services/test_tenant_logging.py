import pytest
from unittest.mock import patch, MagicMock
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
    db.delete = MagicMock()
    return db


# ===== CREATE TENANT LOGGING TESTS =====

def test_create_tenant_logs_info_on_start(mock_db):
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    mock_db.commit.side_effect = Exception("Test exception to stop execution")
    
    with patch.object(sut.logger, "info") as mock_info:
        with pytest.raises(Exception):
            sut.create_tenant(tenant_data, db=mock_db)
        mock_info.assert_called()
        assert "creating" in mock_info.call_args_list[0][0][0].lower()
        assert "acme" in mock_info.call_args_list[0][0][0].lower()


def test_create_tenant_logs_error_on_integrity_error(mock_db):
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    mock_db.commit.side_effect = IntegrityError("duplicate key", {}, None)
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.create_tenant(tenant_data, db=mock_db)
        mock_error.assert_called_once()
        assert "integrity" in mock_error.call_args[0][0].lower()


def test_create_tenant_logs_error_on_db_error(mock_db):
    tenant_data = TenantCreate(slug="acme", name="Acme Corporation")
    mock_db.commit.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.create_tenant(tenant_data, db=mock_db)
        mock_error.assert_called_once()
        assert "database error" in mock_error.call_args[0][0].lower()


# ===== GET TENANT BY SLUG LOGGING TESTS =====

def test_get_tenant_by_slug_logs_warning_when_not_found(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.get_tenant_by_slug("nonexistent", db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()


def test_get_tenant_by_slug_logs_error_on_db_error(mock_db):
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.get_tenant_by_slug("acme", db=mock_db)
        mock_error.assert_called()
        assert "database error" in mock_error.call_args[0][0].lower()


def test_get_tenant_by_slug_logs_info_on_success(mock_db):
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Acme Corporation"
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    
    with patch.object(sut.logger, "info") as mock_info:
        sut.get_tenant_by_slug("acme", db=mock_db)
        assert mock_info.call_count >= 2  # Start and success logs
        # Check success log
        success_log = [call for call in mock_info.call_args_list if "successfully" in call[0][0].lower()]
        assert len(success_log) > 0


# ===== GET TENANT BY ID LOGGING TESTS =====

def test_get_tenant_by_id_logs_warning_when_not_found(mock_db):
    dummy_id = uuid.uuid4()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.get_tenant_by_id(dummy_id, db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()


def test_get_tenant_by_id_logs_error_on_db_error(mock_db):
    dummy_id = uuid.uuid4()
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.get_tenant_by_id(dummy_id, db=mock_db)
        mock_error.assert_called()
        assert "database error" in mock_error.call_args[0][0].lower()


# ===== LIST TENANTS LOGGING TESTS =====

def test_list_tenants_logs_info_on_success(mock_db):
    dummy_tenants = [
        DummyTenant(id=uuid.uuid4(), slug="acme", name="Acme Corporation"),
        DummyTenant(id=uuid.uuid4(), slug="demo", name="Demo Company"),
    ]
    original_Tenant = sut.Tenant
    mock_tenant_class = MagicMock()
    mock_tenant_class.created_at = MagicMock()
    mock_tenant_class.created_at.asc = MagicMock(return_value="created_at_asc")
    sut.Tenant = mock_tenant_class
    
    mock_db.query.return_value.order_by.return_value.all.return_value = dummy_tenants
    
    with patch.object(sut.logger, "info") as mock_info:
        sut.list_tenants(db=mock_db)
        assert mock_info.call_count >= 2  # Start and success logs
        # Check success log mentions count
        success_log = [call for call in mock_info.call_args_list if "successfully" in call[0][0].lower()]
        assert len(success_log) > 0
    
    sut.Tenant = original_Tenant


def test_list_tenants_logs_error_on_db_error(mock_db):
    mock_db.query.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.list_tenants(db=mock_db)
        mock_error.assert_called()
        assert "database error" in mock_error.call_args[0][0].lower()


# ===== UPDATE TENANT LOGGING TESTS =====

def test_update_tenant_logs_warning_when_not_found(mock_db):
    update = TenantUpdate(name="New Name")
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.update_tenant("nonexistent", update, db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()


def test_update_tenant_logs_error_on_db_error(mock_db):
    update = TenantUpdate(name="New Name")
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Old Name"
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    mock_db.commit.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.update_tenant("acme", update, db=mock_db)
        mock_error.assert_called()
        assert "database error" in mock_error.call_args[0][0].lower()


def test_update_tenant_logs_info_on_success(mock_db):
    update = TenantUpdate(name="New Name")
    dummy_tenant = DummyTenant(
        id=uuid.uuid4(),
        slug="acme",
        name="Old Name"
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_tenant
    
    with patch.object(sut.logger, "info") as mock_info:
        sut.update_tenant("acme", update, db=mock_db)
        assert mock_info.call_count >= 2  # Start and success logs
        # Check success log
        success_log = [call for call in mock_info.call_args_list if "successfully" in call[0][0].lower()]
        assert len(success_log) > 0
