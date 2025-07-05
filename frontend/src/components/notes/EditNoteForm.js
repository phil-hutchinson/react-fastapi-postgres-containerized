import React from 'react';
import { useNotes } from '../../hooks/useNotes';

function EditNoteForm() {
  const {
    selectedNote,
    editName,
    setEditName,
    editDescription,
    setEditDescription,
    handleUpdate,
    handleCancelEdit,
    updateError,
    updateSuccess
  } = useNotes();

  if (!selectedNote) return null;

  return (
    <div className="section-content">
      <h3 className="section-title">Edit Note</h3>
      <form onSubmit={handleUpdate}>
        <div className="mb-4">
          <label className="input-label" htmlFor="edit-name">Name:</label>
          <input
            id="edit-name"
            type="text"
            value={editName}
            onChange={e => setEditName(e.target.value)}
            disabled={selectedNote.locked}
            className="input-text"
          />
        </div>
        <div className="mb-4">
          <label className="input-label" htmlFor="edit-description">Description:</label>
          <input
            id="edit-description"
            type="text"
            value={editDescription}
            onChange={e => setEditDescription(e.target.value)}
            disabled={selectedNote.locked}
            className="input-text"
          />
        </div>
        <div className="button-group">
          <button type="submit" disabled={selectedNote.locked} className="btn">Update</button>
          <button type="button" onClick={handleCancelEdit} className="btn btn-cancel">Cancel</button>
        </div>
        {updateError && <div className="error-message">{updateError}</div>}
        {updateSuccess && <div className="success-message">{updateSuccess}</div>}
      </form>
    </div>
  );
}

export default EditNoteForm;
