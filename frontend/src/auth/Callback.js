import React, { useEffect } from 'react';
import { useAuth } from './AuthContext';

export default function Callback() {
  const { exchangeCode } = useAuth();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    if (code) {
      exchangeCode(code).then(() => {
        window.location.replace('/');
      }).catch(() => {
        // could display an error UI
        window.location.replace('/');
      });
    } else {
      window.location.replace('/');
    }
  }, [exchangeCode]);

  return <div style={{ padding: 20 }}>Completing sign-in…</div>;
}
