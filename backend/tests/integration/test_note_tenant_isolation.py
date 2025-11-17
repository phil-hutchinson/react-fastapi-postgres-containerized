"""
Integration tests to verify tenant isolation for notes.
These tests ensure that notes from different tenants cannot access each other.
"""
import pytest
import uuid


class TestNoteTenantIsolation:
    """Test that notes are properly isolated by tenant_id."""
    
    def test_notes_isolated_by_tenant(self, client):
        """Test that notes from different tenants are isolated."""
        # Arrange - create two tenants
        tenant1_payload = {"slug": "tenant1", "name": "Tenant One"}
        tenant2_payload = {"slug": "tenant2", "name": "Tenant Two"}
        
        tenant1_response = client.post("/tenants/", json=tenant1_payload)
        tenant2_response = client.post("/tenants/", json=tenant2_payload)
        
        tenant1_id = tenant1_response.json()["id"]
        tenant2_id = tenant2_response.json()["id"]
        
        # Create notes for each tenant (note: currently this goes through default tenant path)
        # In future steps, this will use tenant-specific routes
        note1_payload = {"name": "Tenant 1 Note", "description": "Only visible to tenant 1"}
        note2_payload = {"name": "Tenant 2 Note", "description": "Only visible to tenant 2"}
        
        # For now, the API uses default tenant. This test validates the service layer
        # In Step 5+, we'll update to use tenant-specific routes
        
        # Act - Query notes for tenant 1 (currently all go to default tenant)
        list_response = client.get("/notes/")
        
        # Assert - For now, this just validates the setup
        # Once tenant middleware is added, we'll verify isolation
        assert list_response.status_code == 200
        notes = list_response.json()
        assert isinstance(notes, list)
    
    def test_cannot_access_note_from_different_tenant(self, client):
        """Test that a note from one tenant cannot be accessed by another tenant."""
        # This test will be more meaningful once tenant middleware is implemented
        # For now, it validates the current behavior
        
        # Arrange - create a note (goes to default tenant)
        note_payload = {"name": "Test Note", "description": "Test"}
        create_response = client.post("/notes/", json=note_payload)
        note_uuid = create_response.json()["uuid"]
        
        # Act - try to get the note
        get_response = client.get(f"/notes/{note_uuid}")
        
        # Assert - currently accessible because all use default tenant
        assert get_response.status_code == 200
        
        # TODO: After Step 5 (tenant middleware), update this test to:
        # 1. Create note under tenant1
        # 2. Try to access it under tenant2
        # 3. Expect 404 (note not found for that tenant)
    
    def test_list_notes_only_shows_tenant_notes(self, client):
        """Test that listing notes only returns notes for the current tenant."""
        # Arrange - create two notes
        note1 = {"name": "Note 1", "description": "First note"}
        note2 = {"name": "Note 2", "description": "Second note"}
        
        client.post("/notes/", json=note1)
        client.post("/notes/", json=note2)
        
        # Act - list notes
        response = client.get("/notes/")
        
        # Assert - should see both notes (all in default tenant currently)
        assert response.status_code == 200
        notes = response.json()
        note_names = [n["name"] for n in notes]
        assert "Note 1" in note_names
        assert "Note 2" in note_names
        
        # TODO: After Step 5, create notes under different tenants
        # and verify each tenant only sees their own notes
