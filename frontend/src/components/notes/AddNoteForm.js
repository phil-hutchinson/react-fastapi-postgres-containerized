import React from 'react';
import { useNotes } from '../../hooks/useNotes';

function AddNoteForm() {
  const {
    addName,
    setAddName,
    addDescription,
    setAddDescription,
    handleAddSubmit,
    handleAddCancel,
    addError,
    addSuccess
  } = useNotes();

  return (
    <div className="section-content">
      <h3 className="section-title">Add Note</h3>
      <form onSubmit={handleAddSubmit} className="">
        <div className="mb-4">
          <label className="input-label" htmlFor="add-name">Name:</label>
          <input
            id="add-name"
            type="text"
            value={addName}
            onChange={e => setAddName(e.target.value)}
            required
            className="input-text"
          />
        </div>
        <div className="mb-4">
          <label className="input-label" htmlFor="add-description">Description:</label>
          <input
            id="add-description"
            type="text"
            value={addDescription}
            onChange={e => setAddDescription(e.target.value)}
            className="input-text"
          />
        </div>
        <div className="button-group">
          <button type="submit" className="btn">Add</button>
          <button type="button" onClick={handleAddCancel} className="btn btn-cancel">Cancel</button>
        </div>
      </form>
      {addError && <div className="error-message">{addError}</div>}
      {addSuccess && <div className="success-message">{addSuccess}</div>}
    </div>
  );
}

export default AddNoteForm;
