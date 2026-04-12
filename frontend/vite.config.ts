import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'import.meta.env.VITE_KEYCLOAK_URL': JSON.stringify(
      process.env.services__keycloak__http__0 ||
      process.env.services__keycloak__https__0 ||
      'http://localhost:8080'
    )
  },
  server: {
    allowedHosts: ['host.docker.internal'],
    host: true,
    proxy: {
      // Proxy API calls to the app service
      '/weather/api': {
        target: process.env.GATEWAY_HTTPS || process.env.GATEWAY_HTTP,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/weather/, '')
      },
      '/weather-ai-outfit/api': {
        target: process.env.GATEWAY_HTTPS || process.env.GATEWAY_HTTP,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/weather-ai-outfit/, '')
      }
    }
  }
});
