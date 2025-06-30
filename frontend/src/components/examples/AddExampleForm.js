import React from 'react';

function AddExampleForm({
  addName,
  setAddName,
  addDescription,
  setAddDescription,
  handleAddSubmit,
  handleAddCancel,
  addError,
  addSuccess
}) {
  return (
    <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
      <h3>Add Example</h3>
      <form onSubmit={handleAddSubmit} style={{marginBottom: '1em'}}>
        <div>
          <label>
            Name:
            <input
              type="text"
              value={addName}
              onChange={e => setAddName(e.target.value)}
              required
              style={{marginLeft: '0.5em'}}
            />
          </label>
        </div>
        <div style={{marginTop: '0.5em'}}>
          <label>
            Description:
            <input
              type="text"
              value={addDescription}
              onChange={e => setAddDescription(e.target.value)}
              style={{marginLeft: '0.5em'}}
            />
          </label>
        </div>
        <button type="submit" style={{marginTop: '1em'}}>Add</button>
        <button type="button" onClick={handleAddCancel} style={{marginLeft: '1em', marginTop: '1em'}}>Cancel</button>
      </form>
      {addError && <div style={{color: 'red'}}>{addError}</div>}
      {addSuccess && <div style={{color: 'green'}}>{addSuccess}</div>}
    </div>
  );
}

export default AddExampleForm;
