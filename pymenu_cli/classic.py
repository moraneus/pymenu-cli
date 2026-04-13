"""Classic input()-based menu display mode.

This module preserves the original pymenu-cli v1.x display behavior.
Activated via the --classic CLI flag or display(classic=True).
"""

import os
import sys
from typing import Optional

from pymenu_cli.ui.styles import BackgroundColors, Styles, TextColors


def _clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def classic_display(menu) -> None:
    """Display a menu using the classic input() loop.

    Args:
        menu: A Menu instance to display.
    """
    while True:
        _clear_screen()

        if menu.banner:
            _print_banner(menu.banner)

        title_color = _get_color_string(menu.color)
        print(f"\n{title_color}{menu.title}{Styles.RESET_ALL}\n")

        for i, item in enumerate(menu.items, start=1):
            item_color = _get_color_string(item.color)
            print(f"{i}. {item_color}{item.title}{Styles.RESET_ALL}")

        print("\nB. Back")
        print("X. Exit")

        choice = input("\nEnter your choice: ").upper()

        if choice == "B":
            return
        if choice == "X":
            sys.exit()
        try:
            index = int(choice) - 1
            if 0 <= index < len(menu.items):
                selected_item = menu.items[index]
                if selected_item.submenu:
                    classic_display(selected_item.submenu)
                elif selected_item.action:
                    getattr(menu.actions, selected_item.action)()
            else:
                raise ValueError
        except (ValueError, IndexError):
            print("\nInvalid choice. Please try again.")


def _print_banner(banner: dict) -> None:
    """Print an ASCII art banner using the art library (v1 compat)."""
    try:
        import art

        banner_text = banner.get("title", "")
        banner_font = banner.get("font", "standard")
        result = art.text2art(banner_text, font=banner_font, chr_ignore=True)
        print(result)
    except ImportError:
        print(banner.get("title", ""))


def _get_color_string(color: Optional[dict]) -> str:
    """Get the ANSI color string for classic mode display."""
    if color:
        text_color = getattr(TextColors, color.get("text", "WHITE").upper())
        background_color = getattr(BackgroundColors, color.get("background", "BLACK").upper())
        return f"{text_color}{background_color}"
    return ""
