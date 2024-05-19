# pymenu-cli

![PyPI](https://img.shields.io/pypi/v/pymenu-cli?label=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymenu-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pymenu-cli is a Python library that simplifies the creation of interactive command-line interface (CLI) menus. It provides a convenient way to define hierarchical menu structures and associate actions with menu items.

## Features

- Define menus and submenus using a simple JSON file format
- Automatically generate navigation options (e.g., "Back" and "Exit")
- Execute specific functions based on user selections
- Customizable menu titles and item labels
- Flexible and extensible architecture
- Execute menus directly from the command line

## Installation

```bash
pip install pymenu-cli
```

## Usage

1. Define your menu structure in a JSON file (`menu.json`)
2. Implement the corresponding action functions in a separate Python file (`actions.py`)

### Using the Python API
```python
from pymenu_cli.menu import load_menu

menu_file_path = 'menu.json'
actions_file_path = 'actions.py'
main_menu = load_menu(menu_file_path, actions_file_path)

main_menu.display()
```

### Using the Command Line
```bash
pymenu-cli --menu menu.json --actions actions.py
```

pymenu-cli takes care of the menu navigation, user input handling, and execution of the associated actions based on the user's selections.

## Menu JSON Format
The `menu.json` file defines the structure of your menu. Here's an example:

```json
{
  "title": "Main Menu",
  "items": [
    {
      "title": "Option 1",
      "action": "action_function_1"
    },
    {
      "title": "Option 2",
      "submenu": {
        "title": "Submenu",
        "items": [
          {
            "title": "Submenu Option 1",
            "action": "action_function_2"
          },
          {
            "title": "Submenu Option 2",
            "action": "action_function_3"
          }
        ]
      }
    }
  ]
}
```

## Actions Python File
The `actions.py` file contains the functions that are executed when a menu item is selected. Here's an example:
```python
def action_function_1():
    print("Executing action 1")

def action_function_2():
    print("Executing action 2")

def action_function_3():
    print("Executing action 3")
```

### Examples
Explore the examples directory for sample menu configurations and action implementations. 
To run an example, follow these steps:

1. Clone the project repository.
2. Open your command line and navigate to the examples directory.
3. Execute the example by running the following command:
```python
python3 menu_example.py
```

### License
This project is licensed under the MIT License.