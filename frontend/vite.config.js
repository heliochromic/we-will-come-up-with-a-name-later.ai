import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwind_css from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwind_css()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
