# cert_converter_gui

桌面工具：把 PFX / PKCS#12 憑證轉成各種 Web 伺服器用的 PEM 檔，Tkinter 圖形介面。

## 檔案

| 路徑 | 用途 |
|------|------|
| `cert_converter_gui.py` | 整個程式（單檔，介面與轉檔邏輯都在 `CertConverterGUI` 類別） |
| `requirements.txt` | 相依套件：cryptography、pyinstaller |
| `build_gui.bat` | Windows 上用 PyInstaller 打包成執行檔 |
| `git_sync.sh` | 同步用的輔助腳本 |
| `readme.md` | 使用說明 |

## 設計約束

- 輸出資料夾與檔名取自憑證的 CN 或使用者輸入，一律先經過 `sanitize_filename`，只留英數與 `.`、`_`、`-`。
- 開啟輸出資料夾不經過 shell：Windows 用 `os.startfile`，macOS 用 `open`，其他平台用 `xdg-open`，路徑以參數清單傳入。
- 含私鑰的輸出檔（私鑰、合併檔、無密碼 PFX）權限設為 0600，輸出資料夾 0700。

## 驗證

沒有自動化測試。改轉檔邏輯後，用自簽憑證（含 CN 帶特殊字元的情況）跑一次 `extract_domain` 與 `generate_certificate_files`，確認資料夾名稱、檔案權限與輸出內容。

## 部署

沒有線上服務，沒有發行版；使用者直接執行原始碼或自行打包。
