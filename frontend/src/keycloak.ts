import Keycloak from 'keycloak-js';

// Setup Keycloak instance
// Vite replaces import.meta.env.VITE_KEYCLOAK_URL during build/dev
const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL,
  realm: 'app',
  clientId: 'frontend'
});

export default keycloak;
