"""Example: Launch pymenu-cli from Python code."""

from pymenu_cli.pymenu import load_menu

# Define the menu and action files
menu_file_path = "menus/colored_menu.json"
actions_file_path = "actions/actions.py"

# Load and display the menu (launches TUI by default)
main_menu = load_menu(menu_file_path, actions_file_path)
main_menu.display()

# For classic mode: main_menu.display(classic=True)
# For light theme: main_menu.display(theme="light")
