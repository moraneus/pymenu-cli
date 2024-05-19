import os
from typing import Optional, List

import art

from pymenu_cli.UI.styles import Styles, TextColors, BackgroundColors
from pymenu_cli.models.menu_item import MenuItem


class Menu:
    """Represents a menu.

    Attributes:
        __m_title (str): The title of the menu.
        __m_items (List[MenuItem]): A list of items in the menu.
        __m_actions (Optional[object]): An object containing callable actions.
        __m_color (Optional[dict]): The color settings for the menu title.
        __m_banner (Optional[dict]): The banner for the menu.
    """

    def __init__(
            self,
            i_title: str,
            i_items: Optional[List[MenuItem]] = None,
            i_actions: Optional[object] = None,
            i_color: Optional[dict] = None,
            i_banner: Optional[dict] = None):
        """
        Args:
            i_title (str): The title of the menu.
            i_items (Optional[List[MenuItem]]): A list of items in the menu. Defaults to None.
            i_actions (Optional[object]): An object containing callable actions. Defaults to None.
            i_color (Optional[dict]): The color settings for the menu title. Defaults to None.
            i_banner (Optional[dict]): The banner for the menu. Defaults to None.
        """
        self.__m_title = i_title
        self.__m_items = i_items or []
        self.__m_actions = i_actions
        self.__m_color = i_color
        self.__m_banner = i_banner

    def add_item(self, i_item: MenuItem) -> None:
        """Adds an item to the menu.

        Args:
            i_item (MenuItem): The item to add.
        """
        self.__m_items.append(i_item)

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
            elif choice == 'X':
                exit()
            else:
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
        banner_text = self.__m_banner.get('title', '')
        banner_font = self.__m_banner.get('font', 'standard')
        banner = art.text2art(banner_text, font=banner_font, chr_ignore=True)
        print(banner)

    @staticmethod
    def get_color_string(i_color: Optional[dict]) -> str:
        """Gets the color string based on the provided color settings.

        Args:
            i_color (Optional[dict]): The color settings.

        Returns:
            str: The color string.
        """
        if i_color:
            text_color = getattr(TextColors, i_color.get('text', 'WHITE').upper())
            background_color = getattr(BackgroundColors, i_color.get('background', 'BLACK').upper())
            return f"{text_color}{background_color}"
        return ""
