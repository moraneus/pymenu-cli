"""
This module defines the Menu class, which represents a text-based menu system.
"""

from typing import Optional, List, Dict
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

    def display(self, classic: bool = False, theme: str = "dark") -> None:
        """Display the menu.

        Args:
            classic: If True, use the classic input() display mode.
            theme: Theme name ('dark' or 'light'). Only used in TUI mode.
        """
        if classic:
            from pymenu_cli.classic import classic_display
            classic_display(self)
            return
        from pymenu_cli.app import MenuApp
        app = MenuApp(self, theme=theme)
        app.run()

    def print_banner(self) -> None:
        """Print the banner. Delegates to classic module."""
        from pymenu_cli.classic import _print_banner
        if self.__m_banner:
            _print_banner(self.__m_banner)

    @staticmethod
    def get_color_string(color) -> str:
        """Get the color string for the given color settings."""
        from pymenu_cli.classic import _get_color_string
        return _get_color_string(color)
