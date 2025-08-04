import pytest
from unittest.mock import patch, MagicMock
from api.services import note as sut
from api.schemas.note import NoteCreate, NoteUpdate

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
    db.delete = MagicMock()
    return db

# --- update_note ---
def test_update_note_logs_warning_when_not_found(mock_db):
    update = NoteUpdate(name="New Name", description="New Desc")
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.update_note("nonexistent", update, db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()

def test_update_note_logs_warning_when_locked(mock_db):
    update = NoteUpdate(name="New Name", description="New Desc")
    dummy_note = DummyNote(uuid="1", name="Old Name", description="Old Desc", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.update_note("1", update, db=mock_db)
        mock_warning.assert_called_once()
        assert "locked" in mock_warning.call_args[0][0].lower()

def test_update_note_logs_error_on_db_error(mock_db):
    update = NoteUpdate(name="New Name", description="New Desc")
    dummy_note = DummyNote(uuid="1", name="Old Name", description="Old Desc", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    mock_db.commit.side_effect = Exception("DB error")
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.update_note("1", update, db=mock_db)
        mock_error.assert_called()
        assert "db error" in mock_error.call_args[0][0].lower()

# --- get_note_detail ---
def test_get_note_detail_logs_warning_when_not_found(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.get_note_detail("nonexistent", db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()

def test_get_note_detail_logs_error_on_db_error(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.side_effect = Exception("DB error")
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.get_note_detail("1", db=mock_db)
        mock_error.assert_called()
        assert "db error" in mock_error.call_args[0][0].lower()

# --- lock_note ---
def test_lock_note_logs_warning_when_not_found(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.lock_note("nonexistent", db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()

def test_lock_note_logs_warning_when_already_locked(mock_db):
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.lock_note("1", db=mock_db)
        mock_warning.assert_called_once()
        assert "already locked" in mock_warning.call_args[0][0].lower()

def test_lock_note_logs_error_on_db_error(mock_db):
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    mock_db.commit.side_effect = Exception("DB error")
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.lock_note("1", db=mock_db)
        mock_error.assert_called()
        assert "db error" in mock_error.call_args[0][0].lower()

# --- delete_note ---
def test_delete_note_logs_warning_when_not_found(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.delete_note("nonexistent", db=mock_db)
        mock_warning.assert_called_once()
        assert "not found" in mock_warning.call_args[0][0].lower()

def test_delete_note_logs_warning_when_locked(mock_db):
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=True)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    with patch.object(sut.logger, "warning") as mock_warning:
        with pytest.raises(Exception):
            sut.delete_note("1", db=mock_db)
        mock_warning.assert_called_once()
        assert "locked" in mock_warning.call_args[0][0].lower()

def test_delete_note_logs_error_on_db_error(mock_db):
    dummy_note = DummyNote(uuid="1", name="Note 1", description="Desc 1", locked=False)
    mock_db.query.return_value.filter_by.return_value.first.return_value = dummy_note
    mock_db.commit.side_effect = Exception("DB error")
    with patch.object(sut.logger, "error") as mock_error:
        with pytest.raises(Exception):
            sut.delete_note("1", db=mock_db)
        mock_error.assert_called()
        assert "db error" in mock_error.call_args[0][0].lower()
