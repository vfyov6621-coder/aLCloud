"""Main application window layout."""

import customtkinter as ctk

from aLCloud.ui.sidebar import Sidebar
from aLCloud.ui.file_browser import FileBrowser
from aLCloud.ui.settings_dialog import SettingsDialog


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
        self.toolbar.pack(fill="x", padx=0, pady=0)
        self.toolbar.pack_propagate(False)

        self.search_entry = ctk.CTkEntry(
            self.toolbar, width=300, placeholder_text="  Поиск файлов...",
            height=30, corner_radius=8
        )
        self.search_entry.pack(side="left", padx=(16, 8), pady=7)

        # Search button
        self.search_btn = ctk.CTkButton(
            self.toolbar, text="Найти", width=60, height=30,
            command=self._on_search, corner_radius=8
        )
        self.search_btn.pack(side="left", padx=(0, 16), pady=7)

        self.right_frame = ctk.CTkFrame(self.toolbar, corner_radius=0, fg_color="transparent")
        self.right_frame.pack(side="right")

        self.settings_btn = ctk.CTkButton(
            self.right_frame, text="\u2699  Настройки", width=120, height=30,
            command=self._open_settings, corner_radius=8
        )
        self.settings_btn.pack(side="right", padx=(0, 16), pady=7)

        self.upload_btn = ctk.CTkButton(
            self.right_frame, text="\u2B06  Загрузить", width=120, height=30,
            command=self._on_upload, corner_radius=8
        )
        self.upload_btn.pack(side="right", padx=(0, 8), pady=7)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=0, pady=0)

        self.sidebar = Sidebar(self.content, width=240, on_select=self._on_provider_select)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        self.file_browser = FileBrowser(self.content)
        self.file_browser.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=0)

    def _build_statusbar(self):
        self.statusbar = ctk.CTkFrame(self, height=28, corner_radius=0)
        self.statusbar.pack(fill="x", padx=0, pady=0)
        self.statusbar.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.statusbar, text="  Выберите провайдер для просмотра файлов",
            anchor="w", height=28, corner_radius=0,
        )
        self.status_label.pack(fill="x", padx=8)

    # ── Callbacks ───────────────────────────────────────
    def _on_provider_select(self, provider_data: dict | None):
        if provider_data:
            name = provider_data.get("display_name", provider_data.get("type", ""))
            self.file_browser.load_provider(provider_data)
            self.status_label.configure(text=f"  {name}  |  Загрузка...")
        else:
            self.file_browser.clear()
            self.status_label.configure(text="  Все файлы")

    def _on_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        self.file_browser.search(query)

    def _on_upload(self):
        self.file_browser.upload_file()

    def _open_settings(self):
        SettingsDialog(self)

    def refresh_sidebar(self):
        self.sidebar.refresh_providers()
