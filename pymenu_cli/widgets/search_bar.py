"""Search/filter bar widget for filtering menu items."""

from textual import on
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Input


class SearchBar(Horizontal):
    """A search bar that filters menu items in real-time."""

    class SearchChanged(Message):
        """Posted when the search input value changes."""

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
        """Compose the search bar with a single text input widget."""
        yield Input(placeholder="\U0001f50d Type to filter...", id="search-input")

    def focus_input(self) -> None:
        """Focus the search input field."""
        self.query_one("#search-input", Input).focus()

    def clear(self) -> None:
        """Clear the search input and emit a SearchChanged event with an empty string."""
        inp = self.query_one("#search-input", Input)
        inp.value = ""
        self.post_message(self.SearchChanged(""))

    @on(Input.Changed, "#search-input")
    def on_input_changed(self, event: Input.Changed) -> None:
        """Forward input changes as a SearchChanged message."""
        self.post_message(self.SearchChanged(event.value))
