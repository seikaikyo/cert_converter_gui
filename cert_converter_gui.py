#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web服務憑證轉換工具 - GUI版本
專為各種Web服務優化的憑證格式轉換，支援PFX到PEM的轉換

版本：2.0.0 GUI Edition

功能特色：
- 直觀的檔案選擇界面
- 支援 PFX (.pfx) 和 PKCS#12 (.p12) 格式
- 多種 Web 服務格式轉換
- 即時進度顯示和詳細日誌
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkFont
import os
import sys
import threading
import time
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography import x509
import webbrowser


class CertConverterGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("憑證轉換工具 v2.0.0")
        self.root.geometry("1000x650")  # 改為更寬的窗口
        self.root.resizable(True, True)

        # 設定圖示和樣式
        self.setup_styles()

        # 初始化變數
        self.selected_file = tk.StringVar()
        self.selected_service = tk.StringVar(value="nginx")
        self.password_var = tk.StringVar()
        self.custom_domain = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.backend = default_backend()

        # 初始化 log_text 為 None
        self.log_text = None

        # Web服務配置
        self.web_service_configs = {
            'nginx': {
                'name': 'Nginx',
                'description': '高性能Web伺服器和反向代理',
                'icon': '🚀',
                'files': {
                    'private_key': '{domain}.key',
                    'certificate': '{domain}.crt',
                    'fullchain': '{domain}.fullchain.crt'
                }
            },
            'apache': {
                'name': 'Apache HTTP Server',
                'description': '世界上最流行的Web伺服器',
                'icon': '🪶',
                'files': {
                    'private_key': '{domain}.key',
                    'certificate': '{domain}.crt',
                    'chain': '{domain}.chain.crt'
                }
            },
            'iis': {
                'name': 'Microsoft IIS',
                'description': 'Windows平台Web伺服器',
                'icon': '🏢',
                'files': {
                    'private_key': '{domain}.key',
                    'certificate': '{domain}.crt',
                    'pfx_output': '{domain}_for_iis.pfx'
                }
            },
            'haproxy': {
                'name': 'HAProxy',
                'description': '高可用性負載均衡器',
                'icon': '⚖️',
                'files': {
                    'combined': '{domain}.pem'
                }
            },
            'traefik': {
                'name': 'Traefik',
                'description': '現代化反向代理和負載均衡器',
                'icon': '🚦',
                'files': {
                    'private_key': '{domain}.key',
                    'certificate': '{domain}.crt'
                }
            },
            'caddy': {
                'name': 'Caddy',
                'description': '自動HTTPS的Web伺服器',
                'icon': '🍭',
                'files': {
                    'private_key': '{domain}.key',
                    'certificate': '{domain}.crt'
                }
            }
        }

        # 建立界面
        self.create_widgets()

        # 設定拖放功能
        self.setup_drag_drop()

    def setup_styles(self):
        """設定樣式"""
        # 設定主題色彩
        self.colors = {
            'primary': '#2C3E50',  # 深藍灰
            'secondary': '#3498DB',  # 天藍
            'accent': '#E74C3C',  # 紅色
            'success': '#27AE60',  # 綠色
            'warning': '#F39C12',  # 橙色
            'background': '#ECF0F1',  # 淺灰
            'text': '#2C3E50',  # 深灰
            'light': '#FFFFFF'  # 白色
        }

        # 設定字體
        self.fonts = {
            'title': ('Arial', 16, 'bold'),
            'subtitle': ('Arial', 12, 'bold'),
            'body': ('Arial', 10),
            'small': ('Arial', 8),
            'mono': ('Consolas', 9)
        }

        # 設定背景色
        self.root.configure(bg=self.colors['background'])

        # 設定ttk樣式
        style = ttk.Style()
        style.theme_use('clam')

        # 自定義按鈕樣式
        style.configure('Primary.TButton',
                        background=self.colors['primary'],
                        foreground='white',
                        font=self.fonts['body'],
                        padding=(10, 5))

        style.configure('Success.TButton',
                        background=self.colors['success'],
                        foreground='white',
                        font=self.fonts['body'],
                        padding=(10, 5))

        style.configure('Warning.TButton',
                        background=self.colors['warning'],
                        foreground='white',
                        font=self.fonts['body'],
                        padding=(10, 5))

    def create_widgets(self):
        """建立界面元件 - 寬格式左右分欄布局"""
        # 建立主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 設定權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)  # 讓日誌區域可以擴展

        # 標題區域 - 跨越兩列
        self.create_header(main_frame)

        # 左側欄位
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1,
                        column=0,
                        sticky=(tk.W, tk.E, tk.N, tk.S),
                        padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)

        # 右側欄位
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1,
                         column=1,
                         sticky=(tk.W, tk.E, tk.N, tk.S),
                         padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)

        # 左側內容
        self.create_file_section_compact(left_frame)
        self.create_service_section_compact(left_frame)

        # 右側內容
        self.create_settings_section_compact(right_frame)
        self.create_progress_section(right_frame)
        self.create_action_section(right_frame)  # 把執行按鈕放在轉換進度下方

        # 日誌區域 - 跨越兩列，放在下方
        self.create_log_section_wide(main_frame)

        # 底部資訊 - 跨越兩列
        self.create_footer(main_frame)

    def create_header(self, parent):
        """建立標題區域"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0,
                          column=0,
                          columnspan=2,
                          sticky=(tk.W, tk.E),
                          pady=(0, 15))  # 跨越兩列
        header_frame.columnconfigure(0, weight=1)

        # ASCII藝術標題 - 置中顯示
        ascii_title = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  ██████╗███████╗██████╗ ████████╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗    ║
║ ██╔════╝██╔════╝██╔══██╗╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║██║   ██║    ║
║ ██║     █████╗  ██████╔╝   ██║       ██║     ██║   ██║██╔██╗ ██║██║   ██║    ║
║ ██║     ██╔══╝  ██╔══██╗   ██║       ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝    ║
║ ╚██████╗███████╗██║  ██║   ██║       ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝     ║
║  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝      ║
║                                                                              ║
║                    🔐 Web服務憑證轉換工具 v2.0.0 GUI版 🔐                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """

        ascii_label = tk.Label(header_frame,
                               text=ascii_title,
                               font=self.fonts['mono'],
                               fg=self.colors['primary'],
                               bg=self.colors['background'],
                               justify=tk.CENTER)
        ascii_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # 功能說明 - 也置中顯示
        desc_text = "🚀 專業的憑證格式轉換工具，支援多種Web服務格式，讓您的SSL/TLS憑證部署更加簡單！\n💡 點擊「瀏覽檔案」開始選擇您的PFX或P12憑證檔案"
        desc_label = tk.Label(
            header_frame,
            text=desc_text,
            font=self.fonts['body'],
            fg=self.colors['text'],
            bg=self.colors['background'],
            wraplength=900,  # 增加換行寬度以適應寬格式
            justify=tk.CENTER)
        desc_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

    def create_file_section_compact(self, parent):
        """建立檔案選擇區域 - 緊湊版（移除拖放區域）"""
        file_frame = ttk.LabelFrame(parent, text="📁 選擇PFX憑證檔案", padding="15")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)

        # 檔案選擇說明
        info_label = tk.Label(file_frame,
                              text="🔐 支援格式：PFX (.pfx) 和 PKCS#12 (.p12) 憑證檔案",
                              font=self.fonts['small'],
                              fg=self.colors['text'],
                              bg=self.colors['background'])
        info_label.grid(row=0,
                        column=0,
                        columnspan=2,
                        sticky=tk.W,
                        pady=(0, 8))

        # 檔案選擇區域
        select_frame = ttk.Frame(file_frame)
        select_frame.grid(row=1,
                          column=0,
                          columnspan=2,
                          sticky=(tk.W, tk.E),
                          pady=(0, 5))
        select_frame.columnconfigure(0, weight=1)

        # 檔案路徑輸入框
        self.file_entry = ttk.Entry(select_frame,
                                    textvariable=self.selected_file,
                                    font=self.fonts['body'],
                                    state='readonly')  # 設為只讀，避免手動輸入錯誤路徑
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8))

        # 瀏覽按鈕 - 更大更顯眼
        browse_btn = ttk.Button(select_frame,
                                text="📂 瀏覽檔案",
                                command=self.browse_file,
                                style='Primary.TButton')
        browse_btn.grid(row=0, column=1, sticky=tk.W)

        # 檔案狀態顯示
        self.file_status_frame = ttk.Frame(file_frame)
        self.file_status_frame.grid(row=2,
                                    column=0,
                                    columnspan=2,
                                    sticky=(tk.W, tk.E),
                                    pady=(8, 0))
        self.file_status_frame.columnconfigure(1, weight=1)

        # 檔案狀態圖示
        self.file_status_icon = tk.Label(self.file_status_frame,
                                         text="⏳",
                                         font=self.fonts['body'],
                                         fg=self.colors['warning'],
                                         bg=self.colors['background'])
        self.file_status_icon.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        # 檔案資訊顯示
        self.file_info_label = tk.Label(self.file_status_frame,
                                        text="請選擇要轉換的PFX憑證檔案",
                                        font=self.fonts['small'],
                                        fg=self.colors['text'],
                                        bg=self.colors['background'])
        self.file_info_label.grid(row=0, column=1, sticky=tk.W)

    def create_service_section_compact(self, parent):
        """建立Web服務選擇區域 - 緊湊版"""
        service_frame = ttk.LabelFrame(parent,
                                       text="🌐 選擇目標Web服務",
                                       padding="10")
        service_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        service_frame.columnconfigure(0, weight=1)

        # 服務選擇網格
        services_grid = ttk.Frame(service_frame)
        services_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # 設定網格列權重，讓按鈕寬度一致
        for col in range(2):  # 改為2列以適應緊湊布局
            services_grid.columnconfigure(col,
                                          weight=1,
                                          uniform="service_buttons")

        # 先建立服務描述標籤
        self.service_desc = tk.Label(service_frame,
                                     text="",
                                     font=self.fonts['small'],
                                     fg=self.colors['text'],
                                     bg=self.colors['background'],
                                     wraplength=400)
        self.service_desc.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # 建立服務按鈕
        self.service_buttons = {}
        row, col = 0, 0

        for service_id, config in self.web_service_configs.items():
            # 服務按鈕
            btn = tk.Button(
                services_grid,
                text=f"{config['icon']}\n{config['name']}",
                font=self.fonts['small'],
                bg=self.colors['light'],
                fg=self.colors['text'],
                relief=tk.RAISED,
                borderwidth=1,
                height=2,
                command=lambda s=service_id: self.select_service(s))

            btn.grid(row=row,
                     column=col,
                     padx=2,
                     pady=2,
                     sticky=(tk.W, tk.E, tk.N, tk.S))

            self.service_buttons[service_id] = btn

            col += 1
            if col >= 2:  # 每行2個
                col = 0
                row += 1

        # 設定預設選擇
        self.select_service('nginx')

    def create_settings_section_compact(self, parent):
        """建立設定區域 - 緊湊版"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ 轉換設定", padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)

        # PFX密碼
        ttk.Label(settings_frame, text="🔐 密碼:",
                  font=self.fonts['body']).grid(row=0, column=0, sticky=tk.W)

        self.password_entry = ttk.Entry(settings_frame,
                                        textvariable=self.password_var,
                                        show="*",
                                        font=self.fonts['body'])
        self.password_entry.grid(row=0,
                                 column=1,
                                 sticky=(tk.W, tk.E),
                                 padx=(5, 5))

        show_password_btn = ttk.Button(settings_frame,
                                       text="👁️",
                                       command=self.toggle_password_visibility,
                                       width=3)
        show_password_btn.grid(row=0, column=2, sticky=tk.W)

        # 自訂域名
        ttk.Label(settings_frame, text="🌍 域名:",
                  font=self.fonts['body']).grid(row=1,
                                                column=0,
                                                sticky=tk.W,
                                                pady=(5, 0))

        self.domain_entry = ttk.Entry(settings_frame,
                                      textvariable=self.custom_domain,
                                      font=self.fonts['body'])
        self.domain_entry.grid(row=1,
                               column=1,
                               columnspan=2,
                               sticky=(tk.W, tk.E),
                               padx=(5, 0),
                               pady=(5, 0))

        # 輸出選項
        self.create_readme_var = tk.BooleanVar(value=True)
        self.open_output_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(settings_frame,
                        text="📄 產生說明",
                        variable=self.create_readme_var).grid(row=2,
                                                              column=0,
                                                              columnspan=2,
                                                              sticky=tk.W,
                                                              pady=(5, 0))

        ttk.Checkbutton(settings_frame,
                        text="📂 開啟資料夾",
                        variable=self.open_output_var).grid(row=3,
                                                            column=0,
                                                            columnspan=2,
                                                            sticky=tk.W)

    def create_action_section(self, parent):
        """建立操作按鈕區域 - 並排布局"""
        action_frame = ttk.LabelFrame(parent, text="🚀 執行操作", padding="10")
        action_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # 設定三列等寬
        for i in range(3):
            action_frame.columnconfigure(i, weight=1, uniform="action_buttons")

        # 轉換按鈕
        self.convert_btn = ttk.Button(action_frame,
                                      text="🚀 開始轉換",
                                      command=self.start_conversion,
                                      style='Success.TButton')
        self.convert_btn.grid(row=0,
                              column=0,
                              sticky=(tk.W, tk.E),
                              padx=(0, 3))

        # 清除按鈕
        clear_btn = ttk.Button(action_frame,
                               text="🗑️ 清除",
                               command=self.clear_all,
                               style='Warning.TButton')
        clear_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(3, 3))

        # 說明按鈕
        help_btn = ttk.Button(action_frame,
                              text="❓ 說明",
                              command=self.show_help,
                              style='Primary.TButton')
        help_btn.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(3, 0))

    def create_progress_section(self, parent):
        """建立進度條區域"""
        progress_frame = ttk.LabelFrame(parent, text="📊 轉換進度", padding="10")
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_label = tk.Label(progress_frame,
                                       text="準備就緒",
                                       font=self.fonts['body'],
                                       fg=self.colors['text'],
                                       bg=self.colors['background'])
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.progress_bar = ttk.Progressbar(progress_frame,
                                            variable=self.progress_var,
                                            maximum=100,
                                            mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def create_log_section_wide(self, parent):
        """建立日誌區域 - 寬版本"""
        log_frame = ttk.LabelFrame(parent, text="📋 執行日誌", padding="10")
        log_frame.grid(row=2,
                       column=0,
                       columnspan=2,
                       sticky=(tk.W, tk.E, tk.N, tk.S),
                       pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=8,
                                                  font=self.fonts['mono'],
                                                  bg=self.colors['light'],
                                                  fg=self.colors['text'],
                                                  wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 日誌工具列
        log_toolbar = ttk.Frame(log_frame)
        log_toolbar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        ttk.Button(log_toolbar, text="🗑️ 清除日誌",
                   command=self.clear_log).grid(row=0, column=0, sticky=tk.W)

        ttk.Button(log_toolbar, text="💾 儲存日誌",
                   command=self.save_log).grid(row=0,
                                               column=1,
                                               sticky=tk.W,
                                               padx=(10, 0))

    def create_footer(self, parent):
        """建立底部資訊"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=3,
                          column=0,
                          columnspan=2,
                          sticky=(tk.W, tk.E),
                          pady=(10, 0))
        footer_frame.columnconfigure(1, weight=1)

        # 版權資訊
        copyright_text = "Certificate Converter v2.0.0"
        copyright_label = tk.Label(footer_frame,
                                   text=copyright_text,
                                   font=self.fonts['small'],
                                   fg=self.colors['text'],
                                   bg=self.colors['background'])
        copyright_label.grid(row=0, column=0, sticky=tk.W)

        # 聯絡連結

    def setup_drag_drop(self):
        """設定拖放功能"""
        # 為檔案輸入框設定點擊事件
        self.file_entry.bind("<Button-1>", lambda e: self.browse_file())

    def browse_file(self):
        """瀏覽檔案"""
        file_path = filedialog.askopenfilename(title="選擇PFX憑證檔案",
                                               filetypes=[
                                                   ("PFX憑證檔案", "*.pfx"),
                                                   ("PKCS#12檔案", "*.p12"),
                                                   ("所有支援格式", "*.pfx;*.p12"),
                                                   ("所有檔案", "*.*")
                                               ])

        if file_path:
            self.selected_file.set(file_path)
            self.update_file_info(file_path)
            self.update_file_status(file_path)
            self.log_message(f"✅ 已選擇檔案: {Path(file_path).name}")

    def update_file_status(self, file_path):
        """更新檔案狀態顯示"""
        filename = Path(file_path).name

        # 更新狀態圖示為成功
        self.file_status_icon.configure(text="✅", fg=self.colors['success'])

        # 顯示檔案名稱（如果太長則截斷）
        if len(filename) > 45:
            display_name = filename[:42] + "..."
        else:
            display_name = filename

        self.file_info_label.configure(text=f"已選擇檔案: {display_name}")

    def update_drop_zone(self, file_path):
        """更新拖放區域顯示（已移除此功能）"""
        pass

    def update_file_info(self, file_path):
        """更新檔案資訊"""
        try:
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024

            info_text = f"📁 {file_size_kb:.1f} KB"
            self.file_info_label.configure(text=info_text)
        except Exception as e:
            self.file_info_label.configure(text=f"❌ 讀取錯誤")

    def select_service(self, service_id):
        """選擇Web服務"""
        self.selected_service.set(service_id)

        # 更新按鈕樣式
        for sid, btn in self.service_buttons.items():
            if sid == service_id:
                btn.configure(bg=self.colors['secondary'],
                              fg='white',
                              relief=tk.SUNKEN)
            else:
                btn.configure(bg=self.colors['light'],
                              fg=self.colors['text'],
                              relief=tk.RAISED)

        # 更新描述
        config = self.web_service_configs[service_id]
        desc_text = f"{config['icon']} {config['name']}"
        self.service_desc.configure(text=desc_text)

        self.log_message(f"🎯 已選擇目標服務: {config['name']}")

    def toggle_password_visibility(self):
        """切換密碼顯示"""
        if self.password_entry.cget('show') == '*':
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')

    def start_conversion(self):
        """開始轉換"""
        if not self.validate_inputs():
            return

        # 在新執行緒中執行轉換
        self.convert_btn.configure(state='disabled', text='🔄 轉換中...')

        conversion_thread = threading.Thread(target=self.perform_conversion)
        conversion_thread.daemon = True
        conversion_thread.start()

    def validate_inputs(self):
        """驗證輸入"""
        if not self.selected_file.get():
            messagebox.showerror("錯誤", "請選擇PFX憑證檔案")
            return False

        if not os.path.exists(self.selected_file.get()):
            messagebox.showerror("錯誤", "選擇的檔案不存在")
            return False

        if not self.selected_service.get():
            messagebox.showerror("錯誤", "請選擇目標Web服務")
            return False

        return True

    def perform_conversion(self):
        """執行轉換"""
        try:
            self.update_progress(0, "開始轉換...")

            # 載入PFX檔案
            self.update_progress(20, "讀取PFX檔案...")
            pfx_content = self.load_pfx_file()

            if not pfx_content:
                return

            # 提取域名
            self.update_progress(40, "分析憑證資訊...")
            domain = self.extract_domain(pfx_content)

            # 生成檔案
            self.update_progress(60, "生成憑證檔案...")
            output_dir = self.generate_certificate_files(pfx_content, domain)

            # 建立說明檔案
            if self.create_readme_var.get():
                self.update_progress(80, "建立使用說明...")
                self.create_readme_file(output_dir, domain)

            self.update_progress(100, "轉換完成！")

            # 顯示完成訊息
            self.root.after(0,
                            lambda: self.show_completion_message(output_dir))

        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
        finally:
            self.root.after(0, self.reset_ui)

    def load_pfx_file(self):
        """載入PFX檔案"""
        try:
            password = self.password_var.get().encode(
                'utf-8') if self.password_var.get() else None

            with open(self.selected_file.get(), 'rb') as f:
                pfx_data = f.read()

            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                pfx_data, password, backend=self.backend)

            return {
                'private_key': private_key,
                'certificate': certificate,
                'additional_certificates': additional_certificates or []
            }
        except Exception as e:
            self.root.after(
                0, lambda: messagebox.showerror("錯誤", f"無法載入PFX檔案: {str(e)}"))
            return None

    def extract_domain(self, pfx_content):
        """提取域名"""
        try:
            # 使用自訂域名或從憑證提取
            if self.custom_domain.get():
                return self.sanitize_filename(self.custom_domain.get())

            # 從憑證提取
            certificate = pfx_content['certificate']
            for attribute in certificate.subject:
                if attribute.oid._name == 'commonName':
                    return self.sanitize_filename(attribute.value)

            return "unknown_domain"
        except Exception:
            return "unknown_domain"

    def sanitize_filename(self, filename):
        """清理檔案名稱"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            if char == '*':
                filename = filename.replace(char, 'wildcard')
            else:
                filename = filename.replace(char, '_')
        return filename.strip() or "certificate"

    def generate_certificate_files(self, pfx_content, domain):
        """生成憑證檔案"""
        service_id = self.selected_service.get()
        config = self.web_service_configs[service_id]

        # 建立輸出目錄
        output_dir = f"{service_id}_{domain}"
        Path(output_dir).mkdir(exist_ok=True)

        # 生成私鑰和憑證
        private_key_pem = pfx_content['private_key'].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()).decode('utf-8')

        cert_pem = pfx_content['certificate'].public_bytes(
            serialization.Encoding.PEM).decode('utf-8')

        # 生成證書鏈
        chain_pems = []
        if pfx_content['additional_certificates']:
            for cert in pfx_content['additional_certificates']:
                chain_pem = cert.public_bytes(
                    serialization.Encoding.PEM).decode('utf-8')
                chain_pems.append(chain_pem)

        # 根據服務類型生成檔案
        for file_type, filename_template in config['files'].items():
            filename = filename_template.format(domain=domain)
            filepath = Path(output_dir) / filename

            if file_type == 'private_key':
                filepath.write_text(private_key_pem, encoding='utf-8')
            elif file_type == 'certificate':
                filepath.write_text(cert_pem, encoding='utf-8')
            elif file_type == 'chain':
                filepath.write_text('\n'.join(chain_pems), encoding='utf-8')
            elif file_type == 'fullchain':
                fullchain = cert_pem + '\n' + '\n'.join(chain_pems)
                filepath.write_text(fullchain, encoding='utf-8')
            elif file_type == 'combined':
                combined = cert_pem + private_key_pem + '\n'.join(chain_pems)
                filepath.write_text(combined, encoding='utf-8')
            elif file_type == 'pfx_output':
                pfx_bytes = pkcs12.serialize_key_and_certificates(
                    name=domain.encode('utf-8'),
                    key=pfx_content['private_key'],
                    cert=pfx_content['certificate'],
                    cas=pfx_content['additional_certificates'],
                    encryption_algorithm=serialization.NoEncryption())
                filepath.write_bytes(pfx_bytes)

            self.log_message(f"✅ 已生成: {filename}")

        return output_dir

    def create_readme_file(self, output_dir, domain):
        """建立說明檔案"""
        service_id = self.selected_service.get()
        config = self.web_service_configs[service_id]

        readme_content = f"""# 憑證轉換結果 - {config['name']}

## 基本資訊
- 目標服務: {config['name']} ({config['description']})
- 域名: {domain}
- 轉換時間: {time.strftime('%Y-%m-%d %H:%M:%S')}
- 轉換工具: 憑證轉換工具 v2.0.0 GUI版

## 生成的檔案
"""

        for file_type, filename_template in config['files'].items():
            filename = filename_template.format(domain=domain)
            readme_content += f"- {filename} - "

            if file_type == 'private_key':
                readme_content += "私鑰檔案（無密碼保護）\n"
            elif file_type == 'certificate':
                readme_content += "憑證檔案\n"
            elif file_type == 'chain':
                readme_content += "憑證鏈檔案\n"
            elif file_type == 'fullchain':
                readme_content += "完整憑證鏈檔案\n"
            elif file_type == 'combined':
                readme_content += "合併檔案（憑證+私鑰）\n"
            elif file_type == 'pfx_output':
                readme_content += "PFX檔案（無密碼）\n"

        readme_content += f"""
## 安全提醒
⚠️ 私鑰檔案已轉換為無密碼保護格式（適合Web服務使用）
⚠️ 請確保私鑰檔案的檔案權限設定正確（建議 600 或 400）
⚠️ 建議將私鑰檔案放在安全的目錄中

## 技術支援
- 工具版本: 2.0.0 GUI版
"""

        readme_path = Path(output_dir) / "README.md"
        readme_path.write_text(readme_content, encoding='utf-8')

        self.log_message(f"📄 已建立說明檔案: README.md")

    def update_progress(self, value, message):
        """更新進度"""
        self.root.after(0, lambda: self.progress_var.set(value))
        self.root.after(0, lambda: self.progress_label.configure(text=message))
        self.root.after(0, lambda: self.log_message(message))

    def show_completion_message(self, output_dir):
        """顯示完成訊息"""
        message = f"🎉 轉換完成！\n\n輸出目錄: {output_dir}\n\n是否要開啟輸出資料夾？"

        if messagebox.askyesno("轉換完成", message):
            try:
                os.startfile(output_dir)
            except:
                os.system(f'explorer "{os.path.abspath(output_dir)}"')

    def show_error(self, error_message):
        """顯示錯誤訊息"""
        messagebox.showerror("轉換失敗", f"轉換過程中發生錯誤:\n\n{error_message}")
        self.log_message(f"❌ 錯誤: {error_message}")

    def reset_ui(self):
        """重置UI狀態"""
        self.convert_btn.configure(state='normal', text='🚀 開始轉換')
        self.progress_var.set(0)
        self.progress_label.configure(text="準備就緒")

    def clear_all(self):
        """清除所有輸入"""
        self.selected_file.set("")
        self.password_var.set("")
        self.custom_domain.set("")
        self.file_info_label.configure(text="")
        self.progress_var.set(0)
        self.progress_label.configure(text="準備就緒")

        # 重置拖放區域
        self.drop_label.configure(text="🎯 拖放PFX檔案到此處，或點擊此區域選擇檔案")
        self.drop_frame.configure(bg=self.colors['light'])
        self.drop_label.configure(bg=self.colors['light'],
                                  fg=self.colors['text'])

        self.clear_log()
        self.log_message("🗑️ 已清除所有輸入")

    def log_message(self, message):
        """記錄訊息"""
        # 檢查 log_text 是否已經建立
        if not hasattr(self, 'log_text') or not self.log_text:
            return

        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def clear_log(self):
        """清除日誌"""
        if hasattr(self, 'log_text') and self.log_text:
            self.log_text.delete(1.0, tk.END)

    def save_log(self):
        """儲存日誌"""
        if not hasattr(self, 'log_text') or not self.log_text:
            return

        file_path = filedialog.asksaveasfilename(title="儲存日誌",
                                                 defaultextension=".txt",
                                                 filetypes=[
                                                     ("Text files", "*.txt"),
                                                     ("All files", "*.*")
                                                 ])

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"💾 日誌已儲存至: {file_path}")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存日誌失敗: {str(e)}")

    def show_help(self):
        """顯示說明"""
        help_text = """
🔐 憑證轉換工具 v2.0.0 GUI版 - 使用說明

📋 功能介紹
本工具可以將PFX格式的SSL/TLS憑證轉換為各種Web服務所需的格式。

🚀 使用步驟
1. 點擊「瀏覽檔案」選擇PFX憑證檔案
2. 選擇目標Web服務
3. 輸入PFX密碼（如有設定）
4. 設定自訂域名（可選，留空自動從憑證提取）
5. 點擊「開始轉換」

📁 支援格式
• PFX (.pfx) - Personal Information Exchange
• PKCS#12 (.p12) - Public Key Cryptography Standards

🌐 支援的Web服務
• Nginx - 高性能Web伺服器
• Apache - 世界上最流行的Web伺服器
• IIS - Windows平台Web伺服器
• HAProxy - 負載均衡器
• Traefik - 現代化反向代理
• Caddy - 自動HTTPS的Web伺服器

💡 快捷鍵
• Ctrl+O - 開啟檔案選擇對話框

⚠️ 注意事項
• 轉換後的私鑰為無密碼保護格式
• 請妥善保管私鑰檔案
• 建議設定適當的檔案權限（Linux/Mac: 600）

技術支援
請透過 GitHub Issues 回報問題
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("使用說明")
        help_window.geometry("600x550")
        help_window.resizable(False, False)

        help_text_widget = scrolledtext.ScrolledText(help_window,
                                                     font=self.fonts['body'],
                                                     wrap=tk.WORD,
                                                     padx=20,
                                                     pady=20)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.configure(state='disabled')


def main():
    """主程式"""
    root = tk.Tk()
    app = CertConverterGUI(root)

    # 設定關閉事件
    def on_closing():
        if messagebox.askokcancel("結束程式", "確定要結束程式嗎？"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 啟動GUI
    root.mainloop()


if __name__ == "__main__":
    main()
