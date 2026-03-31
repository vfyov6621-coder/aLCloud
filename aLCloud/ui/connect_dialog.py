"""Connect provider dialog — OAuth flow directly in UI."""

import customtkinter as ctk
from aLCloud.database import save_provider, update_provider_tokens
from aLCloud.providers import PROVIDER_INFO, create_provider
from aLCloud.ui.telegram_dialog import TelegramDialog


class ConnectDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_done=None):
        super().__init__(parent)
        self._on_done = on_done
        self.title("Добавить провайдер")
        self.geometry("480x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._selected_type: str | None = None
        self._build()

    def _build(self):
        pad = {"padx": 20, "pady": (8, 0)}

        ctk.CTkLabel(self, text="Подключить облако",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(**pad, pady=(24, 4))

        ctk.CTkLabel(self, text="Выберите провайдер и введите данные для подключения",
                     font=ctk.CTkFont(size=12), text_color="gray50").pack(**pad)

        # Provider selector
        self.provider_var = ctk.StringVar(value="")
        names = [p["name"] for p in PROVIDER_INFO]
        self.provider_menu = ctk.CTkOptionMenu(
            self, values=["— Выберите —"] + names,
            variable=self.provider_var, command=self._on_provider_selected,
            width=400, corner_radius=8
        )
        self.provider_menu.pack(**pad, pady=(16, 8))

        # Details frame
        self.details_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.details_frame.pack(fill="x", **pad)

        # Connect button
        self.connect_btn = ctk.CTkButton(
            self, text="Подключить", height=42, width=400,
            corner_radius=8, command=self._on_connect,
            state="disabled"
        )
        self.connect_btn.pack(pady=(16, 24), padx=20)

    def _on_provider_selected(self, value: str):
        # Clear old widgets
        for w in self.details_frame.winfo_children():
            w.destroy()

        # Find selected provider info
        info = None
        for p in PROVIDER_INFO:
            if p["name"] == value:
                info = p
                break

        if not info:
            self._selected_type = None
            self.connect_btn.configure(state="disabled")
            return

        self._selected_type = info["type"]

        # Description
        ctk.CTkLabel(
            self.details_frame,
            text=f"{info['name']}  •  Макс. файл: {info['max_file']}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(0, 8))

        if info["type"] == "telegram":
            ctk.CTkLabel(
                self.details_frame,
                text="Telegram подключается через номер телефона и код.\nНажмите «Подключить» для начала.",
                font=ctk.CTkFont(size=12), text_color="gray50", wraplength=400
            ).pack(anchor="w")
        else:
            # Client ID
            ctk.CTkLabel(self.details_frame, text="Client ID",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(4, 2))
            self.client_id_entry = ctk.CTkEntry(
                self.details_frame, placeholder_text="Ваш Client ID",
                width=400, height=36, corner_radius=8
            )
            self.client_id_entry.pack(anchor="w", pady=(0, 8))

            # Client Secret
            if info["needs_secret"]:
                ctk.CTkLabel(self.details_frame, text="Client Secret",
                             font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(4, 2))
                self.client_secret_entry = ctk.CTkEntry(
                    self.details_frame, placeholder_text="Ваш Client Secret",
                    width=400, height=36, corner_radius=8, show="*"
                )
                self.client_secret_entry.pack(anchor="w", pady=(0, 8))

        self.connect_btn.configure(state="normal")

    def _on_connect(self):
        if not self._selected_type:
            return

        # Telegram special flow
        if self._selected_type == "telegram":
            self.grab_release()
            self.destroy()
            TelegramDialog(self.master, on_done=self._on_done)
            return

        client_id = self.client_id_entry.get().strip() if hasattr(self, "client_id_entry") else ""
        client_secret = self.client_secret_entry.get().strip() if hasattr(self, "client_secret_entry") else ""

        if not client_id:
            self._show_error("Введите Client ID")
            return

        # Disable button during OAuth
        self.connect_btn.configure(text="Авторизация...", state="disabled")
        self.update()

        # Save provider first
        info = next((p for p in PROVIDER_INFO if p["type"] == self._selected_type), None)
        pid = save_provider(
            provider_type=self._selected_type,
            display_name=info["name"] if info else self._selected_type,
            client_id=client_id,
            client_secret=client_secret,
        )

        # Run OAuth flow
        try:
            from aLCloud.database import get_provider
            pd = get_provider(pid)
            provider = create_provider(pd)
            result = provider.authenticate()

            if result.get("error"):
                self.connect_btn.configure(text="Подключить", state="normal")
                self._show_error(f"Ошибка: {result['error']}")
                return

            if result.get("access_token"):
                update_provider_tokens(
                    pid,
                    access_token=result["access_token"],
                    refresh_token=result.get("refresh_token", ""),
                    token_expiry=result.get("expires_in", ""),
                )
        except Exception as e:
            self.connect_btn.configure(text="Подключить", state="normal")
            self._show_error(f"Ошибка авторизации: {e}")
            return

        # Success
        self.grab_release()
        self.destroy()
        if self._on_done:
            self._on_done()

    def _show_error(self, msg: str):
        for w in self.details_frame.winfo_children():
            if hasattr(w, "_is_error"):
                w.destroy()

        label = ctk.CTkLabel(
            self.details_frame, text=f"\u26A0  {msg}",
            font=ctk.CTkFont(size=12), text_color="#FF6B6B",
            wraplength=400
        )
        label._is_error = True
        label.pack(anchor="w", pady=(8, 0))
