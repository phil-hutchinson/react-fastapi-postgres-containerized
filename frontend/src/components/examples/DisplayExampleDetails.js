import React from 'react';
import { useExamples } from '../../hooks/useExamples';

function DisplayExampleDetails() {
  const {
    selectedExample,
    handleEdit,
    handleFinalize,
    handleDelete,
    finalizeError,
    finalizeSuccess,
    detailsError
  } = useExamples();

  if (!selectedExample) return detailsError ? (
    <div className="text-red-600">{detailsError}</div>
  ) : null;

  return (
    <div className="section-content">
      <h3 className="section-title">Note Details</h3>
      <div className="mb-4">
        <span className="display-label">Name:</span>
        <div className="display-value">{selectedExample.name}</div>
      </div>
      <div className="mb-4">
        <span className="display-label">Description:</span>
        <div className="display-value">{selectedExample.description || <em>No description</em>}</div>
      </div>
      {!selectedExample.finalized && (
        <div className="button-group">
          <button onClick={handleEdit} className="btn">Edit</button>
          <button onClick={handleFinalize} className="btn">Finalize</button>
          <button onClick={handleDelete} className="btn btn-cancel">Delete</button>
        </div>
      )}
      {finalizeError && <div className="error-message">{finalizeError}</div>}
      {finalizeSuccess && <div className="success-message">{finalizeSuccess}</div>}
      {selectedExample.finalized && <div className="text-gray-500 mt-2"><em>This note is finalized and cannot be edited or deleted.</em></div>}
    </div>
  );
}

export default DisplayExampleDetails;
