import React from 'react';
import { useExamples } from '../../hooks/useExamples';

function DisplayExampleDetails() {
  const {
    selectedExample,
    handleEdit,
    handleFinalize,
    finalizeError,
    finalizeSuccess,
    detailsError
  } = useExamples();

  if (!selectedExample) return detailsError ? (
    <div style={{color: 'red'}}>{detailsError}</div>
  ) : null;

  return (
    <div style={{marginBottom: '1em'}}>
      <div><strong>Name:</strong> {selectedExample.name}</div>
      <div><strong>Description:</strong> {selectedExample.description || <em>No description</em>}</div>
      {!selectedExample.finalized && (
        <>
          <button onClick={handleEdit} style={{marginTop: '1em', marginRight: '1em'}}>Edit</button>
          <button onClick={handleFinalize} style={{marginTop: '1em'}}>Finalize</button>
        </>
      )}
      {finalizeError && <div style={{color: 'red'}}>{finalizeError}</div>}
      {finalizeSuccess && <div style={{color: 'green'}}>{finalizeSuccess}</div>}
      {selectedExample.finalized && <div style={{color: 'gray', marginTop: '0.5em'}}><em>This example is finalized and cannot be edited.</em></div>}
    </div>
  );
}

export default DisplayExampleDetails;
