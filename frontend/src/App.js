import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [examples, setExamples] = useState([]);
  const [examplesError, setExamplesError] = useState(null);
  const [selectedExample, setSelectedExample] = useState(null);
  const [detailsError, setDetailsError] = useState(null);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [updateError, setUpdateError] = useState(null);
  const [updateSuccess, setUpdateSuccess] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [finalizeError, setFinalizeError] = useState(null);
  const [finalizeSuccess, setFinalizeSuccess] = useState(null);
  const [addMode, setAddMode] = useState(false);
  const [addName, setAddName] = useState("");
  const [addDescription, setAddDescription] = useState("");
  const [addError, setAddError] = useState(null);
  const [addSuccess, setAddSuccess] = useState(null);

  useEffect(() => {
    // Fetch /examples/ endpoint using axios
    axios.get('http://localhost:8000/examples/')
      .then(res => setExamples(res.data))
      .catch(() => setExamplesError('Could not fetch examples'));
  }, []);

  const handleSelect = (uuid) => {
    setDetailsError(null);
    setSelectedExample(null);
    setEditName('');
    setEditDescription('');
    setUpdateError(null);
    setUpdateSuccess(null);
    setEditMode(false);
    setAddMode(false);
    // Fetch selected example details
    axios.get(`http://localhost:8000/examples/${uuid}`)
      .then(res => {
        setSelectedExample(res.data);
        setEditName(res.data.name);
        setEditDescription(res.data.description || '');
      })
      .catch(() => setDetailsError('Could not fetch example details'));
  };

  const handleUpdate = (e) => {
    e.preventDefault();
    setUpdateError(null);
    setUpdateSuccess(null);
    // Update example details
    axios.put(`http://localhost:8000/examples/${selectedExample.uuid}`, {
      name: editName,
      description: editDescription
    })
      .then(res => {
        setSelectedExample(res.data);
        setUpdateSuccess('Example updated successfully!');
        setEditMode(false);
        // Update the name in the list
        setExamples(examples.map(ex =>
          ex.uuid === selectedExample.uuid ? { ...ex, name: res.data.name } : ex
        ));
      })
      .catch(err => {
        if (err.response && err.response.status === 409) {
          setUpdateError('Example is finalized and cannot be modified.');
        } else {
          setUpdateError('Failed to update example.');
        }
      });
  };

  const handleEdit = () => {
    setEditMode(true);
    setUpdateError(null);
    setUpdateSuccess(null);
  };

  const handleCancelEdit = () => {
    setEditMode(false);
    setEditName(selectedExample.name);
    setEditDescription(selectedExample.description || '');
    setUpdateError(null);
    setUpdateSuccess(null);
  };

  const handleFinalize = () => {
    setFinalizeError(null);
    setFinalizeSuccess(null);
    if (!selectedExample || selectedExample.finalized) return;
    if (window.confirm('Are you sure you want to finalize this example? This action cannot be undone.')) {
      axios.post(`http://localhost:8000/examples/${selectedExample.uuid}/finalize`)
        .then(res => {
          setSelectedExample(res.data);
          setFinalizeSuccess('Example finalized successfully!');
          setEditMode(false);
          // Update the finalized status in the list if needed
          setExamples(examples.map(ex =>
            ex.uuid === selectedExample.uuid ? { ...ex, name: res.data.name } : ex
          ));
        })
        .catch(err => {
          if (err.response && err.response.status === 409) {
            setFinalizeError('Example is already finalized.');
          } else {
            setFinalizeError('Failed to finalize example.');
          }
        });
    }
  };

  const handleAddClick = () => {
    setAddMode(true);
    setSelectedExample(null);
    setEditMode(false);
    setAddName("");
    setAddDescription("");
    setAddError(null);
    setAddSuccess(null);
  };

  const handleAddSubmit = (e) => {
    e.preventDefault();
    setAddError(null);
    setAddSuccess(null);
    axios.post("http://localhost:8000/examples/", {
      name: addName,
      description: addDescription
    })
      .then(res => {
        setExamples([...examples, { uuid: res.data.uuid, name: res.data.name }]);
        setSelectedExample(res.data);
        setEditName(res.data.name);
        setEditDescription(res.data.description || "");
        setAddMode(false);
        setAddSuccess("Example added successfully!");
        setAddName("");
        setAddDescription("");
      })
      .catch(() => setAddError("Failed to add example."));
  };

  const handleAddCancel = () => {
    setAddMode(false);
    setAddName("");
    setAddDescription("");
    setAddError(null);
    setAddSuccess(null);
  };

  return (
    <div>
      <h1>Starter App: React &mdash; FastAPI &mdash; Postgres</h1>
      <div>
        <h2>Examples from API:</h2>
        <button onClick={handleAddClick} disabled={addMode || editMode} style={{marginBottom: '1em'}}>Add Example</button>
        {examplesError && <div style={{color: 'red'}}>{examplesError}</div>}
        {examples.length > 0 ? (
          <ul>
            {examples.map(ex => (
              <li key={ex.uuid}>
                <button onClick={() => { setAddMode(false); handleSelect(ex.uuid); }} style={{background:'none',border:'none',color:'blue',textDecoration:'underline',cursor:'pointer'}}>
                  <strong>{ex.name}</strong>
                </button>
              </li>
            ))}
          </ul>
        ) : examplesError ? null : 'Loading...'}
      </div>
      {addMode ? (
        <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
          <h3>Add Example</h3>
          <form onSubmit={handleAddSubmit} style={{marginBottom: '1em'}}>
            <div>
              <label>
                Name:
                <input
                  type="text"
                  value={addName}
                  onChange={e => setAddName(e.target.value)}
                  required
                  style={{marginLeft: '0.5em'}}
                />
              </label>
            </div>
            <div style={{marginTop: '0.5em'}}>
              <label>
                Description:
                <input
                  type="text"
                  value={addDescription}
                  onChange={e => setAddDescription(e.target.value)}
                  style={{marginLeft: '0.5em'}}
                />
              </label>
            </div>
            <button type="submit" style={{marginTop: '1em'}}>Add</button>
            <button type="button" onClick={handleAddCancel} style={{marginLeft: '1em', marginTop: '1em'}}>Cancel</button>
          </form>
          {addError && <div style={{color: 'red'}}>{addError}</div>}
          {addSuccess && <div style={{color: 'green'}}>{addSuccess}</div>}
        </div>
      ) : selectedExample && (
        <div style={{marginTop: '2em', padding: '1em', border: '1px solid #ccc'}}>
          <h3>Example Details</h3>
          {editMode ? (
            <form onSubmit={handleUpdate} style={{marginBottom: '1em'}}>
              <div>
                <label>
                  Name:
                  <input
                    type="text"
                    value={editName}
                    onChange={e => setEditName(e.target.value)}
                    disabled={selectedExample.finalized}
                    style={{marginLeft: '0.5em'}}
                  />
                </label>
              </div>
              <div style={{marginTop: '0.5em'}}>
                <label>
                  Description:
                  <input
                    type="text"
                    value={editDescription}
                    onChange={e => setEditDescription(e.target.value)}
                    disabled={selectedExample.finalized}
                    style={{marginLeft: '0.5em'}}
                  />
                </label>
              </div>
              <button type="submit" disabled={selectedExample.finalized} style={{marginTop: '1em'}}>Update</button>
              <button type="button" onClick={handleCancelEdit} style={{marginLeft: '1em', marginTop: '1em'}}>Cancel</button>
            </form>
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
          {updateError && <div style={{color: 'red'}}>{updateError}</div>}
          {updateSuccess && <div style={{color: 'green'}}>{updateSuccess}</div>}
          {finalizeError && <div style={{color: 'red'}}>{finalizeError}</div>}
          {finalizeSuccess && <div style={{color: 'green'}}>{finalizeSuccess}</div>}
          {selectedExample.finalized && <div style={{color: 'gray', marginTop: '0.5em'}}><em>This example is finalized and cannot be edited.</em></div>}
        </div>
      )}
      {detailsError && <div style={{color: 'red'}}>{detailsError}</div>}
    </div>
  );
}

export default App;
