import argparse
import importlib.util
import json
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


def load_menu(file_path: str, actions_path: str) -> Menu:
    """Loads a menu from a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        actions_path (str): The path to the actions Python file.

    Returns:
        Menu: The loaded menu.

    Raises:
        FileNotFoundError: If the menu JSON file is not found.
        json.JSONDecodeError: If the menu JSON file is not in the correct format.
        FileNotFoundError: If the actions Python file is not found.
    """
    try:
        with open(file_path, 'r') as file:
            menu_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Menu JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format in menu file: {e}", e.doc, e.pos)

    try:
        actions = load_actions_module(actions_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Actions Python file not found: {actions_path}")

    return create_menu_from_data(menu_data, actions)


def create_menu_from_data(menu_data: dict, actions: object) -> Menu:
    """Creates a menu from dictionary data.

    Args:
        menu_data (dict): The menu data.
        actions (object): An object containing callable actions.

    Returns:
        Menu: The created menu.
    """
    menu = Menu(
        menu_data['title'],
        i_actions=actions,
        i_color=menu_data.get('color'),
        i_banner=menu_data.get('banner'))
    for item_data in menu_data['items']:
        if 'submenu' in item_data:
            submenu = create_menu_from_data(item_data['submenu'], actions)
            menu.add_item(
                MenuItem(item_data['title'], i_submenu=submenu, i_color=item_data.get('color')))
        else:
            menu.add_item(
                MenuItem(item_data['title'], i_action=item_data.get('action'), i_color=item_data.get('color')))
    return menu


def load_actions_module(actions_path: str) -> object:
    """Loads an actions module from a file.

    Args:
        actions_path (str): The path to the actions Python file.

    Returns:
        object: The loaded actions module.
    """
    spec = importlib.util.spec_from_file_location("actions", actions_path)
    actions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(actions)
    return actions


def main() -> None:
    """Main function to parse arguments and display the menu."""
    parser = argparse.ArgumentParser(description='pymenu-cli - Create interactive CLI menus')
    parser.add_argument('-m', '--menu', type=str, help='Path to the menu JSON file')
    parser.add_argument('-a', '--actions', type=str, help='Path to the actions Python file')

    args = parser.parse_args()

    if args.menu and args.actions:
        try:
            main_menu = load_menu(args.menu, args.actions)
            main_menu.display()
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"Error: {str(e)}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
