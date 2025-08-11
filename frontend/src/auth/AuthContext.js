import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import axios from 'axios';

const OIDC = {
  authorizeUrl: 'http://localhost:8088/authorize',
  tokenUrl: 'http://localhost:8088/token',
  clientId: 'dev-client',
  redirectUri: 'http://localhost:3000/callback',
  scope: 'openid profile email',
};

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [claims, setClaims] = useState(null);

  // Parse JWT (no verification; dev only)
  const parseJwt = (jwt) => {
    try {
      const [, payload] = jwt.split('.');
      return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    } catch {
      return null;
    }
  };

  const login = () => {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: OIDC.clientId,
      redirect_uri: OIDC.redirectUri,
      scope: OIDC.scope,
      state: 'xyz'
    });
    window.location.assign(`${OIDC.authorizeUrl}?${params.toString()}`);
  };

  const logout = () => {
    setToken(null);
    setClaims(null);
    sessionStorage.removeItem('id_token');
  };

  const exchangeCode = async (code) => {
    const form = new URLSearchParams();
    form.set('grant_type', 'authorization_code');
    form.set('code', code);
    form.set('redirect_uri', OIDC.redirectUri);
    form.set('client_id', OIDC.clientId);

    const res = await fetch(OIDC.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString()
    });
    if (!res.ok) throw new Error('Token exchange failed');
    const data = await res.json();
    const jwt = data.id_token || data.access_token;
    setToken(jwt);
    sessionStorage.setItem('id_token', jwt);
    setClaims(parseJwt(jwt));
  };

  useEffect(() => {
    const stored = sessionStorage.getItem('id_token');
    if (stored) {
      setToken(stored);
      setClaims(parseJwt(stored));
    }
  }, []);

  // Apply/remove Authorization header globally for axios
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const value = useMemo(() => ({ token, claims, login, logout, exchangeCode }), [token, claims]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
