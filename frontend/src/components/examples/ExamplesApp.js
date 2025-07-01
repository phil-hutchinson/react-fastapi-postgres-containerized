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
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-3xl font-bold mb-6 text-center">Template App: React &ndash; FastAPI &ndash; Postgres</h1>
      <div className="w-full max-w-2xl">
        <h2 className="text-xl font-semibold mb-4 text-center">Example Content:</h2>
        <ExampleList />
        <button
          onClick={handleAddClick}
          disabled={addMode || editMode}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 w-full"
        >
          Add Example
        </button>
      </div>
      {addMode ? (
        <AddExampleForm />
      ) : selectedExample || detailsError ? (
        <div className="mt-8 p-6 border border-gray-300 rounded bg-white w-full max-w-2xl transition-all duration-300 ease-in-out opacity-100 scale-100">
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
