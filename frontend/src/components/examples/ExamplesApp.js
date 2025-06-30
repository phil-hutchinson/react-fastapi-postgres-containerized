import React from 'react';
import { ExamplesProvider, useExamples } from '../../hooks/useExamples';
import ExampleList from './ExampleList';
import AddExampleForm from './AddExampleForm';
import EditExampleForm from './EditExampleForm';

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
        <ExampleList />
      </div>
      {addMode ? (
        <AddExampleForm />
      ) : selectedExample && (
        <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
          <h3>Example Details</h3>
          {editMode ? (
            <EditExampleForm />
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
