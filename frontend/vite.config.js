import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwind_css from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwind_css()],
})
