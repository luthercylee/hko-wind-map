# HKO 風場地圖

香港天文台十分鐘平均風向風速即時地圖，利用 GitHub Actions 自動更新資料。

## 架構說明

```
repo/
├── index.html                         # 地圖前端頁面（Leaflet.js）
├── fetch_wind.py                      # 抓取天文台 CSV → 轉存 wind_data.json
├── wind_data.json                     # 由 Actions 自動產生，勿手動修改
└── .github/workflows/
    └── update-wind-data.yml           # GitHub Actions 排程設定
```

## 部署步驟

### 1. 建立 GitHub Repo
建立一個 **public** repo，例如 `hko-wind-map`。

### 2. 上傳所有檔案
保持以上資料夾結構上傳到 repo 根目錄。

### 3. 設定 Actions 寫入權限
Settings → Actions → General → Workflow permissions → **Read and write permissions** → Save

### 4. 手動觸發第一次
Actions → Update HKO Wind Data → **Run workflow**
確認 `wind_data.json` 成功產生在 repo 中。

### 5. 開啟 GitHub Pages
Settings → Pages → Source: **Deploy from a branch** → Branch: `main` / `(root)` → Save

完成後即可透過 `https://你的帳號.github.io/hko-wind-map/` 瀏覽風場地圖。

## 運作說明

- GitHub Actions 每 10 分鐘在雲端執行 `fetch_wind.py`，直接呼叫天文台 API（無 CORS 限制），更新 `wind_data.json` 並自動 commit。
- 網頁每分鐘讀取一次 `wind_data.json`，屬同源請求，完全不需要任何第三方 CORS 代理。
- 完全免費，public repo 的 Actions 額度非常充足。
