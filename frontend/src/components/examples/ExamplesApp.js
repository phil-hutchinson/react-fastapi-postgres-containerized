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
    <div className="layout-container min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="app-title">Template App: React &ndash; FastAPI &ndash; Postgres</h1>
      <div className="w-full max-w-2xl">
        <h2 className="section-title">Example Content:</h2>
        <ExampleList />
        <button
          onClick={handleAddClick}
          disabled={addMode || editMode}
          className="btn mt-4 w-full disabled:opacity-50"
        >
          Add Example
        </button>
      </div>
      {addMode ? (
        <AddExampleForm />
      ) : selectedExample || detailsError ? (
        <div className="mt-8 selection-card w-full max-w-2xl transition-all duration-300 ease-in-out opacity-100 scale-100">
          <h3 className="text-lg font-semibold mb-4 text-center">Example Details</h3>
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
