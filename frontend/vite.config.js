import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: './dist',
    manifest: true,     // Генерирует manifest.json (опционально)
    emptyOutDir: true,  // Очищать папку перед сборкой
    rollupOptions: {
      input: path.resolve(__dirname, 'src/main.js'),  // Точка входа
      // output: { # это если мы не используем manifest
      //   entryFileNames: 'assets/main.js',    // Фиксированное имя JS
      //   chunkFileNames: 'assets/[name].js',  // Фиксированные имена чанков
      //   assetFileNames: 'assets/[name].[ext]' // Фиксированные имена CSS/других assets
      // }
    },
  },
  server: {
    port: 5173,        // Порт для dev-сервера
    strictPort: true,
    cors: true,
    historyApiFallback: true,
    proxy: {
      '/admin': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    }
  },
})

