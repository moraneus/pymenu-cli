# pymenu-cli

![PyPI](https://img.shields.io/pypi/v/pymenu-cli)
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
- Support for color customization of menu titles and items
- Display a banner using ASCII art with customizable text and font


## Installation

```bash
pip install pymenu-cli
```

## Usage

1. Define your menu structure in a JSON file (`menu.json`)
2. Implement the corresponding action functions in a separate Python file (`actions.py`)

### Using the Python API
```python
from pymenu_cli.pymenu import load_menu

# Define the 'menu' and the 'action' files 
menu_file_path = 'menu.json'
actions_file_path = 'actions.py'

# Init the menu with this files
main_menu = load_menu(menu_file_path, actions_file_path)

# Display the menu
main_menu.display()
```

### Using the Command Line
```bash
pymenu-cli --menu menu.json --actions actions.py
```

pymenu-cli takes care of the menu navigation, menu stying, user input handling, and execution of the associated actions based on the user's selections.

## Menu JSON Format
The `menu.json` file defines the structure of your menu. Here's an example:

```json
{
  "banner": {
    "title": "HELLO",
    "font": "white_bubble"
  },
  "title": "Main Menu",
  "color": {
    "text": "light_blue",
    "background": "black"
  },
  "items": [
    {
      "title": "Option 1",
      "color": {
        "text": "yellow",
        "background": "blue"
      },
      "action": "action_function_1"
    },
    {
      "title": "Option 2",
      "color": {
        "text": "black",
        "background": "light_yellow"
      },
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

In the `menu.json` file, you can specify the following properties:
* `banner` (optional): The banner configuration for the menu.
  * `title`: The text to display in the banner.
  * `font` (optional): The font to use for the banner. If not specified, the default font will be used.
* `title`: The title of the menu or submenu.
* `color` (optional): The color settings for the menu or submenu title. 
  * `text`: The color of the text (e.g., "red", "light_blue").
  * `background`: The color of the background (e.g., "white", "black").
* `items`: An array of menu items, each with its own properties:
  * `title`: The title of the menu item.
  * `color` (optional): The color settings for the menu item title. 
  * `action` (optional): The name of the action function to execute when the item is selected.
  * `submenu` (optional): A nested submenu with its own title and items.

### Banner Customization
PyMenu CLI supports displaying a banner using ASCII art. 
The banner can be customized by specifying the banner property in the menu.json file.
The banner property has the following sub-properties:
* `title`: The text to display in the banner.
* `font` (optional): The font to use for the banner. If not specified, the default font will be used.

PyMenu CLI uses the art library to generate the ASCII art for the banner. 
You can choose from a wide range of available fonts provided by the [art](https://pypi.org/project/art/) library. Here are some font options:

* "standard"
```text
 _____                _   
|  ___|  ___   _ __  | |_ 
| |_    / _ \ | '_ \ | __|
|  _|  | (_) || | | || |_ 
|_|     \___/ |_| |_| \__|
```
  
* "block"
```text
 .----------------.  .----------------.  .-----------------. .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |     ____     | || | ____  _____  | || |  _________   | |
| | |_   ___  |  | || |   .'    `.   | || ||_   \|_   _| | || | |  _   _  |  | |
| |   | |_  \_|  | || |  /  .--.  \  | || |  |   \ | |   | || | |_/ | | \_|  | |
| |   |  _|      | || |  | |    | |  | || |  | |\ \| |   | || |     | |      | |
| |  _| |_       | || |  \  `--'  /  | || | _| |_\   |_  | || |    _| |_     | |
| | |_____|      | || |   `.____.'   | || ||_____|\____| | || |   |_____|    | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 
```
* "bubble"
```text
  _    _    _    _  
 / \  / \  / \  / \ 
( F )( o )( n )( t )
 \_/  \_/  \_/  \_/ 
```
* "white_bubble"
```text
Ⓕⓞⓝⓣ
```
* "black_bubble"
```text
🅕🅞🅝🅣
```
* "digital"
```text
+-++-++-++-+
|f||o||n||t|
+-++-++-++-+
```
* "isometric1"
```text
      ___           ___           ___           ___     
     /\  \         /\  \         /\__\         /\  \    
    /::\  \       /::\  \       /::|  |        \:\  \   
   /:/\:\  \     /:/\:\  \     /:|:|  |         \:\  \  
  /::\~\:\  \   /:/  \:\  \   /:/|:|  |__       /::\  \ 
 /:/\:\ \:\__\ /:/__/ \:\__\ /:/ |:| /\__\     /:/\:\__\
 \/__\:\ \/__/ \:\  \ /:/  / \/__|:|/:/  /    /:/  \/__/
      \:\__\    \:\  /:/  /      |:/:/  /    /:/  /     
       \/__/     \:\/:/  /       |::/  /     \/__/      
                  \::/  /        /:/  /                 
                   \/__/         \/__/                  
```
* "letters"
```text
FFFFFFF                tt    
FF       oooo  nn nnn  tt    
FFFF    oo  oo nnn  nn tttt  
FF      oo  oo nn   nn tt    
FF       oooo  nn   nn  tttt 
```
* "arrow"
```text
>=======>                        >=>   
>=>                              >=>   
>=>          >=>     >==>>==>  >=>>==> 
>=====>    >=>  >=>   >=>  >=>   >=>   
>=>       >=>    >=>  >=>  >=>   >=>   
>=>        >=>  >=>   >=>  >=>   >=>   
>=>          >=>     >==>  >=>    >=>  
```
* "slant"
```text
    ______                  __ 
   / ____/  ____    ____   / /_
  / /_     / __ \  / __ \ / __/
 / __/    / /_/ / / / / // /_  
/_/       \____/ /_/ /_/ \__/  
```

For a complete list of available fonts, 
please refer to the [art library documentation](https://pypi.org/project/art/).
If no font is specified in the banner configuration, PyMenu CLI will use the default font provided by the art library.

### Color Customization
PyMenu CLI supports color customization of menu titles and items using the colorama library. 
You can specify the color of the text and background for each menu and item in the menu.json file.
The available color options are defined in the TextColors and BackgroundColors enums:

#### TextColors
`RED`, `LIGHT_RED`, `BLUE`, `LIGHT_BLUE`, `YELLOW`, 
`LIGHT_YELLOW`, `GREEN`, `LIGHT_GREEN`, `CYAN`, `LIGHT_CYAN`,
`MAGENTA`, `LIGHT_MAGENTA`, `BLACK`, `LIGHT_BLACK`, `WHITE`, 
`LIGHT_WHITE`


#### BackgroundColors
`RED`, `LIGHT_RED`, `BLUE`, `LIGHT_BLUE`, `YELLOW`, 
`LIGHT_YELLOW`, `GREEN`, `LIGHT_GREEN`, `CYAN`, `LIGHT_CYAN`,
`MAGENTA`, `LIGHT_MAGENTA`, `BLACK`, `LIGHT_BLACK`, `WHITE`, 
`LIGHT_WHITE`

To apply colors to a menu or item, 
add the color property with the desired `text` and `background` colors in the menu.json file.

### Color Example

Here's an example of how the menu with colors would look like:
* [View Color Examples](https://htmlpreview.github.io/?https://github.com/moraneus/pymenu-cli/blob/main/docs/colors_example.html)

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