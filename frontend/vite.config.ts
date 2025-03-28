import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    host: true,       // Acepta conexiones externas
    port: 5173,
    strictPort: true, // No intentar otros puertos si este está ocupado
    hmr: {
      clientPort: 5173,  // Puerto para Hot Module Replacement
      protocol: 'ws'     // Usar WebSockets para HMR
    },
    watch: {
      usePolling: true   // Necesario para detectar cambios en Docker
    }
  }
})