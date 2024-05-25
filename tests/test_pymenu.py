import json
import pytest
from unittest.mock import Mock, patch

from pymenu_cli.pymenu import load_menu, create_menu_from_data, load_actions_module, main
from pymenu_cli.models.menu import Menu


# Tests for load_menu function
def test_load_menu_with_valid_paths(tmp_path):
    """
    Test that the load_menu function correctly loads a menu from a JSON file
    and associates actions from a Python module when provided with valid file paths.
    """
    # Create temporary files
    menu_file = tmp_path / "menu.json"
    actions_file = tmp_path / "actions.py"

    # Write sample data to the temporary files
    menu_data = {"title": "Main Menu", "items": [{"title": "Item 1"}, {"title": "Item 2"}]}
    with open(menu_file, "w", encoding="utf-8") as f:
        json.dump(menu_data, f)

    with open(actions_file, "w", encoding="utf-8") as f:
        f.write("def action1(): pass\ndef action2(): pass")

    # Call the load_menu function
    menu = load_menu(str(menu_file), str(actions_file))

    # Assert that the menu and its items were loaded correctly
    assert isinstance(menu, Menu)
    assert menu.title == "Main Menu"
    assert len(menu.items) == 2
    assert menu.items[0].title == "Item 1"
    assert menu.items[1].title == "Item 2"


def test_load_menu_with_missing_files():
    """
    Test that the load_menu function raises a FileNotFoundError when the
    provided file paths are invalid or the files are missing.
    """
    with pytest.raises(FileNotFoundError):
        load_menu("invalid_path.json", "actions.py")

    with pytest.raises(FileNotFoundError):
        load_menu("menu.json", "invalid_path.py")


# Tests for create_menu_from_data function
def test_create_menu_from_data():
    """
    Test that the create_menu_from_data function correctly creates a Menu object
    and its associated MenuItem objects from a dictionary of menu data.
    """
    menu_data = {
        "title": "Main Menu",
        "items": [
            {"title": "Item 1", "action": "action1"},
            {"title": "Item 2", "submenu": {"title": "Submenu", "items": [{"title": "Subitem 1"}]}},
        ],
    }
    actions = Mock()
    actions.action1 = Mock()

    menu = create_menu_from_data(menu_data, actions)

    assert isinstance(menu, Menu)
    assert menu.title == "Main Menu"
    assert len(menu.items) == 2
    assert menu.items[0].title == "Item 1"
    assert menu.items[0].action == "action1"
    assert menu.items[1].title == "Item 2"
    assert isinstance(menu.items[1].submenu, Menu)
    assert menu.items[1].submenu.title == "Submenu"
    assert len(menu.items[1].submenu.items) == 1
    assert menu.items[1].submenu.items[0].title == "Subitem 1"


# Tests for load_actions_module function
def test_load_actions_module(tmp_path):
    """
    Test that the load_actions_module function correctly loads a Python module
    from a file and returns an object containing the module's callable functions.
    """
    actions_file = tmp_path / "actions.py"

    with open(actions_file, "w", encoding="utf-8") as f:
        f.write("def action1(): pass\ndef action2(): pass")

    actions = load_actions_module(str(actions_file))

    assert hasattr(actions, "action1")
    assert hasattr(actions, "action2")


def test_load_actions_module_with_missing_file():
    """
    Test that the load_actions_module function raises a FileNotFoundError
    when the provided file path is invalid or the file is missing.
    """
    with pytest.raises(FileNotFoundError):
        load_actions_module("invalid_path.py")


# Tests for the main function
def test_main_with_valid_args(tmp_path, monkeypatch, capsys):
    """
    Test that the main function correctly loads and displays the menu
    when provided with valid command-line arguments.
    """
    # Create temporary files
    menu_file = tmp_path / "menu.json"
    actions_file = tmp_path / "actions.py"

    # Write sample data to the temporary files
    menu_data = {"title": "Main Menu", "items": [{"title": "Item 1"}, {"title": "Item 2"}]}
    with open(menu_file, "w", encoding="utf-8") as f:
        json.dump(menu_data, f)

    with open(actions_file, "w", encoding="utf-8") as f:
        f.write("def action1(): pass\ndef action2(): pass")

    # Mock the display method of the Menu class
    with patch.object(Menu, "display") as mock_display:
        # Mock the argparse.ArgumentParser.parse_args method
        monkeypatch.setattr("argparse.ArgumentParser.parse_args",
                            lambda self: Mock(menu=str(menu_file), actions=str(actions_file)))

        # Call the main function
        main()

        # Assert that the display method was called
        mock_display.assert_called_once()


def test_main_with_missing_args(capsys):
    """
    Test that the main function prints the help message
    when command-line arguments are missing.
    """
    # Mock the argparse.ArgumentParser.parse_args method
    with patch("argparse.ArgumentParser.parse_args", return_value=Mock(menu=None, actions=None)):
        with patch("argparse.ArgumentParser.print_help") as mock_print_help:
            # Call the main function
            main()

            # Assert that the print_help method was called
            mock_print_help.assert_called_once()

    # Capture the printed output
    captured = capsys.readouterr()
    assert captured.out == ""  # No output should be printed
