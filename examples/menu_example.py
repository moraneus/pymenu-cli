from pymenu_cli.pymenu import load_menu

# Define the 'menu' and the 'action' files
menu_file_path = 'menus/colored_menu.json'
actions_file_path = 'actions/actions.py'

# Init the menu with this files
main_menu = load_menu(menu_file_path, actions_file_path)

# Display the menu
main_menu.display()
