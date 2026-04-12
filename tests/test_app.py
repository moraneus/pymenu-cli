"""Tests for the MenuApp TUI application."""

from unittest.mock import Mock

from pymenu_cli.app import MenuApp
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


def _make_menu():
    actions = Mock()
    actions.action1 = Mock()

    root = Menu("Main Menu", i_config={"actions": actions})
    sub = Menu("Settings", i_config={"actions": actions})
    sub.add_item(MenuItem("Display", i_action="action1"))

    root.add_item(MenuItem("Item 1", i_action="action1"))
    root.add_item(MenuItem("Settings", i_submenu=sub))
    return root


async def test_app_launches():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        assert app.query_one("#sidebar") is not None
        assert app.query_one("#breadcrumb") is not None
        assert app.query_one("#menu-panel") is not None
        assert app.query_one("#output-panel") is not None


async def test_app_breadcrumb_shows_root():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        assert "Main Menu" in bar.render_path()


async def test_app_navigate_into_submenu():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause()

        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        path = bar.render_path()
        assert "Settings" in path


async def test_app_navigate_back():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause()

        await pilot.press("escape")
        await pilot.pause()

        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        path = bar.render_path()
        assert "Settings" not in path
        assert "Main Menu" in path


async def test_app_quit():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        await pilot.press("q")


async def test_app_action_execution():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("enter")
        await pilot.pause()

        menu.actions.action1.assert_called_once()


async def test_app_search_focus():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        await pilot.press("slash")
        await pilot.pause()
        from pymenu_cli.widgets.search_bar import SearchBar
        from textual.widgets import Input
        search = app.query_one(SearchBar)
        inp = search.query_one(Input)
        assert inp.has_focus


async def test_app_theme_toggle():
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        initial_theme = app.app_theme
        await pilot.press("t")
        await pilot.pause()
        assert app.app_theme != initial_theme
