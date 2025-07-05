import React from 'react';
import { useExamples } from '../../hooks/useExamples';

function EditNoteForm() {
  const {
    selectedExample,
    editName,
    setEditName,
    editDescription,
    setEditDescription,
    handleUpdate,
    handleCancelEdit,
    updateError,
    updateSuccess
  } = useExamples();

  if (!selectedExample) return null;

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
            disabled={selectedExample.finalized}
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
            disabled={selectedExample.finalized}
            className="input-text"
          />
        </div>
        <div className="button-group">
          <button type="submit" disabled={selectedExample.finalized} className="btn">Update</button>
          <button type="button" onClick={handleCancelEdit} className="btn btn-cancel">Cancel</button>
        </div>
        {updateError && <div className="error-message">{updateError}</div>}
        {updateSuccess && <div className="success-message">{updateSuccess}</div>}
      </form>
    </div>
  );
}

export default EditNoteForm;
