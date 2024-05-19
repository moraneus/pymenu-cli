from typing import Optional


class MenuItem:
    """Represents an item in a menu.

    Attributes:
        __m_title (str): The title of the menu item.
        __m_action (Optional[str]): The action associated with the menu item.
        __m_submenu (Optional['Menu']): A submenu associated with the menu item.
        __m_color (Optional[dict]): The color settings for the menu item title.
    """

    def __init__(
            self,
            i_title: str,
            i_action: Optional[str] = None,
            i_submenu: Optional['Menu'] = None,
            i_color: Optional[dict] = None):
        """
        Args:
            i_title (str): The title of the menu item.
            i_action (Optional[str]): The action associated with the menu item. Defaults to None.
            i_submenu (Optional['Menu']): A submenu associated with the menu item. Defaults to None.
            i_color (Optional[dict]): The color settings for the menu item title. Defaults to None.
        """
        self.__m_title = i_title
        self.__m_action = i_action
        self.__m_submenu = i_submenu
        self.__m_color = i_color

    @property
    def title(self) -> str:
        return self.__m_title

    @property
    def color(self) -> Optional[dict]:
        return self.__m_color

    @property
    def action(self) -> Optional[str]:
        return self.__m_action

    @property
    def submenu(self) -> Optional['Menu']:
        return self.__m_submenu


