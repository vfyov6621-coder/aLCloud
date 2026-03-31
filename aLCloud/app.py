"""Application controller — initializes DB, theme, and window."""

import customtkinter as ctk
from aLCloud.database import init_db
from aLCloud.theme import ThemeManager
from aLCloud.ui.main_window import MainWindow


class App:
    def __init__(self):
        init_db()

        self._theme = ThemeManager()
        self._theme.load_saved()

        self.root = MainWindow()

    def run(self):
        self.root.mainloop()
