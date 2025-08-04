class TestNoteIntegration:
    """Comprehensive integration tests for the Note API endpoints."""
    
    def test_create_note_integration(self, client):
        """Test creating a note via API."""
        # Arrange
        payload = {"name": "Integration Note", "description": "Created by integration test"}
        
        # Act
        response = client.post("/notes/", json=payload)
        
        # Assert
        assert response.status_code == 200
        created_note = response.json()
        assert created_note["name"] == "Integration Note"
        assert created_note["description"] == "Created by integration test"
        assert created_note["locked"] is False
        
        # Verify
        note_uuid = created_note["uuid"]
        get_response = client.get(f"/notes/{note_uuid}")
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["uuid"] == note_uuid
        assert retrieved_note["name"] == "Integration Note"
        assert retrieved_note["description"] == "Created by integration test"
        assert retrieved_note["locked"] is False

    # ===== LIST NOTES TESTS =====
    
    def test_list_notes_empty(self, client):
        """Test listing notes when database is empty."""
        # Act
        response = client.get("/notes/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_list_notes_with_data(self, client):
        """Test listing notes with data, ensuring correct order."""
        # Arrange
        note1_payload = {"name": "First Note", "description": "Description 1"}
        note2_payload = {"name": "Second Note", "description": "Description 2"}
        
        # Create notes in specific order
        note1_response = client.post("/notes/", json=note1_payload)
        note2_response = client.post("/notes/", json=note2_payload)
        
        note1_uuid = note1_response.json()["uuid"]
        note2_uuid = note2_response.json()["uuid"]
        
        # Act
        response = client.get("/notes/")
        
        # Assert
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 2
        
        # Verify order (should be ID ascending, which matches creation order)
        assert notes[0]["uuid"] == note1_uuid
        assert notes[0]["name"] == "First Note"
        assert notes[1]["uuid"] == note2_uuid
        assert notes[1]["name"] == "Second Note"

    # ===== GET NOTE DETAIL TESTS =====
    
    def test_get_note_detail_success(self, client):
        """Test getting note details for existing note."""
        # Arrange
        payload = {"name": "Detail Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Act
        response = client.get(f"/notes/{note_uuid}")
        
        # Assert
        assert response.status_code == 200
        note = response.json()
        assert note["uuid"] == note_uuid
        assert note["name"] == "Detail Test Note"
        assert note["description"] == "Test description"
        assert note["locked"] is False

    def test_get_note_detail_not_found(self, client):
        """Test getting note details for non-existent note."""
        # Arrange
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        # Act
        response = client.get(f"/notes/{fake_uuid}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"

    # ===== UPDATE NOTE TESTS =====
    
    def test_update_note_success(self, client):
        """Test updating a note successfully."""
        # Arrange
        payload = {"name": "Original Name", "description": "Original description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        update_payload = {"name": "Updated Name", "description": "Updated description"}
        
        # Act
        response = client.put(f"/notes/{note_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["name"] == "Updated Name"
        assert updated_note["description"] == "Updated description"
        assert updated_note["locked"] is False
        
        # Verify
        get_response = client.get(f"/notes/{note_uuid}")
        verified_note = get_response.json()
        assert verified_note["name"] == "Updated Name"
        assert verified_note["description"] == "Updated description"

    def test_update_note_partial_name_only(self, client):
        """Test updating only the name field."""
        # Arrange
        payload = {"name": "Original Name", "description": "Original description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        update_payload = {"name": "New Name Only"}
        
        # Act
        response = client.put(f"/notes/{note_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["name"] == "New Name Only"
        assert updated_note["description"] == "Original description"  # Should remain unchanged

    def test_update_note_partial_description_only(self, client):
        """Test updating only the description field."""
        # Arrange
        payload = {"name": "Original Name", "description": "Original description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        update_payload = {"description": "New description only"}
        
        # Act
        response = client.put(f"/notes/{note_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["name"] == "Original Name"  # Should remain unchanged
        assert updated_note["description"] == "New description only"

    def test_update_note_locked(self, client):
        """Test updating a locked note should fail."""
        # Arrange
        payload = {"name": "Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Lock the note
        client.post(f"/notes/{note_uuid}/actions/lock")
        
        update_payload = {"name": "Should Not Update", "description": "Should not change"}
        
        # Act
        response = client.put(f"/notes/{note_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 409
        assert response.json()["detail"] == "Note is locked and cannot be modified."
        
        # Verify note unchanged
        get_response = client.get(f"/notes/{note_uuid}")
        verified_note = get_response.json()
        assert verified_note["name"] == "Test Note"  # Original name
        assert verified_note["description"] == "Test description"  # Original description
        assert verified_note["locked"] is True

    def test_update_note_not_found(self, client):
        """Test updating a non-existent note."""
        # Arrange
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        update_payload = {"name": "Should Not Work"}
        
        # Act
        response = client.put(f"/notes/{fake_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"

    # ===== LOCK NOTE TESTS =====
    
    def test_lock_note_success(self, client):
        """Test locking a note successfully."""
        # Arrange
        payload = {"name": "Lock Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Act
        response = client.post(f"/notes/{note_uuid}/actions/lock")
        
        # Assert
        assert response.status_code == 200
        locked_note = response.json()
        assert locked_note["locked"] is True
        assert locked_note["name"] == "Lock Test Note"
        
        # Verify
        get_response = client.get(f"/notes/{note_uuid}")
        verified_note = get_response.json()
        assert verified_note["locked"] is True

    def test_lock_note_already_locked(self, client):
        """Test locking an already locked note should fail."""
        # Arrange
        payload = {"name": "Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Lock the note first time
        client.put(f"/notes/{note_uuid}/lock")
        
        # Act - try to lock again
        response = client.put(f"/notes/{note_uuid}/lock")
        
        # Assert
        assert response.status_code == 409
        assert response.json()["detail"] == "Note is already locked."

    def test_lock_note_not_found(self, client):
        """Test locking a non-existent note."""
        # Arrange
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        # Act
        response = client.put(f"/notes/{fake_uuid}/lock")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"

    # ===== DELETE NOTE TESTS =====
    
    def test_delete_note_success(self, client):
        """Test deleting a note successfully."""
        # Arrange
        payload = {"name": "Delete Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Act
        response = client.delete(f"/notes/{note_uuid}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["detail"] == "Note deleted"
        
        # Verify - note should no longer exist
        get_response = client.get(f"/notes/{note_uuid}")
        assert get_response.status_code == 404

    def test_delete_note_locked(self, client):
        """Test deleting a locked note should fail."""
        # Arrange
        payload = {"name": "Test Note", "description": "Test description"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        # Lock the note
        client.put(f"/notes/{note_uuid}/lock")
        
        # Act
        response = client.delete(f"/notes/{note_uuid}")
        
        # Assert
        assert response.status_code == 409
        assert response.json()["detail"] == "Note is locked and cannot be deleted."
        
        # Verify note still exists
        get_response = client.get(f"/notes/{note_uuid}")
        assert get_response.status_code == 200
        assert get_response.json()["locked"] is True

    def test_delete_note_not_found(self, client):
        """Test deleting a non-existent note."""
        # Arrange
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        # Act
        response = client.delete(f"/notes/{fake_uuid}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"

    # ===== EDGE CASE TESTS =====
    
    def test_create_note_with_empty_strings(self, client):
        """Test creating note with empty strings."""
        # Arrange
        payload = {"name": "", "description": ""}
        
        # Act
        response = client.post("/notes/", json=payload)
        
        # Assert
        assert response.status_code == 200
        created_note = response.json()
        assert created_note["name"] == ""
        assert created_note["description"] == ""
        assert created_note["locked"] is False

    def test_update_note_with_empty_strings(self, client):
        """Test updating note with empty strings."""
        # Arrange
        payload = {"name": "Original", "description": "Original"}
        create_response = client.post("/notes/", json=payload)
        note_uuid = create_response.json()["uuid"]
        
        update_payload = {"name": "", "description": ""}
        
        # Act
        response = client.put(f"/notes/{note_uuid}", json=update_payload)
        
        # Assert
        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["name"] == ""
        assert updated_note["description"] == ""
