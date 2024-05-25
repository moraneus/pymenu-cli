"""
This module defines the Menu class, which represents a text-based menu system.
"""

import os
import sys
from typing import Optional, List, Dict

import art

from pymenu_cli.ui.styles import Styles, TextColors, BackgroundColors
from pymenu_cli.models.menu_item import MenuItem


class Menu:
    """Represents a menu.

    Attributes:
        __m_title (str): The title of the menu.
        __m_items (List[MenuItem]): A list of items in the menu.
        __m_actions (Optional[object]): An object containing callable actions.
        __m_color (Optional[Dict]): The color settings for the menu title.
        __m_banner (Optional[Dict]): The banner for the menu.
    """

    def __init__(self, i_title: str, i_config: Optional[Dict] = None):
        """
        Initialize the Menu instance.

        Args:
            i_title (str): The title of the menu.
            i_config (Optional[Dict]): A dictionary containing optional settings for items,
                                     actions, color, and banner.
        """
        i_config = i_config or {}
        self.__m_title = i_title
        self.__m_items = i_config.get('items', [])
        self.__m_actions = i_config.get('actions')
        self.__m_color = i_config.get('color')
        self.__m_banner = i_config.get('banner')

    @property
    def title(self) -> str:
        """
        Gets the title of the menu item.

        Returns:
            str: The title of the menu item.
        """
        return self.__m_title

    @property
    def color(self) -> Optional[Dict]:
        """
        Gets the color settings of the menu item.

        Returns:
            Optional[Dict]: The color settings of the menu item.
        """
        return self.__m_color

    @property
    def items(self) -> List[MenuItem]:
        """
        Gets the items in the menu.

        Returns:
            List[MenuItem]: A list of items in the menu.
        """
        return self.__m_items

    @property
    def actions(self) -> Optional[object]:
        """
        Gets the actions associated with the menu.

        Returns:
            Optional[object]: An object containing callable actions.
        """
        return self.__m_actions

    @property
    def banner(self) -> Optional[Dict]:
        """
        Gets the banner for the menu.

        Returns:
            Optional[Dict]: The banner for the menu.
        """
        return self.__m_banner

    def add_item(self, item: MenuItem) -> None:
        """Adds an item to the menu.

        Args:
            item (MenuItem): The item to add.
        """
        self.__m_items.append(item)

    def display(self) -> None:
        """Displays the menu and handles user input."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            if self.__m_banner:
                self.print_banner()

            title_color = Menu.get_color_string(self.__m_color)
            print(f"\n{title_color}{self.__m_title}{Styles.RESET_ALL}\n")

            for i, item in enumerate(self.__m_items, start=1):
                item_color = self.get_color_string(item.color)
                print(f"{i}. {item_color}{item.title}{Styles.RESET_ALL}")

            print("\nB. Back")
            print("X. Exit")

            choice = input("\nEnter your choice: ").upper()

            if choice == 'B':
                return
            if choice == 'X':
                sys.exit()
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.__m_items):
                    selected_item = self.__m_items[index]
                    if selected_item.submenu:
                        selected_item.submenu.display()
                    elif selected_item.action:
                        getattr(self.__m_actions, selected_item.action)()
                else:
                    raise ValueError
            except (ValueError, IndexError):
                input("\nInvalid choice. Press Enter to try again.")

    def print_banner(self) -> None:
        """Prints the banner using the art library."""
        banner_text = self.__m_banner.get('title', '')
        banner_font = self.__m_banner.get('font', 'standard')
        banner = art.text2art(banner_text, font=banner_font, chr_ignore=True)
        print(banner)

    @staticmethod
    def get_color_string(color: Optional[Dict]) -> str:
        """Gets the color string based on the provided color settings.

        Args:
            color (Optional[Dict]): The color settings.

        Returns:
            str: The color string.
        """
        if color:
            text_color = getattr(TextColors, color.get('text', 'WHITE').upper())
            background_color = getattr(BackgroundColors, color.get('background', 'BLACK').upper())
            return f"{text_color}{background_color}"
        return ""
