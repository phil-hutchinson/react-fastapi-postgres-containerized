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
    selectedExample,
    detailsError,
    editMode,
    addMode,
    handleAddClick
  } = useExamples();

  return (
    <div className="layout-container min-h-screen flex flex-col items-center bg-gray-50">
      <h1 className="app-title">Template App: React &ndash; FastAPI &ndash; Postgres</h1>
      <div className="w-full max-w-2xl">
        <h2 className="section-title">Example Content:</h2>
        <ExampleList />
        <button
          onClick={handleAddClick}
          disabled={addMode || editMode}
          className="btn mt-4 w-full"
        >
          Add Note
        </button>
        {addMode ? (
          <AddExampleForm />
        ) : selectedExample || detailsError ?
            editMode ? (
              <EditExampleForm />
            ) : (
              <DisplayExampleDetails />
            )
          : null
        }
      </div>
    </div>
  );
}

export default ExamplesApp;
