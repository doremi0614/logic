# Sequential Circuit Design Automation System

以 React + Tailwind CSS 製作的循序電路設計自動化系統（SPA）。
輸入狀態表後會**真正執行設計流程**並即時產生輸出，所有 UI 與運算邏輯集中在單一檔案 [src/App.jsx](src/App.jsx)。

## 運算流程（按下 GENERATE 後）

1. **狀態指定（State Assignment）**：依出現順序給每個狀態二進位編碼（A=00、B=01…），自動決定需要幾個 Flip-Flop
2. **激勵表（Excitation Table）**：依 JK 或 T Flip-Flop 的激勵表，從「現態 → 次態」推導每個 FF 輸入的真值表（未出現的組合自動視為 don't care）
3. **布林化簡**：用 Quine-McCluskey 演算法求質含項（prime implicants）並選出最小覆蓋
4. **輸出**：
   - 化簡後的 FF 輸入方程式與輸出方程式（Mealy 看狀態+輸入；Moore 只看狀態）
   - 即時 K-Map（可切換任一函數，用顏色標示選到的質含項群組）
   - 依方程式動態繪製的電路圖（AND/OR 閘與接線自動佈局，可縮放、全螢幕、下載 SVG）
   - EXPORT REPORT 會下載完整設計報告（.txt）

輸入驗證：空狀態、未定義的次態、重複的（狀態,輸入)列、Moore 模型下同狀態輸出不一致等都會顯示錯誤或警告。

## 本機開發

```powershell
npm install
npm run dev      # 開發伺服器 http://localhost:5173
npm run build    # 打包到 dist/
```

不想裝任何東西的話，直接用瀏覽器開啟 [standalone.html](standalone.html)（CDN 版，需要網路）。

## 放上 GitHub 並自動部署網站

本 repo 已附好 [.github/workflows/deploy.yml](.github/workflows/deploy.yml)，push 到 GitHub 後會自動建置並部署到 GitHub Pages。

1. 到 [github.com/new](https://github.com/new) 建立一個新 repository（例如 `sequential-circuit-design`），**不要**勾選任何初始化選項
2. 在專案資料夾執行：

   ```powershell
   git remote add origin https://github.com/<你的帳號>/sequential-circuit-design.git
   git push -u origin main
   ```

   第一次 push 會跳出瀏覽器要求登入 GitHub（Git Credential Manager）
3. 到 repo 的 **Settings → Pages**，把 **Source** 改成 **GitHub Actions**
4. 等 Actions 跑完（repo 的 Actions 分頁可以看進度），網站就會出現在：
   `https://<你的帳號>.github.io/sequential-circuit-design/`

之後每次更新只要：

```powershell
git add -A
git commit -m "說明這次改了什麼"
git push
```

## 技術

- React 19 + Vite 6
- Tailwind CSS v4（`@tailwindcss/vite` plugin）
- Lucide React icons
- 無任何後端 —— 布林化簡與電路佈局皆在前端計算
