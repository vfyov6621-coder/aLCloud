"""Sidebar — provider list."""

import customtkinter as ctk
from aLCloud.database import get_providers


PROVIDER_ICONS = {
    "google_drive": "G", "telegram": "T",
    "yandex_disk": "Y", "mailru": "M", "github": "H",
}


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, width=240, on_select=None):
        super().__init__(parent, width=width, corner_radius=0)
        self._on_select = on_select
        self._providers_data: list[dict] = []
        self._selected_id: int | None = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="  aLCloud", font=ctk.CTkFont(size=18, weight="bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(16, 2))
        ctk.CTkLabel(self, text="    Облачные хранилища", font=ctk.CTkFont(size=11),
                     anchor="w", text_color="gray50").pack(fill="x", padx=12, pady=(0, 8))

        self._sep()

        self.all_btn = ctk.CTkButton(
            self, text="  Все файлы", height=36, corner_radius=8, anchor="w",
            command=lambda: self._select(None), fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][1],
        )
        self.all_btn.pack(fill="x", padx=8, pady=(4, 2))

        self._sep()

        ctk.CTkLabel(self, text="  Провайдеры", font=ctk.CTkFont(size=12, weight="bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(4, 4))

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=4)

        # Bottom
        bottom = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=56)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        ctk.CTkButton(
            bottom, text="  Браузер", height=36,
            corner_radius=8, fg_color="transparent",
            command=self._open_browser,
        ).pack(fill="x", padx=8, pady=(8, 2))

        ctk.CTkButton(
            bottom, text="+  Добавить провайдер", height=36,
            corner_radius=8, command=self._open_connect,
        ).pack(fill="x", padx=8, pady=(2, 12))

    def _sep(self):
        sep_color = ctk.ThemeManager.theme.get("CTkFrame", {}).get("border_color", ["#333", "#333"])[1]
        ctk.CTkFrame(self, height=1, corner_radius=0, fg_color=sep_color).pack(fill="x", padx=12, pady=(6, 4))

    def refresh_providers(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        self._providers_data = get_providers()
        for p in self._providers_data:
            self._create_provider_item(p)

    def _create_provider_item(self, p: dict):
        name = p.get("display_name", p.get("type", ""))
        connected = p.get("is_connected", False)
        icon = PROVIDER_ICONS.get(p.get("type", ""), "?")

        row = ctk.CTkFrame(self.scroll, corner_radius=8, fg_color="transparent", height=38)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        hover = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][1]

        btn = ctk.CTkButton(
            row, text=f"  [{icon}]  {name}", height=36, corner_radius=8, anchor="w",
            fg_color=hover if self._selected_id == p["id"] else "transparent",
            hover_color=hover,
            command=lambda pid=p["id"]: self._select(pid),
        )
        btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        dot_color = "#4ECDC4" if connected else "#555"
        dot = ctk.CTkLabel(row, text="\u25CF", font=ctk.CTkFont(size=14),
                           text_color=dot_color, width=24, anchor="e")
        dot.pack(side="right", padx=(0, 8))

    def _select(self, provider_id: int | None):
        self._selected_id = provider_id
        hover = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][1]
        for row in self.scroll.winfo_children():
            for w in row.winfo_children():
                if isinstance(w, ctk.CTkButton):
                    w.configure(fg_color="transparent")

        if provider_id:
            idx = next((i for i, p in enumerate(self._providers_data) if p["id"] == provider_id), -1)
            rows = self.scroll.winfo_children()
            if 0 <= idx < len(rows):
                for w in rows[idx].winfo_children():
                    if isinstance(w, ctk.CTkButton):
                        w.configure(fg_color=hover)
            provider = next((p for p in self._providers_data if p["id"] == provider_id), None)
        else:
            provider = None

        if self._on_select:
            self._on_select(provider)

    def _open_connect(self):
        root = self.winfo_toplevel()
        if hasattr(root, "_open_connect"):
            root._open_connect()

    def _open_browser(self):
        root = self.winfo_toplevel()
        if hasattr(root, "_open_browser"):
            root._open_browser()
