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
    <div className="text-red-600">{detailsError}</div>
  ) : null;

  return (
    <div className="section-content">
      <div><strong>Name:</strong> {selectedExample.name}</div>
      <div><strong>Description:</strong> {selectedExample.description || <em>No description</em>}</div>
      {!selectedExample.finalized && (
        <div className="mt-4 flex gap-2">
          <button onClick={handleEdit} className="btn">Edit</button>
          <button onClick={handleFinalize} className="btn">Finalize</button>
        </div>
      )}
      {finalizeError && <div className="text-red-600 mt-2">{finalizeError}</div>}
      {finalizeSuccess && <div className="text-green-600 mt-2">{finalizeSuccess}</div>}
      {selectedExample.finalized && <div className="text-gray-500 mt-2"><em>This example is finalized and cannot be edited.</em></div>}
    </div>
  );
}

export default DisplayExampleDetails;
