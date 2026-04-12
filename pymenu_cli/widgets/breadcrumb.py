"""Breadcrumb navigation bar widget."""

from textual.widget import Widget
from textual.message import Message
from rich.text import Text


class BreadcrumbBar(Widget):
    """Displays the navigation path as a breadcrumb trail."""

    class BreadcrumbNavigate(Message):
        def __init__(self, level: int) -> None:
            super().__init__()
            self.level = level

    DEFAULT_CSS = """
    BreadcrumbBar {
        height: 1;
        dock: top;
        padding: 0 1;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="breadcrumb")
        self._path: list[str] = []

    def set_path(self, path: list[str]) -> None:
        self._path = list(path)
        self.refresh()

    def render_path(self) -> str:
        return " › ".join(self._path)

    def render(self) -> Text:
        if not self._path:
            return Text("")
        result = Text("\U0001f4cd ")
        for i, segment in enumerate(self._path):
            if i > 0:
                result.append(" › ", style="dim")
            if i < len(self._path) - 1:
                result.append(segment, style="dim")
            else:
                result.append(segment, style="bold")
        return result
