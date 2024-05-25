import pytest
from unittest.mock import patch, Mock

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

    # Mock the user input
    user_inputs = iter(["1", "2", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    # Mock the actions and submenu.display methods
    mock_action1 = Mock()
    mock_submenu_display = Mock()
    actions.action1 = mock_action1  # Assign the Mock to actions.action1
    menu.items[1].submenu.display = mock_submenu_display

    # Call the display method
    menu.display()

    # Assert that the actions and submenu.display methods were called
    mock_action1.assert_called_once()
    mock_submenu_display.assert_called_once()


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
    correctly prints the banner using the art library.
    """
    menu = Menu("Test Menu", i_config={"banner": {"title": "Banner Text", "font": "standard"}})

    # Mock the art.text2art function
    with patch("art.text2art", return_value="ASCII_ART"):
        menu.print_banner()
        captured = capsys.readouterr()
        assert captured.out == "ASCII_ART\n"
