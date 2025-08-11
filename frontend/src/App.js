import './index.css';
import NotesApp from './components/notes/NotesApp';
import { AuthProvider } from './auth/AuthContext';
import Callback from './auth/Callback';

function App() {
  const path = window.location.pathname;
  if (path === '/callback') {
    return (
      <AuthProvider>
        <Callback />
      </AuthProvider>
    );
  }
  return (
    <AuthProvider>
      <NotesApp />
    </AuthProvider>
  );
}

export default App;
