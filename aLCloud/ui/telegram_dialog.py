"""Telegram auth dialog — phone + code flow."""

import customtkinter as ctk
from aLCloud.database import save_provider


class TelegramDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_done=None):
        super().__init__(parent)
        self._on_done = on_done
        self.title("Подключить Telegram")
        self.geometry("440x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build()

    def _build(self):
        pad = {"padx": 24}

        ctk.CTkLabel(self, text="\u2708\uFE0F  Telegram",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(**pad, pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Подключение через номер телефона.\nВведите данные от my.telegram.org",
            font=ctk.CTkFont(size=12), text_color="gray50", wraplength=380
        ).pack(**pad, pady=(0, 16))

        ctk.CTkLabel(self, text="API ID",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", **pad)
        self.api_id_entry = ctk.CTkEntry(
            self, placeholder_text="12345", width=380, height=36, corner_radius=8
        )
        self.api_id_entry.pack(**pad, pady=(0, 10))

        ctk.CTkLabel(self, text="API Hash",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", **pad)
        self.api_hash_entry = ctk.CTkEntry(
            self, placeholder_text="abc123def456...", width=380, height=36, corner_radius=8
        )
        self.api_hash_entry.pack(**pad, pady=(0, 10))

        ctk.CTkLabel(self, text="Номер телефона",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", **pad)
        self.phone_entry = ctk.CTkEntry(
            self, placeholder_text="+79001234567", width=380, height=36, corner_radius=8
        )
        self.phone_entry.pack(**pad, pady=(0, 16))

        self.connect_btn = ctk.CTkButton(
            self, text="Подключить", height=42, width=380,
            corner_radius=8, command=self._on_connect
        )
        self.connect_btn.pack(pady=(0, 24), padx=24)

        self.status_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11),
            text_color="gray50", wraplength=380
        )
        self.status_label.pack(**pad)

    def _on_connect(self):
        api_id = self.api_id_entry.get().strip()
        api_hash = self.api_hash_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not api_id or not api_hash or not phone:
            self.status_label.configure(text="\u26A0 Заполните все поля", text_color="#FF6B6B")
            return

        self.connect_btn.configure(text="Подключение...", state="disabled")
        self.status_label.configure(text="\u23F3 Отправка кода подтверждения...", text_color="gray50")
        self.update()

        # Save provider (demo mode — real Telegram requires gram.js)
        pid = save_provider(
            provider_type="telegram",
            display_name="Telegram",
            client_id=api_id,
            client_secret=api_hash,
            extra={"phone": phone, "api_id": api_id, "api_hash": api_hash},
        )

        self.status_label.configure(
            text="\u2705 Telegram подключён (демо-режим).\nДля полноценной работы нужен gram.js.",
            text_color="#4ECDC4"
        )
        self.connect_btn.configure(text="Готово", command=self._close)

    def _close(self):
        self.grab_release()
        self.destroy()
        if self._on_done:
            self._on_done()
