import React, { useEffect, useState } from 'react';

function App() {
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/test')
      .then(res => res.json())
      .then(data => setTestResult(data))
      .catch(() => setTestResult({ error: 'Could not reach backend' }));
  }, []);

  return (
    <div>
      <h1>Starter App: React &mdash; FastAPI &mdash; Postgres</h1>
      <div>
        <h2>Backend /test endpoint:</h2>
        <pre>{testResult ? JSON.stringify(testResult, null, 2) : 'Loading...'}</pre>
      </div>
    </div>
  );
}

export default App;
