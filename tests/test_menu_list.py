"""Tests for the MenuListPanel widget."""

from unittest.mock import Mock

from textual.app import App, ComposeResult

from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.widgets.menu_list import MenuListPanel


def _make_menu():
    actions = Mock()
    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Item 1", i_action="action1"))
    menu.add_item(MenuItem("Item 2", i_action="action2"))
    menu.add_item(MenuItem("Sub Menu", i_submenu=Menu("Sub")))
    return menu


class MenuListTestApp(App):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu

    def compose(self) -> ComposeResult:
        yield MenuListPanel(self.menu)


async def test_menu_list_renders():
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        assert panel is not None


async def test_menu_list_shows_items():
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        assert panel.item_count == 3


async def test_menu_list_keyboard_navigation():
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        panel.focus()
        assert panel.cursor_index == 0
        await pilot.press("down")
        assert panel.cursor_index == 1
        await pilot.press("down")
        assert panel.cursor_index == 2
        await pilot.press("up")
        assert panel.cursor_index == 1


async def test_menu_list_filter():
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        panel.filter_items("Sub")
        await pilot.pause()
        assert panel.visible_item_count == 1
