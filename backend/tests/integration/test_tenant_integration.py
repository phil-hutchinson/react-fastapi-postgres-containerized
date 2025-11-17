import pytest
import uuid


class TestTenantIntegration:
    """Comprehensive integration tests for the Tenant API endpoints."""
    
    # ===== CREATE TENANT TESTS =====
    
    def test_create_tenant_integration(self, client):
        """Test creating a tenant via API."""
        # Arrange
        payload = {"slug": "integration-test", "name": "Integration Test Company"}
        
        # Act
        response = client.post("/tenants/", json=payload)
        
        # Assert
        assert response.status_code == 201
        created_tenant = response.json()
        assert created_tenant["slug"] == "integration-test"
        assert created_tenant["name"] == "Integration Test Company"
        assert created_tenant["is_active"] is True
        assert "id" in created_tenant
        assert "created_at" in created_tenant
        
        # Verify by fetching it back
        tenant_slug = created_tenant["slug"]
        get_response = client.get(f"/tenants/{tenant_slug}")
        assert get_response.status_code == 200
        retrieved_tenant = get_response.json()
        assert retrieved_tenant["id"] == created_tenant["id"]
        assert retrieved_tenant["slug"] == "integration-test"
        assert retrieved_tenant["name"] == "Integration Test Company"

    def test_create_tenant_duplicate_slug_raises_409(self, client):
        """Test that creating a tenant with duplicate slug raises 409."""
        # Arrange
        payload = {"slug": "duplicate-test", "name": "First Company"}
        client.post("/tenants/", json=payload)
        
        # Act
        duplicate_payload = {"slug": "duplicate-test", "name": "Second Company"}
        response = client.post("/tenants/", json=duplicate_payload)
        
        # Assert
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()

    # ===== GET TENANT BY SLUG TESTS =====
    
    def test_get_tenant_by_slug_success(self, client):
        """Test getting tenant by slug."""
        # Arrange
        payload = {"slug": "get-by-slug-test", "name": "Get By Slug Company"}
        create_response = client.post("/tenants/", json=payload)
        created_tenant = create_response.json()
        
        # Act
        response = client.get("/tenants/get-by-slug-test")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["id"] == created_tenant["id"]
        assert result["slug"] == "get-by-slug-test"
        assert result["name"] == "Get By Slug Company"
        assert result["is_active"] is True

    def test_get_tenant_by_slug_not_found_raises_404(self, client):
        """Test that getting non-existent tenant raises 404."""
        # Act
        response = client.get("/tenants/nonexistent-tenant")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    # ===== GET TENANT BY ID TESTS =====
    
    def test_get_tenant_by_id_success(self, client):
        """Test getting tenant by ID."""
        # Arrange
        payload = {"slug": "get-by-id-test", "name": "Get By ID Company"}
        create_response = client.post("/tenants/", json=payload)
        created_tenant = create_response.json()
        tenant_id = created_tenant["id"]
        
        # Act
        response = client.get(f"/tenants/id/{tenant_id}")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["id"] == tenant_id
        assert result["slug"] == "get-by-id-test"
        assert result["name"] == "Get By ID Company"
        assert result["is_active"] is True

    def test_get_tenant_by_id_not_found_raises_404(self, client):
        """Test that getting tenant with invalid ID raises 404."""
        # Arrange
        random_uuid = str(uuid.uuid4())
        
        # Act
        response = client.get(f"/tenants/id/{random_uuid}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    # ===== LIST TENANTS TESTS =====
    
    def test_list_tenants_empty_except_default(self, client):
        """Test listing tenants when only default tenant exists."""
        # Act
        response = client.get("/tenants/")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        # Check if default tenant exists
        default_tenant = [t for t in result if t["slug"] == "default"]
        assert len(default_tenant) == 1

    def test_list_tenants_with_data(self, client):
        """Test listing tenants with data, ensuring correct order."""
        # Arrange - get initial count (default tenant)
        initial_response = client.get("/tenants/")
        initial_count = len(initial_response.json())
        
        # Create tenants in specific order
        payload1 = {"slug": "list-test-1", "name": "First Tenant"}
        payload2 = {"slug": "list-test-2", "name": "Second Tenant"}
        
        client.post("/tenants/", json=payload1)
        client.post("/tenants/", json=payload2)
        
        # Act
        response = client.get("/tenants/")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == initial_count + 2
        
        # Find our created tenants
        created_tenants = [t for t in result if t["slug"] in ["list-test-1", "list-test-2"]]
        assert len(created_tenants) == 2
        
        # Verify they're in creation order (by created_at)
        list_test_1 = next(t for t in created_tenants if t["slug"] == "list-test-1")
        list_test_2 = next(t for t in created_tenants if t["slug"] == "list-test-2")
        assert list_test_1["created_at"] <= list_test_2["created_at"]

    def test_list_tenants_includes_all_active_by_default(self, client):
        """Test that list_tenants includes active tenants by default."""
        # Arrange
        payload = {"slug": "active-test", "name": "Active Tenant"}
        client.post("/tenants/", json=payload)
        
        # Act
        response = client.get("/tenants/?include_inactive=true")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        active_tenants = [t for t in result if t["slug"] == "active-test"]
        assert len(active_tenants) == 1
        assert active_tenants[0]["is_active"] is True

    def test_list_tenants_filters_inactive(self, client):
        """Test that list_tenants can filter out inactive tenants."""
        # Arrange - create and then deactivate a tenant
        payload = {"slug": "inactive-test", "name": "Inactive Tenant"}
        client.post("/tenants/", json=payload)
        
        # Deactivate it
        update = {"is_active": False}
        client.put("/tenants/inactive-test", json=update)
        
        # Act
        response_with_inactive = client.get("/tenants/?include_inactive=true")
        response_without_inactive = client.get("/tenants/?include_inactive=false")
        
        # Assert
        result_with = response_with_inactive.json()
        result_without = response_without_inactive.json()
        
        inactive_in_full_list = [t for t in result_with if t["slug"] == "inactive-test"]
        inactive_in_filtered_list = [t for t in result_without if t["slug"] == "inactive-test"]
        
        assert len(inactive_in_full_list) == 1
        assert len(inactive_in_filtered_list) == 0

    # ===== UPDATE TENANT TESTS =====
    
    def test_update_tenant_name_success(self, client):
        """Test updating tenant name."""
        # Arrange
        payload = {"slug": "update-name-test", "name": "Old Name"}
        client.post("/tenants/", json=payload)
        
        # Act
        update = {"name": "New Name"}
        response = client.put("/tenants/update-name-test", json=update)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["slug"] == "update-name-test"
        assert result["name"] == "New Name"
        assert result["is_active"] is True
        
        # Verify persistence
        get_response = client.get("/tenants/update-name-test")
        fetched = get_response.json()
        assert fetched["name"] == "New Name"

    def test_update_tenant_is_active_success(self, client):
        """Test updating tenant is_active status."""
        # Arrange
        payload = {"slug": "update-active-test", "name": "Test Tenant"}
        client.post("/tenants/", json=payload)
        
        # Act
        update = {"is_active": False}
        response = client.put("/tenants/update-active-test", json=update)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["slug"] == "update-active-test"
        assert result["is_active"] is False
        
        # Verify persistence
        get_response = client.get("/tenants/update-active-test")
        fetched = get_response.json()
        assert fetched["is_active"] is False

    def test_update_tenant_both_fields_success(self, client):
        """Test updating both name and is_active."""
        # Arrange
        payload = {"slug": "update-both-test", "name": "Old Name"}
        client.post("/tenants/", json=payload)
        
        # Act
        update = {"name": "New Name", "is_active": False}
        response = client.put("/tenants/update-both-test", json=update)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["name"] == "New Name"
        assert result["is_active"] is False

    def test_update_tenant_not_found_raises_404(self, client):
        """Test that updating non-existent tenant raises 404."""
        # Arrange
        update = {"name": "New Name"}
        
        # Act
        response = client.put("/tenants/nonexistent-tenant", json=update)
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_tenant_partial_update(self, client):
        """Test that partial updates don't affect other fields."""
        # Arrange
        payload = {"slug": "partial-update-test", "name": "Original Name"}
        client.post("/tenants/", json=payload)
        
        # Act - only update name
        update = {"name": "Updated Name"}
        response = client.put("/tenants/partial-update-test", json=update)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["name"] == "Updated Name"
        assert result["is_active"] is True  # Should still be True

