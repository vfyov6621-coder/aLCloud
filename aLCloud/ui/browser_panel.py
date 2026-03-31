"""Built-in browser panel — pywebview embedded in app."""

import customtkinter as ctk
import threading
import webview
from http.server import HTTPServer, BaseHTTPRequestHandler


class BrowserPanel(ctk.CTkFrame):
    """Built-in browser panel using pywebview."""

    def __init__(self, parent, on_done=None):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._on_done = on_done
        self._window = None
        self._thread = None
        self._build()

    def _build(self):
        # Address bar
        bar = ctk.CTkFrame(self, height=42, corner_radius=0, fg_color="transparent")
        bar.pack(fill="x")
        bar.pack_propagate(False)

        ctk.CTkButton(bar, text="<-", width=32, height=30, corner_radius=6,
                      fg_color="transparent", command=self._back).pack(side="left", padx=(8, 4))

        self.url_entry = ctk.CTkEntry(
            bar, placeholder_text="https://...", height=30, corner_radius=8
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.url_entry.bind("<Return>", lambda e: self._navigate())

        ctk.CTkButton(bar, text="Go", width=50, height=30, corner_radius=6,
                      command=self._navigate).pack(side="left", padx=(0, 8))

        # Go back
        ctk.CTkButton(bar, text="X", width=32, height=30, corner_radius=6,
                      fg_color="transparent", text_color="#FF6B6B",
                      command=self._close_browser).pack(side="right", padx=(0, 8))

        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self, text="Браузер откроется в отдельном окне\n"
                       "Введите URL и нажмите Go",
            font=ctk.CTkFont(size=14), text_color="gray50"
        )
        self.placeholder.pack(expand=True)

    def open_url(self, url: str):
        """Open URL in the built-in browser."""
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)
        self.placeholder.pack_forget()
        self._launch_webview(url)

    def _navigate(self):
        url = self.url_entry.get().strip()
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            self.placeholder.pack_forget()
            self._launch_webview(url)

    def _launch_webview(self, url: str):
        """Launch pywebview window."""
        if self._window:
            try:
                self._window.destroy()
            except Exception:
                pass

        self._window = webview.create_window(
            "aLCloud — Браузер",
            url,
            width=800,
            height=600,
            resizable=True,
        )

        def run():
            webview.start()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def _back(self):
        if self._window:
            try:
                # pywebview doesn't have a simple back, but we can try
                pass
            except Exception:
                pass

    def _close_browser(self):
        if self._window:
            try:
                self._window.destroy()
                self._window = None
            except Exception:
                pass
        self.placeholder.pack(expand=True)

    def destroy(self):
        """Clean up when panel is hidden."""
        self._close_browser()
        super().destroy()
