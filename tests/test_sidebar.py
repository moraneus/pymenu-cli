"""Tests for the MenuSidebar widget."""

from textual.app import App, ComposeResult

from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.widgets.sidebar import MenuSidebar


def _make_menu():
    root = Menu("Main Menu")
    sub1 = Menu("Settings")
    sub1.add_item(MenuItem("Display", i_action="display_settings"))
    sub1.add_item(MenuItem("Audio", i_action="audio_settings"))
    root.add_item(MenuItem("Files", i_action="open_files"))
    root.add_item(MenuItem("Settings", i_submenu=sub1))
    root.add_item(MenuItem("Help", i_action="show_help"))
    return root


class SidebarTestApp(App):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu

    def compose(self) -> ComposeResult:
        yield MenuSidebar(self.menu)


async def test_sidebar_renders_tree():
    menu = _make_menu()
    app = SidebarTestApp(menu)
    async with app.run_test() as pilot:
        sidebar = app.query_one(MenuSidebar)
        assert sidebar is not None


async def test_sidebar_shows_root_items():
    menu = _make_menu()
    app = SidebarTestApp(menu)
    async with app.run_test() as pilot:
        sidebar = app.query_one(MenuSidebar)
        tree = sidebar.query_one("Tree")
        assert tree.root.data == menu
