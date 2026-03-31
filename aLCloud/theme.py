"""Theme manager for CustomTkinter — Light, Dark, Custom RGB."""

import customtkinter as ctk
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager as CTkTM
import json
import copy
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

PRESETS = {"light": LIGHT_COLORS, "dark": DARK_COLORS}


def _rgb_hex(rgb: tuple) -> str:
    return f"#{max(0,min(255,rgb[0])):02x}{max(0,min(255,rgb[1])):02x}{max(0,min(255,rgb[2])):02x}"


def _lighter(rgb: tuple, a: int = 15) -> tuple:
    return tuple(min(255, c + a) for c in rgb)


def _darker(rgb: tuple, a: int = 15) -> tuple:
    return tuple(max(0, c - a) for c in rgb)


def _load_builtin_theme(name: str) -> dict:
    """Load a built-in CTk theme JSON as a base template."""
    ctk.set_default_color_theme(name)
    # After loading, the theme dict is in CTkTM.theme
    return copy.deepcopy(CTkTM.theme)


def _color_pair(light_val, dark_val) -> list[str]:
    """Return [light_mode_value, dark_mode_value]."""
    return [_rgb_hex(light_val), _rgb_hex(dark_val)]


def _recolor_theme(base: dict, colors: dict[str, tuple], is_dark_mode: bool) -> dict:
    """
    Override colors in a theme dict.
    Uses the base theme's keys (guaranteed correct), replaces color values.
    """
    bg = colors["bg"]
    fg = colors["fg"]
    accent = colors["accent"]
    border = colors["border"]

    # Helper: pick from (light_val, dark_val) pair based on mode
    def cp(light_v, dark_v):
        return dark_v if is_dark_mode else light_v

    def cp_pair(light_v, dark_v):
        return [_rgb_hex(light_v), _rgb_hex(dark_v)]

    theme = copy.deepcopy(base)

    for widget_key in theme:
        if widget_key == "name":
            continue
        w = theme[widget_key]
        if not isinstance(w, dict):
            continue

        bg_pair = cp_pair(_lighter(bg, 8), _darker(bg, 5))
        fg_pair = cp_pair(_darker(fg, 30), fg)
        accent_pair = cp_pair(_lighter(accent, 20), _darker(accent, 20))
        border_pair = cp_pair(border, border)

        # Override keys that contain "color" in their name
        for key in list(w.keys()):
            val = w[key]

            # Skip non-color values
            if not isinstance(val, (str, list)):
                continue

            if key == "fg_color":
                if isinstance(val, list):
                    w[key] = bg_pair
                elif val == "transparent":
                    w[key] = "transparent"
                else:
                    w[key] = _rgb_hex(bg)
            elif key == "top_fg_color":
                if isinstance(val, list):
                    w[key] = bg_pair
                else:
                    w[key] = _rgb_hex(bg)
            elif key == "bottom_fg_color":
                if isinstance(val, list):
                    w[key] = cp_pair(_lighter(bg, 15), bg)
                else:
                    w[key] = _rgb_hex(bg)
            elif key == "text_color":
                if isinstance(val, list):
                    w[key] = fg_pair
                else:
                    w[key] = _rgb_hex(fg)
            elif key == "border_color":
                if isinstance(val, list):
                    w[key] = border_pair
                else:
                    w[key] = _rgb_hex(border)
            elif key == "button_color":
                if isinstance(val, list):
                    w[key] = accent_pair
            elif key == "hover_color":
                if isinstance(val, list):
                    w[key] = cp_pair(_lighter(accent, 35), _darker(accent, 5))
            elif key == "button_hover_color":
                if isinstance(val, list):
                    w[key] = cp_pair(_lighter(accent, 35), _darker(accent, 5))
            elif key == "selected_color":
                if isinstance(val, list):
                    w[key] = cp_pair(accent, accent)
            elif key == "selected_hover_color":
                if isinstance(val, list):
                    w[key] = cp_pair(_lighter(accent, 20), _lighter(accent, 20))
            elif key == "progress_color":
                if isinstance(val, list):
                    w[key] = cp_pair(accent, accent)
            elif key == "checkmark_color":
                if isinstance(val, list):
                    w[key] = cp_pair(bg, bg)
            elif key == "button_fg_color":
                if isinstance(val, list):
                    w[key] = cp_pair(accent, accent)
            elif key == "placeholder_text_color":
                if isinstance(val, list):
                    w[key] = cp_pair(_lighter(fg, 80), _darker(fg, 80))
            elif key == "menu_fg_color":
                w[key] = _rgb_hex(_lighter(bg, 5))
            elif key == "menu_hover_color":
                w[key] = _rgb_hex(accent)

    return theme


class ThemeManager:
    """Manages app themes — applies CustomTkinter themes."""

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

        is_dark = theme_name == "dark" or (
            theme_name == "custom" and
            (colors["bg"][0] * 299 + colors["bg"][1] * 587 + colors["bg"][2] * 114) / 1000 < 128
        )

        # 1. Load a built-in theme as base (has all required keys for this CTk version)
        builtin = "dark-blue" if is_dark else "blue"
        base = _load_builtin_theme(builtin)

        # 2. Recolor the base theme with our colors
        theme_json = _recolor_theme(base, colors, is_dark)
        theme_json["name"] = f"alcloud_{theme_name}"

        # 3. Write to file
        theme_path = THEME_DIR / f"alcloud_{theme_name}.json"
        with open(theme_path, "w", encoding="utf-8") as f:
            json.dump(theme_json, f, indent=2)

        # 4. Set appearance mode
        ctk.set_appearance_mode("dark" if is_dark else "light")

        # 5. Apply theme
        CTkTM.theme = theme_json
        CTkTM._currently_loaded_theme = str(theme_path)

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
