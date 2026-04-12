"""Search/filter bar widget for filtering menu items."""

from textual.containers import Horizontal
from textual.widgets import Input
from textual.message import Message
from textual import on


class SearchBar(Horizontal):
    """A search bar that filters menu items in real-time."""

    class SearchChanged(Message):
        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query

    DEFAULT_CSS = """
    SearchBar {
        height: 3;
        dock: top;
        margin: 0 0 1 0;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="search-bar")

    def compose(self):
        yield Input(placeholder="\U0001f50d Type to filter...", id="search-input")

    def focus_input(self) -> None:
        self.query_one("#search-input", Input).focus()

    def clear(self) -> None:
        inp = self.query_one("#search-input", Input)
        inp.value = ""
        self.post_message(self.SearchChanged(""))

    @on(Input.Changed, "#search-input")
    def on_input_changed(self, event: Input.Changed) -> None:
        self.post_message(self.SearchChanged(event.value))
