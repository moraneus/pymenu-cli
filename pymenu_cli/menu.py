import os
import json
import importlib.util
import argparse
from typing import Optional, List


class MenuItem:
    """Represents an item in a menu.

    Attributes:
        title (str): The title of the menu item.
        action (Optional[str]): The action associated with the menu item.
        submenu (Optional['Menu']): A submenu associated with the menu item.
    """

    def __init__(self, title: str, action: Optional[str] = None, submenu: Optional['Menu'] = None):
        """
        Args:
            title (str): The title of the menu item.
            action (Optional[str], optional): The action associated with the menu item. Defaults to None.
            submenu (Optional['Menu'], optional): A submenu associated with the menu item. Defaults to None.
        """
        self.title = title
        self.action = action
        self.submenu = submenu


class Menu:
    """Represents a menu.

    Attributes:
        title (str): The title of the menu.
        items (List[MenuItem]): A list of items in the menu.
        actions (Optional[object]): An object containing callable actions.
    """

    def __init__(self, title: str, items: Optional[List[MenuItem]] = None, actions: Optional[object] = None):
        """
        Args:
            title (str): The title of the menu.
            items (Optional[List[MenuItem]], optional): A list of items in the menu. Defaults to None.
            actions (Optional[object], optional): An object containing callable actions. Defaults to None.
        """
        self.title = title
        self.items = items or []
        self.actions = actions

    def add_item(self, item: MenuItem) -> None:
        """Adds an item to the menu.

        Args:
            item (MenuItem): The item to add.
        """
        self.items.append(item)

    def display(self) -> None:
        """Displays the menu and handles user input."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{self.title}\n")
            for i, item in enumerate(self.items, start=1):
                print(f"{i}. {item.title}")
            print("\nB. Back")
            print("X. Exit")

            choice = input("\nEnter your choice: ").upper()

            if choice == 'B':
                return
            elif choice == 'X':
                exit()
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(self.items):
                        selected_item = self.items[index]
                        if selected_item.submenu:
                            selected_item.submenu.display()
                        elif selected_item.action:
                            getattr(self.actions, selected_item.action)()
                    else:
                        raise ValueError
                except (ValueError, IndexError):
                    input("\nInvalid choice. Press Enter to try again.")


def load_menu(file_path: str, actions_path: str) -> Menu:
    """Loads a menu from a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        actions_path (str): The path to the actions Python file.

    Returns:
        Menu: The loaded menu.
    """
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
        actions = load_actions_module(actions_path)
        return create_menu_from_data(menu_data, actions)


def create_menu_from_data(menu_data: dict, actions: object) -> Menu:
    """Creates a menu from dictionary data.

    Args:
        menu_data (dict): The menu data.
        actions (object): An object containing callable actions.

    Returns:
        Menu: The created menu.
    """
    menu = Menu(menu_data['title'], actions=actions)
    for item_data in menu_data['items']:
        if 'submenu' in item_data:
            submenu = create_menu_from_data(item_data['submenu'], actions)
            menu.add_item(MenuItem(item_data['title'], submenu=submenu))
        else:
            menu.add_item(MenuItem(item_data['title'], action=item_data.get('action')))
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
        main_menu = load_menu(args.menu, args.actions)
        main_menu.display()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
