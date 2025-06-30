import React from 'react';

function ExampleList({ examples, onSelect, disabled, examplesError }) {
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
            onClick={() => onSelect(ex.uuid)}
            disabled={disabled}
            style={{background:'none',border:'none',color:'blue',textDecoration:'underline',cursor:'pointer'}}
          >
            <strong>{ex.name}</strong>
          </button>
        </li>
      ))}
    </ul>
  );
}

export default ExampleList;
