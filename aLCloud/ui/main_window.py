"""Main application window — single window, panels switch inside."""

import customtkinter as ctk

from aLCloud.ui.sidebar import Sidebar
from aLCloud.ui.file_browser import FileBrowser
from aLCloud.ui.connect_panel import ConnectPanel
from aLCloud.ui.settings_panel import SettingsPanel


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

        self.search_entry = ctk.CTkEntry(
            self.toolbar, width=300, placeholder_text="  Поиск файлов...",
            height=30, corner_radius=8
        )
        self.search_entry.pack(side="left", padx=(16, 8), pady=7)
        self.search_entry.bind("<Return>", lambda e: self._on_search())

        ctk.CTkButton(
            self.toolbar, text="Найти", width=60, height=30,
            command=self._on_search, corner_radius=8
        ).pack(side="left", padx=(0, 16), pady=7)

        ctk.CTkButton(
            self.toolbar, text="\u2699  Настройки", width=120, height=30,
            command=self._open_settings, corner_radius=8
        ).pack(side="right", padx=(0, 16), pady=7)

        self.upload_btn = ctk.CTkButton(
            self.toolbar, text="\u2B06  Загрузить", width=120, height=30,
            command=self._on_upload, corner_radius=8
        ).pack(side="right", padx=(0, 8), pady=7)

        self.back_btn = ctk.CTkButton(
            self.toolbar, text="\u2190  Назад", width=90, height=30,
            command=self._back_to_files, corner_radius=8
        )
        # back_btn is hidden initially

    def _build_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self.content, width=240, on_select=self._on_provider_select)
        self.sidebar.pack(side="left", fill="y")

        # Right panel container
        self.right_panel = ctk.CTkFrame(self.content, corner_radius=0, fg_color="transparent")
        self.right_panel.pack(side="left", fill="both", expand=True)

        self.file_browser = FileBrowser(self.right_panel)
        self.file_browser.pack(fill="both", expand=True)

        self.connect_panel = ConnectPanel(self.right_panel, on_done=self._panel_done)
        self.settings_panel = SettingsPanel(self.right_panel, on_done=self._panel_done)
        # panels are packed_forget initially

    def _build_statusbar(self):
        self.statusbar = ctk.CTkFrame(self, height=28, corner_radius=0)
        self.statusbar.pack(fill="x")
        self.statusbar.pack_propagate(False)
        self.status_label = ctk.CTkLabel(
            self.statusbar, text="  Выберите провайдер для просмотра файлов",
            anchor="w", height=28
        )
        self.status_label.pack(fill="x", padx=8)

    # ── Panel switching ────────────────────────────────
    def _show_panel(self, panel):
        """Hide file browser, show given panel."""
        self.file_browser.pack_forget()
        self.connect_panel.pack_forget()
        self.settings_panel.pack_forget()
        panel.pack(fill="both", expand=True)

        self.search_entry.pack_forget()
        self.upload_btn.pack_forget()
        self.back_btn.pack(side="left", padx=(16, 8), pady=7)
        self.back_btn.pack_configure(before=self.back_btn.master.winfo_children()[-1])

        # place back button before the right-side buttons
        self.back_btn.pack_forget()
        for child in list(self.toolbar.winfo_children()):
            child.pack_forget()
        self.back_btn.pack(side="left", padx=(16, 8), pady=7)
        self.search_entry.pack(side="left", padx=(0, 8), pady=7)
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        # Re-find and pack right-side buttons
        # We'll just rebuild toolbar for simplicity

    def _back_to_files(self):
        """Restore file browser view."""
        self.connect_panel.pack_forget()
        self.settings_panel.pack_forget()
        self.file_browser.pack(fill="both", expand=True)

        # Rebuild toolbar
        for child in list(self.toolbar.winfo_children()):
            child.pack_forget()

        self.search_entry.pack(side="left", padx=(16, 8), pady=7)
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        ctk.CTkButton(
            self.toolbar, text="Найти", width=60, height=30,
            command=self._on_search, corner_radius=8
        ).pack(side="left", padx=(0, 16), pady=7)
        ctk.CTkButton(
            self.toolbar, text="\u2699  Настройки", width=120, height=30,
            command=self._open_settings, corner_radius=8
        ).pack(side="right", padx=(0, 16), pady=7)
        self.upload_btn = ctk.CTkButton(
            self.toolbar, text="\u2B06  Загрузить", width=120, height=30,
            command=self._on_upload, corner_radius=8
        )
        self.upload_btn.pack(side="right", padx=(0, 8), pady=7)

    def _open_connect(self):
        self.connect_panel.reset()
        self._show_panel(self.connect_panel)
        self.status_label.configure(text="  Подключение провайдера")

    def _open_settings(self):
        self.settings_panel.refresh()
        self._show_panel(self.settings_panel)
        self.status_label.configure(text="  Настройки")

    def _panel_done(self):
        self._back_to_files()
        self.sidebar.refresh_providers()

    # ── Callbacks ───────────────────────────────────────
    def _on_provider_select(self, provider_data: dict | None):
        # If we're in a panel, go back first
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
