# 🔐 憑證轉換工具 v2.0.0 GUI版

## [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org) [![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

> 🚀 專業的SSL/TLS憑證格式轉換工具，支援多種Web服務格式，讓您的憑證部署更加簡單！

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  ██████╗███████╗██████╗ ████████╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗    ║
║ ██╔════╝██╔════╝██╔══██╗╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║██║   ██║    ║
║ ██║     █████╗  ██████╔╝   ██║       ██║     ██║   ██║██╔██╗ ██║██║   ██║    ║
║ ██║     ██╔══╝  ██╔══██╗   ██║       ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝    ║
║ ╚██████╗███████╗██║  ██║   ██║       ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝     ║
║  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 目錄

- [功能特色](#-功能特色)
- [支援格式](#-支援格式)
- [支援的Web服務](#-支援的web服務)
- [系統需求](#-系統需求)
- [安裝說明](#-安裝說明)
- [使用方法](#-使用方法)
- [建置說明](#-建置說明)
- [常見問題](#-常見問題)
- [技術支援](#-技術支援)
- [版本歷史](#-版本歷史)
- [授權信息](#-授權信息)

## ✨ 功能特色

### 🎯 核心功能
- **🔄 格式轉換**：PFX/P12 → PEM、CRT、KEY 等格式
- **🌐 多服務支援**：一鍵轉換為各種Web服務所需格式
- **🖥️ 圖形界面**：直觀易用的GUI操作界面
- **📊 即時進度**：轉換進度條和詳細日誌顯示
- **🔒 安全處理**：自動移除私鑰密碼保護（適合自動部署）

### 💡 界面特色
- **🎨 現代化設計**：美觀的ASCII藝術標題和配色方案
- **📁 智慧檔案選擇**：支援多種憑證格式，自動驗證
- **⚙️ 靈活設定**：自訂域名、輸出選項等
- **📋 詳細日誌**：完整的操作記錄，支援儲存
- **🚀 一鍵操作**：並排按鈕設計，操作更便捷

## 📄 支援格式

### 輸入格式
| 格式 | 副檔名 | 說明 |
|------|--------|------|
| **PFX** | `.pfx` | Personal Information Exchange，Windows常用格式 |
| **PKCS#12** | `.p12` | Public Key Cryptography Standards #12 |

### 輸出格式
| 格式 | 副檔名 | 用途 |
|------|--------|------|
| **PEM私鑰** | `.key` | OpenSSL格式私鑰檔案 |
| **PEM憑證** | `.crt` | X.509憑證檔案 |
| **憑證鏈** | `.chain.crt` | 中繼憑證鏈 |
| **完整鏈** | `.fullchain.crt` | 憑證+憑證鏈合併檔案 |
| **合併檔** | `.pem` | 憑證+私鑰+鏈合併檔案 |

## 🌐 支援的Web服務

| 服務 | 圖示 | 說明 | 產生檔案 |
|------|------|------|----------|
| **Nginx** | 🚀 | 高性能Web伺服器和反向代理 | `.key`, `.crt`, `.fullchain.crt` |
| **Apache** | 🪶 | 世界上最流行的Web伺服器 | `.key`, `.crt`, `.chain.crt` |
| **Microsoft IIS** | 🏢 | Windows平台Web伺服器 | `.key`, `.crt`, `.pfx` |
| **HAProxy** | ⚖️ | 高可用性負載均衡器 | `.pem` (合併檔) |
| **Traefik** | 🚦 | 現代化反向代理和負載均衡器 | `.key`, `.crt` |
| **Caddy** | 🍭 | 自動HTTPS的Web伺服器 | `.key`, `.crt` |

## 💻 系統需求

### 最低需求
- **作業系統**：Windows 7/8/10/11、macOS 10.12+、Linux (Ubuntu 18.04+)
- **Python版本**：Python 3.7 或更高版本
- **記憶體**：至少 50MB 可用空間
- **硬碟空間**：100MB（包含依賴套件）

### 推薦環境
- **作業系統**：Windows 10/11、macOS 12+、Linux (Ubuntu 20.04+)
- **Python版本**：Python 3.9 或更高版本
- **記憶體**：100MB 或更多

## 🚀 安裝說明

### 方式一：執行檔版本（推薦）
1. 下載最新的 Release 版本
2. 解壓縮到任意目錄
3. 執行 `CertConverter-GUI.exe`（Windows）
4. 無需安裝 Python 或任何依賴

### 方式二：Python 原始碼
```bash
# 1. 克隆專案
git clone https://github.com/yourname/cert-converter-gui.git
cd cert-converter-gui

# 2. 建立虛擬環境（推薦）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 執行程式
python cert_converter_gui.py
```

### 依賴套件
```txt
cryptography>=3.4.8
pathlib>=1.0.1
```

## 📖 使用方法

### 基本操作流程

1. **🔴 選擇憑證檔案**
   - 點擊「📂 瀏覽檔案」選擇 PFX 或 P12 檔案
   - 或使用快捷鍵 `Ctrl+O`

2. **🔵 選擇目標服務**
   - 點擊對應的 Web 服務圖示
   - 程式會自動配置對應的輸出格式

3. **🟡 設定轉換參數**
   - 輸入 PFX 密碼（如有設定）
   - 自訂域名（可選，留空自動提取）
   - 選擇輸出選項

4. **🟢 執行轉換**
   - 點擊「🚀 開始轉換」
   - 觀察進度條和日誌訊息
   - 轉換完成後可選擇開啟輸出資料夾

### 快捷鍵
| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+O` | 開啟檔案選擇對話框 |
| `F1` | 顯示說明視窗 |

### 輸出結構
```
nginx_example.com/
├── example.com.key           # 私鑰檔案
├── example.com.crt           # 憑證檔案
├── example.com.fullchain.crt # 完整憑證鏈
└── README.md                 # 使用說明
```

## 🔨 建置說明

### Windows 執行檔建置
```batch
# 執行自動建置腳本
build_gui.bat
```

### 手動建置
```bash
# 1. 安裝 PyInstaller
pip install pyinstaller

# 2. 建置單一執行檔
pyinstaller --onefile --windowed --name "CertConverter-GUI" cert_converter_gui.py

# 3. 建置目錄版本
pyinstaller --onedir --windowed --name "CertConverter-GUI" cert_converter_gui.py
```

### 建置選項說明
- `--onefile`：建置為單一執行檔
- `--onedir`：建置為目錄版本（啟動較快）
- `--windowed`：隱藏命令列視窗
- `--clean`：清除快取，確保乾淨建置

## ❓ 常見問題

### Q: 轉換後的私鑰沒有密碼，安全嗎？
**A:** 這是設計行為。Web 伺服器通常需要無密碼的私鑰來實現自動啟動。請確保：
- 設定適當的檔案權限（Linux/macOS: `chmod 600 *.key`）
- 將私鑰存放在安全的目錄
- 定期更新憑證

### Q: 支援萬用字元憑證嗎？
**A:** 是的，完全支援萬用字元憑證（Wildcard Certificate）。檔案名稱中的 `*` 會自動替換為 `wildcard`。

### Q: 可以批次轉換多個憑證嗎？
**A:** 目前版本不支援批次轉換，每次只能轉換一個憑證檔案。

### Q: 轉換失敗怎麼辦？
**A:** 請檢查：
1. PFX 檔案是否損壞
2. 密碼是否正確
3. 檔案權限是否足夠
4. 查看詳細日誌了解錯誤原因

### Q: 程式無法啟動？
**A:** 可能的解決方案：
- 以系統管理員身分執行
- 檢查防毒軟體是否阻擋
- 確認 Python 版本相容性

## 📞 技術支援

### 🐛 問題回報
如果您遇到任何問題，請提供以下資訊：
- 作業系統版本
- Python 版本（如適用）
- 錯誤訊息的完整日誌
- 重現問題的步驟

### 💡 功能建議
歡迎透過 GitHub Issues 提供功能改進建議：
- 新的 Web 服務支援
- 界面優化建議
- 自動化功能需求

## 📈 版本歷史

### v2.0.0 (2025-01-XX) - GUI版本
- ✨ **新增**：完整的圖形用戶界面
- ✨ **新增**：即時進度顯示和詳細日誌
- ✨ **新增**：6種主流Web服務支援
- 🎨 **改進**：現代化界面設計
- 🔧 **優化**：更好的錯誤處理和用戶體驗

### v1.0.0 (2024-XX-XX) - 命令列版本
- 🎉 **初版**：基本的PFX轉換功能
- 📝 **功能**：命令列操作界面
- 🔧 **支援**：基本的憑證格式轉換

## 📋 待辦事項

- [ ] 增加批次轉換功能
- [ ] 支援更多憑證格式（JKS、DER等）
- [ ] 增加憑證資訊檢視功能
- [ ] 支援憑證有效期檢查
- [ ] 增加多語言支援
- [ ] macOS 和 Linux 原生建置

## 🤝 貢獻指南

歡迎貢獻程式碼！請遵循以下步驟：

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權信息

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**🔐 讓SSL憑證部署變得簡單！**

Made with ❤️

[⬆ 回到頂部](#-憑證轉換工具-v200-gui版)

</div>