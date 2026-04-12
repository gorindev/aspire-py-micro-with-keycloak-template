import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

import keycloak from './keycloak';

keycloak.init({ onLoad: 'login-required', checkLoginIframe: false }).then(authenticated => {
  if (!authenticated) {
    window.location.reload();
  } else {
    createRoot(document.getElementById('root')!).render(
      <StrictMode>
        <App />
      </StrictMode>,
    );
  }
}).catch(err => {
  console.error("Keycloak initialization failed", err);
  document.getElementById('root')!.innerHTML = '<div style="color: red; padding: 20px;">Failed to connect to authentication server. Is Keycloak running?</div>';
});
