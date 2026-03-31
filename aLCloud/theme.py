"""Theme manager for CustomTkinter — Light, Dark, Custom RGB."""

import customtkinter as ctk
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager as CTkThemeManager
import json
from pathlib import Path

THEME_DIR = Path.home() / ".alcloud" / "themes"

# ── Presets ────────────────────────────────────────────────

LIGHT_COLORS = {
    "bg": (255, 255, 255),
    "fg": (0, 0, 0),
    "accent": (45, 45, 45),
    "border": (0, 0, 0),
}

DARK_COLORS = {
    "bg": (30, 30, 30),
    "fg": (240, 240, 240),
    "accent": (78, 205, 196),
    "border": (80, 80, 80),
}

PRESETS = {
    "light": LIGHT_COLORS,
    "dark": DARK_COLORS,
}


def _rgb_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def _lighter(rgb: tuple, amount: int = 15) -> tuple:
    return tuple(min(255, c + amount) for c in rgb)


def _darker(rgb: tuple, amount: int = 15) -> tuple:
    return tuple(max(0, c - amount) for c in rgb)


def _build_ctk_json(name: str, colors: dict[str, tuple]) -> dict:
    bg = colors["bg"]
    fg = colors["fg"]
    accent = colors["accent"]
    border = colors["border"]

    return {
        "name": name,
        "CTk": {
            "fg_color": [_rgb_hex(_lighter(bg, 10)), _rgb_hex(_darker(bg, 10))],
            "menu_fg_color": _rgb_hex(_lighter(bg, 5)),
            "menu_hover_color": _rgb_hex(accent),
        },
        "CTkToplevel": {
            "fg_color": [_rgb_hex(_lighter(bg, 10)), _rgb_hex(_darker(bg, 10))],
        },
        "CTkFrame": {
            "top_fg_color": [
                _rgb_hex(_lighter(bg, 8)),
                _rgb_hex(_darker(bg, 5)),
            ],
            "bottom_fg_color": [
                _rgb_hex(_lighter(bg, 15)),
                _rgb_hex(bg),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
        },
        "CTkLabel": {
            "fg_color": "transparent",
            "text_color": [_rgb_hex(_darker(fg, 30)), _rgb_hex(fg)],
        },
        "CTkButton": {
            "fg_color": [
                _rgb_hex(_lighter(accent, 20)),
                _rgb_hex(_darker(accent, 20)),
            ],
            "hover_color": [
                _rgb_hex(_lighter(accent, 35)),
                _rgb_hex(_darker(accent, 5)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "text_color": [
                _rgb_hex(bg),
                _rgb_hex(bg),
            ],
        },
        "CTkEntry": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
            "placeholder_text_color": [
                _rgb_hex(_lighter(fg, 80)),
                _rgb_hex(_darker(fg, 80)),
            ],
        },
        "CTkTextbox": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
        },
        "CTkScrollableFrame": {
            "fg_color": "transparent",
        },
        "CTkSegmentedButton": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "selected_color": [
                _rgb_hex(accent),
                _rgb_hex(accent),
            ],
            "selected_hover_color": [
                _rgb_hex(_lighter(accent, 20)),
                _rgb_hex(_lighter(accent, 20)),
            ],
            "unselected_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "unselected_hover_color": [
                _rgb_hex(_lighter(bg, 30)),
                _rgb_hex(_darker(bg, 5)),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
            "text_color_disabled": [_rgb_hex(_lighter(fg, 60)), _rgb_hex(_darker(fg, 60))],
        },
        "CTkTabview": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 8)),
                _rgb_hex(_darker(bg, 5)),
            ],
            "top_fg_color": [
                _rgb_hex(_lighter(bg, 15)),
                _rgb_hex(_darker(bg, 12)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "button_color": [
                _rgb_hex(_lighter(bg, 10)),
                _rgb_hex(_darker(bg, 8)),
            ],
            "button_hover_color": [
                _rgb_hex(_lighter(bg, 25)),
                _rgb_hex(_darker(bg, 0)),
            ],
        },
        "CTkSlider": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "progress_color": [
                _rgb_hex(accent),
                _rgb_hex(accent),
            ],
            "button_color": [
                _rgb_hex(accent),
                _rgb_hex(accent),
            ],
            "button_hover_color": [
                _rgb_hex(_lighter(accent, 25)),
                _rgb_hex(_lighter(accent, 25)),
            ],
        },
        "CTkProgressBar": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "progress_color": [
                _rgb_hex(accent),
                _rgb_hex(accent),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
        },
        "CTkSwitch": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "progress_color": [
                _rgb_hex(accent),
                _rgb_hex(accent),
            ],
            "button_color": [
                _rgb_hex(bg),
                _rgb_hex(bg),
            ],
            "button_hover_color": [
                _rgb_hex(_lighter(bg, 30)),
                _rgb_hex(_lighter(bg, 30)),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
        },
        "CTkOptionMenu": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "button_color": [
                _rgb_hex(_lighter(accent, 20)),
                _rgb_hex(_darker(accent, 20)),
            ],
            "button_hover_color": [
                _rgb_hex(_lighter(accent, 35)),
                _rgb_hex(_darker(accent, 5)),
            ],
        },
        "CTkComboBox": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "button_color": [
                _rgb_hex(_lighter(accent, 20)),
                _rgb_hex(_darker(accent, 20)),
            ],
            "button_hover_color": [
                _rgb_hex(_lighter(accent, 35)),
                _rgb_hex(_darker(accent, 5)),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
        },
        "CTkCheckbox": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "hover_color": [
                _rgb_hex(_lighter(accent, 15)),
                _rgb_hex(_lighter(accent, 15)),
            ],
            "checkmark_color": [_rgb_hex(bg), _rgb_hex(bg)],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
        },
        "CTkRadioButton": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 20)),
                _rgb_hex(_darker(bg, 15)),
            ],
            "border_color": [
                _rgb_hex(border),
                _rgb_hex(border),
            ],
            "hover_color": [
                _rgb_hex(_lighter(accent, 15)),
                _rgb_hex(_lighter(accent, 15)),
            ],
            "text_color": [_rgb_hex(fg), _rgb_hex(fg)],
        },
        "CTkDialog": {
            "fg_color": [
                _rgb_hex(_lighter(bg, 10)),
                _rgb_hex(_darker(bg, 10)),
            ],
        },
    }


class ThemeManager:
    """Manages app themes — applies CustomTkinter JSON themes."""

    def __init__(self):
        THEME_DIR.mkdir(parents=True, exist_ok=True)
        self._current_mode: str = "dark"
        self._custom_colors: dict[str, tuple] | None = None

    @property
    def current_mode(self) -> str:
        return self._current_mode

    @property
    def current_colors(self) -> dict[str, tuple]:
        if self._current_mode == "custom" and self._custom_colors:
            return self._custom_colors
        return PRESETS.get(self._current_mode, DARK_COLORS)

    def apply(self, theme_name: str, custom_colors: dict | None = None):
        """Apply a theme by name."""
        self._current_mode = theme_name
        self._custom_colors = custom_colors

        if theme_name == "custom" and custom_colors:
            colors = custom_colors
        else:
            colors = PRESETS.get(theme_name, DARK_COLORS)

        theme_json = _build_ctk_json(f"alcloud_{theme_name}", colors)

        # Write theme JSON file
        theme_path = THEME_DIR / f"alcloud_{theme_name}.json"
        with open(theme_path, "w", encoding="utf-8") as f:
            json.dump(theme_json, f, indent=2)

        # Set appearance mode
        if theme_name == "dark":
            ctk.set_appearance_mode("dark")
        elif theme_name == "light":
            ctk.set_appearance_mode("light")
        else:
            # Custom: determine light or dark based on bg brightness
            r, g, b = colors["bg"]
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            ctk.set_appearance_mode("light" if brightness > 128 else "dark")

        # Apply theme JSON
        CTkThemeManager.theme = theme_json
        CTkThemeManager._currently_loaded_theme = str(theme_path)

        # Save preference
        from aLCloud.database import save_setting
        save_setting("theme_mode", theme_name)
        if custom_colors:
            save_setting("theme_custom", json.dumps(
                {k: list(v) for k, v in custom_colors.items()}
            ))

    def load_saved(self):
        """Load and apply the saved theme."""
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
