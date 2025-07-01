import React from 'react';
import { useExamples } from '../../hooks/useExamples';

function ExampleList() {
  const { examples, handleSelect, examplesError, addMode, editMode } = useExamples();
  const disabled = addMode || editMode;

  if (examplesError) {
    return <div style={{color: 'red'}}>{examplesError}</div>;
  }
  if (examples === null) {
    return <div>Loading...</div>;
  }
  if (examples.length === 0) {
    return <div>No examples found.</div>;
  }
  return (
    <ul>
      {examples.map(ex => (
        <li key={ex.uuid}>
          <button
            onClick={() => handleSelect(ex.uuid)}
            disabled={disabled}
            className="block w-full text-left px-4 py-2 mb-2 bg-white rounded shadow hover:bg-blue-100 transition-colors cursor-pointer text-blue-700 font-medium"
          >
            <strong>{ex.name}</strong>
          </button>
        </li>
      ))}
    </ul>
  );
}

export default ExampleList;
