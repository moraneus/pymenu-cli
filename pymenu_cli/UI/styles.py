from enum import Enum
from colorama import Fore, Style, Back


# Used for returning the value from an enum as a string
class StrEnum(Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


class TextColors(StrEnum):
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
    BRIGHT = Style.BRIGHT
    NORMAL = Style.NORMAL
    DIM = Style.DIM
    RESET_ALL = Style.RESET_ALL

# print(f"{BackgroundColors.WHITE}{TextColors.BLACK}sdfsdfsdfsdf{Styles.RESET_ALL}")
