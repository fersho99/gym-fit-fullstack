import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    // semantic-ui-css trae selectores que el minificador de CSS de Vite rechaza.
    cssMinify: false,
  },
});
