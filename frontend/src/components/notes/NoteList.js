import React from 'react';
import { useNotes } from '../../hooks/useNotes';

function NoteList() {
  const { notes, handleSelect, notesError, addMode, editMode } = useNotes();
  const disabled = addMode || editMode;

  if (notesError) {
    return <div style={{color: 'red'}}>{notesError}</div>;
  }
  if (notes === null) {
    return <div>Loading...</div>;
  }
  if (notes.length === 0) {
    return <div>No notes found.</div>;
  }
  return (
    <ul>
      {notes.map(note => (
        <li key={note.uuid}>
          <button
            onClick={() => handleSelect(note.uuid)}
            disabled={disabled}
            className="selection-card"
          >
            <strong>{note.name}</strong>
          </button>
        </li>
      ))}
    </ul>
  );
}

export default NoteList;
