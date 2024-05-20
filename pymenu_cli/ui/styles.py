"""
Module for defining text and background colors as well as text styles
using the colorama library.
"""

from enum import Enum
from colorama import Fore, Style, Back


class StrEnum(Enum):
    """
    Enum class that returns the value as a string.
    """

    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


class TextColors(StrEnum):
    """
    Enum for defining text colors using colorama's Fore class.
    """
    RED = Fore.RED
    LIGHT_RED = Fore.LIGHTRED_EX
    BLUE = Fore.BLUE
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    YELLOW = Fore.YELLOW
    LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    GREEN = Fore.GREEN
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    CYAN = Fore.CYAN
    LIGHT_CYAN = Fore.LIGHTCYAN_EX
    MAGENTA = Fore.MAGENTA
    LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    BLACK = Fore.BLACK
    LIGHT_BLACK = Fore.LIGHTBLACK_EX
    WHITE = Fore.WHITE
    LIGHT_WHITE = Fore.LIGHTWHITE_EX


class BackgroundColors(StrEnum):
    """
    Enum for defining background colors using colorama's Back class.
    """
    RED = Back.RED
    LIGHT_RED = Back.LIGHTRED_EX
    BLUE = Back.BLUE
    LIGHT_BLUE = Back.LIGHTBLUE_EX
    YELLOW = Back.YELLOW
    LIGHT_YELLOW = Back.LIGHTYELLOW_EX
    GREEN = Back.GREEN
    LIGHT_GREEN = Back.LIGHTGREEN_EX
    CYAN = Back.CYAN
    LIGHT_CYAN = Back.LIGHTCYAN_EX
    MAGENTA = Back.MAGENTA
    LIGHT_MAGENTA = Back.LIGHTMAGENTA_EX
    BLACK = Back.BLACK
    LIGHT_BLACK = Back.LIGHTBLACK_EX
    WHITE = Back.WHITE
    LIGHT_WHITE = Back.LIGHTWHITE_EX


class Styles(StrEnum):
    """
    Enum for defining text styles using colorama's Style class.
    """
    BRIGHT = Style.BRIGHT
    NORMAL = Style.NORMAL
    DIM = Style.DIM
    RESET_ALL = Style.RESET_ALL

# Example usage:
# print(f"{BackgroundColors.WHITE}{TextColors.BLACK}test_text{Styles.RESET_ALL}")
