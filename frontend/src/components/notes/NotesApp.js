import React from 'react';
import { NotesProvider, useNotes } from '../../hooks/useNotes';
import NoteList from './NoteList';
import AddNoteForm from './AddNoteForm';
import EditNoteForm from './EditNoteForm';
import DisplayNoteDetails from './DisplayNoteDetails';

function NotesApp() {
  return (
    <NotesProvider>
      <NotesAppContent />
    </NotesProvider>
  );
}

function NotesAppContent() {
  const {
    selectedNote,
    detailsError,
    editMode,
    addMode,
    handleAddClick
  } = useNotes();

  return (
    <div className="layout-container min-h-screen flex flex-col items-center bg-gray-50">
      <h1 className="app-title">Template App: React/FastAPI/Postgres</h1>
      <div className="w-full max-w-2xl">
        <h2 className="section-title">Notes:</h2>
        <NoteList />
        <button
          onClick={handleAddClick}
          disabled={addMode || editMode}
          className="btn mt-4 w-full"
        >
          Add Note
        </button>
        {addMode ? (
          <AddNoteForm />
        ) : selectedNote || detailsError ?
            editMode ? (
              <EditNoteForm />
            ) : (
              <DisplayNoteDetails />
            )
          : null
        }
      </div>
    </div>
  );
}

export default NotesApp;
