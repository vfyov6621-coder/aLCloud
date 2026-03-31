"""Theme manager — simple built-in theme switching + custom RGB."""

import customtkinter as ctk
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager as CTkTM
import json
import copy
from pathlib import Path

THEME_DIR = Path.home() / ".alcloud" / "themes"

PRESETS = {"light", "dark", "custom"}


def _rgb_hex(rgb: tuple) -> str:
    return f"#{max(0,min(255,rgb[0])):02x}{max(0,min(255,rgb[1])):02x}{max(0,min(255,rgb[2])):02x}"


def _lighter(rgb: tuple, a=15) -> tuple:
    return tuple(min(255, c + a) for c in rgb)


def _darker(rgb: tuple, a=15) -> tuple:
    return tuple(max(0, c - a) for c in rgb)


class ThemeManager:
    def __init__(self):
        THEME_DIR.mkdir(parents=True, exist_ok=True)
        self._current_mode = "dark"
        self._custom_colors: dict | None = None

    @property
    def current_mode(self) -> str:
        return self._current_mode

    def apply(self, mode: str, custom_colors: dict | None = None):
        self._current_mode = mode
        self._custom_colors = custom_colors

        if mode == "light":
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
        elif mode == "dark":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
        elif mode == "custom" and custom_colors:
            self._apply_custom(custom_colors)

        from aLCloud.database import save_setting
        save_setting("theme_mode", mode)
        if custom_colors:
            save_setting("theme_custom", json.dumps(
                {k: list(v) for k, v in custom_colors.items()}))

    def _apply_custom(self, colors: dict):
        is_dark = (colors["bg"][0]*299 + colors["bg"][1]*587 + colors["bg"][2]*114) / 1000 < 128
        ctk.set_appearance_mode("dark" if is_dark else "light")

        # Load built-in as base to keep all keys
        builtin = "dark-blue" if is_dark else "blue"
        ctk.set_default_color_theme(builtin)
        base = copy.deepcopy(CTkTM.theme)

        bg = colors["bg"]
        fg = colors["fg"]
        accent = colors["accent"]
        border = colors["border"]

        bp = [_rgb_hex(_lighter(bg, 10)), _rgb_hex(_darker(bg, 10))]
        fp = [_rgb_hex(_darker(fg, 30)), _rgb_hex(fg)]
        ap = [_rgb_hex(_lighter(accent, 20)), _rgb_hex(_darker(accent, 20))]
        brdp = [_rgb_hex(border), _rgb_hex(border)]

        for wk in base:
            if wk == "name":
                continue
            w = base[wk]
            if not isinstance(w, dict):
                continue
            for key in list(w.keys()):
                val = w[key]
                if not isinstance(val, (str, list)):
                    continue
                if key == "fg_color":
                    if isinstance(val, list):
                        w[key] = bp
                    elif val == "transparent":
                        pass
                elif key == "top_fg_color":
                    if isinstance(val, list):
                        w[key] = bp
                elif key == "bottom_fg_color":
                    if isinstance(val, list):
                        w[key] = [_rgb_hex(_lighter(bg, 15)), _rgb_hex(bg)]
                elif key == "text_color":
                    if isinstance(val, list):
                        w[key] = fp
                elif key == "border_color":
                    if isinstance(val, list):
                        w[key] = brdp
                elif key in ("hover_color", "button_hover_color"):
                    if isinstance(val, list):
                        w[key] = [_rgb_hex(_lighter(accent, 35)), _rgb_hex(_darker(accent, 5))]
                elif key == "button_color":
                    if isinstance(val, list):
                        w[key] = ap

        theme_path = THEME_DIR / "alcloud_custom.json"
        with open(theme_path, "w") as f:
            json.dump(base, f, indent=2)
        CTkTM.theme = base
        CTkTM._currently_loaded_theme = str(theme_path)

    def load_saved(self):
        from aLCloud.database import get_setting
        mode = get_setting("theme_mode", "dark")
        custom_json = get_setting("theme_custom", "")
        custom_colors = None
        if custom_json:
            try:
                raw = json.loads(custom_json)
                custom_colors = {k: tuple(v) for k, v in raw.items()}
            except (json.JSONDecodeError, TypeError):
                pass
        self.apply(mode, custom_colors)
