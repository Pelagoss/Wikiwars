import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path";
import tailwindcss from 'tailwindcss'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), tailwindcss()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "/src"),
            "~@": path.resolve(__dirname, "/src"),
        },
    },
})
