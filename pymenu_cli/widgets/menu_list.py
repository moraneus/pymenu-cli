"""Menu list panel widget for displaying and navigating menu items."""

from __future__ import annotations

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive


class SearchResult:
    """A search result entry from the global menu index."""

    __slots__ = ("item", "path", "menu")

    def __init__(self, item, path: str, menu) -> None:
        self.item = item
        self.path = path
        self.menu = menu


class MenuListPanel(Vertical, can_focus=True):
    """Displays the current menu's items as a navigable list.

    Supports two modes:
    - Normal: shows items from the current menu
    - Search: shows global search results from all menus
    """

    class MenuItemSelected(Message):
        def __init__(self, item, menu=None) -> None:
            super().__init__()
            self.item = item
            self.menu = menu

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
        self._search_results: list[SearchResult] | None = None
        self._update_filtered()

    @property
    def item_count(self) -> int:
        return len(self.menu.items)

    @property
    def visible_item_count(self) -> int:
        if self._search_results is not None:
            return len(self._search_results)
        return len(self._filtered_indices)

    def _update_filtered(self) -> None:
        if not self._filter_query:
            self._filtered_indices = list(range(len(self.menu.items)))
        else:
            query = self._filter_query.lower()
            self._filtered_indices = [
                i for i, item in enumerate(self.menu.items) if query in item.title.lower()
            ]
        if self._filtered_indices:
            self.cursor_index = min(self.cursor_index, len(self._filtered_indices) - 1)
        else:
            self.cursor_index = 0

    def filter_items(self, query: str) -> None:
        """Filter current menu items (local filter, no search results)."""
        self._filter_query = query
        self._search_results = None
        self._update_filtered()
        self.refresh()

    def set_search_results(self, results: list[SearchResult]) -> None:
        """Switch to search results mode with global results."""
        self._search_results = results
        self.cursor_index = 0
        self.refresh()

    def clear_search(self) -> None:
        """Exit search mode and show current menu items."""
        self._search_results = None
        self._filter_query = ""
        self._update_filtered()
        self.refresh()

    def set_menu(self, menu) -> None:
        self.menu = menu
        self._filter_query = ""
        self._search_results = None
        self.cursor_index = 0
        self._update_filtered()
        self.refresh()

    def render(self) -> Text:
        if self._search_results is not None:
            return self._render_search_results()
        return self._render_menu_items()

    def _render_menu_items(self) -> Text:
        result = Text()
        for list_idx, item_idx in enumerate(self._filtered_indices):
            item = self.menu.items[item_idx]
            is_highlighted = list_idx == self.cursor_index
            if is_highlighted:
                prefix = "❯ "
                style = "bold reverse"
            else:
                prefix = "  "
                style = ""
            result.append(f"{prefix}{item.title}", style=style)
            if item.submenu:
                result.append("  → submenu", style="dim" if not is_highlighted else style)
            elif item.action:
                result.append("  ⚡ action", style="dim" if not is_highlighted else style)
            result.append("\n")
        return result

    def _render_search_results(self) -> Text:
        result = Text()
        if not self._search_results:
            result.append("  No results found\n", style="dim")
            return result
        for idx, sr in enumerate(self._search_results):
            is_highlighted = idx == self.cursor_index
            if is_highlighted:
                prefix = "❯ "
                style = "bold reverse"
            else:
                prefix = "  "
                style = ""
            result.append(f"{prefix}{sr.item.title}", style=style)
            if sr.item.submenu:
                result.append("  → submenu", style="dim" if not is_highlighted else style)
            elif sr.item.action:
                result.append("  ⚡", style="dim" if not is_highlighted else style)
            # Show the path in dim below the item
            result.append(f"  ({sr.path})", style="dim" if not is_highlighted else style)
            result.append("\n")
        return result

    def _get_selected_item(self):
        if self._search_results is not None:
            if not self._search_results or self.cursor_index >= len(self._search_results):
                return None
            return self._search_results[self.cursor_index]
        if not self._filtered_indices:
            return None
        idx = self._filtered_indices[self.cursor_index]
        return self.menu.items[idx]

    def _max_index(self) -> int:
        if self._search_results is not None:
            return len(self._search_results) - 1
        return len(self._filtered_indices) - 1

    def key_down(self) -> None:
        if self.cursor_index < self._max_index():
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
        selected = self._get_selected_item()
        if selected is None:
            return
        if isinstance(selected, SearchResult):
            self.post_message(self.MenuItemSelected(selected.item, menu=selected.menu))
        else:
            self.post_message(self.MenuItemSelected(selected))
