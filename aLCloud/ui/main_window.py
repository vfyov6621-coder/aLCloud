"""Main application window — single window, panels switch inside."""

import customtkinter as ctk

from aLCloud.ui.sidebar import Sidebar
from aLCloud.ui.file_browser import FileBrowser
from aLCloud.ui.connect_panel import ConnectPanel
from aLCloud.ui.settings_panel import SettingsPanel
from aLCloud.ui.browser_panel import BrowserPanel


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("aLCloud")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self._build_toolbar()
        self._build_content()
        self._build_statusbar()

        self.sidebar.refresh_providers()

    # ── Toolbar ─────────────────────────────────────────
    def _build_toolbar(self):
        self.toolbar = ctk.CTkFrame(self, height=44, corner_radius=0)
        self.toolbar.pack(fill="x")
        self.toolbar.pack_propagate(False)

        # Left side — back button (hidden), search
        self.back_btn = ctk.CTkButton(
            self.toolbar, text="  <- Назад", width=100, height=30,
            corner_radius=8, command=self._back_to_files
        )
        # NOT packed — hidden initially

        self.search_entry = ctk.CTkEntry(
            self.toolbar, width=280, placeholder_text="Поиск файлов...",
            height=30, corner_radius=8
        )
        self.search_entry.pack(side="left", padx=(16, 8), pady=7)
        self.search_entry.bind("<Return>", lambda e: self._on_search())

        self.search_btn = ctk.CTkButton(
            self.toolbar, text="Найти", width=60, height=30,
            command=self._on_search, corner_radius=8
        )
        self.search_btn.pack(side="left", padx=(0, 16), pady=7)

        # Right side — upload, settings
        self.upload_btn = ctk.CTkButton(
            self.toolbar, text="Загрузить", width=110, height=30,
            command=self._on_upload, corner_radius=8
        )
        self.upload_btn.pack(side="right", padx=(0, 16), pady=7)

        self.settings_btn = ctk.CTkButton(
            self.toolbar, text="Настройки", width=110, height=30,
            command=self._open_settings, corner_radius=8
        )
        self.settings_btn.pack(side="right", padx=(0, 8), pady=7)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self.content, width=240, on_select=self._on_provider_select)
        self.sidebar.pack(side="left", fill="y")

        self.right_panel = ctk.CTkFrame(self.content, corner_radius=0, fg_color="transparent")
        self.right_panel.pack(side="left", fill="both", expand=True)

        self.file_browser = FileBrowser(self.right_panel)
        self.file_browser.pack(fill="both", expand=True)

        self.connect_panel = ConnectPanel(self.right_panel, on_done=self._panel_done)
        self.settings_panel = SettingsPanel(self.right_panel, on_done=self._panel_done)
        self.browser_panel = BrowserPanel(self.right_panel, on_done=self._panel_done)
        # All created but NOT packed — hidden initially

    def _build_statusbar(self):
        self.statusbar = ctk.CTkFrame(self, height=28, corner_radius=0)
        self.statusbar.pack(fill="x")
        self.statusbar.pack_propagate(False)
        self.status_label = ctk.CTkLabel(
            self.statusbar, text="  Выберите провайдер",
            anchor="w", height=28
        )
        self.status_label.pack(fill="x", padx=8)

    # ── Panel switching ────────────────────────────────
    def _show_panel(self, panel):
        """Hide file browser, show given panel, adjust toolbar."""
        self.file_browser.pack_forget()
        self.connect_panel.pack_forget()
        self.settings_panel.pack_forget()
        self.browser_panel.pack_forget()
        panel.pack(fill="both", expand=True)

        # Toolbar: hide search+upload, show back
        self.search_entry.pack_forget()
        self.search_btn.pack_forget()
        self.upload_btn.pack_forget()
        self.back_btn.pack(side="left", padx=(16, 8), pady=7)

    def _back_to_files(self):
        """Restore file browser view."""
        self.connect_panel.pack_forget()
        self.settings_panel.pack_forget()
        self.browser_panel.pack_forget()
        self.file_browser.pack(fill="both", expand=True)

        # Toolbar: show search+upload, hide back
        self.back_btn.pack_forget()
        self.search_entry.pack(side="left", padx=(16, 8), pady=7)
        self.search_btn.pack(side="left", padx=(0, 16), pady=7)
        self.upload_btn.pack(side="right", padx=(0, 16), pady=7)

    def _open_connect(self):
        self.connect_panel.reset()
        self._show_panel(self.connect_panel)
        self.status_label.configure(text="  Подключение провайдера")

    def _open_settings(self):
        self.settings_panel.refresh()
        self._show_panel(self.settings_panel)
        self.status_label.configure(text="  Настройки")

    def _open_browser(self):
        self.browser_panel.open_url("https://www.google.com")
        self._show_panel(self.browser_panel)
        self.status_label.configure(text="  Браузер")

    def _panel_done(self):
        self._back_to_files()
        self.sidebar.refresh_providers()

    # ── Callbacks ───────────────────────────────────────
    def _on_provider_select(self, provider_data):
        self._back_to_files()
        if provider_data:
            name = provider_data.get("display_name", provider_data.get("type", ""))
            self.file_browser.load_provider(provider_data)
            self.status_label.configure(text=f"  {name}")
        else:
            self.file_browser.clear()
            self.status_label.configure(text="  Все файлы")

    def _on_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        self._back_to_files()
        self.file_browser.search(query)

    def _on_upload(self):
        self.file_browser.upload_file()

    def refresh_sidebar(self):
        self.sidebar.refresh_providers()
