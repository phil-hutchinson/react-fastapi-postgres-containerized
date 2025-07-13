import pytest
from unittest.mock import MagicMock
from api.services import note as sut
from api.schemas.note import NoteCreate

class DummyNote:
    def __init__(self, uuid, name, description, locked=False):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.locked = locked

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    return db

def test_create_note_success(mock_db):
    # Arrange
    note_data = NoteCreate(name="Test Note", description="A test note")
    dummy_uuid = "1234-abcd"
    dummy_note = DummyNote(uuid=dummy_uuid, name=note_data.name, description=note_data.description, locked=False)
    mock_db.refresh.side_effect = lambda obj: None
    # Patch Note constructor to return dummy_note
    original_Note = sut.Note
    sut.Note = lambda name, description: dummy_note

    # Act
    result = sut.create_note(note_data, db=mock_db)

    # Restore
    sut.Note = original_Note

    # Assert
    assert result["uuid"] == dummy_uuid
    assert result["name"] == note_data.name
    assert result["description"] == note_data.description
    assert result["locked"] is False
    mock_db.add.assert_called_once_with(dummy_note)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(dummy_note)

def test_list_notes_success(mock_db):
    # Arrange
    dummy_notes = [
        DummyNote(uuid="1", name="Note 1", description="Desc 1"),
        DummyNote(uuid="2", name="Note 2", description="Desc 2"),
    ]
    mock_db.query.return_value.order_by.return_value.all.return_value = dummy_notes

    # Act
    result = sut.list_notes(db=mock_db)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["uuid"] == "1"
    assert result[0]["name"] == "Note 1"
    assert result[1]["uuid"] == "2"
    assert result[1]["name"] == "Note 2"

def test_get_note_detail_success(mock_db):
    # Arrange
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=False)

    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note

    # Act
    result = sut.get_note_detail("1", db=mock_db)

    # Assert
    assert isinstance(result, dict)
    assert result["uuid"] == "1"
    assert result["name"] == "Note 1"
    assert result["description"] == "Desc 1"
    assert result["locked"] is False

def test_get_note_detail_raises_404_when_note_not_found(mock_db):
    # Arrange
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.get_note_detail("nonexistent", db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Note not found" in str(exc_info.value)


def test_update_note_success(mock_db):
    # Arrange
    from api.schemas.note import NoteUpdate
    dummy_note = DummyNote(uuid="1", name="Old Name", description="Old Desc", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    update = NoteUpdate(name="New Name", description="New Desc")

    # Act
    result = sut.update_note("1", update, db=mock_db)

    # Assert
    assert result["uuid"] == "1"
    assert result["name"] == "New Name"
    assert result["description"] == "New Desc"
    assert result["locked"] is False
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(dummy_note)


def test_update_note_raises_404_when_note_not_found(mock_db):
    # Arrange
    from api.schemas.note import NoteUpdate
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    update = NoteUpdate(name="New Name", description="New Desc")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.update_note("nonexistent", update, db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Note not found" in str(exc_info.value)


def test_update_note_raises_409_when_note_locked(mock_db):
    # Arrange
    from api.schemas.note import NoteUpdate
    dummy_note = DummyNote(uuid="1", name="Old Name", description="Old Desc", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    update = NoteUpdate(name="New Name", description="New Desc")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.update_note("1", update, db=mock_db)
    assert exc_info.value.status_code == 409
    assert "locked" in str(exc_info.value).lower()


def test_lock_note_success(mock_db):
    # Arrange
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note

    # Act
    result = sut.lock_note("1", db=mock_db)

    # Assert
    assert result["uuid"] == "1"
    assert result["name"] == "Note 1"
    assert result["description"] == "Desc 1"
    assert result["locked"] is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(dummy_note)


def test_lock_note_raises_404_when_note_not_found(mock_db):
    # Arrange
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.lock_note("nonexistent", db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Note not found" in str(exc_info.value)


def test_lock_note_raises_409_when_note_already_locked(mock_db):
    # Arrange
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.lock_note("1", db=mock_db)
    assert exc_info.value.status_code == 409
    assert "already locked" in str(exc_info.value).lower()


def test_delete_note_success(mock_db):
    # Arrange
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note

    # Act
    result = sut.delete_note("1", db=mock_db)

    # Assert
    assert result["detail"] == "Note deleted"
    mock_db.delete.assert_called_once_with(dummy_note)
    mock_db.commit.assert_called_once()


def test_delete_note_raises_404_when_note_not_found(mock_db):
    # Arrange
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.delete_note("nonexistent", db=mock_db)
    assert exc_info.value.status_code == 404
    assert "Note not found" in str(exc_info.value)


def test_delete_note_raises_409_when_note_locked(mock_db):
    # Arrange
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        sut.delete_note("1", db=mock_db)
    assert exc_info.value.status_code == 409
    assert "locked" in str(exc_info.value).lower()
