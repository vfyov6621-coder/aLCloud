"""Sidebar — provider list with status indicators."""

import customtkinter as ctk
from aLCloud.database import get_providers
from aLCloud.providers import PROVIDER_INFO
from aLCloud.ui.connect_dialog import ConnectDialog


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, width=240, on_select=None):
        super().__init__(parent, width=width, corner_radius=0)
        self._on_select = on_select
        self._providers_data: list[dict] = []
        self._selected_id: int | None = None

        self._build()

    def _build(self):
        # Title
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=50)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="  \u2601  aLCloud", font=ctk.CTkFont(size=18, weight="bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(12, 4))
        ctk.CTkLabel(header, text="    Облачные хранилища", font=ctk.CTkFont(size=11),
                     anchor="w", text_color="gray").pack(fill="x", padx=12)

        # Separator
        ctk.CTkFrame(self, height=1, corner_radius=0, fg_color="gray30").pack(fill="x", padx=12, pady=(8, 4))

        # "All files" button
        self.all_btn = ctk.CTkButton(
            self, text="  \uD83C\uDF10  Все файлы", height=36,
            corner_radius=8, anchor="w",
            command=lambda: self._select(None),
            fg_color="transparent", text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][0],
            hover_color="gray20",
        )
        self.all_btn.pack(fill="x", padx=8, pady=(4, 2))

        # Separator
        ctk.CTkFrame(self, height=1, corner_radius=0, fg_color="gray30").pack(fill="x", padx=12, pady=(8, 4))

        # Provider label
        ctk.CTkLabel(self, text="  Провайдеры", font=ctk.CTkFont(size=12, weight="bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(4, 4))

        # Scrollable provider list
        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=4)

        # Add button at bottom
        bottom = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=60)
        bottom.pack(fill="x", padx=0, pady=0, side="bottom")
        bottom.pack_propagate(False)

        self.add_btn = ctk.CTkButton(
            bottom, text="+  Добавить провайдер", height=38,
            corner_radius=8, command=self._open_connect,
        )
        self.add_btn.pack(fill="x", padx=8, pady=(8, 12))

    def refresh_providers(self):
        """Reload providers from database and rebuild list."""
        # Clear old widgets
        for w in self.scroll.winfo_children():
            w.destroy()

        self._providers_data = get_providers()

        for p in self._providers_data:
            item = self._create_provider_item(p)
            item.pack(fill="x", padx=4, pady=2)

    def _create_provider_item(self, p: dict) -> ctk.CTkButton:
        name = p.get("display_name", p.get("type", ""))
        connected = p.get("is_connected", False)

        # Status dot
        dot = "\U0001F7E2" if connected else "\u26AA"

        # Determine provider icon
        icons = {
            "google_drive": "\uD83D\uDD13", "telegram": "\u2708\uFE0F",
            "yandex_disk": "\uD83C\uDF0E", "mailru": "\uD83D\uDCE7",
            "github": "\uD83D\uDC19",
        }
        icon = icons.get(p.get("type", ""), "\u2601")

        btn = ctk.CTkButton(
            self.scroll,
            text=f" {icon}  {name}",
            height=38,
            corner_radius=8,
            anchor="w",
            command=lambda pid=p["id"]: self._select(pid),
            fg_color="transparent",
            hover_color="gray20",
        )

        # Status indicator label
        status = ctk.CTkLabel(
            self.scroll, text=dot, font=ctk.CTkFont(size=10),
            anchor="e", width=20,
        )

        row = ctk.CTkFrame(self.scroll, corner_radius=8, fg_color="transparent")
        row.pack(fill="x", pady=1)
        btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        status.pack(side="right", padx=(0, 4))

        # Highlight selected
        if self._selected_id == p["id"]:
            btn.configure(fg_color="gray25")

        # Bind click on the entire row
        for widget in [btn]:
            widget.bind("<Button-1>", lambda e, pid=p["id"]: self._select(pid))

        return row

    def _select(self, provider_id: int | None):
        self._selected_id = provider_id

        # Refresh highlight
        for row in self.scroll.winfo_children():
            for w in row.winfo_children():
                try:
                    w.configure(fg_color="transparent")
                except Exception:
                    pass

        if provider_id:
            # Find the selected row and highlight
            idx = next((i for i, p in enumerate(self._providers_data) if p["id"] == provider_id), -1)
            rows = self.scroll.winfo_children()
            if 0 <= idx < len(rows):
                for w in rows[idx].winfo_children():
                    try:
                        w.configure(fg_color="gray25")
                    except Exception:
                        pass
            provider = next((p for p in self._providers_data if p["id"] == provider_id), None)
        else:
            provider = None
            try:
                self.all_btn.configure(fg_color="gray25")
            except Exception:
                pass

        if self._on_select:
            self._on_select(provider)

    def _open_connect(self):
        ConnectDialog(self, on_done=self.refresh_providers)
