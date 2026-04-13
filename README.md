# pymenu-cli

![PyPI](https://img.shields.io/pypi/v/pymenu-cli)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymenu-cli)
![Python](https://img.shields.io/pypi/pyversions/pymenu-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for creating interactive terminal user interface (TUI) menus from JSON configuration files. Define your menu structure in JSON, write your actions in Python, and get a full-featured TUI application with keyboard navigation, mouse support, global search, theming, and more.

> **v2.0** — Complete rewrite with a modern TUI powered by [Textual](https://textual.textualize.io/). The classic numbered-menu mode is still available via `--classic`.

## Features

- **Full TUI Application** — Sidebar navigation, breadcrumb trail, action output panel, footer with keybinding hints
- **Keyboard & Mouse Navigation** — Arrow keys, vim keys (`j`/`k`), Enter to select, mouse click support
- **Global Search** — Press `/` to search across all menus and submenus instantly
- **Dark & Light Themes** — Toggle with `T` at runtime, or start with `--theme light`
- **5 Banner Styles** — Rich text, box-drawing, FIGlet, gradient, and emoji
- **Classic Mode** — Original v1 numbered-menu experience via `--classic` flag
- **JSON-Driven** — Define menus, submenus, colors, and banners in simple JSON
- **Backward Compatible** — Existing v1 JSON files and action modules work unchanged
- **Python 3.9+** — Modern Python with `pyproject.toml` packaging

## TUI Layout

```
┌─────────────────────────────────────────────────────────┐
│  HEADER — App title/banner                              │
├─────────────────────────────────────────────────────────┤
│  BREADCRUMB — Main Menu › Tools › Settings              │
├──────────────┬──────────────────────────────────────────┤
│              │  🔍 Search/filter bar                     │
│  SIDEBAR     │                                           │
│  Menu Tree   │  ❯ General Settings          ⚡ action    │
│              │    Advanced Settings          ⚡ action    │
│  ▼ Main      │                                           │
│    ▶ Tools   │──────────────────────────────────────────│
│      Help    │  OUTPUT PANEL                             │
│              │  $ open_general_settings()                │
│              │  ✓ Working directory: /home/user          │
├──────────────┴──────────────────────────────────────────┤
│  ↑↓ Navigate   Enter Select   Esc Back   / Search      │
└─────────────────────────────────────────────────────────┘
```

## Installation

```bash
pip install pymenu-cli
```

## Quick Start

### 1. Create a menu JSON file (`menu.json`)

```json
{
  "banner": {
    "title": "My App",
    "style": "gradient",
    "colors": ["red", "magenta"],
    "subtitle": "v1.0"
  },
  "title": "Main Menu",
  "items": [
    {
      "title": "Say Hello",
      "action": "say_hello"
    },
    {
      "title": "Settings",
      "submenu": {
        "title": "Settings",
        "items": [
          {
            "title": "Show Config",
            "action": "show_config"
          }
        ]
      }
    }
  ]
}
```

### 2. Create an actions file (`actions.py`)

```python
import platform

def say_hello():
    print("Hello from pymenu-cli!")
    print(f"Running on {platform.system()} {platform.machine()}")

def show_config():
    print("Config: default settings loaded")
```

### 3. Run it

```bash
# Launch the TUI (default)
pymenu-cli --menu menu.json --actions actions.py

# Classic numbered-menu mode
pymenu-cli --menu menu.json --actions actions.py --classic

# Start with light theme
pymenu-cli --menu menu.json --actions actions.py --theme light
```

### Or use the Python API

```python
from pymenu_cli.pymenu import load_menu

menu = load_menu("menu.json", "actions.py")
menu.display()                          # TUI mode (default)
menu.display(classic=True)              # Classic mode
menu.display(theme="light")             # Light theme
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `k` | Move cursor up |
| `↓` / `j` | Move cursor down |
| `Enter` | Select item (enter submenu or run action) |
| `Esc` | Go back / clear search |
| `Backspace` | Go back to parent menu |
| `/` | Focus global search bar |
| `T` | Toggle dark/light theme |
| `Q` | Quit application |

**Mouse:** Click menu items, sidebar nodes, or scroll the output panel.

## Menu JSON Format

### Full Structure

```json
{
  "banner": {
    "title": "App Name",
    "style": "gradient",
    "colors": ["red", "blue"],
    "subtitle": "Optional subtitle"
  },
  "title": "Main Menu",
  "color": {
    "text": "yellow",
    "background": "light_blue"
  },
  "items": [
    {
      "title": "Action Item",
      "action": "function_name",
      "color": { "text": "green", "background": "black" }
    },
    {
      "title": "Submenu Item",
      "submenu": {
        "title": "Submenu Title",
        "items": [ ... ]
      }
    }
  ]
}
```

### Properties

| Property | Required | Description |
|----------|----------|-------------|
| `title` | Yes | Menu or item title |
| `items` | Yes | Array of menu items |
| `banner` | No | Header banner configuration |
| `color` | No | Text and background color for the title |
| `action` | No | Name of the Python function to execute |
| `submenu` | No | Nested submenu (same structure as root) |

### Banner Styles

All banner styles are rendered using Rich/Textual — no extra dependencies needed (except `pyfiglet` for FIGlet style).

#### Rich Text (`"style": "rich"`)
Clean, bold title with optional subtitle.
```json
"banner": { "title": "My App", "style": "rich", "subtitle": "v1.0" }
```

#### Box Drawing (`"style": "box"`)
Unicode box frame around the title.
```json
"banner": { "title": "My App", "style": "box" }
```
```
╔════════════════╗
║    My App      ║
╚════════════════╝
```

#### FIGlet (`"style": "figlet"`)
Large ASCII art text. Supports font selection via the `font` parameter. See [pyfiglet fonts](https://github.com/pwaller/pyfiglet#supported-fonts).
```json
"banner": { "title": "My App", "style": "figlet", "font": "slant" }
```
```
    __  ___         ___                
   /  |/  /__  __  /   |  ____   ____ 
  / /|_/ / / / / / / /| | / __ \ / __ \
 / /  / / /_/ / / ___ |/ /_/ // /_/ /
/_/  /_/\__, / /_/  |_/ .___// .___/ 
       /____/        /_/    /_/      
```

#### Gradient (`"style": "gradient"`)
Color gradient across the title text.
```json
"banner": { "title": "My App", "style": "gradient", "colors": ["red", "blue"] }
```

#### Emoji (`"style": "emoji"`)
Emoji icon paired with styled text.
```json
"banner": { "title": "My App", "style": "emoji", "icon": "🚀" }
```

#### Backward Compatibility
Existing v1 format with `"font"` (no `"style"`) automatically maps to FIGlet:
```json
"banner": { "title": "My App", "font": "standard" }
```

### Color Options

Colors work in **classic mode** for text and background styling. In TUI mode, they act as overrides on top of the active theme.

**Available colors:** `RED`, `LIGHT_RED`, `BLUE`, `LIGHT_BLUE`, `YELLOW`, `LIGHT_YELLOW`, `GREEN`, `LIGHT_GREEN`, `CYAN`, `LIGHT_CYAN`, `MAGENTA`, `LIGHT_MAGENTA`, `BLACK`, `LIGHT_BLACK`, `WHITE`, `LIGHT_WHITE`

```json
{
  "title": "Highlighted Item",
  "color": { "text": "yellow", "background": "blue" },
  "action": "my_function"
}
```

## Actions File

The actions file is a plain Python module. Each function name corresponds to an `"action"` value in the JSON. Functions receive no arguments. In TUI mode, `print()` output is captured and displayed in the output panel.

```python
import os
import platform

def show_system_info():
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"CWD: {os.getcwd()}")

def create_file():
    with open("output.txt", "w") as f:
        f.write("Hello from pymenu-cli!\n")
    print("✓ Created output.txt")

def risky_action():
    # Exceptions are caught and shown in the output panel
    raise ValueError("Something went wrong!")
```

## Global Search

Press `/` to activate the search bar. It searches across **all menus and submenus**, not just the current view. Results show the full path to each matching item:

```
❯ General Settings  ⚡ (Main Menu › Tools › Settings)
  Advanced Settings  ⚡ (Main Menu › Tools › Settings)
  Generate Password  ⚡ (Main Menu › Tools)
```

Press `Enter` to navigate to the item and execute it. Press `Esc` to clear the search.

## Theming

Two built-in themes: **dark** (default) and **light**.

- Toggle at runtime: press `T`
- Start with a theme: `--theme light`
- Via API: `menu.display(theme="light")`

Themes are implemented as Textual CSS files in `pymenu_cli/themes/`. Custom themes can be added by creating new `.tcss` files.

## Classic Mode

The original v1 numbered-menu experience is preserved:

```bash
pymenu-cli --menu menu.json --actions actions.py --classic
```

```
Main Menu

1. File
2. Edit
3. Tools
4. Help

B. Back
X. Exit

Enter your choice:
```

## CLI Reference

```
pymenu-cli [-h] [-m MENU] [-a ACTIONS] [--classic] [--theme {dark,light}]

Options:
  -m, --menu MENU          Path to the menu JSON file
  -a, --actions ACTIONS    Path to the actions Python file
  --classic                Use classic numbered-menu mode
  --theme {dark,light}     Color theme for TUI mode (default: dark)
  -h, --help               Show help message
```

## Examples

The `examples/` directory contains a full working example with real actions:

```bash
# Clone and run
git clone https://github.com/moraneus/pymenu-cli.git
cd pymenu-cli

# Install
pip install -e ".[dev]"

# Run the TUI example
pymenu-cli --menu examples/menus/colored_menu.json --actions examples/actions/actions.py

# Run in classic mode
pymenu-cli --menu examples/menus/colored_menu.json --actions examples/actions/actions.py --classic

# Run with light theme
pymenu-cli --menu examples/menus/colored_menu.json --actions examples/actions/actions.py --theme light
```

The example includes:
- **File operations** — Create files, list workspace, export as text/JSON/XML
- **Edit operations** — Clipboard cut/copy/paste, workspace stats
- **Tools** — System info, password generator, plugin manager, backup/restore
- **Help** — User guide with keybindings, FAQ, about page

## Migration from v1

pymenu-cli v2.0 is fully backward compatible. Your existing JSON files and action modules work without changes:

| What | v1 | v2 |
|------|----|----|
| Default display | Numbered menu (`input()`) | Full TUI (Textual) |
| Old display mode | — | `--classic` flag |
| Dependencies | `colorama`, `art` | `textual`, `pyfiglet`, `colorama` |
| Python | 3.8+ | 3.9+ |
| Packaging | `setup.py` | `pyproject.toml` |
| Banner format | `"font": "standard"` | Still works (auto-detected as FIGlet) |
| New banner styles | — | `rich`, `box`, `gradient`, `emoji` |
| Theming | — | `dark` / `light` with `T` toggle |
| Search | — | Global search with `/` |

**Breaking changes:** Python 3.8 is no longer supported (EOL since Oct 2024).

## Development

```bash
# Clone
git clone https://github.com/moraneus/pymenu-cli.git
cd pymenu-cli

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
pylint pymenu_cli/

# Run with Textual dev console (live CSS reload)
textual run --dev pymenu_cli.app:MenuApp
```

## Project Structure

```
pymenu_cli/
├── __init__.py          # Public API exports
├── app.py               # MenuApp — main Textual TUI application
├── banner.py            # Banner rendering (5 styles)
├── classic.py           # Classic v1 numbered-menu mode
├── pymenu.py            # CLI entry point, JSON/module loading
├── models/
│   ├── menu.py          # Menu class
│   └── menu_item.py     # MenuItem class
├── widgets/
│   ├── sidebar.py       # Menu tree sidebar
│   ├── menu_list.py     # Navigable menu items panel
│   ├── breadcrumb.py    # Breadcrumb navigation bar
│   ├── search_bar.py    # Global search/filter bar
│   └── output_panel.py  # Action stdout/stderr panel
└── themes/
    ├── dark.tcss        # Dark theme (default)
    └── light.tcss       # Light theme
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Author

Created by [Moraneus](https://github.com/moraneus).
