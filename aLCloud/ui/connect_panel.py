"""Connect provider panel — shown inside main window, not a new window."""

import customtkinter as ctk
from aLCloud.database import save_provider, update_provider_tokens
from aLCloud.providers import PROVIDER_INFO, create_provider


class ConnectPanel(ctk.CTkFrame):
    def __init__(self, parent, on_done=None):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self._on_done = on_done
        self._selected_type: str | None = None
        self._build()

    def reset(self):
        """Reset state when panel is reopened."""
        for w in self.winfo_children():
            w.destroy()
        self._selected_type = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Подключить облако",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(self, text="Выберите провайдер и введите данные",
                     font=ctk.CTkFont(size=13), text_color="gray50").pack(anchor="w", padx=24)

        names = [p["name"] for p in PROVIDER_INFO]
        self.provider_menu = ctk.CTkOptionMenu(
            self, values=["— Выберите —"] + names,
            command=self._on_provider_selected, width=500, corner_radius=8
        )
        self.provider_menu.pack(anchor="w", padx=24, pady=(20, 12))

        self.details_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.details_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        self.bottom_bar = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.bottom_bar.pack(fill="x", side="bottom", padx=24, pady=(0, 16))
        self.bottom_bar.pack_propagate(False)

        self.error_label = ctk.CTkLabel(self.bottom_bar, text="", font=ctk.CTkFont(size=12),
                                        text_color="#FF6B6B", anchor="w")
        self.error_label.pack(side="bottom", fill="x")

        self.connect_btn = ctk.CTkButton(
            self.bottom_bar, text="Подключить", height=40, width=200,
            corner_radius=8, command=self._on_connect, state="disabled"
        )
        self.connect_btn.pack(side="right")

    def _on_provider_selected(self, value: str):
        for w in self.details_frame.winfo_children():
            w.destroy()
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

        ctk.CTkLabel(
            self.details_frame,
            text=f"{info['name']}  —  Макс. размер файла: {info['max_file']}",
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
        ).pack(fill="x", pady=(0, 12))

        if info["type"] == "telegram":
            ctk.CTkLabel(
                self.details_frame,
                text="Telegram подключается через номер телефона.\nВведите данные от my.telegram.org.",
                font=ctk.CTkFont(size=12), text_color="gray50", wraplength=500, anchor="w"
            ).pack(fill="x", pady=(0, 8))

            ctk.CTkLabel(self.details_frame, text="API ID", font=ctk.CTkFont(size=12, weight="bold"),
                         anchor="w").pack(fill="x", pady=(8, 2))
            self.api_id_entry = ctk.CTkEntry(self.details_frame, placeholder_text="12345",
                                              width=500, height=38, corner_radius=8)
            self.api_id_entry.pack(fill="x", pady=(0, 8))

            ctk.CTkLabel(self.details_frame, text="API Hash", font=ctk.CTkFont(size=12, weight="bold"),
                         anchor="w").pack(fill="x", pady=(4, 2))
            self.api_hash_entry = ctk.CTkEntry(self.details_frame, placeholder_text="abc123...",
                                                width=500, height=38, corner_radius=8)
            self.api_hash_entry.pack(fill="x", pady=(0, 8))

            ctk.CTkLabel(self.details_frame, text="Номер телефона", font=ctk.CTkFont(size=12, weight="bold"),
                         anchor="w").pack(fill="x", pady=(4, 2))
            self.phone_entry = ctk.CTkEntry(self.details_frame, placeholder_text="+79001234567",
                                             width=500, height=38, corner_radius=8)
            self.phone_entry.pack(fill="x", pady=(0, 8))
        else:
            ctk.CTkLabel(self.details_frame, text="Client ID",
                         font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x", pady=(4, 2))
            self.client_id_entry = ctk.CTkEntry(
                self.details_frame, placeholder_text="Ваш Client ID",
                width=500, height=38, corner_radius=8
            )
            self.client_id_entry.pack(fill="x", pady=(0, 8))

            if info["needs_secret"]:
                ctk.CTkLabel(self.details_frame, text="Client Secret",
                             font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x", pady=(4, 2))
                self.client_secret_entry = ctk.CTkEntry(
                    self.details_frame, placeholder_text="Ваш Client Secret",
                    width=500, height=38, corner_radius=8, show="*"
                )
                self.client_secret_entry.pack(fill="x", pady=(0, 8))

    def _on_connect(self):
        if not self._selected_type:
            return

        if self._selected_type == "telegram":
            api_id = self.api_id_entry.get().strip()
            api_hash = self.api_hash_entry.get().strip()
            phone = self.phone_entry.get().strip()
            if not api_id or not api_hash or not phone:
                self.error_label.configure(text="Заполните все поля")
                return
            save_provider("telegram", "Telegram", client_id=api_id, client_secret=api_hash,
                          extra={"phone": phone})
            if self._on_done:
                self._on_done()
            return

        client_id = self.client_id_entry.get().strip() if hasattr(self, "client_id_entry") else ""
        client_secret = self.client_secret_entry.get().strip() if hasattr(self, "client_secret_entry") else ""

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
