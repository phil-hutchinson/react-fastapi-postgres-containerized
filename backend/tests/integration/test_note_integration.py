def test_create_note_integration(client):
    # Debug: Check if tables exist
    from sqlalchemy import text, create_engine
    
    # Use the same connection string as conftest
    TEST_DATABASE_URL = "postgresql://testuser:testpass@db_test:5432/testdb"
    debug_engine = create_engine(TEST_DATABASE_URL)
    
    with debug_engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Available tables: {tables}")
    
    # Arrange
    payload = {"name": "Integration Note", "description": "Created by integration test"}
    
    # Act
    print(f"Sending payload: {payload}")
    response = client.post("/notes/", json=payload)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
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
