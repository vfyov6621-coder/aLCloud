"""Settings panel — theme picker + provider management, inside main window."""

import customtkinter as ctk
from aLCloud.theme import ThemeManager, _rgb_hex, PRESETS
from aLCloud.database import get_providers, delete_provider, get_setting


class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, on_done=None):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._on_done = on_done
        self._theme = ThemeManager()
        self._current_mode = self._theme.current_mode
        self._custom_colors = dict(PRESETS.get("light", {"bg": (240,240,240), "fg": (20,20,20),
                                                         "accent": (0,150,136), "border": (0,0,0)}))
        self._build()

    def refresh(self):
        """Refresh when panel is reopened."""
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(20, 12))

        ctk.CTkLabel(scroll, text="Настройки", font=ctk.CTkFont(size=22, weight="bold"),
                     anchor="w").pack(fill="x", pady=(0, 16))

        # ── Theme section ────────────────────────────
        sec_theme = ctk.CTkFrame(scroll, corner_radius=10)
        sec_theme.pack(fill="x", pady=(0, 12))
        inner = ctk.CTkFrame(sec_theme, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(inner, text="Тема оформления",
                     font=ctk.CTkFont(size=15, weight="bold"), anchor="w").pack(fill="x", pady=(0, 12))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 12))

        self._theme_btns = {}
        for label, mode in [("Светлая", "light"), ("Тёмная", "dark"), ("Кастомная", "custom")]:
            active = mode == self._current_mode
            b = ctk.CTkButton(
                btn_row, text=label, width=140, height=38, corner_radius=8,
                command=lambda m=mode: self._pick_theme(m),
            )
            b.pack(side="left", padx=(0, 8), expand=True, fill="x")
            self._theme_btns[mode] = b

        # Previews
        preview_row = ctk.CTkFrame(inner, fg_color="transparent")
        preview_row.pack(fill="x", pady=(0, 8))

        # Light preview
        lp = ctk.CTkFrame(preview_row, width=90, height=50, corner_radius=8,
                           fg_color="#FFFFFF", border_width=2, border_color="#000000")
        lp.pack(side="left", padx=(0, 12))
        lp.pack_propagate(False)
        ctk.CTkLabel(lp, text="Aa", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").pack(expand=True)

        # Dark preview
        dp = ctk.CTkFrame(preview_row, width=90, height=50, corner_radius=8,
                           fg_color="#1E1E1E", border_width=2, border_color="#555555")
        dp.pack(side="left", padx=(0, 12))
        dp.pack_propagate(False)
        ctk.CTkLabel(dp, text="Aa", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#FFFFFF").pack(expand=True)

        # Custom preview
        self.custom_preview = ctk.CTkFrame(preview_row, width=90, height=50, corner_radius=8,
                                           border_width=2)
        self.custom_preview.pack(side="left")
        self.custom_preview.pack_propagate(False)
        self.preview_label = ctk.CTkLabel(self.custom_preview, text="Aa",
                                           font=ctk.CTkFont(size=14, weight="bold"))
        self.preview_label.pack(expand=True)

        # ── Custom RGB section ────────────────────────
        self.custom_frame = ctk.CTkFrame(scroll, corner_radius=10)
        if self._current_mode != "custom":
            self.custom_frame.pack_forget()

        self._build_custom_section()

        # ── Providers section ─────────────────────────
        sec_prov = ctk.CTkFrame(scroll, corner_radius=10)
        sec_prov.pack(fill="x", pady=(0, 12))
        prov_inner = ctk.CTkFrame(sec_prov, fg_color="transparent")
        prov_inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(prov_inner, text="Подключённые провайдеры",
                     font=ctk.CTkFont(size=15, weight="bold"), anchor="w").pack(fill="x", pady=(0, 8))

        providers = get_providers()
        if not providers:
            ctk.CTkLabel(prov_inner, text="Нет подключённых провайдеров",
                         font=ctk.CTkFont(size=12), text_color="gray50", anchor="w").pack(fill="x")
        else:
            for p in providers:
                row = ctk.CTkFrame(prov_inner, fg_color="transparent")
                row.pack(fill="x", pady=2)
                name = p.get("display_name", p.get("type", ""))
                cid = p.get("client_id", "")
                masked = f"{cid[:8]}...{cid[-4:]}" if len(cid) > 12 else (cid or "демо")
                ctk.CTkLabel(row, text=f"  {name}  —  {masked}",
                             font=ctk.CTkFont(size=12), anchor="w").pack(side="left", fill="x", expand=True)

                def make_del(pid=p["id"], r=row):
                    def do():
                        delete_provider(pid)
                        r.destroy()
                    return do

                ctk.CTkButton(row, text="Удалить", width=80, height=28, corner_radius=6,
                              fg_color="transparent", hover_color="#FF6B6B",
                              text_color="#FF6B6B", command=make_del()).pack(side="right")

        # ── Bottom buttons ────────────────────────────
        bottom = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom.pack(fill="x", pady=(8, 0))

        ctk.CTkButton(bottom, text="Отмена", width=120, height=38, corner_radius=8,
                      fg_color="transparent", border_width=1,
                      command=self._cancel).pack(side="right", padx=(8, 0))
        ctk.CTkButton(bottom, text="Сохранить", width=120, height=38, corner_radius=8,
                      command=self._save).pack(side="right")

        # Highlight active theme button
        self._highlight_theme_btns()
        self._update_custom_preview()

    def _build_custom_section(self):
        for w in self.custom_frame.winfo_children():
            w.destroy()

        inner = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(inner, text="Кастомная тема (RGB)",
                     font=ctk.CTkFont(size=15, weight="bold"), anchor="w").pack(fill="x", pady=(0, 8))

        self.color_entries = {}
        for key, label in [("bg", "Фон"), ("fg", "Текст"), ("accent", "Акцент"), ("border", "Рамка")]:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(row, text=f"{label}:", width=60, anchor="w",
                         font=ctk.CTkFont(size=12)).pack(side="left")

            r = ctk.CTkEntry(row, width=60, height=30, placeholder_text="R", corner_radius=6)
            r.insert(0, str(self._custom_colors[key][0]))
            r.pack(side="left", padx=2)
            g = ctk.CTkEntry(row, width=60, height=30, placeholder_text="G", corner_radius=6)
            g.insert(0, str(self._custom_colors[key][1]))
            g.pack(side="left", padx=2)
            b = ctk.CTkEntry(row, width=60, height=30, placeholder_text="B", corner_radius=6)
            b.insert(0, str(self._custom_colors[key][2]))
            b.pack(side="left", padx=2)

            swatch = ctk.CTkLabel(row, text="  ", width=24, height=24, corner_radius=4,
                                  fg_color=_rgb_hex(self._custom_colors[key]))
            swatch.pack(side="left", padx=(8, 0))

            self.color_entries[key] = {"r": r, "g": g, "b": b, "swatch": swatch}
            for entry in [r, g, b]:
                entry.bind("<KeyRelease>", lambda e, k=key: self._on_color_change(k))

        ctk.CTkButton(inner, text="Предпросмотр", height=34, corner_radius=8,
                      command=self._preview_custom).pack(anchor="w", pady=(12, 0))

    def _pick_theme(self, mode):
        self._current_mode = mode
        if mode == "custom":
            self.custom_frame.pack(fill="x", pady=(0, 12),
                                   after=list(self.winfo_children())[0].winfo_children()[0])
        else:
            self.custom_frame.pack_forget()
        self._highlight_theme_btns()

    def _highlight_theme_btns(self):
        accent = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        for mode, btn in self._theme_btns.items():
            if mode == self._current_mode:
                btn.configure(fg_color=accent)
            else:
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"])

    def _on_color_change(self, key):
        try:
            e = self.color_entries[key]
            r = max(0, min(255, int(e["r"].get() or 0)))
            g = max(0, min(255, int(e["g"].get() or 0)))
            b = max(0, min(255, int(e["b"].get() or 0)))
            e["swatch"].configure(fg_color=_rgb_hex((r, g, b)))
        except ValueError:
            pass

    def _read_custom_colors(self):
        colors = {}
        for key, entries in self.color_entries.items():
            r = max(0, min(255, int(entries["r"].get() or 0)))
            g = max(0, min(255, int(entries["g"].get() or 0)))
            b = max(0, min(255, int(entries["b"].get() or 0)))
            colors[key] = (r, g, b)
        return colors

    def _update_custom_preview(self):
        c = self._custom_colors
        self.custom_preview.configure(fg_color=_rgb_hex(c["bg"]), border_color=_rgb_hex(c["border"]))
        self.preview_label.configure(text_color=_rgb_hex(c["fg"]))

    def _preview_custom(self):
        self._custom_colors = self._read_custom_colors()
        self._update_custom_preview()
        self._theme.apply("custom", self._custom_colors)

    def _save(self):
        if self._current_mode == "custom":
            self._custom_colors = self._read_custom_colors()
            self._theme.apply("custom", self._custom_colors)
        else:
            self._theme.apply(self._current_mode)
        if self._on_done:
            self._on_done()

    def _cancel(self):
        # Revert theme on cancel
        self._theme.load_saved()
        if self._on_done:
            self._on_done()
