from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.models.menu import Menu


# Tests for the MenuItem class
def test_menu_item_init():
    """
    Test that the MenuItem instance is correctly initialized with the
    provided title, action, submenu, and color settings.
    """
    title = "Menu Item"
    action = "action_name"
    submenu = Menu("Submenu")
    color = {"text": "green", "background": "black"}

    item = MenuItem(title, action, submenu, color)

    assert item.title == title
    assert item.action == action
    assert item.submenu == submenu
    assert item.color == color


def test_menu_item_properties():
    """
    Test that the properties of the MenuItem class
    return the correct values.
    """
    title = "Menu Item"
    action = "action_name"
    submenu = Menu("Submenu")
    color = {"text": "green", "background": "black"}

    item = MenuItem(title, action, submenu, color)

    assert item.title == title
    assert item.action == action
    assert item.submenu == submenu
    assert item.color == color


def test_menu_item_with_optional_args():
    """
    Test that the MenuItem instance is correctly initialized
    when some arguments are not provided.
    """
    title = "Menu Item"

    # No action, submenu, or color
    item = MenuItem(title)
    assert item.title == title
    assert item.action is None
    assert item.submenu is None
    assert item.color is None

    # Only action
    item = MenuItem(title, i_action="action_name")
    assert item.title == title
    assert item.action == "action_name"
    assert item.submenu is None
    assert item.color is None

    # Only submenu
    item = MenuItem(title, i_submenu=Menu("Submenu"))
    assert item.title == title
    assert item.action is None
    assert isinstance(item.submenu, Menu)
    assert item.color is None

    # Only color
    item = MenuItem(title, i_color={"text": "red"})
    assert item.title == title
    assert item.action is None
    assert item.submenu is None
    assert item.color == {"text": "red"}