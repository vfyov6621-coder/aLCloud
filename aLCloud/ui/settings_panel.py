"""Settings panel — theme + providers, inside main window."""

import customtkinter as ctk
from aLCloud.theme import ThemeManager, _rgb_hex, PRESETS
from aLCloud.database import get_providers, delete_provider


class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, on_done=None):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._on_done = on_done
        self._theme = ThemeManager()
        self._current_mode = self._theme.current_mode
        self._custom_colors = {"bg": (240, 240, 240), "fg": (20, 20, 20),
                               "accent": (0, 150, 136), "border": (0, 0, 0)}
        self._build()

    def refresh(self):
        """Rebuild content when panel is reopened."""
        self._current_mode = self._theme.current_mode
        self._load_custom_colors()
        self._build()

    def _load_custom_colors(self):
        from aLCloud.database import get_setting
        raw = get_setting("theme_custom", "")
        if raw:
            try:
                d = __import__("json").loads(raw)
                self._custom_colors = {k: tuple(v) for k, v in d.items()}
            except Exception:
                pass

    def _build(self):
        for w in self.winfo_children():
            w.destroy()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(20, 12))

        ctk.CTkLabel(scroll, text="Настройки",
                     font=ctk.CTkFont(size=20, weight="bold"), anchor="w"
                     ).pack(fill="x", pady=(0, 16))

        # ── Theme ────────────────────────────────────
        sec = ctk.CTkFrame(scroll, corner_radius=10)
        sec.pack(fill="x", pady=(0, 12))
        inner = ctk.CTkFrame(sec, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(inner, text="Тема оформления",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(fill="x", pady=(0, 10))

        # Theme buttons
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 12))

        self._theme_btns = {}
        for label, mode in [("Светлая", "light"), ("Тёмная", "dark"), ("Кастомная", "custom")]:
            b = ctk.CTkButton(btn_row, text=label, height=36, corner_radius=8,
                              command=lambda m=mode: self._pick_theme(m))
            b.pack(side="left", padx=(0, 8), expand=True, fill="x")
            self._theme_btns[mode] = b

        # Previews
        prev_row = ctk.CTkFrame(inner, fg_color="transparent")
        prev_row.pack(fill="x", pady=(0, 8))

        lp = ctk.CTkFrame(prev_row, width=80, height=44, corner_radius=8,
                           fg_color="#FFFFFF", border_width=2, border_color="#000000")
        lp.pack(side="left", padx=(0, 10))
        lp.pack_propagate(False)
        ctk.CTkLabel(lp, text="Aa", font=ctk.CTkFont(weight="bold"), text_color="#000").pack(expand=True)

        dp = ctk.CTkFrame(prev_row, width=80, height=44, corner_radius=8,
                           fg_color="#1E1E1E", border_width=2, border_color="#555")
        dp.pack(side="left", padx=(0, 10))
        dp.pack_propagate(False)
        ctk.CTkLabel(dp, text="Aa", font=ctk.CTkFont(weight="bold"), text_color="#FFF").pack(expand=True)

        self.custom_prev = ctk.CTkFrame(prev_row, width=80, height=44, corner_radius=8, border_width=2)
        self.custom_prev.pack(side="left")
        self.custom_prev.pack_propagate(False)
        self.prev_lbl = ctk.CTkLabel(self.custom_prev, text="Aa", font=ctk.CTkFont(weight="bold"))
        self.prev_lbl.pack(expand=True)

        self._highlight_theme_btns()
        self._update_preview()

        # ── Custom RGB ───────────────────────────────
        self.custom_frame = ctk.CTkFrame(scroll, corner_radius=10)
        if self._current_mode == "custom":
            self.custom_frame.pack(fill="x", pady=(0, 12))
        self._build_custom_rgb()

        # ── Providers ────────────────────────────────
        sec2 = ctk.CTkFrame(scroll, corner_radius=10)
        sec2.pack(fill="x", pady=(0, 12))
        p_inner = ctk.CTkFrame(sec2, fg_color="transparent")
        p_inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(p_inner, text="Подключённые провайдеры",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(fill="x", pady=(0, 8))

        providers = get_providers()
        if not providers:
            ctk.CTkLabel(p_inner, text="Нет подключённых провайдеров",
                         font=ctk.CTkFont(size=12), text_color="gray50", anchor="w").pack(fill="x")
        else:
            for p in providers:
                row = ctk.CTkFrame(p_inner, fg_color="transparent")
                row.pack(fill="x", pady=2)
                name = p.get("display_name", p.get("type", ""))
                cid = p.get("client_id", "")
                masked = f"{cid[:8]}...{cid[-4:]}" if len(cid) > 12 else (cid or "демо")
                ctk.CTkLabel(row, text=f"  {name}  -  {masked}",
                             font=ctk.CTkFont(size=12), anchor="w"
                             ).pack(side="left", fill="x", expand=True)

                pid = p["id"]
                ctk.CTkButton(row, text="Удалить", width=80, height=26, corner_radius=6,
                              fg_color="transparent", hover_color="#FF6B6B", text_color="#FF6B6B",
                              command=lambda _pid=pid, _row=row: self._del_provider(_pid, _row)
                              ).pack(side="right")

        # ── Bottom ───────────────────────────────────
        btm = ctk.CTkFrame(scroll, fg_color="transparent")
        btm.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(btm, text="Отмена", width=100, height=36, corner_radius=8,
                      fg_color="transparent", border_width=1, command=self._cancel
                      ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btm, text="Сохранить", width=100, height=36, corner_radius=8,
                      command=self._save).pack(side="right")

    def _build_custom_rgb(self):
        for w in self.custom_frame.winfo_children():
            w.destroy()
        inner = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(inner, text="Кастомная тема (RGB)",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x", pady=(0, 8))

        self._color_entries = {}
        for key, label in [("bg", "Фон"), ("fg", "Текст"), ("accent", "Акцент"), ("border", "Рамка")]:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{label}:", width=60, anchor="w",
                         font=ctk.CTkFont(size=12)).pack(side="left")

            entries = {}
            for ph, sub in [("R", "r"), ("G", "g"), ("B", "b")]:
                e = ctk.CTkEntry(row, width=55, height=28, placeholder_text=ph, corner_radius=6)
                e.insert(0, str(self._custom_colors[key][["r", "g", "b"].index(sub)]))
                e.pack(side="left", padx=2)
                entries[sub] = e

            sw = ctk.CTkLabel(row, text="  ", width=22, height=22, corner_radius=4,
                              fg_color=_rgb_hex(self._custom_colors[key]))
            sw.pack(side="left", padx=(8, 0))

            self._color_entries[key] = (entries, sw)
            for e in entries.values():
                e.bind("<KeyRelease>", lambda ev, k=key: self._color_changed(k))

        ctk.CTkButton(inner, text="Предпросмотр", height=32, corner_radius=8,
                      command=self._preview_custom).pack(anchor="w", pady=(10, 0))

    def _highlight_theme_btns(self):
        try:
            btn_bg = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        except Exception:
            btn_bg = ("#3B82F6", "#1D4ED8")
        frame_bg = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]
        for mode, btn in self._theme_btns.items():
            btn.configure(fg_color=btn_bg if mode == self._current_mode else frame_bg)

    def _pick_theme(self, mode):
        self._current_mode = mode
        if mode == "custom":
            self.custom_frame.pack(fill="x", pady=(0, 12))
        else:
            self.custom_frame.pack_forget()
        self._highlight_theme_btns()

    def _color_changed(self, key):
        try:
            ents, sw = self._color_entries[key]
            r = max(0, min(255, int(ents["r"].get() or 0)))
            g = max(0, min(255, int(ents["g"].get() or 0)))
            b = max(0, min(255, int(ents["b"].get() or 0)))
            sw.configure(fg_color=_rgb_hex((r, g, b)))
        except Exception:
            pass

    def _read_colors(self):
        colors = {}
        for key, (ents, _) in self._color_entries.items():
            r = max(0, min(255, int(ents["r"].get() or 0)))
            g = max(0, min(255, int(ents["g"].get() or 0)))
            b = max(0, min(255, int(ents["b"].get() or 0)))
            colors[key] = (r, g, b)
        return colors

    def _update_preview(self):
        c = self._custom_colors
        self.custom_prev.configure(fg_color=_rgb_hex(c["bg"]), border_color=_rgb_hex(c["border"]))
        self.prev_lbl.configure(text_color=_rgb_hex(c["fg"]))

    def _preview_custom(self):
        self._custom_colors = self._read_colors()
        self._update_preview()
        self._theme.apply("custom", self._custom_colors)

    def _save(self):
        if self._current_mode == "custom":
            self._custom_colors = self._read_colors()
            self._theme.apply("custom", self._custom_colors)
        else:
            self._theme.apply(self._current_mode)
        if self._on_done:
            self._on_done()

    def _cancel(self):
        self._theme.load_saved()
        if self._on_done:
            self._on_done()

    def _del_provider(self, pid, row):
        delete_provider(pid)
        row.destroy()
