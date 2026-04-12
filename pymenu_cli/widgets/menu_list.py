"""Menu list panel widget for displaying and navigating menu items."""

from textual.message import Message
from textual.reactive import reactive
from textual.containers import Vertical
from rich.text import Text


class MenuListPanel(Vertical, can_focus=True):
    """Displays the current menu's items as a navigable list."""

    class MenuItemSelected(Message):
        def __init__(self, item) -> None:
            super().__init__()
            self.item = item

    DEFAULT_CSS = """
    MenuListPanel {
        height: 1fr;
    }
    """

    cursor_index: reactive[int] = reactive(0)

    def __init__(self, menu) -> None:
        super().__init__(id="menu-panel")
        self.menu = menu
        self._filter_query = ""
        self._filtered_indices: list[int] = []
        self._update_filtered()

    @property
    def item_count(self) -> int:
        return len(self.menu.items)

    @property
    def visible_item_count(self) -> int:
        return len(self._filtered_indices)

    def _update_filtered(self) -> None:
        if not self._filter_query:
            self._filtered_indices = list(range(len(self.menu.items)))
        else:
            query = self._filter_query.lower()
            self._filtered_indices = [
                i for i, item in enumerate(self.menu.items)
                if query in item.title.lower()
            ]
        if self._filtered_indices:
            self.cursor_index = min(self.cursor_index, len(self._filtered_indices) - 1)
        else:
            self.cursor_index = 0

    def filter_items(self, query: str) -> None:
        self._filter_query = query
        self._update_filtered()
        self.refresh()

    def set_menu(self, menu) -> None:
        self.menu = menu
        self._filter_query = ""
        self.cursor_index = 0
        self._update_filtered()
        self.refresh()

    def render(self) -> Text:
        result = Text()
        for list_idx, item_idx in enumerate(self._filtered_indices):
            item = self.menu.items[item_idx]
            is_highlighted = list_idx == self.cursor_index
            if is_highlighted:
                prefix = "\u276f "
                style = "bold reverse"
            else:
                prefix = "  "
                style = ""
            result.append(f"{prefix}{item.title}", style=style)
            if item.submenu:
                result.append("  \u2192 submenu", style="dim" if not is_highlighted else style)
            elif item.action:
                result.append("  \u26a1 action", style="dim" if not is_highlighted else style)
            result.append("\n")
        return result

    def _get_selected_item(self):
        if not self._filtered_indices:
            return None
        idx = self._filtered_indices[self.cursor_index]
        return self.menu.items[idx]

    def key_down(self) -> None:
        if self._filtered_indices and self.cursor_index < len(self._filtered_indices) - 1:
            self.cursor_index += 1
            self.refresh()

    def key_up(self) -> None:
        if self.cursor_index > 0:
            self.cursor_index -= 1
            self.refresh()

    def key_j(self) -> None:
        self.key_down()

    def key_k(self) -> None:
        self.key_up()

    def key_enter(self) -> None:
        item = self._get_selected_item()
        if item:
            self.post_message(self.MenuItemSelected(item))
