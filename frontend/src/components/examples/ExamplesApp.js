import React from 'react';
import { ExamplesProvider, useExamples } from '../../hooks/useExamples';
import ExampleList from './ExampleList';

function ExamplesApp() {
  return (
    <ExamplesProvider>
      <ExamplesAppContent />
    </ExamplesProvider>
  );
}

function ExamplesAppContent() {
  const {
    examples, examplesError, selectedExample, detailsError,
    editName, setEditName, editDescription, setEditDescription,
    updateError, updateSuccess, editMode, setEditMode,
    finalizeError, finalizeSuccess, addMode, addName, setAddName,
    addDescription, setAddDescription, addError, addSuccess,
    handleSelect, handleUpdate, handleEdit, handleCancelEdit,
    handleFinalize, handleAddClick, handleAddSubmit, handleAddCancel
  } = useExamples();

  return (
    <div>
      <h1>Starter App: React &mdash; FastAPI &mdash; Postgres</h1>
      <div>
        <h2>Examples from API:</h2>
        <button onClick={handleAddClick} disabled={addMode || editMode} style={{marginBottom: '1em'}}>Add Example</button>
        <ExampleList examples={examples} onSelect={handleSelect} disabled={addMode || editMode} examplesError={examplesError} />
      </div>
      {addMode ? (
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
      ) : selectedExample && (
        <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
          <h3>Example Details</h3>
          {editMode ? (
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
            </form>
          ) : (
            <div style={{marginBottom: '1em'}}>
              <div><strong>Name:</strong> {selectedExample.name}</div>
              <div><strong>Description:</strong> {selectedExample.description || <em>No description</em>}</div>
              {!selectedExample.finalized && (
                <>
                  <button onClick={handleEdit} style={{marginTop: '1em', marginRight: '1em'}}>Edit</button>
                  <button onClick={handleFinalize} style={{marginTop: '1em'}}>Finalize</button>
                </>
              )}
            </div>
          )}
          {updateError && <div style={{color: 'red'}}>{updateError}</div>}
          {updateSuccess && <div style={{color: 'green'}}>{updateSuccess}</div>}
          {finalizeError && <div style={{color: 'red'}}>{finalizeError}</div>}
          {finalizeSuccess && <div style={{color: 'green'}}>{finalizeSuccess}</div>}
          {selectedExample.finalized && <div style={{color: 'gray', marginTop: '0.5em'}}><em>This example is finalized and cannot be edited.</em></div>}
        </div>
      )}
      {detailsError && <div style={{color: 'red'}}>{detailsError}</div>}
    </div>
  );
}

export default ExamplesApp;
