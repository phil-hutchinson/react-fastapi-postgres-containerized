import React from 'react';
import { NotesProvider, useNotes } from '../../hooks/useNotes';
import NoteList from './NoteList';
import AddNoteForm from './AddNoteForm';
import EditNoteForm from './EditNoteForm';
import DisplayNoteDetails from './DisplayNoteDetails';
import { useAuth } from '../../auth/AuthContext';

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
  const { token, claims, login, logout } = useAuth();

  return (
    <div className="layout-container min-h-screen flex flex-col items-center bg-gray-50">
      {/* Top auth bar */}
      <div className="w-full max-w-2xl flex justify-end items-center py-4">
        {token ? (
          <>
            <span className="text-sm text-gray-700 mr-3">Signed in as {claims?.email || claims?.sub}</span>
            <button className="btn" onClick={logout}>Logout</button>
          </>
        ) : (
          <button className="btn" onClick={login}>Login</button>
        )}
      </div>

      <h1 className="app-title">Template Application</h1>
      <div className="w-full max-w-2xl">
        <h2 className="section-title text-center">Notes</h2>
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
