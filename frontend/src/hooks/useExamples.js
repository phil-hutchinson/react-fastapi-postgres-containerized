import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const ExamplesContext = createContext();

export function ExamplesProvider({ children }) {
  const value = useExamplesProvider();
  return (
    <ExamplesContext.Provider value={value}>
      {children}
    </ExamplesContext.Provider>
  );
}

function useExamplesProvider() {
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
    axios.get('http://localhost:8000/examples/')
      .then(res => setExamples(res.data))
      .catch(() => setExamplesError('Could not fetch examples'));
  }, []);

  const handleSelect = (uuid) => {
    setDetailsError(null);
    setEditName('');
    setEditDescription('');
    setUpdateError(null);
    setUpdateSuccess(null);
    setEditMode(false);
    setAddMode(false);
    axios.get(`http://localhost:8000/examples/${uuid}`)
      .then(res => {
        setSelectedExample(res.data);
        setEditName(res.data.name);
        setEditDescription(res.data.description || '');
      })
      .catch(() => {
        setDetailsError('Could not fetch example details');
        setSelectedExample(null);
      });
  };

  const handleUpdate = (e) => {
    e.preventDefault();
    setUpdateError(null);
    setUpdateSuccess(null);
    axios.put(`http://localhost:8000/examples/${selectedExample.uuid}`, {
      name: editName,
      description: editDescription
    })
      .then(res => {
        setSelectedExample(res.data);
        setUpdateSuccess('Example updated successfully!');
        setEditMode(false);
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

  const handleDelete = () => {
    if (!selectedExample || selectedExample.finalized) return;
    if (window.confirm('Are you sure you want to delete this note? This action cannot be undone.')) {
      axios.delete(`http://localhost:8000/examples/${selectedExample.uuid}`)
        .then(() => {
          setExamples(examples.filter(ex => ex.uuid !== selectedExample.uuid));
          setSelectedExample(null);
          setEditMode(false);
          setDetailsError(null);
        })
        .catch(err => {
          if (err.response && err.response.status === 409) {
            setDetailsError('Note is finalized and cannot be deleted.');
          } else {
            setDetailsError('Failed to delete note.');
          }
        });
    }
  };

  return {
    examples, setExamples,
    examplesError, setExamplesError,
    selectedExample, setSelectedExample,
    detailsError, setDetailsError,
    editName, setEditName,
    editDescription, setEditDescription,
    updateError, setUpdateError,
    updateSuccess, setUpdateSuccess,
    editMode, setEditMode,
    finalizeError, setFinalizeError,
    finalizeSuccess, setFinalizeSuccess,
    addMode, setAddMode,
    addName, setAddName,
    addDescription, setAddDescription,
    addError, setAddError,
    addSuccess, setAddSuccess,
    handleSelect,
    handleUpdate,
    handleEdit,
    handleCancelEdit,
    handleFinalize,
    handleAddClick,
    handleAddSubmit,
    handleAddCancel,
    handleDelete,
  };
}

export function useExamples() {
  return useContext(ExamplesContext);
}
