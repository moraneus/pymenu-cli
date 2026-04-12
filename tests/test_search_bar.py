"""Tests for the SearchBar widget."""
from textual.app import App, ComposeResult
from pymenu_cli.widgets.search_bar import SearchBar


class SearchBarTestApp(App):
    BINDINGS = [("slash", "focus_search", "Search")]

    def compose(self) -> ComposeResult:
        yield SearchBar()

    def action_focus_search(self):
        self.query_one(SearchBar).focus_input()


async def test_search_bar_renders():
    app = SearchBarTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(SearchBar)
        assert bar is not None


async def test_search_bar_posts_message_on_input():
    messages = []

    class CapturingApp(App):
        def compose(self) -> ComposeResult:
            yield SearchBar()

        def on_search_bar_search_changed(self, event: SearchBar.SearchChanged):
            messages.append(event.query)

    app = CapturingApp()
    async with app.run_test() as pilot:
        bar = app.query_one(SearchBar)
        bar.focus_input()
        await pilot.press("t", "e", "s", "t")
        await pilot.pause()
        assert len(messages) > 0
