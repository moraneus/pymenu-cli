"""Tests for the classic input()-based display mode."""

from unittest.mock import Mock

from pymenu_cli.classic import classic_display
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


def test_classic_display_action(monkeypatch):
    """Test that classic_display executes an action when selected."""
    actions = Mock()
    mock_action = Mock()
    actions.action1 = mock_action

    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Item 1", i_action="action1"))

    user_inputs = iter(["1", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)

    mock_action.assert_called_once()


def test_classic_display_submenu(monkeypatch):
    """Test that classic_display navigates into a submenu."""
    actions = Mock()
    submenu = Menu("Submenu", i_config={"actions": actions})
    submenu.add_item(MenuItem("Sub Item", i_action="sub_action"))
    actions.sub_action = Mock()

    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Go to submenu", i_submenu=submenu))

    user_inputs = iter(["1", "1", "B", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)

    actions.sub_action.assert_called_once()


def test_classic_display_back(monkeypatch):
    """Test that classic_display returns on 'B' input."""
    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    monkeypatch.setattr("builtins.input", lambda _: "B")

    classic_display(menu)


def test_classic_display_exit(monkeypatch):
    """Test that classic_display exits on 'X' input."""
    import pytest

    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    monkeypatch.setattr("builtins.input", lambda _: "X")

    with pytest.raises(SystemExit):
        classic_display(menu)


def test_classic_display_invalid_input(monkeypatch):
    """Test that classic_display handles invalid input gracefully."""
    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    user_inputs = iter(["invalid", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)
