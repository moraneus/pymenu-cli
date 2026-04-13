"""Output panel widget for displaying action stdout/stderr."""

from rich.text import Text
from textual.containers import Vertical
from textual.widgets import RichLog


class OutputPanel(Vertical):
    """A scrollable log panel for action output."""

    DEFAULT_CSS = """
    OutputPanel {
        height: 1fr;
        max-height: 12;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="output-panel")

    def compose(self):
        """Compose the output panel with a scrollable RichLog widget."""
        yield RichLog(highlight=True, markup=True, id="output-log")

    def append_output(self, text: str) -> None:
        """Append a plain-text line to the output log."""
        log = self.query_one("#output-log", RichLog)
        log.write(text)

    def append_error(self, text: str) -> None:
        """Append an error message in bold red to the output log."""
        log = self.query_one("#output-log", RichLog)
        error_text = Text(text, style="bold red")
        log.write(error_text)

    def append_action_header(self, action_name: str) -> None:
        """Append a cyan action header line showing the action being executed."""
        log = self.query_one("#output-log", RichLog)
        header = Text(f"$ {action_name}()", style="bold cyan")
        log.write(header)
