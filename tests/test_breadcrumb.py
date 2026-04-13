"""Tests for the BreadcrumbBar widget."""

from textual.app import App, ComposeResult

from pymenu_cli.widgets.breadcrumb import BreadcrumbBar


class BreadcrumbTestApp(App):
    def compose(self) -> ComposeResult:
        yield BreadcrumbBar()


async def test_breadcrumb_initial_state():
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        assert bar is not None


async def test_breadcrumb_set_path():
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        bar.set_path(["Main Menu", "Settings", "Display"])
        await pilot.pause()
        text = bar.render_path()
        assert "Main Menu" in text
        assert "Settings" in text
        assert "Display" in text


async def test_breadcrumb_single_level():
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        bar.set_path(["Main Menu"])
        text = bar.render_path()
        assert "Main Menu" in text
