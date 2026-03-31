"""File browser — list/grid views with breadcrumbs."""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

from aLCloud.providers import create_provider
from aLCloud.database import save_file_cache, get_cached_files


class FileBrowser(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._current_provider = None
        self._current_files: list[dict] = []
        self._current_path: str = "/"
        self._view_mode: str = "list"  # list or grid
        self._build()

    def _build(self):
        # Breadcrumb bar
        self.breadcrumb_frame = ctk.CTkFrame(self, height=38, corner_radius=0, fg_color="transparent")
        self.breadcrumb_frame.pack(fill="x", padx=0, pady=(8, 0))
        self.breadcrumb_frame.pack_propagate(False)

        self.back_btn = ctk.CTkButton(
            self.breadcrumb_frame, text="\u2190", width=32, height=28,
            corner_radius=6, command=self._go_back,
            fg_color="transparent", hover_color="gray20"
        )
        self.back_btn.pack(side="left", padx=(12, 4))

        self.breadcrumb_label = ctk.CTkLabel(
            self.breadcrumb_frame, text="/", anchor="w", font=ctk.CTkFont(size=12)
        )
        self.breadcrumb_label.pack(side="left", padx=8)

        # View toggle
        self.view_btn = ctk.CTkButton(
            self.breadcrumb_frame, text="\u2630", width=32, height=28,
            corner_radius=6, command=self._toggle_view,
            fg_color="transparent", hover_color="gray20"
        )
        self.view_btn.pack(side="right", padx=(0, 12))

        # File area
        self.file_area = ctk.CTkScrollableFrame(self, corner_radius=8)
        self.file_area.pack(fill="both", expand=True, padx=12, pady=8)

        # Empty state
        self._show_empty("Подключите провайдер для просмотра файлов")

    def _show_empty(self, msg: str):
        for w in self.file_area.winfo_children():
            w.destroy()

        empty = ctk.CTkFrame(self.file_area, fg_color="transparent")
        empty.pack(expand=True, fill="both", pady=100)
        ctk.CTkLabel(empty, text="\u2601", font=ctk.CTkFont(size=48)).pack(pady=(0, 12))
        ctk.CTkLabel(empty, text=msg, font=ctk.CTkFont(size=14),
                     text_color="gray50").pack()

    def _show_empty_provider(self):
        self._show_empty("Нет файлов для отображения")

    def load_provider(self, provider_data: dict):
        """Load and display files for a provider."""
        self._current_provider = provider_data
        self._current_path = "/"

        try:
            provider = create_provider(provider_data)
            self._current_files = provider.list_files("/")
        except Exception:
            self._current_files = []

        save_file_cache(provider_data["id"], self._current_files)
        self._update_breadcrumb()
        self._render_files()

    def search(self, query: str):
        """Search files in current provider."""
        if not self._current_provider:
            self._show_empty("Сначала выберите провайдер")
            return
        try:
            provider = create_provider(self._current_provider)
            results = provider.search(query)
        except Exception:
            results = []
        self._current_files = results
        self._render_files()

    def upload_file(self):
        """Open file dialog and upload to current provider."""
        if not self._current_provider:
            messagebox.showinfo("aLCloud", "Сначала подключите провайдер")
            return
        filepath = filedialog.askopenfilename(title="Выберите файл для загрузки")
        if not filepath:
            return
        try:
            provider = create_provider(self._current_provider)
            result = provider.upload(filepath, self._current_path)
            if "error" in result:
                messagebox.showerror("Ошибка загрузки", result["error"])
            else:
                messagebox.showinfo("Успешно", "Файл загружен!")
                self.load_provider(self._current_provider)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear(self):
        self._current_provider = None
        self._current_files = []
        self._show_empty("Подключите провайдер для просмотра файлов")

    def _update_breadcrumb(self):
        self.breadcrumb_label.configure(text=f"  {self._current_path}")

    def _toggle_view(self):
        self._view_mode = "grid" if self._view_mode == "list" else "list"
        self.view_btn.configure(text="\u25A6" if self._view_mode == "list" else "\u2630")
        self._render_files()

    def _go_back(self):
        if self._current_path == "/":
            return
        parts = self._current_path.rstrip("/").split("/")
        if len(parts) <= 1:
            self._current_path = "/"
        else:
            self._current_path = "/".join(parts[:-1])
        self._update_breadcrumb()
        self._refresh_path()

    def _refresh_path(self):
        if not self._current_provider:
            return
        try:
            provider = create_provider(self._current_provider)
            self._current_files = provider.list_files(self._current_path)
        except Exception:
            self._current_files = []
        self._render_files()

    def _render_files(self):
        for w in self.file_area.winfo_children():
            w.destroy()

        if not self._current_files:
            self._show_empty_provider()
            return

        if self._view_mode == "list":
            self._render_list()
        else:
            self._render_grid()

    def _render_list(self):
        # Header
        header = ctk.CTkFrame(self.file_area, corner_radius=6, fg_color="gray20", height=32)
        header.pack(fill="x", pady=(0, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="  Название", font=ctk.CTkFont(size=11, weight="bold"),
                     anchor="w", width=300).pack(side="left", padx=4)
        ctk.CTkLabel(header, text="Размер", font=ctk.CTkFont(size=11, weight="bold"),
                     anchor="center", width=100).pack(side="left", padx=4)
        ctk.CTkLabel(header, text="Изменён", font=ctk.CTkFont(size=11, weight="bold"),
                     anchor="center", width=150).pack(side="left", padx=4)
        ctk.CTkLabel(header, text="Тип", font=ctk.CTkFont(size=11, weight="bold"),
                     anchor="w").pack(side="left", padx=4)

        for f in self._current_files:
            self._create_list_row(f)

    def _create_list_row(self, f: dict):
        is_folder = f.get("is_folder", False)
        icon = "\uD83D\uDCC1" if is_folder else "\uD83D\uDCC4"
        name = f.get("name", "Unknown")
        size = self._format_size(f.get("size", 0))
        modified = f.get("modified_at", "")[:16] if f.get("modified_at") else ""
        mime = f.get("mime_type", "Папка" if is_folder else "Файл")

        row = ctk.CTkFrame(self.file_area, corner_radius=6, fg_color="transparent", height=36)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        ctk.CTkLabel(row, text=f"  {icon}  {name}", anchor="w",
                     font=ctk.CTkFont(size=12), width=300).pack(side="left", padx=4)
        ctk.CTkLabel(row, text=size, anchor="center",
                     font=ctk.CTkFont(size=11), width=100, text_color="gray50").pack(side="left", padx=4)
        ctk.CTkLabel(row, text=modified, anchor="center",
                     font=ctk.CTkFont(size=11), width=150, text_color="gray50").pack(side="left", padx=4)
        ctk.CTkLabel(row, text=mime, anchor="w",
                     font=ctk.CTkFont(size=11), text_color="gray50").pack(side="left", padx=4)

        if is_folder:
            for w in row.winfo_children():
                w.bind("<Double-1>", lambda e, path=f.get("name", ""): self._navigate(path))
                w.bind("<Button-1>", lambda e, path=f.get("name", ""): self._navigate(path))

        # Right-click context menu
        def on_right_click(event, file_data=f):
            menu = tk.Menu(self, tearoff=0)
            if not is_folder:
                menu.add_command(label="\u2B07 Скачать", command=lambda: self._download_file(file_data))
                menu.add_separator()
            menu.add_command(label="\uD83D\uDDD1 Удалить", command=lambda: self._delete_file(file_data))
            menu.tk_popup(event.x_root, event.y_root)

        row.bind("<Button-3>", on_right_click)
        for w in row.winfo_children():
            w.bind("<Button-3>", on_right_click)

    def _render_grid(self):
        grid_frame = ctk.CTkFrame(self.file_area, corner_radius=0, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        columns = 4
        for i, f in enumerate(self._current_files):
            row_idx = i // columns
            col_idx = i % columns

            is_folder = f.get("is_folder", False)
            icon = "\uD83D\uDCC1" if is_folder else "\uD83D\uDCC4"
            name = f.get("name", "Unknown")
            size = self._format_size(f.get("size", 0))

            card = ctk.CTkFrame(grid_frame, corner_radius=10, fg_color="gray15", width=160, height=120)
            card.grid(row=row_idx, column=col_idx, padx=6, pady=6, sticky="nsew")
            grid_frame.grid_columnconfigure(col_idx, weight=1)

            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=32)).pack(pady=(16, 4))
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=11, weight="bold"),
                         anchor="center", wraplength=140).pack(pady=2)
            ctk.CTkLabel(card, text=size, font=ctk.CTkFont(size=10),
                         text_color="gray50").pack()

            if is_folder:
                for w in card.winfo_children():
                    w.bind("<Button-1>", lambda e, path=f.get("name", ""): self._navigate(path))

    def _navigate(self, folder_name: str):
        if self._current_path == "/":
            self._current_path = f"/{folder_name}"
        else:
            self._current_path = f"{self._current_path}/{folder_name}"
        self._update_breadcrumb()
        self._refresh_path()

    def _download_file(self, f: dict):
        if not self._current_provider:
            return
        save_path = filedialog.asksaveasfilename(
            initialfile=f.get("name", "file"), title="Сохранить файл"
        )
        if not save_path:
            return
        try:
            provider = create_provider(self._current_provider)
            result = provider.download(f.get("id", ""), save_path)
            if "error" in result:
                messagebox.showerror("Ошибка", result["error"])
            else:
                messagebox.showinfo("Успешно", "Файл скачан!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete_file(self, f: dict):
        if not self._current_provider:
            return
        if not messagebox.askyesno("Удалить", f"Удалить '{f.get('name', '')}'?"):
            return
        try:
            provider = create_provider(self._current_provider)
            result = provider.delete(f.get("id", ""))
            if "error" in result:
                messagebox.showerror("Ошибка", result["error"])
            else:
                self.load_provider(self._current_provider)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    @staticmethod
    def _format_size(size: int) -> str:
        if size == 0:
            return "—"
        for unit in ["Б", "КБ", "МБ", "ГБ", "ТБ"]:
            if size < 1024:
                return f"{size:.0f} {unit}"
            size /= 1024
        return f"{size:.1f} ПБ"
