"""Connect provider panel — inside main window."""

import customtkinter as ctk
from aLCloud.database import save_provider, update_provider_tokens
from aLCloud.providers import PROVIDER_INFO, create_provider


class ConnectPanel(ctk.CTkFrame):
    def __init__(self, parent, on_done=None):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._on_done = on_done
        self._selected_type = None

        # Title (static)
        self.title_label = ctk.CTkLabel(self, text="Подключить облако",
                                        font=ctk.CTkFont(size=20, weight="bold"), anchor="w")
        self.title_label.pack(anchor="w", padx=24, pady=(24, 2))

        ctk.CTkLabel(self, text="Выберите провайдер и введите данные",
                     font=ctk.CTkFont(size=12), text_color="gray50").pack(anchor="w", padx=24)

        # Provider selector
        names = [p["name"] for p in PROVIDER_INFO]
        self.provider_menu = ctk.CTkOptionMenu(
            self, values=["-- Выберите --"] + names,
            command=self._on_select, width=500, corner_radius=8
        )
        self.provider_menu.pack(anchor="w", padx=24, pady=(16, 12))

        # Dynamic details area
        self.details = ctk.CTkFrame(self, fg_color="transparent")
        self.details.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12),
                                        text_color="#FF6B6B", anchor="w")
        self.error_label.pack(anchor="w", padx=24)

        # Connect button
        self.connect_btn = ctk.CTkButton(
            self, text="Подключить", height=40, width=200,
            corner_radius=8, command=self._on_connect, state="disabled"
        )
        self.connect_btn.pack(pady=(8, 24), padx=24, anchor="e")

    def reset(self):
        """Clear dynamic content, ready for reuse."""
        self.provider_menu.set("-- Выберите --")
        self._clear_details()
        self.error_label.configure(text="")
        self.connect_btn.configure(state="disabled", text="Подключить")
        self._selected_type = None

    def _clear_details(self):
        for w in self.details.winfo_children():
            w.destroy()

    def _on_select(self, value):
        self._clear_details()
        self.error_label.configure(text="")

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
        self.connect_btn.configure(state="normal")

        ctk.CTkLabel(self.details,
                     text=f"{info['name']}  |  Макс. файл: {info['max_file']}",
                     font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
                     ).pack(fill="x", pady=(0, 12))

        if info["type"] == "telegram":
            ctk.CTkLabel(self.details,
                         text="Telegram: подключение через номер телефона.\nДанные от my.telegram.org",
                         font=ctk.CTkFont(size=12), text_color="gray50",
                         wraplength=500, anchor="w").pack(fill="x", pady=(0, 10))

            self.telegram_fields = {}
            for label, key, ph in [("API ID", "api_id", "12345"),
                                    ("API Hash", "api_hash", "abc123..."),
                                    ("Номер телефона", "phone", "+79001234567")]:
                ctk.CTkLabel(self.details, text=label, font=ctk.CTkFont(size=12, weight="bold"),
                             anchor="w").pack(fill="x", pady=(6, 2))
                e = ctk.CTkEntry(self.details, placeholder_text=ph, height=36, corner_radius=8)
                e.pack(fill="x", pady=(0, 6))
                self.telegram_fields[key] = e
        else:
            self.oauth_fields = {}

            ctk.CTkLabel(self.details, text="Client ID",
                         font=ctk.CTkFont(size=12, weight="bold"), anchor="w"
                         ).pack(fill="x", pady=(6, 2))
            e1 = ctk.CTkEntry(self.details, placeholder_text="Ваш Client ID", height=36, corner_radius=8)
            e1.pack(fill="x", pady=(0, 6))
            self.oauth_fields["client_id"] = e1

            if info["needs_secret"]:
                ctk.CTkLabel(self.details, text="Client Secret",
                             font=ctk.CTkFont(size=12, weight="bold"), anchor="w"
                             ).pack(fill="x", pady=(6, 2))
                e2 = ctk.CTkEntry(self.details, placeholder_text="Ваш Client Secret",
                                   height=36, corner_radius=8, show="*")
                e2.pack(fill="x", pady=(0, 6))
                self.oauth_fields["client_secret"] = e2

    def _on_connect(self):
        if not self._selected_type:
            return

        # Telegram flow
        if self._selected_type == "telegram":
            api_id = self.telegram_fields["api_id"].get().strip()
            api_hash = self.telegram_fields["api_hash"].get().strip()
            phone = self.telegram_fields["phone"].get().strip()
            if not api_id or not api_hash or not phone:
                self.error_label.configure(text="Заполните все поля")
                return
            save_provider("telegram", "Telegram", client_id=api_id, client_secret=api_hash,
                          extra={"phone": phone})
            if self._on_done:
                self._on_done()
            return

        # OAuth flow
        client_id = self.oauth_fields["client_id"].get().strip()
        client_secret = self.oauth_fields["client_secret"].get().strip() if "client_secret" in self.oauth_fields else ""

        if not client_id:
            self.error_label.configure(text="Введите Client ID")
            return

        self.connect_btn.configure(text="Авторизация...", state="disabled")
        self.error_label.configure(text="")
        self.update_idletasks()

        info = next((p for p in PROVIDER_INFO if p["type"] == self._selected_type), None)
        pid = save_provider(
            provider_type=self._selected_type,
            display_name=info["name"] if info else self._selected_type,
            client_id=client_id, client_secret=client_secret,
        )

        try:
            from aLCloud.database import get_provider
            pd = get_provider(pid)
            provider = create_provider(pd)
            result = provider.authenticate()

            if result.get("error"):
                self.connect_btn.configure(text="Подключить", state="normal")
                self.error_label.configure(text=f"Ошибка: {result['error']}")
                return

            if result.get("access_token"):
                update_provider_tokens(pid, access_token=result["access_token"],
                                       refresh_token=result.get("refresh_token", ""),
                                       token_expiry=result.get("expires_in", ""))
        except Exception as e:
            self.connect_btn.configure(text="Подключить", state="normal")
            self.error_label.configure(text=f"Ошибка: {e}")
            return

        if self._on_done:
            self._on_done()
