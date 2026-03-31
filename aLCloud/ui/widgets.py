"""Reusable custom widgets for aLCloud UI."""

import customtkinter as ctk


class IconButton(ctk.CTkButton):
    """A button with an icon (unicode/emoji) and optional text."""

    def __init__(self, master, icon="", text="", width=36, height=36,
                 icon_font_size=16, text_font_size=12, **kwargs):
        self.icon = icon
        self.icon_text = f"{icon} {text}".strip() if text else icon

        super().__init__(
            master,
            text=self.icon_text,
            width=width,
            height=height,
            font=ctk.CTkFont(size=icon_font_size if not text else text_font_size),
            **kwargs,
        )

    def set_icon(self, icon):
        """Update the icon."""
        self.icon = icon
        current_text = self.cget("text")
        # Preserve any text after the icon
        parts = current_text.split(" ", 1)
        new_text = f"{icon} {parts[1]}".strip() if len(parts) > 1 else icon
        self.configure(text=new_text)


class ProviderCard(ctk.CTkFrame):
    """Single provider item for the sidebar.

    Displays: icon, name, status indicator, storage usage bar.
    """

    def __init__(self, master, provider_data, on_click=None, on_right_click=None, **kwargs):
        super().__init__(master, corner_radius=8, **kwargs)

        self.provider_data = provider_data
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.selected = False

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # Icon label
        icon = provider_data.get("icon", "☁️")
        self.icon_label = ctk.CTkLabel(
            self, text=icon, font=ctk.CTkFont(size=20), width=36
        )
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=8)

        # Provider name
        name = provider_data.get("display_name", provider_data.get("type", "Unknown"))
        self.name_label = ctk.CTkLabel(
            self, text=name,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.name_label.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(8, 0))

        # Status indicator
        is_connected = provider_data.get("is_connected", 0)
        status_color = "#2ECC71" if is_connected else "#E74C3C"
        self.status_dot = ctk.CTkLabel(
            self, text="●", font=ctk.CTkFont(size=10),
            text_color=status_color, width=16
        )
        self.status_dot.grid(row=0, column=2, padx=(0, 10), pady=(8, 0))

        # Storage usage bar
        used = provider_data.get("used_space", 0) or 0
        total = provider_data.get("total_space", 0) or 1
        self.progress = ctk.CTkProgressBar(
            self, height=4, corner_radius=2
        )
        self.progress.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(4, 8))
        if total > 0:
            self.progress.set(used / total)
        else:
            self.progress.set(0)

        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Button-3>", self._on_right_click)
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_click)
            child.bind("<Button-3>", self._on_right_click)

    def _on_click(self, event=None):
        if self.on_click:
            self.on_click(self.provider_data)

    def _on_right_click(self, event=None):
        if self.on_right_click:
            self.on_right_click(self.provider_data, event)

    def set_selected(self, selected):
        """Highlight this card as selected."""
        self.selected = selected
        if selected:
            self.configure(fg_color=("gray85", "gray25"))
        else:
            self.configure(fg_color=("gray90", "gray20"))

    def update_storage(self, used, total):
        """Update the storage usage bar."""
        if total > 0:
            self.progress.set(used / total)
        else:
            self.progress.set(0)


class FileItem(ctk.CTkFrame):
    """Single file row in the list view."""

    def __init__(self, master, file_data, on_double_click=None,
                 on_right_click=None, on_select=None, **kwargs):
        super().__init__(master, corner_radius=6, height=44, **kwargs)

        self.file_data = file_data
        self.on_double_click = on_double_click
        self.on_right_click = on_right_click
        self.on_select = on_select
        self.selected = False

        # Configure columns
        self.grid_columnconfigure(1, weight=1)  # Name takes remaining space

        # Icon
        icon = file_data.get("icon", "📄")
        self.icon_label = ctk.CTkLabel(
            self, text=icon, font=ctk.CTkFont(size=18), width=40
        )
        self.icon_label.grid(row=0, column=0, padx=(12, 5), pady=6)

        # File name
        name = file_data.get("name", "Unknown")
        self.name_label = ctk.CTkLabel(
            self, text=name,
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.name_label.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=6)

        # Size
        size = file_data.get("size_display", "")
        if size:
            self.size_label = ctk.CTkLabel(
                self, text=size,
                font=ctk.CTkFont(size=12),
                width=90,
                anchor="e",
            )
            self.size_label.grid(row=0, column=2, padx=(0, 10), pady=6)

        # Modified
        modified = file_data.get("modified_display", "")
        if modified:
            self.modified_label = ctk.CTkLabel(
                self, text=modified,
                font=ctk.CTkFont(size=12),
                width=110,
                anchor="e",
            )
            self.modified_label.grid(row=0, column=3, padx=(0, 10), pady=6)

        # Type
        file_type = file_data.get("type_display", "")
        if file_type:
            self.type_label = ctk.CTkLabel(
                self, text=file_type,
                font=ctk.CTkFont(size=12),
                width=130,
                anchor="e",
            )
            self.type_label.grid(row=0, column=4, padx=(0, 12), pady=6)

        # Bind events
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<Button-1>", self._on_select)
        for child in self.winfo_children():
            child.bind("<Double-Button-1>", self._on_double_click)
            child.bind("<Button-3>", self._on_right_click)
            child.bind("<Button-1>", self._on_select)

    def _on_double_click(self, event=None):
        if self.on_double_click:
            self.on_double_click(self.file_data)

    def _on_right_click(self, event=None):
        if self.on_right_click:
            self.on_right_click(self.file_data, event)

    def _on_select(self, event=None):
        if self.on_select:
            self.on_select(self.file_data)
        self.set_selected(True)

    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.configure(fg_color=("gray85", "gray25"))
        else:
            self.configure(fg_color=("transparent", "transparent"))


class FileCard(ctk.CTkFrame):
    """File card for grid view."""

    def __init__(self, master, file_data, on_double_click=None, on_right_click=None, **kwargs):
        super().__init__(master, corner_radius=10, width=150, height=120, **kwargs)

        self.file_data = file_data
        self.on_double_click = on_double_click
        self.on_right_click = on_right_click

        self.grid_columnconfigure(0, weight=1)

        # Icon
        icon = file_data.get("icon", "📄")
        self.icon_label = ctk.CTkLabel(
            self, text=icon, font=ctk.CTkFont(size=32)
        )
        self.icon_label.pack(pady=(12, 4))

        # Name (truncated)
        name = file_data.get("name", "Unknown")
        if len(name) > 18:
            name = name[:16] + "…"
        self.name_label = ctk.CTkLabel(
            self, text=name,
            font=ctk.CTkFont(size=12),
            wraplength=130,
        )
        self.name_label.pack(pady=(0, 2))

        # Size
        size = file_data.get("size_display", "")
        if size:
            self.size_label = ctk.CTkLabel(
                self, text=size, font=ctk.CTkFont(size=11),
                text_color="gray50",
            )
            self.size_label.pack(pady=(0, 8))

        # Bind events
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<Button-3>", self._on_right_click)
        for child in self.winfo_children():
            child.bind("<Double-Button-1>", self._on_double_click)
            child.bind("<Button-3>", self._on_right_click)

    def _on_double_click(self, event=None):
        if self.on_double_click:
            self.on_double_click(self.file_data)

    def _on_right_click(self, event=None):
        if self.on_right_click:
            self.on_right_click(self.file_data, event)


class Breadcrumb(ctk.CTkFrame):
    """Path breadcrumb navigation bar."""

    def __init__(self, master, on_navigate=None, **kwargs):
        super().__init__(master, height=36, **kwargs)
        self.on_navigate = on_navigate
        self._segments = []

    def set_path(self, path):
        """Update the breadcrumb to show the given path."""
        # Clear existing segments
        for widget in self.winfo_children():
            widget.destroy()

        self._segments = []

        # Parse path
        if not path or path == "/":
            parts = ["/"]
        else:
            parts = path.strip("/").split("/")
            parts = ["/"] + parts

        for i, part in enumerate(parts):
            # Build the path for this segment
            if i == 0:
                seg_path = "/"
                label = "🏠"
            else:
                seg_path = "/" + "/".join(parts[1:i+1])
                label = part

            is_last = (i == len(parts) - 1)

            seg_label = ctk.CTkLabel(
                self, text=label,
                font=ctk.CTkFont(size=13, weight="bold" if is_last else "normal"),
                cursor="hand2" if not is_last else "",
            )

            if not is_last:
                seg_label.bind("<Button-1>", lambda e, p=seg_path: self._navigate(p))

            seg_label.pack(side="left", padx=(0 if i == 0 else 4, 0))

            self._segments.append((seg_path, seg_label))

            # Add separator
            if not is_last:
                sep = ctk.CTkLabel(self, text=" / ", font=ctk.CTkFont(size=13),
                                   text_color="gray50")
                sep.pack(side="left")

    def _navigate(self, path):
        if self.on_navigate:
            self.on_navigate(path)


class ColorEntry(ctk.CTkFrame):
    """RGB color input with preview square."""

    def __init__(self, master, label="", initial_color="#000000",
                 on_change=None, **kwargs):
        super().__init__(master, **kwargs)

        self.on_change = on_change
        self._color = initial_color

        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        row = 0

        # Label
        if label:
            self.label = ctk.CTkLabel(
                self, text=label, font=ctk.CTkFont(size=13), anchor="w", width=100
            )
            self.label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)
            col_start = 1
        else:
            col_start = 0

        # R entry
        r, g, b = self._hex_to_rgb(initial_color)

        ctk.CTkLabel(self, text="R", font=ctk.CTkFont(size=12)).grid(
            row=row, column=col_start, padx=2, pady=4
        )
        self.r_entry = ctk.CTkEntry(self, width=50, height=28,
                                     font=ctk.CTkFont(size=12))
        self.r_entry.insert(0, str(r))
        self.r_entry.grid(row=row, column=col_start + 1, padx=2, pady=4)
        self.r_entry.bind("<KeyRelease>", self._on_entry_change)

        # G entry
        ctk.CTkLabel(self, text="G", font=ctk.CTkFont(size=12)).grid(
            row=row, column=col_start + 2, padx=2, pady=4
        )
        self.g_entry = ctk.CTkEntry(self, width=50, height=28,
                                     font=ctk.CTkFont(size=12))
        self.g_entry.insert(0, str(g))
        self.g_entry.grid(row=row, column=col_start + 3, padx=2, pady=4)
        self.g_entry.bind("<KeyRelease>", self._on_entry_change)

        # B entry
        ctk.CTkLabel(self, text="B", font=ctk.CTkFont(size=12)).grid(
            row=row, column=col_start + 4, padx=2, pady=4
        )
        self.b_entry = ctk.CTkEntry(self, width=50, height=28,
                                     font=ctk.CTkFont(size=12))
        self.b_entry.insert(0, str(b))
        self.b_entry.grid(row=row, column=col_start + 5, padx=2, pady=4)
        self.b_entry.bind("<KeyRelease>", self._on_entry_change)

        # Preview square
        self.preview = ctk.CTkLabel(
            self, text="    ", width=30, height=28,
            fg_color=initial_color, corner_radius=4,
        )
        self.preview.grid(row=row, column=col_start + 6, padx=(8, 0), pady=4)

    def _on_entry_change(self, event=None):
        try:
            r = int(self.r_entry.get() or "0")
            g = int(self.g_entry.get() or "0")
            b = int(self.b_entry.get() or "0")
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            self._color = self._rgb_to_hex(r, g, b)
            self.preview.configure(fg_color=self._color)
            if self.on_change:
                self.on_change(self._color)
        except ValueError:
            pass

    def get_color(self):
        """Return current color as hex string."""
        self._on_entry_change()
        return self._color

    def get_rgb(self):
        """Return current color as (r, g, b) tuple."""
        try:
            r = int(self.r_entry.get() or "0")
            g = int(self.g_entry.get() or "0")
            b = int(self.b_entry.get() or "0")
            return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        except ValueError:
            return (0, 0, 0)

    def set_color(self, hex_color):
        """Set the color from a hex string."""
        r, g, b = self._hex_to_rgb(hex_color)
        self.r_entry.delete(0, "end")
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, "end")
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, "end")
        self.b_entry.insert(0, str(b))
        self._color = hex_color
        self.preview.configure(fg_color=hex_color)

    @staticmethod
    def _hex_to_rgb(hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(r, g, b):
        return "#{:02X}{:02X}{:02X}".format(r, g, b)


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing current path, file count, storage info."""

    def __init__(self, master, **kwargs):
        super().__init__(master, height=28, corner_radius=0, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.path_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12),
            anchor="w", text_color="gray50",
        )
        self.path_label.grid(row=0, column=0, sticky="w", padx=12, pady=4)

        self.count_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12),
            anchor="center", text_color="gray50",
        )
        self.count_label.grid(row=0, column=1, sticky="e", padx=12, pady=4)

        self.storage_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12),
            anchor="e", text_color="gray50",
        )
        self.storage_label.grid(row=0, column=2, sticky="e", padx=12, pady=4)

    def set_path(self, path):
        self.path_label.configure(text=f"Путь: {path}")

    def set_file_count(self, count):
        self.count_label.configure(text=f"{count} элементов")

    def set_storage(self, used, total):
        from aLCloud.providers import format_size
        self.storage_label.configure(
            text=f"Использовано: {format_size(used)} / {format_size(total)}"
        )

    def update_all(self, path="", count=0, used=0, total=0):
        self.set_path(path)
        self.set_file_count(count)
        self.set_storage(used, total)
