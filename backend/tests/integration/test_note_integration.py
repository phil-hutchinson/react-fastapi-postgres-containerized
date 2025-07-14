def test_create_note_integration(client):
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
