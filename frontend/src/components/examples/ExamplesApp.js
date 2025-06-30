import React from 'react';
import { ExamplesProvider, useExamples } from '../../hooks/useExamples';
import ExampleList from './ExampleList';
import AddExampleForm from './AddExampleForm';
import EditExampleForm from './EditExampleForm';
import DisplayExampleDetails from './DisplayExampleDetails';

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
    addMode, addName, setAddName,
    addDescription, setAddDescription, addError, addSuccess,
    handleSelect, handleUpdate, handleEdit, handleCancelEdit,
    handleAddClick, handleAddSubmit, handleAddCancel
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
      ) : selectedExample || detailsError ? (
        <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
          <h3>Example Details</h3>
          {editMode ? (
            <EditExampleForm />
          ) : (
            <DisplayExampleDetails />
          )}
        </div>
      ) : null}
    </div>
  );
}

export default ExamplesApp;
