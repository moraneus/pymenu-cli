"""
This module contains tests for the Menu and MenuItem classes in the pymenu_cli.models.menu module.
"""

from unittest.mock import Mock, patch

import pytest

from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


# Tests for the Menu class
def test_menu_init():
    """
    Test that the Menu instance is correctly initialized with the
    provided title and configuration.
    """
    title = "Main Menu"
    config = {
        "items": [],
        "actions": Mock(),
        "color": {"text": "red", "background": "blue"},
        "banner": {"title": "Banner", "font": "standard"},
    }

    menu = Menu(title, i_config=config)

    assert menu.title == title
    assert menu.items == config["items"]
    assert menu.actions == config["actions"]
    assert menu.color == config["color"]
    assert menu.banner == config["banner"]


def test_menu_add_item():
    """
    Test that the add_item method of the Menu class correctly adds
    a new MenuItem to the menu.
    """
    menu = Menu("Test Menu")
    item = MenuItem("Item 1")

    menu.add_item(item)

    assert len(menu.items) == 1
    assert menu.items[0] == item


def test_menu_display(capsys, monkeypatch):
    """
    Test that the display method of the Menu class correctly displays
    the menu and handles user input.
    """
    actions = Mock()  # Create a Mock object for actions

    menu = Menu("Test Menu", i_config={"actions": actions})
    item1 = MenuItem("Item 1", i_action="action1")
    item2 = MenuItem("Item 2", i_submenu=Menu("Submenu"))
    menu.add_item(item1)
    menu.add_item(item2)

    # Mock the user input: select item1 (action), select item2 (submenu), back from submenu, exit main
    user_inputs = iter(["1", "2", "B", "X"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    # Mock the action
    mock_action1 = Mock()
    actions.action1 = mock_action1  # Assign the Mock to actions.action1

    # Call the display method in classic mode to avoid launching TUI
    with pytest.raises(SystemExit):
        menu.display(classic=True)

    # Assert that the action was called and submenu was navigated into (shown in output)
    mock_action1.assert_called_once()
    captured = capsys.readouterr()
    assert "Submenu" in captured.out


def test_menu_get_color_string():
    """
    Test that the get_color_string method of the Menu class
    correctly returns the color string based on the provided color settings.
    """
    # Test with valid color settings
    color = {"text": "red", "background": "blue"}
    expected_color_string = "\x1b[31m\x1b[44m"
    assert Menu.get_color_string(color) == expected_color_string

    # Test with invalid color settings
    color = {"text": "invalid", "background": "invalid"}
    with pytest.raises(AttributeError):
        Menu.get_color_string(color)

    # Test with no color settings
    assert Menu.get_color_string(None) == ""


def test_menu_print_banner(capsys):
    """
    Test that the print_banner method of the Menu class
    correctly delegates to classic._print_banner.
    """
    menu = Menu("Test Menu", i_config={"banner": {"title": "Banner Text", "font": "standard"}})

    # Patch _print_banner in the classic module since print_banner delegates there
    with patch("pymenu_cli.classic._print_banner") as mock_print_banner:
        menu.print_banner()
        mock_print_banner.assert_called_once_with({"title": "Banner Text", "font": "standard"})
