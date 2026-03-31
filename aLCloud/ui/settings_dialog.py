"""Settings dialog — theme picker (Light, Dark, Custom RGB)."""

import customtkinter as ctk

from aLCloud.theme import ThemeManager, PRESETS, _rgb_hex


class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self._theme = ThemeManager()
        self._current_mode = self._theme.current_mode
        self._custom_colors = self._theme.current_colors if self._current_mode == "custom" else {
            "bg": (240, 240, 240), "fg": (20, 20, 20),
            "accent": (0, 150, 136), "border": (0, 0, 0),
        }

        self.title("Настройки")
        self.geometry("560x580")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build()

    def _build(self):
        pad_x = 24
        pad = {"padx": pad_x, "pady": (6, 0)}

        ctk.CTkLabel(self, text="Настройки",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(**pad, pady=(20, 12))

        # ── Theme Section ────────────────────────────────
        section = ctk.CTkFrame(self, corner_radius=10, fg_color="gray15")
        section.pack(fill="x", padx=pad_x, pady=(0, 8))

        ctk.CTkLabel(section, text="  Тема оформления",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12, 8))

        self.theme_var = ctk.StringVar(value=self._current_mode)

        # Theme options row
        opts_frame = ctk.CTkFrame(section, fg_color="transparent")
        opts_frame.pack(fill="x", padx=12, pady=(0, 12))

        themes = [
            ("Светлая", "light"),
            ("Тёмная", "dark"),
            ("Кастомная", "custom"),
        ]

        for label, value in themes:
            is_active = value == self._current_mode
            btn = ctk.CTkButton(
                opts_frame, text=label, width=130, height=38,
                corner_radius=8,
                fg_color="gray30" if is_active else "gray20",
                command=lambda v=value: self._on_theme_select(v),
            )
            btn.pack(side="left", padx=4, expand=True, fill="x")

        # Theme previews
        preview_frame = ctk.CTkFrame(section, fg_color="transparent")
        preview_frame.pack(fill="x", padx=12, pady=(0, 12))

        # Light preview
        light_box = ctk.CTkFrame(preview_frame, width=80, height=50, corner_radius=8,
                                  fg_color="#FFFFFF", border_width=2, border_color="#000000")
        light_box.pack(side="left", padx=(0, 16))
        light_box.pack_propagate(False)
        ctk.CTkLabel(light_box, text="Aa", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").pack(expand=True)

        # Dark preview
        dark_box = ctk.CTkFrame(preview_frame, width=80, height=50, corner_radius=8,
                                 fg_color="#1E1E1E", border_width=2, border_color="#555555")
        dark_box.pack(side="left", padx=(0, 16))
        dark_box.pack_propagate(False)
        ctk.CTkLabel(dark_box, text="Aa", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#FFFFFF").pack(expand=True)

        # Custom preview (live)
        self.custom_preview = ctk.CTkFrame(preview_frame, width=80, height=50, corner_radius=8)
        self.custom_preview.pack(side="left")
        self.custom_preview.pack_propagate(False)
        self.custom_preview_label = ctk.CTkLabel(
            self.custom_preview, text="Aa", font=ctk.CTkFont(size=14, weight="bold")
        )
        self.custom_preview_label.pack(expand=True)
        self._update_custom_preview()

        # ── Custom RGB Section ───────────────────────────
        self.custom_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="gray15")
        self.custom_frame.pack(fill="x", padx=pad_x, pady=(0, 8))

        ctk.CTkLabel(self.custom_frame, text="  Кастомная тема (RGB)",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12, 8))

        self.color_entries: dict[str, ctk.CTkEntry] = {}
        colors_config = [
            ("bg", "Фон"),
            ("fg", "Текст"),
            ("accent", "Акцент"),
            ("border", "Рамка"),
        ]

        for key, label in colors_config:
            row = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(row, text=f"{label}:", width=70, anchor="w",
                         font=ctk.CTkFont(size=12)).pack(side="left")

            r = ctk.CTkEntry(row, width=55, height=30, placeholder_text="R", corner_radius=6)
            r.pack(side="left", padx=2)
            r.insert(0, str(self._custom_colors[key][0]))

            g = ctk.CTkEntry(row, width=55, height=30, placeholder_text="G", corner_radius=6)
            g.pack(side="left", padx=2)
            g.insert(0, str(self._custom_colors[key][1]))

            b = ctk.CTkEntry(row, width=55, height=30, placeholder_text="B", corner_radius=6)
            b.pack(side="left", padx=2)
            b.insert(0, str(self._custom_colors[key][2]))

            # Color swatch
            swatch = ctk.CTkLabel(row, text="  ", width=24, height=24, corner_radius=4,
                                  fg_color=_rgb_hex(self._custom_colors[key]))
            swatch.pack(side="left", padx=(8, 0))

            self.color_entries[key] = {"r": r, "g": g, "b": b, "swatch": swatch}

            # Live update on change
            for entry in [r, g, b]:
                entry.bind("<KeyRelease>", lambda e, k=key: self._on_color_change(k))

        # Live preview button
        self.preview_btn = ctk.CTkButton(
            self.custom_frame, text="\U0001F441  Предпросмотр", height=34,
            corner_radius=8, command=self._apply_preview,
            fg_color="gray30"
        )
        self.preview_btn.pack(padx=12, pady=(8, 12))

        if self._current_mode != "custom":
            self.custom_frame.pack_forget()

        # ── Providers Section ────────────────────────────
        providers_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="gray15")
        providers_frame.pack(fill="x", padx=pad_x, pady=(0, 8))

        ctk.CTkLabel(providers_frame, text="  Подключённые провайдеры",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12, 8))

        from aLCloud.database import get_providers, delete_provider
        providers = get_providers()
        if providers:
            for p in providers:
                row = ctk.CTkFrame(providers_frame, fg_color="transparent")
                row.pack(fill="x", padx=12, pady=2)

                name = p.get("display_name", p.get("type", ""))
                cid = p.get("client_id", "")
                masked = f"{cid[:8]}...{cid[-4:]}" if len(cid) > 12 else (cid or "(демо)")

                ctk.CTkLabel(row, text=f"  {name}  —  {masked}",
                             font=ctk.CTkFont(size=12), anchor="w").pack(side="left", fill="x", expand=True)

                def make_del(pid=p["id"]):
                    return lambda: self._delete_provider(pid, providers_frame)

                ctk.CTkButton(row, text="\uD83D\uDDD1", width=36, height=28,
                              corner_radius=6, fg_color="transparent",
                              hover_color="#FF6B6B", command=make_del()).pack(side="right", padx=(0, 4))
        else:
            ctk.CTkLabel(providers_frame, text="  Нет подключённых провайдеров",
                         font=ctk.CTkFont(size=12), text_color="gray50").pack(anchor="w", padx=12, pady=(0, 12))

        # Bottom buttons
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=pad_x, pady=(8, 20))

        ctk.CTkButton(bottom, text="Отмена", width=120, height=38, corner_radius=8,
                      fg_color="gray30", command=self._close).pack(side="right", padx=(8, 0))

        ctk.CTkButton(bottom, text="Сохранить", width=120, height=38, corner_radius=8,
                      command=self._on_save).pack(side="right")

    def _on_theme_select(self, mode: str):
        self._current_mode = mode
        if mode == "custom":
            self.custom_frame.pack(fill="x", padx=24, pady=(0, 8), after=self.winfo_children()[1])
        else:
            self.custom_frame.pack_forget()

    def _on_color_change(self, key: str):
        try:
            entries = self.color_entries[key]
            r = max(0, min(255, int(entries["r"].get() or 0)))
            g = max(0, min(255, int(entries["g"].get() or 0)))
            b = max(0, min(255, int(entries["b"].get() or 0)))
            entries["swatch"].configure(fg_color=_rgb_hex((r, g, b)))
        except ValueError:
            pass

    def _update_custom_preview(self):
        colors = self._custom_colors
        self.custom_preview.configure(
            fg_color=_rgb_hex(colors["bg"]),
            border_color=_rgb_hex(colors["border"]),
            border_width=2,
        )
        self.custom_preview_label.configure(text_color=_rgb_hex(colors["fg"]))

    def _apply_preview(self):
        try:
            colors = {}
            for key, entries in self.color_entries.items():
                r = max(0, min(255, int(entries["r"].get() or 0)))
                g = max(0, min(255, int(entries["g"].get() or 0)))
                b = max(0, min(255, int(entries["b"].get() or 0)))
                colors[key] = (r, g, b)
            self._custom_colors = colors
            self._update_custom_preview()
            self._theme.apply("custom", colors)
        except ValueError:
            pass

    def _on_save(self):
        if self._current_mode == "custom":
            self._apply_preview()
        else:
            self._theme.apply(self._current_mode)
        self._close()

    def _delete_provider(self, pid: int, frame: ctk.CTkFrame):
        from aLCloud.database import delete_provider
        delete_provider(pid)
        self._close()
        # Reopen settings to refresh list
        SettingsDialog(self.master)

    def _close(self):
        self.grab_release()
        self.destroy()
        # Refresh main window
        if hasattr(self.master, "refresh_sidebar"):
            self.master.refresh_sidebar()
