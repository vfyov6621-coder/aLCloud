"""File browser — list/grid views."""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

from aLCloud.providers import create_provider
from aLCloud.database import save_file_cache


class FileBrowser(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._current_provider = None
        self._current_files: list[dict] = []
        self._current_path = "/"
        self._view_mode = "list"
        self._build()

    def _build(self):
        bar = ctk.CTkFrame(self, height=36, corner_radius=0, fg_color="transparent")
        bar.pack(fill="x", padx=0, pady=(8, 0))
        bar.pack_propagate(False)

        ctk.CTkButton(bar, text="<-", width=32, height=28, corner_radius=6,
                      command=self._go_back, fg_color="transparent").pack(side="left", padx=(12, 4))

        self.path_label = ctk.CTkLabel(bar, text="/", anchor="w", font=ctk.CTkFont(size=12))
        self.path_label.pack(side="left", padx=8)

        self.view_btn = ctk.CTkButton(bar, text="List", width=50, height=28, corner_radius=6,
                                       command=self._toggle_view, fg_color="transparent")
        self.view_btn.pack(side="right", padx=(0, 12))

        self.file_area = ctk.CTkScrollableFrame(self, corner_radius=8)
        self.file_area.pack(fill="both", expand=True, padx=12, pady=8)
        self._show_empty("Подключите провайдер для просмотра файлов")

    def _show_empty(self, msg):
        for w in self.file_area.winfo_children():
            w.destroy()
        f = ctk.CTkFrame(self.file_area, fg_color="transparent")
        f.pack(expand=True, fill="both", pady=80)
        ctk.CTkLabel(f, text=msg, font=ctk.CTkFont(size=14), text_color="gray50").pack()

    def load_provider(self, provider_data: dict):
        self._current_provider = provider_data
        self._current_path = "/"
        try:
            p = create_provider(provider_data)
            self._current_files = p.list_files("/")
        except Exception:
            self._current_files = []
        save_file_cache(provider_data["id"], self._current_files)
        self.path_label.configure(text="  /")
        self._render()

    def search(self, query):
        if not self._current_provider:
            self._show_empty("Сначала выберите провайдер")
            return
        try:
            p = create_provider(self._current_provider)
            self._current_files = p.search(query)
        except Exception:
            self._current_files = []
        self._render()

    def upload_file(self):
        if not self._current_provider:
            messagebox.showinfo("aLCloud", "Сначала подключите провайдер")
            return
        fp = filedialog.askopenfilename(title="Выберите файл")
        if not fp:
            return
        try:
            p = create_provider(self._current_provider)
            r = p.upload(fp, self._current_path)
            if "error" in r:
                messagebox.showerror("Ошибка", r["error"])
            else:
                messagebox.showinfo("OK", "Файл загружен!")
                self.load_provider(self._current_provider)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear(self):
        self._current_provider = None
        self._current_files = []
        self._show_empty("Подключите провайдер для просмотра файлов")

    def _toggle_view(self):
        self._view_mode = "grid" if self._view_mode == "list" else "list"
        self.view_btn.configure(text="Grid" if self._view_mode == "list" else "List")
        self._render()

    def _go_back(self):
        if self._current_path == "/":
            return
        parts = self._current_path.rstrip("/").split("/")
        self._current_path = "/" if len(parts) <= 1 else "/".join(parts[:-1])
        self.path_label.configure(text=f"  {self._current_path}")
        self._refresh()

    def _refresh(self):
        if not self._current_provider:
            return
        try:
            p = create_provider(self._current_provider)
            self._current_files = p.list_files(self._current_path)
        except Exception:
            self._current_files = []
        self._render()

    def _render(self):
        for w in self.file_area.winfo_children():
            w.destroy()
        if not self._current_files:
            self._show_empty("Нет файлов")
            return
        if self._view_mode == "list":
            self._render_list()
        else:
            self._render_grid()

    def _render_list(self):
        # Header
        h = ctk.CTkFrame(self.file_area, corner_radius=6, height=30)
        h.pack(fill="x", pady=(0, 4))
        h.pack_propagate(False)
        for txt, w in [("Название", 280), ("Размер", 90), ("Изменён", 140), ("Тип", 140)]:
            ctk.CTkLabel(h, text=txt, font=ctk.CTkFont(size=11, weight="bold"),
                         anchor="w", width=w).pack(side="left", padx=4)

        for f in self._current_files:
            self._list_row(f)

    def _list_row(self, f):
        is_dir = f.get("is_folder", False)
        icon = "[D]" if is_dir else "[F]"
        name = f.get("name", "?")
        size = self._fmt_size(f.get("size", 0))
        mod = f.get("modified_at", "")[:16] or ""
        mime = "Папка" if is_dir else (f.get("mime_type", "") or "Файл")

        row = ctk.CTkFrame(self.file_area, corner_radius=6, fg_color="transparent", height=34)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        ctk.CTkLabel(row, text=f"  {icon}  {name}", anchor="w",
                     font=ctk.CTkFont(size=12), width=280).pack(side="left", padx=4)
        ctk.CTkLabel(row, text=size, anchor="w", font=ctk.CTkFont(size=11),
                     width=90, text_color="gray50").pack(side="left", padx=4)
        ctk.CTkLabel(row, text=mod, anchor="w", font=ctk.CTkFont(size=11),
                     width=140, text_color="gray50").pack(side="left", padx=4)
        ctk.CTkLabel(row, text=mime, anchor="w", font=ctk.CTkFont(size=11),
                     width=140, text_color="gray50").pack(side="left", padx=4)

        if is_dir:
            for w in row.winfo_children():
                w.bind("<Double-1>", lambda e, n=name: self._navigate(n))

        def ctx(event, fd=f):
            m = tk.Menu(self, tearoff=0)
            if not fd.get("is_folder"):
                m.add_command(label="Скачать", command=lambda: self._download(fd))
                m.add_separator()
            m.add_command(label="Удалить", command=lambda: self._delete(fd))
            m.tk_popup(event.x_root, event.y_root)

        row.bind("<Button-3>", ctx)
        for w in row.winfo_children():
            w.bind("<Button-3>", ctx)

    def _render_grid(self):
        gf = ctk.CTkFrame(self.file_area, fg_color="transparent")
        gf.pack(fill="both", expand=True)
        cols = 4
        for i, f in enumerate(self._current_files):
            is_dir = f.get("is_folder", False)
            icon = "[D]" if is_dir else "[F]"
            name = f.get("name", "?")
            size = self._fmt_size(f.get("size", 0))
            card = ctk.CTkFrame(gf, corner_radius=10, width=150, height=110)
            card.grid(row=i // cols, column=i % cols, padx=6, pady=6, sticky="nsew")
            gf.grid_columnconfigure(i % cols, weight=1)
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=24)).pack(pady=(12, 2))
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=11, weight="bold"),
                         wraplength=130).pack(pady=2)
            ctk.CTkLabel(card, text=size, font=ctk.CTkFont(size=10),
                         text_color="gray50").pack()
            if is_dir:
                for w in card.winfo_children():
                    w.bind("<Button-1>", lambda e, n=name: self._navigate(n))

    def _navigate(self, folder):
        self._current_path = f"{self._current_path}/{folder}" if self._current_path != "/" else f"/{folder}"
        self.path_label.configure(text=f"  {self._current_path}")
        self._refresh()

    def _download(self, f):
        if not self._current_provider:
            return
        sp = filedialog.asksaveasfilename(initialfile=f.get("name", "file"))
        if not sp:
            return
        try:
            p = create_provider(self._current_provider)
            r = p.download(f.get("id", ""), sp)
            if "error" in r:
                messagebox.showerror("Ошибка", r["error"])
            else:
                messagebox.showinfo("OK", "Файл скачан!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete(self, f):
        if not self._current_provider:
            return
        if not messagebox.askyesno("Удалить", f"Удалить '{f.get('name', '')}'?"):
            return
        try:
            p = create_provider(self._current_provider)
            r = p.delete(f.get("id", ""))
            if "error" in r:
                messagebox.showerror("Ошибка", r["error"])
            else:
                self.load_provider(self._current_provider)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    @staticmethod
    def _fmt_size(size):
        if size == 0:
            return "-"
        for u in ["Б", "КБ", "МБ", "ГБ", "ТБ"]:
            if size < 1024:
                return f"{size:.0f} {u}"
            size /= 1024
        return f"{size:.1f} ПБ"
