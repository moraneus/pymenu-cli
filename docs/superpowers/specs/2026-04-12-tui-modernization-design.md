# pymenu-cli v2.0 — TUI Modernization Design

## Overview

Modernize pymenu-cli from a simple `input()`-based numbered menu into a full Terminal User Interface (TUI) application powered by Textual. The upgrade delivers panels, borders, sidebar navigation, mouse support, search/filter, theming, and an action output panel — while preserving full backward compatibility with existing JSON configs, action modules, and the Python API.

## Goals

- Transform the user experience into a modern, full-featured TUI application
- Maintain full backward compatibility with existing JSON format, Python API, and CLI usage
- Replace `art` with `pyfiglet` (lighter) and `colorama` with Textual (which includes Rich)
- Modernize packaging from `setup.py` to `pyproject.toml`
- Support Python 3.9+

## Non-Goals

- Changing the JSON schema in breaking ways
- Building a generic TUI framework or widget library for third-party reuse
- Supporting plugin systems or custom widget injection
- Web-based or GUI rendering

---

## TUI Layout

The application screen is divided into 6 zones:

```
┌─────────────────────────────────────────────────────────┐
│  1. HEADER BAR — App title/banner + version             │
├─────────────────────────────────────────────────────────┤
│  2. BREADCRUMB — Main Menu › Settings › Display         │
├──────────────┬──────────────────────────────────────────┤
│              │  4. MENU ITEMS PANEL                     │
│  3. SIDEBAR  │     🔍 Search/filter bar                 │
│  Menu Tree   │     ❯ Item 1 (highlighted)               │
│              │       Item 2                              │
│  ▼ Main      │       Item 3                              │
│    ▶ Settings│                                           │
│      Help    │──────────────────────────────────────────│
│              │  5. ACTION OUTPUT PANEL                   │
│              │     Scrollable stdout/stderr log          │
├──────────────┴──────────────────────────────────────────┤
│  6. FOOTER — ↑↓ Navigate  Enter Select  Esc Back  Q Quit│
└─────────────────────────────────────────────────────────┘
```

### Zone Details

**1. Header Bar**
- Renders the app title from the JSON `banner` field
- Supports 5 banner styles: rich, box, figlet, gradient, emoji (see Banner Styles section)
- Falls back to plain title text if no banner is configured
- Right-aligned version/metadata area

**2. Breadcrumb Trail**
- Auto-generated from menu navigation depth
- Format: `Main Menu › Settings › Display`
- Updates on every menu navigation
- Clickable segments (mouse support) to jump back to any level

**3. Sidebar**
- Displays the full menu tree hierarchy
- Highlights the current menu location
- Collapsible/expandable tree nodes
- Syncs with menu navigation in the main panel
- Shows `▼` for expanded and `▶` for collapsed/current nodes

**4. Menu Items Panel**
- Displays the current menu's items as a navigable list
- Arrow-key cursor with visual highlight on the selected item
- Each item shows an indicator: `→ submenu` or `⚡ action`
- Search/filter bar at the top, activated with `/`
- Mouse click support for direct item selection

**5. Action Output Panel**
- Captures stdout and stderr from executed action functions
- Scrollable log — previous output is preserved
- Auto-scrolls to latest output
- Exceptions/tracebacks displayed in red/error styling
- Panel can be scrolled independently with mouse or keyboard

**6. Footer Bar**
- Context-sensitive keybinding hints
- Always visible
- Updates based on current state (e.g., search mode shows different hints)

---

## Interaction Model

### Keybindings

| Key | Action |
|---|---|
| `↑` / `k` | Move cursor up |
| `↓` / `j` | Move cursor down |
| `Enter` | Select item (enter submenu or execute action) |
| `Esc` / `Backspace` | Go back to parent menu |
| `/` | Focus search/filter bar |
| `Esc` (in search) | Clear search, return focus to menu list |
| `T` | Toggle dark/light theme |
| `Q` | Quit application |

### Mouse Support

- Click menu items to select them
- Click sidebar tree nodes to navigate directly
- Click breadcrumb segments to jump to that level
- Scroll wheel on menu list and output panel

### Search/Filter

- `/` focuses the search bar
- Typing filters items in real-time (case-insensitive substring match on item titles)
- Filtered results maintain arrow-key navigation
- `Esc` clears the filter and returns to the full list
- If only one match remains, `Enter` selects it directly

### Menu Transitions

- Entering a submenu updates: menu list content, sidebar highlight, breadcrumb trail
- Textual's built-in transition support for smooth visual updates
- Going back reverses the navigation (restores previous cursor position)

### Action Execution

- Selecting an action item runs the associated Python function
- stdout and stderr are captured via `contextlib.redirect_stdout/redirect_stderr`
- Output appears in the action output panel
- Exceptions are caught and displayed as formatted tracebacks in error styling
- The menu remains interactive during and after action execution

---

## Theming

### Built-in Themes

Two themes ship by default:
- **Dark** (default) — Dark background, light text, accent color for highlights
- **Light** — Light background, dark text, adjusted accent color

Toggled at runtime with `T` key.

### Implementation

- Themes are implemented as Textual CSS files (`.tcss`)
- Located in `pymenu_cli/themes/dark.tcss` and `pymenu_cli/themes/light.tcss`
- Textual's CSS system handles all styling: colors, borders, spacing, focus states

### JSON Color Override

Existing `"color"` fields in JSON configs act as overrides on top of the active theme:

```json
{
  "title": "Settings",
  "color": { "text": "RED", "background": "WHITE" }
}
```

These override the theme's default colors for that specific title/item. If no color is specified, the theme defaults apply.

### Accent Color

The highlight/accent color drives: cursor highlight, sidebar active state, selected items, and interactive elements. Configurable per theme in the TCSS files.

---

## Banner Styles

The JSON `banner` field supports 5 styles, all rendered using Rich/Textual (no extra dependencies):

### 1. Rich Styled Text (`"style": "rich"`)
Bold, colored title with optional subtitle. Clean and minimal.
```json
"banner": { "title": "My App", "style": "rich", "subtitle": "v1.0" }
```

### 2. Box-Drawing Frame (`"style": "box"`)
Unicode box-drawing characters frame the title.
```json
"banner": { "title": "My App", "style": "box" }
```

### 3. FIGlet (`"style": "figlet"`)
Large stylized text via the `pyfiglet` library. Supports font selection. `pyfiglet` is added as a dependency (lightweight, pure Python) to maintain backward compat with existing `"font"` configs.
```json
"banner": { "title": "My App", "style": "figlet", "font": "standard" }
```

### 4. Gradient (`"style": "gradient"`)
Color gradient across the title text.
```json
"banner": { "title": "My App", "style": "gradient", "colors": ["red", "blue"] }
```

### 5. Emoji + Text (`"style": "emoji"`)
Configurable emoji icon paired with styled title.
```json
"banner": { "title": "My App", "style": "emoji", "icon": "🚀" }
```

### Backward Compatibility

If `"style"` is absent but `"font"` is present, defaults to `"figlet"`:
```json
// Old format — still works, treated as figlet
"banner": { "title": "My App", "font": "standard" }
```

All styles accept an optional `"subtitle"` field.

---

## Architecture

### Project Structure

```
pymenu_cli/
├── __init__.py              # Public API: load_menu(), MenuApp
├── app.py                   # MenuApp(textual.app.App) — main TUI application
├── classic.py               # Classic input() loop (--classic fallback)
├── pymenu.py                # CLI entry point (argparse, load_menu, main)
├── models/
│   ├── __init__.py
│   ├── menu.py              # Menu dataclass (unchanged public interface)
│   └── menu_item.py         # MenuItem dataclass (unchanged public interface)
├── widgets/
│   ├── __init__.py
│   ├── sidebar.py           # MenuTree sidebar widget
│   ├── menu_list.py         # Main menu items list with cursor
│   ├── breadcrumb.py        # Breadcrumb trail widget
│   ├── search_bar.py        # Filter/search input widget
│   └── output_panel.py      # Action stdout/stderr capture panel
├── themes/
│   ├── __init__.py
│   ├── dark.tcss            # Textual CSS — dark theme
│   └── light.tcss           # Textual CSS — light theme
└── ui/
    ├── __init__.py
    └── styles.py            # Kept for backward compat (color enums)
```

### Component Responsibilities

**`app.py` — `MenuApp(textual.app.App)`**
- Owns the screen layout (compose method)
- Manages navigation state (menu stack, current position)
- Handles keybindings at the app level
- Routes messages between widgets
- Manages theme switching

**`models/menu.py` — `Menu`**
- Unchanged public interface: `title`, `items`, `actions`, `color`, `banner`
- `display()` method now creates and runs `MenuApp`
- Accepts `classic=False` parameter to fall back to classic mode
- `add_item()` works as before

**`models/menu_item.py` — `MenuItem`**
- Unchanged: `title`, `action`, `submenu`, `color`

**`widgets/sidebar.py` — `MenuSidebar`**
- Renders the full menu tree as an indented, collapsible list
- Posts `SidebarItemSelected` message when a node is clicked
- Receives `MenuChanged` message to update highlight

**`widgets/menu_list.py` — `MenuListPanel`**
- Renders current menu items as a navigable list
- Manages cursor position
- Posts `MenuItemSelected` message on Enter/click
- Accepts filter text from search bar to hide non-matching items

**`widgets/breadcrumb.py` — `BreadcrumbBar`**
- Renders the navigation path as clickable segments
- Posts `BreadcrumbNavigate` message when a segment is clicked

**`widgets/search_bar.py` — `SearchBar`**
- Text input that posts `SearchChanged` message on each keystroke
- `/` key from app focuses this widget
- `Esc` clears and defocuses

**`widgets/output_panel.py` — `OutputPanel`**
- Rich text log widget for action output
- Appends captured stdout/stderr after each action
- Scrollable, auto-scrolls to bottom on new output
- Renders exceptions with error styling

**`classic.py`**
- Contains the current `input()`-based rendering loop
- Moved from the existing `Menu.display()` logic
- Activated via `--classic` CLI flag or `display(classic=True)`

### Data Flow

1. `load_menu(json_path, actions_path)` parses JSON and loads actions module → returns `Menu` object (unchanged)
2. `Menu.display()` creates `MenuApp(menu=self)` and calls `app.run()`
3. `MenuApp.compose()` assembles widgets: `Header`, `BreadcrumbBar`, `MenuSidebar`, `MenuListPanel`, `OutputPanel`, `Footer`
4. User navigates → `MenuListPanel` posts `MenuItemSelected` → `MenuApp` handles it:
   - If submenu: push to menu stack, update all widgets
   - If action: execute function, capture output, send to `OutputPanel`
5. Back navigation: pop menu stack, restore previous state

### Message Types

| Message | Source | Handler | Purpose |
|---|---|---|---|
| `MenuItemSelected` | `MenuListPanel` | `MenuApp` | User selected a menu item |
| `SidebarItemSelected` | `MenuSidebar` | `MenuApp` | User clicked sidebar node |
| `BreadcrumbNavigate` | `BreadcrumbBar` | `MenuApp` | User clicked breadcrumb segment |
| `SearchChanged` | `SearchBar` | `MenuListPanel` | Filter text updated |
| `MenuChanged` | `MenuApp` | All widgets | Current menu changed, update display |

---

## Backward Compatibility

### Python API — Unchanged

```python
from pymenu_cli.pymenu import load_menu

menu = load_menu("menu.json", "actions.py")
menu.display()           # Launches TUI (new default)
menu.display(classic=True)  # Old input() mode
```

### CLI — Unchanged + New Flags

```bash
# Existing usage works unchanged
pymenu-cli --menu menu.json --actions actions.py

# New optional flags
pymenu-cli --menu menu.json --actions actions.py --classic      # Old input() mode
pymenu-cli --menu menu.json --actions actions.py --theme light  # Start in light theme
```

### JSON Format — Unchanged

All existing JSON files work without modification. The only addition is the optional `"style"` field in `banner`, which existing files don't have (they use `"font"`, which maps to `"figlet"` automatically).

### What Changes for Users

- `pip install pymenu-cli` pulls `textual` instead of `colorama` directly
- `display()` launches a full TUI instead of a numbered list
- Python 3.8 is no longer supported (3.9+ required)

### What Doesn't Change

- `load_menu()` function signature and return type
- JSON schema (all existing fields honored)
- Action module format (plain Python functions)
- CLI command name (`pymenu-cli`) and required arguments (`--menu`, `--actions`)

---

## Packaging

### pyproject.toml

Replace `setup.py` and `requirements.txt` with a single `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pymenu-cli"
version = "2.0.0"
description = "A simple yet powerful Python library for creating interactive CLI menus"
readme = "README.md"
license = "MIT"
requires-python = ">=3.9"
authors = [
    { name = "Moraneus", email = "moraneus@gmail.com" }
]
dependencies = [
    "textual>=0.50.0",
    "pyfiglet>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio",
    "textual-dev",
]

[project.scripts]
pymenu-cli = "pymenu_cli.pymenu:main"

[project.urls]
Homepage = "https://github.com/moraneus/pymenu-cli"
Repository = "https://github.com/moraneus/pymenu-cli"
```

### Files Removed

- `setup.py` — replaced by `pyproject.toml`
- `requirements.txt` — replaced by `pyproject.toml` dependency sections

### CI Updates

- GitHub Actions matrix: Python 3.9, 3.10, 3.11, 3.12, 3.13
- Install via `pip install -e ".[dev]"` instead of `pip install -r requirements.txt`

---

## Testing Strategy

### Existing Tests

Existing tests in `tests/` are preserved and updated to work with the new structure:
- `test_menu.py` — Menu model tests (unchanged logic, updated imports if needed)
- `test_menu_item.py` — MenuItem model tests (unchanged)
- `test_pymenu.py` — CLI and loader tests (updated for new flags)

### New Tests

**Widget tests** (using Textual's `pilot` testing framework):
- `test_app.py` — MenuApp lifecycle: mount, compose, theme toggle, quit
- `test_sidebar.py` — Sidebar rendering, highlight, click navigation
- `test_menu_list.py` — Cursor movement, item selection, filtering
- `test_breadcrumb.py` — Path rendering, segment click navigation
- `test_search_bar.py` — Focus, typing, filter dispatch, clear
- `test_output_panel.py` — Output capture, scrolling, error display
- `test_classic.py` — Classic mode still works with input() mocking
- `test_banner.py` — All 5 banner styles render correctly

### Testing Approach

- Textual provides `app.run_test()` and the `Pilot` class for headless widget testing
- `pytest-asyncio` for async test support
- Action output capture tested by redirecting stdout in tests
- Classic mode tested with existing mock-based approach
