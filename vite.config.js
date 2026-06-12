import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // 相對路徑 base，讓打包結果放在 GitHub Pages 子路徑下也能正常載入資源
  base: "./",
  plugins: [react(), tailwindcss()],
});
