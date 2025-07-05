import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const NotesContext = createContext();

export function NotesProvider({ children }) {
  const value = useNotesProvider();
  return (
    <NotesContext.Provider value={value}>
      {children}
    </NotesContext.Provider>
  );
}

function useNotesProvider() {
  const [notes, setNotes] = useState([]);
  const [notesError, setNotesError] = useState(null);
  const [selectedNote, setSelectedNote] = useState(null);
  const [detailsError, setDetailsError] = useState(null);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [updateError, setUpdateError] = useState(null);
  const [updateSuccess, setUpdateSuccess] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const [addName, setAddName] = useState("");
  const [addDescription, setAddDescription] = useState("");
  const [addError, setAddError] = useState(null);
  const [addSuccess, setAddSuccess] = useState(null);
  const [lockError, setLockError] = useState(null);
  const [lockSuccess, setLockSuccess] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/notes/')
      .then(res => setNotes(res.data))
      .catch(() => setNotesError('Could not fetch notes'));
  }, []);

  const handleSelect = (uuid) => {
    setDetailsError(null);
    setEditName('');
    setEditDescription('');
    setUpdateError(null);
    setUpdateSuccess(null);
    setEditMode(false);
    setAddMode(false);
    axios.get(`http://localhost:8000/notes/${uuid}`)
      .then(res => {
        setSelectedNote(res.data);
        setEditName(res.data.name);
        setEditDescription(res.data.description || '');
      })
      .catch(() => {
        setDetailsError('Could not fetch note details');
        setSelectedNote(null);
      });
  };

  const handleUpdate = (e) => {
    e.preventDefault();
    setUpdateError(null);
    setUpdateSuccess(null);
    axios.put(`http://localhost:8000/notes/${selectedNote.uuid}`,
      {
        name: editName,
        description: editDescription
      })
      .then(res => {
        setSelectedNote(res.data);
        setUpdateSuccess('Note updated successfully!');
        setEditMode(false);
        setNotes(notes.map(n =>
          n.uuid === selectedNote.uuid ? { ...n, name: res.data.name } : n
        ));
      })
      .catch(err => {
        if (err.response && err.response.status === 409) {
          setUpdateError('Note is locked and cannot be modified.');
        } else {
          setUpdateError('Failed to update note.');
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
    setEditName(selectedNote.name);
    setEditDescription(selectedNote.description || '');
    setUpdateError(null);
    setUpdateSuccess(null);
  };

  const handleLock = () => {
    setLockError(null);
    setLockSuccess(null);
    if (!selectedNote || selectedNote.finalized) return;
    if (window.confirm('Are you sure you want to lock this note? This action cannot be undone.')) {
      axios.put(`http://localhost:8000/notes/${selectedNote.uuid}/lock`)
        .then(res => {
          setSelectedNote(res.data);
          setLockSuccess('Note locked successfully!');
          setEditMode(false);
          setNotes(notes.map(n =>
            n.uuid === selectedNote.uuid ? { ...n, name: res.data.name } : n
          ));
        })
        .catch(err => {
          if (err.response && err.response.status === 409) {
            setLockError('Note is already locked.');
          } else {
            setLockError('Failed to lock note.');
          }
        });
    }
  };

  const handleAddClick = () => {
    setAddMode(true);
    setSelectedNote(null);
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
    axios.post("http://localhost:8000/notes/", {
      name: addName,
      description: addDescription
    })
      .then(res => {
        setNotes([...notes, { uuid: res.data.uuid, name: res.data.name }]);
        setSelectedNote(res.data);
        setEditName(res.data.name);
        setEditDescription(res.data.description || "");
        setAddMode(false);
        setAddSuccess("Note added successfully!");
        setAddName("");
        setAddDescription("");
      })
      .catch(() => setAddError("Failed to add note."));
  };

  const handleAddCancel = () => {
    setAddMode(false);
    setAddName("");
    setAddDescription("");
    setAddError(null);
    setAddSuccess(null);
  };

  const handleDelete = () => {
    if (!selectedNote || selectedNote.finalized) return;
    if (window.confirm('Are you sure you want to delete this note? This action cannot be undone.')) {
      axios.delete(`http://localhost:8000/notes/${selectedNote.uuid}`)
        .then(() => {
          setNotes(notes.filter(n => n.uuid !== selectedNote.uuid));
          setSelectedNote(null);
          setEditMode(false);
          setDetailsError(null);
        })
        .catch(err => {
          if (err.response && err.response.status === 409) {
            setDetailsError('Note is locked and cannot be deleted.');
          } else {
            setDetailsError('Failed to delete note.');
          }
        });
    }
  };

  return {
    notes, setNotes,
    notesError, setNotesError,
    selectedNote, setSelectedNote,
    detailsError, setDetailsError,
    editName, setEditName,
    editDescription, setEditDescription,
    updateError, setUpdateError,
    updateSuccess, setUpdateSuccess,
    editMode, setEditMode,
    addMode, setAddMode,
    addName, setAddName,
    addDescription, setAddDescription,
    addError, setAddError,
    addSuccess, setAddSuccess,
    lockError, lockSuccess, handleSelect, handleUpdate, handleEdit, handleCancelEdit, handleLock, handleAddClick, handleAddSubmit, handleAddCancel, handleDelete,
  };
}

export function useNotes() {
  return useContext(NotesContext);
}
