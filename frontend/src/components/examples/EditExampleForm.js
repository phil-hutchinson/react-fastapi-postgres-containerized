import React from 'react';
import { useExamples } from '../../hooks/useExamples';

function EditExampleForm() {
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
    <form onSubmit={handleUpdate} style={{marginBottom: '1em'}}>
      <div>
        <label>
          Name:
          <input
            type="text"
            value={editName}
            onChange={e => setEditName(e.target.value)}
            disabled={selectedExample.finalized}
            style={{marginLeft: '0.5em'}}
          />
        </label>
      </div>
      <div style={{marginTop: '0.5em'}}>
        <label>
          Description:
          <input
            type="text"
            value={editDescription}
            onChange={e => setEditDescription(e.target.value)}
            disabled={selectedExample.finalized}
            style={{marginLeft: '0.5em'}}
          />
        </label>
      </div>
      <button type="submit" disabled={selectedExample.finalized} style={{marginTop: '1em'}}>Update</button>
      <button type="button" onClick={handleCancelEdit} style={{marginLeft: '1em', marginTop: '1em'}}>Cancel</button>
      {updateError && <div style={{color: 'red'}}>{updateError}</div>}
      {updateSuccess && <div style={{color: 'green'}}>{updateSuccess}</div>}
    </form>
  );
}

export default EditExampleForm;
