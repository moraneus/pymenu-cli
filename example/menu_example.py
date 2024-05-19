from pymenu_cli.menu import load_menu

menu_file_path = 'menu.json'
actions_file_path = 'actions.py'
main_menu = load_menu(menu_file_path, actions_file_path)

main_menu.display()