"""Tests for the OutputPanel widget."""

from textual.app import App, ComposeResult

from pymenu_cli.widgets.output_panel import OutputPanel


class OutputTestApp(App):
    def compose(self) -> ComposeResult:
        yield OutputPanel()


async def test_output_panel_renders():
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        assert panel is not None


async def test_output_panel_append_output():
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        panel.append_output("Hello, world!")
        await pilot.pause()


async def test_output_panel_append_error():
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        panel.append_error("Something went wrong")
        await pilot.pause()
