# pymenu-cli v2.0 TUI Modernization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform pymenu-cli from an `input()`-based numbered menu into a full Textual TUI application with sidebar, breadcrumbs, search, theming, and action output panel — while keeping the existing JSON format, Python API, and CLI fully backward compatible.

**Architecture:** Monolithic `MenuApp(textual.app.App)` composed of custom widgets (sidebar, menu list, breadcrumb, search bar, output panel). The existing `Menu`/`MenuItem` models keep their public interface. The current `display()` loop moves to `classic.py` behind a `--classic` flag. Textual CSS files handle theming.

**Tech Stack:** Python 3.9+, Textual (TUI framework), pyfiglet (FIGlet banners), Rich (included via Textual), pytest + pytest-asyncio (testing), hatchling (build)

**Spec:** `docs/superpowers/specs/2026-04-12-tui-modernization-design.md`

---

## File Structure

```
pymenu_cli/
├── __init__.py              # Modify: export load_menu, MenuApp
├── app.py                   # Create: MenuApp(textual.app.App)
├── classic.py               # Create: classic input() display loop
├── pymenu.py                # Modify: add --classic, --theme flags
├── models/
│   ├── __init__.py          # Keep
│   ├── menu.py              # Modify: display() delegates to TUI or classic
│   └── menu_item.py         # Keep unchanged
├── widgets/
│   ├── __init__.py          # Create
│   ├── sidebar.py           # Create: MenuSidebar widget
│   ├── menu_list.py         # Create: MenuListPanel widget
│   ├── breadcrumb.py        # Create: BreadcrumbBar widget
│   ├── search_bar.py        # Create: SearchBar widget
│   └── output_panel.py      # Create: OutputPanel widget
├── themes/
│   ├── __init__.py          # Create
│   ├── dark.tcss            # Create: dark theme CSS
│   └── light.tcss           # Create: light theme CSS
├── banner.py                # Create: banner rendering (5 styles)
└── ui/
    ├── __init__.py          # Keep
    └── styles.py            # Keep for backward compat
pyproject.toml               # Create: replaces setup.py + requirements.txt
tests/
├── test_menu.py             # Modify: update for new display() signature
├── test_menu_item.py        # Keep unchanged
├── test_pymenu.py           # Modify: add --classic, --theme flag tests
├── test_classic.py          # Create: classic mode tests
├── test_banner.py           # Create: banner style tests
├── test_app.py              # Create: MenuApp TUI tests
├── test_sidebar.py          # Create: sidebar widget tests
├── test_menu_list.py        # Create: menu list widget tests
├── test_breadcrumb.py       # Create: breadcrumb widget tests
├── test_search_bar.py       # Create: search bar widget tests
└── test_output_panel.py     # Create: output panel widget tests
.github/workflows/
├── pytest.yml               # Modify: Python 3.9-3.13, pip install -e ".[dev]"
└── pylint.yml               # Modify: Python 3.9-3.13, pip install -e ".[dev]"
```

---

### Task 1: Modernize Packaging

**Files:**
- Create: `pyproject.toml`
- Delete: `setup.py`
- Delete: `requirements.txt`
- Modify: `.github/workflows/pytest.yml`
- Modify: `.github/workflows/pylint.yml`
- Modify: `.gitignore`

- [ ] **Step 1: Create pyproject.toml**

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
keywords = ["cli", "menu", "tui", "terminal", "interactive"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "textual>=0.50.0",
    "pyfiglet>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "textual-dev>=1.0",
    "pylint>=3.0",
]

[project.scripts]
pymenu-cli = "pymenu_cli.pymenu:main"

[project.urls]
Homepage = "https://github.com/moraneus/pymenu-cli"
Repository = "https://github.com/moraneus/pymenu-cli"

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

- [ ] **Step 2: Delete setup.py and requirements.txt**

```bash
rm setup.py requirements.txt
```

- [ ] **Step 3: Update .github/workflows/pytest.yml**

Replace the full file with:

```yaml
name: Pytest

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    - name: Run tests with pytest
      run: |
        pytest
```

- [ ] **Step 4: Update .github/workflows/pylint.yml**

Replace the full file with:

```yaml
name: Pylint

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    - name: Analyse the code with Pylint
      run: |
        pylint $(git ls-files '*.py' ':!examples/**' ':!tests/**')
```

- [ ] **Step 5: Add `.superpowers/` to .gitignore**

Append to `.gitignore`:

```
.superpowers/
```

- [ ] **Step 6: Install the project in dev mode and verify**

```bash
pip install -e ".[dev]"
pytest
```

Expected: All existing tests pass. If any tests fail due to import issues from removing `setup.py`, note them — they'll be fixed in later tasks.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml .github/workflows/pytest.yml .github/workflows/pylint.yml .gitignore
git rm setup.py requirements.txt
git commit -m "build: replace setup.py with pyproject.toml, update CI to Python 3.9-3.13"
```

---

### Task 2: Extract Classic Display Mode

Move the existing `input()`-based display loop from `Menu.display()` into `classic.py` so it's preserved behind the `--classic` flag.

**Files:**
- Create: `pymenu_cli/classic.py`
- Create: `tests/test_classic.py`
- Modify: `pymenu_cli/models/menu.py`

- [ ] **Step 1: Write the failing test for classic display**

Create `tests/test_classic.py`:

```python
"""Tests for the classic input()-based display mode."""

from unittest.mock import Mock

from pymenu_cli.classic import classic_display
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


def test_classic_display_action(monkeypatch):
    """Test that classic_display executes an action when selected."""
    actions = Mock()
    mock_action = Mock()
    actions.action1 = mock_action

    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Item 1", i_action="action1"))

    user_inputs = iter(["1", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)

    mock_action.assert_called_once()


def test_classic_display_submenu(monkeypatch):
    """Test that classic_display navigates into a submenu."""
    actions = Mock()
    submenu = Menu("Submenu", i_config={"actions": actions})
    submenu.add_item(MenuItem("Sub Item", i_action="sub_action"))
    actions.sub_action = Mock()

    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Go to submenu", i_submenu=submenu))

    user_inputs = iter(["1", "1", "B", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)

    actions.sub_action.assert_called_once()


def test_classic_display_back(monkeypatch):
    """Test that classic_display returns on 'B' input."""
    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    monkeypatch.setattr("builtins.input", lambda _: "B")

    classic_display(menu)
    # If we reach here without hanging, the back command worked


def test_classic_display_exit(monkeypatch):
    """Test that classic_display exits on 'X' input."""
    import pytest

    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    monkeypatch.setattr("builtins.input", lambda _: "X")

    with pytest.raises(SystemExit):
        classic_display(menu)


def test_classic_display_invalid_input(monkeypatch):
    """Test that classic_display handles invalid input gracefully."""
    menu = Menu("Test Menu")
    menu.add_item(MenuItem("Item 1"))

    user_inputs = iter(["invalid", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    classic_display(menu)
    # No crash means invalid input was handled
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_classic.py -v
```

Expected: FAIL — `ImportError: cannot import name 'classic_display' from 'pymenu_cli.classic'`

- [ ] **Step 3: Create pymenu_cli/classic.py**

```python
"""Classic input()-based menu display mode.

This module preserves the original pymenu-cli v1.x display behavior.
Activated via the --classic CLI flag or display(classic=True).
"""

import subprocess
import sys
from typing import Optional

from pymenu_cli.ui.styles import Styles, TextColors, BackgroundColors


def _clear_screen() -> None:
    """Clear the terminal screen."""
    import platform
    cmd = "cls" if platform.system() == "Windows" else "clear"
    subprocess.run([cmd], shell=False, check=False)


def classic_display(menu) -> None:
    """Display a menu using the classic input() loop.

    Args:
        menu: A Menu instance to display.
    """
    while True:
        _clear_screen()

        if menu.banner:
            _print_banner(menu.banner)

        title_color = _get_color_string(menu.color)
        print(f"\n{title_color}{menu.title}{Styles.RESET_ALL}\n")

        for i, item in enumerate(menu.items, start=1):
            item_color = _get_color_string(item.color)
            print(f"{i}. {item_color}{item.title}{Styles.RESET_ALL}")

        print("\nB. Back")
        print("X. Exit")

        choice = input("\nEnter your choice: ").upper()

        if choice == 'B':
            return
        if choice == 'X':
            sys.exit()
        try:
            index = int(choice) - 1
            if 0 <= index < len(menu.items):
                selected_item = menu.items[index]
                if selected_item.submenu:
                    classic_display(selected_item.submenu)
                elif selected_item.action:
                    getattr(menu.actions, selected_item.action)()
            else:
                raise ValueError
        except (ValueError, IndexError):
            input("\nInvalid choice. Press Enter to try again.")


def _print_banner(banner: dict) -> None:
    """Print an ASCII art banner using the art library (v1 compat)."""
    try:
        import art
        banner_text = banner.get('title', '')
        banner_font = banner.get('font', 'standard')
        result = art.text2art(banner_text, font=banner_font, chr_ignore=True)
        print(result)
    except ImportError:
        # art is no longer a required dependency; just print the title
        print(banner.get('title', ''))


def _get_color_string(color: Optional[dict]) -> str:
    """Get the ANSI color string for classic mode display."""
    if color:
        text_color = getattr(TextColors, color.get('text', 'WHITE').upper())
        background_color = getattr(BackgroundColors, color.get('background', 'BLACK').upper())
        return f"{text_color}{background_color}"
    return ""
```

- [ ] **Step 4: Run classic tests to verify they pass**

```bash
pytest tests/test_classic.py -v
```

Expected: All 5 tests PASS.

- [ ] **Step 5: Update Menu.display() to support classic mode**

Modify `pymenu_cli/models/menu.py`:

Replace the imports at the top. Remove `import os`, `import sys`, `import art`, and `from pymenu_cli.ui.styles import Styles, TextColors, BackgroundColors`. The new imports:

```python
from typing import Optional, List, Dict
from pymenu_cli.models.menu_item import MenuItem
```

Replace the `display` method (lines 100-135):

```python
    def display(self, classic: bool = False, theme: str = "dark") -> None:
        """Display the menu.

        Args:
            classic: If True, use the classic input() display mode.
            theme: Theme name ('dark' or 'light'). Only used in TUI mode.
        """
        if classic:
            from pymenu_cli.classic import classic_display
            classic_display(self)
            return
        # TUI mode — will be implemented in Task 6
        # For now, fall back to classic
        from pymenu_cli.classic import classic_display
        classic_display(self)
```

Replace the `print_banner` method (lines 137-142):

```python
    def print_banner(self) -> None:
        """Print the banner. Delegates to classic module."""
        from pymenu_cli.classic import _print_banner
        if self.__m_banner:
            _print_banner(self.__m_banner)
```

Replace the `get_color_string` static method (lines 144-158):

```python
    @staticmethod
    def get_color_string(color) -> str:
        """Get the color string for the given color settings."""
        from pymenu_cli.classic import _get_color_string
        return _get_color_string(color)
```

- [ ] **Step 6: Run all existing tests to verify backward compat**

```bash
pytest -v
```

Expected: All existing tests in `test_menu.py`, `test_menu_item.py`, `test_pymenu.py`, and `test_classic.py` pass. The `test_menu_print_banner` test may need a minor update since we changed the import — if it patches `art.text2art`, it should still work because `classic.py` imports `art` inline.

- [ ] **Step 7: Commit**

```bash
git add pymenu_cli/classic.py tests/test_classic.py pymenu_cli/models/menu.py
git commit -m "refactor: extract classic display mode to classic.py, add classic=True flag"
```

---

### Task 3: Banner Rendering System

Implement the 5 banner styles (rich, box, figlet, gradient, emoji) using Rich/Textual and pyfiglet.

**Files:**
- Create: `pymenu_cli/banner.py`
- Create: `tests/test_banner.py`

- [ ] **Step 1: Write failing tests for banner rendering**

Create `tests/test_banner.py`:

```python
"""Tests for the banner rendering system."""

from pymenu_cli.banner import render_banner


def test_render_banner_rich():
    """Test rich styled text banner."""
    config = {"title": "My App", "style": "rich"}
    result = render_banner(config)
    assert "My App" in result.plain


def test_render_banner_rich_with_subtitle():
    """Test rich banner with subtitle."""
    config = {"title": "My App", "style": "rich", "subtitle": "v1.0"}
    result = render_banner(config)
    assert "My App" in result.plain
    assert "v1.0" in result.plain


def test_render_banner_box():
    """Test box-drawing banner."""
    config = {"title": "My App", "style": "box"}
    result = render_banner(config)
    text = result.plain
    assert "My App" in text
    assert "╔" in text
    assert "╗" in text


def test_render_banner_figlet():
    """Test FIGlet banner."""
    config = {"title": "Hi", "style": "figlet", "font": "standard"}
    result = render_banner(config)
    # FIGlet output is multi-line and taller than the input
    assert len(result.plain.strip().split("\n")) > 1


def test_render_banner_figlet_backward_compat():
    """Test that old format (font without style) defaults to figlet."""
    config = {"title": "Hi", "font": "standard"}
    result = render_banner(config)
    assert len(result.plain.strip().split("\n")) > 1


def test_render_banner_gradient():
    """Test gradient banner."""
    config = {"title": "My App", "style": "gradient", "colors": ["red", "blue"]}
    result = render_banner(config)
    assert "My App" in result.plain


def test_render_banner_gradient_default_colors():
    """Test gradient banner with default colors."""
    config = {"title": "My App", "style": "gradient"}
    result = render_banner(config)
    assert "My App" in result.plain


def test_render_banner_emoji():
    """Test emoji banner."""
    config = {"title": "My App", "style": "emoji", "icon": "🚀"}
    result = render_banner(config)
    assert "My App" in result.plain
    assert "🚀" in result.plain


def test_render_banner_emoji_default_icon():
    """Test emoji banner with default icon."""
    config = {"title": "My App", "style": "emoji"}
    result = render_banner(config)
    assert "My App" in result.plain


def test_render_banner_no_style_no_font():
    """Test banner with just a title falls back to rich style."""
    config = {"title": "My App"}
    result = render_banner(config)
    assert "My App" in result.plain


def test_render_banner_empty_config():
    """Test banner with empty config returns empty."""
    result = render_banner({})
    assert result.plain.strip() == ""


def test_render_banner_none():
    """Test banner with None returns empty."""
    result = render_banner(None)
    assert result.plain.strip() == ""
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_banner.py -v
```

Expected: FAIL — `ImportError: cannot import name 'render_banner' from 'pymenu_cli.banner'`

- [ ] **Step 3: Implement banner.py**

Create `pymenu_cli/banner.py`:

```python
"""Banner rendering system for pymenu-cli.

Supports 5 banner styles, all using Rich Text objects:
- rich: Bold styled text with optional subtitle
- box: Unicode box-drawing frame
- figlet: Large FIGlet text via pyfiglet
- gradient: Color gradient across text
- emoji: Emoji icon + styled text
"""

from __future__ import annotations

from rich.text import Text


def render_banner(config: dict | None) -> Text:
    """Render a banner from configuration.

    Args:
        config: Banner configuration dict with 'title' and optional
                'style', 'subtitle', 'font', 'colors', 'icon' keys.
                If None or empty, returns empty Text.

    Returns:
        Rich Text object containing the rendered banner.
    """
    if not config or not config.get("title"):
        return Text("")

    style = config.get("style")
    if style is None and config.get("font"):
        style = "figlet"
    elif style is None:
        style = "rich"

    renderers = {
        "rich": _render_rich,
        "box": _render_box,
        "figlet": _render_figlet,
        "gradient": _render_gradient,
        "emoji": _render_emoji,
    }

    renderer = renderers.get(style, _render_rich)
    return renderer(config)


def _render_rich(config: dict) -> Text:
    """Render a bold styled text banner."""
    title = config["title"]
    subtitle = config.get("subtitle", "")

    result = Text()
    result.append(f"◆ {title}", style="bold")
    if subtitle:
        result.append(f"  {subtitle}", style="dim")
    return result


def _render_box(config: dict) -> Text:
    """Render a box-drawing framed banner."""
    title = config["title"]
    subtitle = config.get("subtitle", "")
    padding = 4
    width = len(title) + padding * 2

    result = Text()
    result.append(f"╔{'═' * width}╗\n")
    result.append(f"║{' ' * padding}{title}{' ' * padding}║\n")
    result.append(f"╚{'═' * width}╝")
    if subtitle:
        result.append(f"\n{subtitle}", style="dim")
    return result


def _render_figlet(config: dict) -> Text:
    """Render a FIGlet banner using pyfiglet."""
    import pyfiglet

    title = config["title"]
    font = config.get("font", "standard")
    subtitle = config.get("subtitle", "")

    figlet_text = pyfiglet.figlet_format(title, font=font)
    result = Text(figlet_text.rstrip())
    if subtitle:
        result.append(f"\n{subtitle}", style="dim")
    return result


def _render_gradient(config: dict) -> Text:
    """Render a gradient-colored banner."""
    title = config["title"]
    colors = config.get("colors", ["red", "magenta"])
    subtitle = config.get("subtitle", "")

    if len(colors) < 2:
        colors = ["red", "magenta"]

    result = Text()
    steps = max(len(title) - 1, 1)
    for i, char in enumerate(title):
        ratio = i / steps
        if ratio < 0.5:
            result.append(char, style=f"bold {colors[0]}")
        else:
            result.append(char, style=f"bold {colors[1]}")

    if subtitle:
        result.append(f"\n{subtitle}", style="dim")
    return result


def _render_emoji(config: dict) -> Text:
    """Render an emoji + styled text banner."""
    title = config["title"]
    icon = config.get("icon", "◆")
    subtitle = config.get("subtitle", "")

    result = Text()
    result.append(f"{icon} ", style="bold")
    result.append(title, style="bold")
    if subtitle:
        result.append(f"  {subtitle}", style="dim")
    return result
```

- [ ] **Step 4: Run banner tests to verify they pass**

```bash
pytest tests/test_banner.py -v
```

Expected: All 13 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add pymenu_cli/banner.py tests/test_banner.py
git commit -m "feat: add banner rendering system with 5 styles (rich, box, figlet, gradient, emoji)"
```

---

### Task 4: Textual Theme Files

Create the dark and light Textual CSS themes.

**Files:**
- Create: `pymenu_cli/themes/__init__.py`
- Create: `pymenu_cli/themes/dark.tcss`
- Create: `pymenu_cli/themes/light.tcss`

- [ ] **Step 1: Create themes package**

Create `pymenu_cli/themes/__init__.py`:

```python
"""Textual CSS themes for pymenu-cli."""
```

- [ ] **Step 2: Create dark.tcss**

Create `pymenu_cli/themes/dark.tcss`:

```css
/* pymenu-cli Dark Theme */

Screen {
    background: #1a1a2e;
}

#header {
    dock: top;
    height: auto;
    background: #16213e;
    color: #e94560;
    padding: 0 1;
}

#breadcrumb {
    dock: top;
    height: 1;
    background: #1a1a3e;
    color: #888888;
    padding: 0 1;
}

#sidebar {
    width: 30;
    background: #16213e;
    border-right: solid #0f3460;
    padding: 1 0;
}

#sidebar .sidebar-label {
    color: #555555;
    text-style: bold;
    padding: 0 1;
}

#sidebar .sidebar-item {
    color: #e0e0e0;
    padding: 0 1;
}

#sidebar .sidebar-item.--active {
    background: #0f3460;
    color: #e94560;
}

#menu-panel {
    background: #1a1a2e;
    padding: 1;
}

#search-bar {
    dock: top;
    height: 3;
    background: #16213e;
    border: solid #0f3460;
    margin: 0 0 1 0;
}

#search-bar Input {
    background: #16213e;
    color: #e0e0e0;
    border: none;
}

.menu-item {
    height: 3;
    padding: 0 1;
    color: #e0e0e0;
    background: #1a1a2e;
}

.menu-item.--highlighted {
    background: #e94560;
    color: #ffffff;
}

.menu-item .item-indicator {
    color: #555555;
}

.menu-item.--highlighted .item-indicator {
    color: #ffffff;
}

#output-panel {
    height: 1fr;
    max-height: 12;
    background: #0d1117;
    border-top: solid #0f3460;
    padding: 1;
}

#output-panel .output-label {
    color: #555555;
    text-style: bold;
}

#output-panel .output-success {
    color: #4ec9b0;
}

#output-panel .output-error {
    color: #e94560;
}

Footer {
    background: #16213e;
    color: #888888;
}

Footer > .footer--key {
    background: #0f3460;
    color: #e94560;
}
```

- [ ] **Step 3: Create light.tcss**

Create `pymenu_cli/themes/light.tcss`:

```css
/* pymenu-cli Light Theme */

Screen {
    background: #fafafa;
}

#header {
    dock: top;
    height: auto;
    background: #e8e8e8;
    color: #c0392b;
    padding: 0 1;
}

#breadcrumb {
    dock: top;
    height: 1;
    background: #f0f0f0;
    color: #999999;
    padding: 0 1;
}

#sidebar {
    width: 30;
    background: #f0f0f0;
    border-right: solid #dddddd;
    padding: 1 0;
}

#sidebar .sidebar-label {
    color: #999999;
    text-style: bold;
    padding: 0 1;
}

#sidebar .sidebar-item {
    color: #333333;
    padding: 0 1;
}

#sidebar .sidebar-item.--active {
    background: #e0e0e0;
    color: #c0392b;
}

#menu-panel {
    background: #fafafa;
    padding: 1;
}

#search-bar {
    dock: top;
    height: 3;
    background: #f0f0f0;
    border: solid #dddddd;
    margin: 0 0 1 0;
}

#search-bar Input {
    background: #f0f0f0;
    color: #333333;
    border: none;
}

.menu-item {
    height: 3;
    padding: 0 1;
    color: #333333;
    background: #fafafa;
}

.menu-item.--highlighted {
    background: #c0392b;
    color: #ffffff;
}

.menu-item .item-indicator {
    color: #999999;
}

.menu-item.--highlighted .item-indicator {
    color: #ffffff;
}

#output-panel {
    height: 1fr;
    max-height: 12;
    background: #f5f5f5;
    border-top: solid #dddddd;
    padding: 1;
}

#output-panel .output-label {
    color: #999999;
    text-style: bold;
}

#output-panel .output-success {
    color: #27ae60;
}

#output-panel .output-error {
    color: #c0392b;
}

Footer {
    background: #e8e8e8;
    color: #999999;
}

Footer > .footer--key {
    background: #dddddd;
    color: #c0392b;
}
```

- [ ] **Step 4: Commit**

```bash
git add pymenu_cli/themes/
git commit -m "feat: add dark and light Textual CSS themes"
```

---

### Task 5: TUI Widgets

Build all 5 custom Textual widgets. Each widget is self-contained with its own test file.

**Files:**
- Create: `pymenu_cli/widgets/__init__.py`
- Create: `pymenu_cli/widgets/sidebar.py`
- Create: `pymenu_cli/widgets/menu_list.py`
- Create: `pymenu_cli/widgets/breadcrumb.py`
- Create: `pymenu_cli/widgets/search_bar.py`
- Create: `pymenu_cli/widgets/output_panel.py`
- Create: `tests/test_sidebar.py`
- Create: `tests/test_menu_list.py`
- Create: `tests/test_breadcrumb.py`
- Create: `tests/test_search_bar.py`
- Create: `tests/test_output_panel.py`

#### 5A: Sidebar Widget

- [ ] **Step 1: Write failing sidebar tests**

Create `tests/test_sidebar.py`:

```python
"""Tests for the MenuSidebar widget."""

from textual.app import App, ComposeResult

from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.widgets.sidebar import MenuSidebar


def _make_menu():
    """Create a test menu hierarchy."""
    root = Menu("Main Menu")
    sub1 = Menu("Settings")
    sub1.add_item(MenuItem("Display", i_action="display_settings"))
    sub1.add_item(MenuItem("Audio", i_action="audio_settings"))

    root.add_item(MenuItem("Files", i_action="open_files"))
    root.add_item(MenuItem("Settings", i_submenu=sub1))
    root.add_item(MenuItem("Help", i_action="show_help"))
    return root


class SidebarTestApp(App):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu

    def compose(self) -> ComposeResult:
        yield MenuSidebar(self.menu)


async def test_sidebar_renders_tree():
    """Test that the sidebar renders the menu tree."""
    menu = _make_menu()
    app = SidebarTestApp(menu)
    async with app.run_test() as pilot:
        sidebar = app.query_one(MenuSidebar)
        assert sidebar is not None


async def test_sidebar_shows_root_items():
    """Test that root menu items appear in the sidebar."""
    menu = _make_menu()
    app = SidebarTestApp(menu)
    async with app.run_test() as pilot:
        sidebar = app.query_one(MenuSidebar)
        tree = sidebar.query_one("Tree")
        assert tree.root.data == menu
```

- [ ] **Step 2: Run to verify they fail**

```bash
pytest tests/test_sidebar.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'pymenu_cli.widgets'`

- [ ] **Step 3: Create widgets package and sidebar**

Create `pymenu_cli/widgets/__init__.py`:

```python
"""Textual widgets for pymenu-cli TUI."""
```

Create `pymenu_cli/widgets/sidebar.py`:

```python
"""Sidebar widget displaying the menu tree hierarchy."""

from textual.widgets import Tree
from textual.containers import Vertical
from textual.message import Message
from textual import on


class MenuSidebar(Vertical):
    """A sidebar that displays the full menu tree.

    Posts SidebarItemSelected when a tree node representing a menu is clicked.
    """

    class SidebarItemSelected(Message):
        """Posted when a sidebar menu node is selected."""
        def __init__(self, menu) -> None:
            super().__init__()
            self.menu = menu

    DEFAULT_CSS = """
    MenuSidebar {
        width: 30;
        dock: left;
    }
    """

    def __init__(self, root_menu) -> None:
        super().__init__(id="sidebar")
        self.root_menu = root_menu
        self._active_menu = root_menu

    def compose(self):
        tree = Tree(self.root_menu.title, id="sidebar-tree")
        tree.root.data = self.root_menu
        self._build_tree(tree.root, self.root_menu)
        tree.root.expand()
        yield tree

    def _build_tree(self, node, menu) -> None:
        """Recursively build the tree from menu structure."""
        for item in menu.items:
            if item.submenu:
                child = node.add(item.title, data=item.submenu)
                self._build_tree(child, item.submenu)
            else:
                node.add_leaf(item.title, data=item)

    def set_active(self, menu) -> None:
        """Highlight the given menu in the tree."""
        self._active_menu = menu

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node click."""
        from pymenu_cli.models.menu import Menu
        if isinstance(event.node.data, Menu):
            self.post_message(self.SidebarItemSelected(event.node.data))
```

- [ ] **Step 4: Run sidebar tests**

```bash
pytest tests/test_sidebar.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 5: Commit sidebar**

```bash
git add pymenu_cli/widgets/__init__.py pymenu_cli/widgets/sidebar.py tests/test_sidebar.py
git commit -m "feat: add MenuSidebar widget with tree navigation"
```

#### 5B: Breadcrumb Widget

- [ ] **Step 6: Write failing breadcrumb tests**

Create `tests/test_breadcrumb.py`:

```python
"""Tests for the BreadcrumbBar widget."""

from textual.app import App, ComposeResult

from pymenu_cli.widgets.breadcrumb import BreadcrumbBar


class BreadcrumbTestApp(App):
    def compose(self) -> ComposeResult:
        yield BreadcrumbBar()


async def test_breadcrumb_initial_state():
    """Test that breadcrumb starts empty."""
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        assert bar is not None


async def test_breadcrumb_set_path():
    """Test setting breadcrumb path."""
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        bar.set_path(["Main Menu", "Settings", "Display"])
        await pilot.pause()
        text = bar.render_path()
        assert "Main Menu" in text
        assert "Settings" in text
        assert "Display" in text


async def test_breadcrumb_single_level():
    """Test breadcrumb with single level."""
    app = BreadcrumbTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(BreadcrumbBar)
        bar.set_path(["Main Menu"])
        text = bar.render_path()
        assert "Main Menu" in text
```

- [ ] **Step 7: Create breadcrumb widget**

Create `pymenu_cli/widgets/breadcrumb.py`:

```python
"""Breadcrumb navigation bar widget."""

from textual.widget import Widget
from textual.message import Message
from rich.text import Text


class BreadcrumbBar(Widget):
    """Displays the navigation path as a breadcrumb trail.

    Posts BreadcrumbNavigate when a segment is clicked.
    """

    class BreadcrumbNavigate(Message):
        """Posted when a breadcrumb segment is clicked."""
        def __init__(self, level: int) -> None:
            super().__init__()
            self.level = level

    DEFAULT_CSS = """
    BreadcrumbBar {
        height: 1;
        dock: top;
        padding: 0 1;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="breadcrumb")
        self._path: list[str] = []

    def set_path(self, path: list[str]) -> None:
        """Update the breadcrumb path."""
        self._path = list(path)
        self.refresh()

    def render_path(self) -> str:
        """Return the breadcrumb path as a plain string."""
        return " › ".join(self._path)

    def render(self) -> Text:
        """Render the breadcrumb bar."""
        if not self._path:
            return Text("")
        result = Text("📍 ")
        for i, segment in enumerate(self._path):
            if i > 0:
                result.append(" › ", style="dim")
            if i < len(self._path) - 1:
                result.append(segment, style="dim")
            else:
                result.append(segment, style="bold")
        return result
```

- [ ] **Step 8: Run breadcrumb tests**

```bash
pytest tests/test_breadcrumb.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 9: Commit breadcrumb**

```bash
git add pymenu_cli/widgets/breadcrumb.py tests/test_breadcrumb.py
git commit -m "feat: add BreadcrumbBar widget"
```

#### 5C: Search Bar Widget

- [ ] **Step 10: Write failing search bar tests**

Create `tests/test_search_bar.py`:

```python
"""Tests for the SearchBar widget."""

from textual.app import App, ComposeResult

from pymenu_cli.widgets.search_bar import SearchBar


class SearchBarTestApp(App):
    BINDINGS = [("slash", "focus_search", "Search")]

    def compose(self) -> ComposeResult:
        yield SearchBar()

    def action_focus_search(self):
        self.query_one(SearchBar).focus_input()


async def test_search_bar_renders():
    """Test that search bar renders."""
    app = SearchBarTestApp()
    async with app.run_test() as pilot:
        bar = app.query_one(SearchBar)
        assert bar is not None


async def test_search_bar_posts_message_on_input():
    """Test that typing posts SearchChanged messages."""
    messages = []

    class CapturingApp(App):
        def compose(self) -> ComposeResult:
            yield SearchBar()

        def on_search_bar_search_changed(self, event: SearchBar.SearchChanged):
            messages.append(event.query)

    app = CapturingApp()
    async with app.run_test() as pilot:
        bar = app.query_one(SearchBar)
        bar.focus_input()
        await pilot.press("t", "e", "s", "t")
        await pilot.pause()
        assert len(messages) > 0
```

- [ ] **Step 11: Create search bar widget**

Create `pymenu_cli/widgets/search_bar.py`:

```python
"""Search/filter bar widget for filtering menu items."""

from textual.containers import Horizontal
from textual.widgets import Input
from textual.message import Message
from textual import on


class SearchBar(Horizontal):
    """A search bar that filters menu items in real-time.

    Posts SearchChanged on each keystroke with the current query text.
    """

    class SearchChanged(Message):
        """Posted when the search query changes."""
        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query

    DEFAULT_CSS = """
    SearchBar {
        height: 3;
        dock: top;
        margin: 0 0 1 0;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="search-bar")

    def compose(self):
        yield Input(placeholder="🔍 Type to filter...", id="search-input")

    def focus_input(self) -> None:
        """Focus the search input."""
        self.query_one("#search-input", Input).focus()

    def clear(self) -> None:
        """Clear the search input and post empty query."""
        inp = self.query_one("#search-input", Input)
        inp.value = ""
        self.post_message(self.SearchChanged(""))

    @on(Input.Changed, "#search-input")
    def on_input_changed(self, event: Input.Changed) -> None:
        """Forward input changes as SearchChanged messages."""
        self.post_message(self.SearchChanged(event.value))
```

- [ ] **Step 12: Run search bar tests**

```bash
pytest tests/test_search_bar.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 13: Commit search bar**

```bash
git add pymenu_cli/widgets/search_bar.py tests/test_search_bar.py
git commit -m "feat: add SearchBar widget with real-time filtering"
```

#### 5D: Output Panel Widget

- [ ] **Step 14: Write failing output panel tests**

Create `tests/test_output_panel.py`:

```python
"""Tests for the OutputPanel widget."""

from textual.app import App, ComposeResult

from pymenu_cli.widgets.output_panel import OutputPanel


class OutputTestApp(App):
    def compose(self) -> ComposeResult:
        yield OutputPanel()


async def test_output_panel_renders():
    """Test that output panel renders."""
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        assert panel is not None


async def test_output_panel_append_output():
    """Test appending output to the panel."""
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        panel.append_output("Hello, world!")
        await pilot.pause()


async def test_output_panel_append_error():
    """Test appending error output to the panel."""
    app = OutputTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(OutputPanel)
        panel.append_error("Something went wrong")
        await pilot.pause()
```

- [ ] **Step 15: Create output panel widget**

Create `pymenu_cli/widgets/output_panel.py`:

```python
"""Output panel widget for displaying action stdout/stderr."""

from textual.containers import Vertical
from textual.widgets import RichLog


class OutputPanel(Vertical):
    """A scrollable log panel for action output.

    Captures stdout/stderr from executed actions and displays them.
    Auto-scrolls to the latest output.
    """

    DEFAULT_CSS = """
    OutputPanel {
        height: 1fr;
        max-height: 12;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="output-panel")

    def compose(self):
        yield RichLog(highlight=True, markup=True, id="output-log")

    def append_output(self, text: str) -> None:
        """Append standard output text."""
        log = self.query_one("#output-log", RichLog)
        log.write(text)

    def append_error(self, text: str) -> None:
        """Append error output text in error styling."""
        from rich.text import Text
        log = self.query_one("#output-log", RichLog)
        error_text = Text(text, style="bold red")
        log.write(error_text)

    def append_action_header(self, action_name: str) -> None:
        """Append a header line before action output."""
        from rich.text import Text
        log = self.query_one("#output-log", RichLog)
        header = Text(f"$ {action_name}()", style="bold cyan")
        log.write(header)
```

- [ ] **Step 16: Run output panel tests**

```bash
pytest tests/test_output_panel.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 17: Commit output panel**

```bash
git add pymenu_cli/widgets/output_panel.py tests/test_output_panel.py
git commit -m "feat: add OutputPanel widget for action stdout/stderr"
```

#### 5E: Menu List Widget

- [ ] **Step 18: Write failing menu list tests**

Create `tests/test_menu_list.py`:

```python
"""Tests for the MenuListPanel widget."""

from textual.app import App, ComposeResult
from unittest.mock import Mock

from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.widgets.menu_list import MenuListPanel


def _make_menu():
    """Create a test menu."""
    actions = Mock()
    menu = Menu("Test Menu", i_config={"actions": actions})
    menu.add_item(MenuItem("Item 1", i_action="action1"))
    menu.add_item(MenuItem("Item 2", i_action="action2"))
    menu.add_item(MenuItem("Sub Menu", i_submenu=Menu("Sub")))
    return menu


class MenuListTestApp(App):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu

    def compose(self) -> ComposeResult:
        yield MenuListPanel(self.menu)


async def test_menu_list_renders():
    """Test that menu list renders with items."""
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        assert panel is not None


async def test_menu_list_shows_items():
    """Test that all menu items are displayed."""
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        assert panel.item_count == 3


async def test_menu_list_keyboard_navigation():
    """Test arrow key navigation moves the cursor."""
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        panel.focus()
        assert panel.cursor_index == 0
        await pilot.press("down")
        assert panel.cursor_index == 1
        await pilot.press("down")
        assert panel.cursor_index == 2
        await pilot.press("up")
        assert panel.cursor_index == 1


async def test_menu_list_filter():
    """Test filtering items by search query."""
    menu = _make_menu()
    app = MenuListTestApp(menu)
    async with app.run_test() as pilot:
        panel = app.query_one(MenuListPanel)
        panel.filter_items("Sub")
        await pilot.pause()
        assert panel.visible_item_count == 1
```

- [ ] **Step 19: Create menu list widget**

Create `pymenu_cli/widgets/menu_list.py`:

```python
"""Menu list panel widget for displaying and navigating menu items."""

from textual.message import Message
from textual.reactive import reactive
from textual.containers import Vertical
from rich.text import Text


class MenuListPanel(Vertical, can_focus=True):
    """Displays the current menu's items as a navigable list.

    Posts MenuItemSelected when an item is chosen via Enter or click.
    """

    class MenuItemSelected(Message):
        """Posted when a menu item is selected."""
        def __init__(self, item) -> None:
            super().__init__()
            self.item = item

    DEFAULT_CSS = """
    MenuListPanel {
        height: 1fr;
    }
    """

    cursor_index: reactive[int] = reactive(0)

    def __init__(self, menu) -> None:
        super().__init__(id="menu-panel")
        self.menu = menu
        self._filter_query = ""
        self._filtered_indices: list[int] = []
        self._update_filtered()

    @property
    def item_count(self) -> int:
        """Total number of items in the menu."""
        return len(self.menu.items)

    @property
    def visible_item_count(self) -> int:
        """Number of items visible after filtering."""
        return len(self._filtered_indices)

    def _update_filtered(self) -> None:
        """Update the filtered indices based on query."""
        if not self._filter_query:
            self._filtered_indices = list(range(len(self.menu.items)))
        else:
            query = self._filter_query.lower()
            self._filtered_indices = [
                i for i, item in enumerate(self.menu.items)
                if query in item.title.lower()
            ]
        if self._filtered_indices:
            self.cursor_index = min(self.cursor_index, len(self._filtered_indices) - 1)
        else:
            self.cursor_index = 0

    def filter_items(self, query: str) -> None:
        """Filter menu items by search query."""
        self._filter_query = query
        self._update_filtered()
        self.refresh()

    def set_menu(self, menu) -> None:
        """Switch to displaying a different menu."""
        self.menu = menu
        self._filter_query = ""
        self.cursor_index = 0
        self._update_filtered()
        self.refresh()

    def render(self) -> Text:
        """Render the menu items list."""
        result = Text()
        for list_idx, item_idx in enumerate(self._filtered_indices):
            item = self.menu.items[item_idx]
            is_highlighted = list_idx == self.cursor_index

            if is_highlighted:
                prefix = "❯ "
                style = "bold reverse"
            else:
                prefix = "  "
                style = ""

            result.append(f"{prefix}{item.title}", style=style)

            if item.submenu:
                result.append("  → submenu", style="dim" if not is_highlighted else style)
            elif item.action:
                result.append("  ⚡ action", style="dim" if not is_highlighted else style)

            result.append("\n")

        return result

    def _get_selected_item(self):
        """Get the currently highlighted item."""
        if not self._filtered_indices:
            return None
        idx = self._filtered_indices[self.cursor_index]
        return self.menu.items[idx]

    def key_down(self) -> None:
        """Move cursor down."""
        if self._filtered_indices and self.cursor_index < len(self._filtered_indices) - 1:
            self.cursor_index += 1
            self.refresh()

    def key_up(self) -> None:
        """Move cursor up."""
        if self.cursor_index > 0:
            self.cursor_index -= 1
            self.refresh()

    def key_j(self) -> None:
        """Vim-style down."""
        self.key_down()

    def key_k(self) -> None:
        """Vim-style up."""
        self.key_up()

    def key_enter(self) -> None:
        """Select the highlighted item."""
        item = self._get_selected_item()
        if item:
            self.post_message(self.MenuItemSelected(item))
```

- [ ] **Step 20: Run menu list tests**

```bash
pytest tests/test_menu_list.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 21: Commit menu list**

```bash
git add pymenu_cli/widgets/menu_list.py tests/test_menu_list.py
git commit -m "feat: add MenuListPanel widget with cursor navigation and filtering"
```

---

### Task 6: Main TUI Application

Wire all widgets together into `MenuApp`.

**Files:**
- Create: `pymenu_cli/app.py`
- Create: `tests/test_app.py`
- Modify: `pymenu_cli/models/menu.py` (swap TUI fallback to real app)

- [ ] **Step 1: Write failing app tests**

Create `tests/test_app.py`:

```python
"""Tests for the MenuApp TUI application."""

from unittest.mock import Mock

from pymenu_cli.app import MenuApp
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem


def _make_menu():
    """Create a test menu hierarchy."""
    actions = Mock()
    actions.action1 = Mock()

    root = Menu("Main Menu", i_config={"actions": actions})
    sub = Menu("Settings", i_config={"actions": actions})
    sub.add_item(MenuItem("Display", i_action="action1"))

    root.add_item(MenuItem("Item 1", i_action="action1"))
    root.add_item(MenuItem("Settings", i_submenu=sub))
    return root


async def test_app_launches():
    """Test that MenuApp launches and shows widgets."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        assert app.query_one("#sidebar") is not None
        assert app.query_one("#breadcrumb") is not None
        assert app.query_one("#menu-panel") is not None
        assert app.query_one("#output-panel") is not None


async def test_app_breadcrumb_shows_root():
    """Test that breadcrumb shows root menu title on launch."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        assert "Main Menu" in bar.render_path()


async def test_app_navigate_into_submenu():
    """Test navigating into a submenu via Enter key."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause()

        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        path = bar.render_path()
        assert "Settings" in path


async def test_app_navigate_back():
    """Test navigating back with Escape."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause()

        await pilot.press("escape")
        await pilot.pause()

        from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
        bar = app.query_one(BreadcrumbBar)
        path = bar.render_path()
        assert "Settings" not in path
        assert "Main Menu" in path


async def test_app_quit():
    """Test that Q quits the app."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        await pilot.press("q")


async def test_app_action_execution():
    """Test that selecting an action item runs the action."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        from pymenu_cli.widgets.menu_list import MenuListPanel
        panel = app.query_one(MenuListPanel)
        panel.focus()
        await pilot.press("enter")
        await pilot.pause()

        menu.actions.action1.assert_called_once()


async def test_app_search_focus():
    """Test that / focuses the search bar."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        await pilot.press("slash")
        await pilot.pause()
        from pymenu_cli.widgets.search_bar import SearchBar
        from textual.widgets import Input
        search = app.query_one(SearchBar)
        inp = search.query_one(Input)
        assert inp.has_focus


async def test_app_theme_toggle():
    """Test that T toggles theme."""
    menu = _make_menu()
    app = MenuApp(menu)
    async with app.run_test() as pilot:
        initial_theme = app.current_theme
        await pilot.press("t")
        await pilot.pause()
        assert app.current_theme != initial_theme
```

- [ ] **Step 2: Run to verify they fail**

```bash
pytest tests/test_app.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'pymenu_cli.app'`

- [ ] **Step 3: Create app.py**

Create `pymenu_cli/app.py`:

```python
"""Main TUI application for pymenu-cli."""

import contextlib
import io
import traceback
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from pymenu_cli.banner import render_banner
from pymenu_cli.widgets.sidebar import MenuSidebar
from pymenu_cli.widgets.menu_list import MenuListPanel
from pymenu_cli.widgets.breadcrumb import BreadcrumbBar
from pymenu_cli.widgets.search_bar import SearchBar
from pymenu_cli.widgets.output_panel import OutputPanel

THEMES_DIR = Path(__file__).parent / "themes"


class MenuApp(App):
    """The main pymenu-cli TUI application."""

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "go_back", "Back", show=True),
        Binding("backspace", "go_back", "Back", show=False),
        Binding("slash", "focus_search", "Search", show=True),
        Binding("t", "toggle_theme", "Theme", show=True),
    ]

    CSS_PATH = [
        THEMES_DIR / "dark.tcss",
    ]

    def __init__(self, menu, theme: str = "dark") -> None:
        super().__init__()
        self.root_menu = menu
        self._menu_stack: list = [menu]
        self._cursor_stack: list[int] = [0]
        self._current_theme = theme

    @property
    def current_menu(self):
        """The currently displayed menu."""
        return self._menu_stack[-1]

    @property
    def current_theme(self) -> str:
        """The current theme name."""
        return self._current_theme

    def compose(self) -> ComposeResult:
        """Compose the TUI layout."""
        if self.root_menu.banner:
            banner_text = render_banner(self.root_menu.banner)
            yield Static(banner_text, id="header")
        else:
            yield Static(self.root_menu.title, id="header")

        yield BreadcrumbBar()

        with Horizontal():
            yield MenuSidebar(self.root_menu)
            with Vertical():
                yield SearchBar()
                yield MenuListPanel(self.root_menu)
                yield OutputPanel()

        yield Footer()

    def on_mount(self) -> None:
        """Initialize state after mount."""
        self._update_breadcrumb()
        if self._current_theme == "light":
            self._apply_theme("light")

    def _update_breadcrumb(self) -> None:
        """Update the breadcrumb bar with current navigation path."""
        path = [m.title for m in self._menu_stack]
        self.query_one(BreadcrumbBar).set_path(path)

    def _navigate_to(self, menu) -> None:
        """Navigate into a submenu."""
        panel = self.query_one(MenuListPanel)
        if len(self._cursor_stack) == len(self._menu_stack):
            self._cursor_stack[-1] = panel.cursor_index

        self._menu_stack.append(menu)
        self._cursor_stack.append(0)

        panel.set_menu(menu)
        self.query_one(MenuSidebar).set_active(menu)
        self._update_breadcrumb()

    def _execute_action(self, item) -> None:
        """Execute an action and capture output."""
        output_panel = self.query_one(OutputPanel)
        output_panel.append_action_header(item.action)

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                action_fn = getattr(self.current_menu.actions, item.action)
                action_fn()

            stdout_text = stdout_capture.getvalue()
            stderr_text = stderr_capture.getvalue()

            if stdout_text:
                output_panel.append_output(stdout_text.rstrip())
            if stderr_text:
                output_panel.append_error(stderr_text.rstrip())
            if not stdout_text and not stderr_text:
                output_panel.append_output("✓ Done (no output)")

        except Exception:
            output_panel.append_error(traceback.format_exc())

    # --- Event Handlers ---

    def on_menu_list_panel_menu_item_selected(
        self, event: MenuListPanel.MenuItemSelected
    ) -> None:
        """Handle menu item selection."""
        item = event.item
        if item.submenu:
            self._navigate_to(item.submenu)
        elif item.action:
            self._execute_action(item)

    def on_menu_sidebar_sidebar_item_selected(
        self, event: MenuSidebar.SidebarItemSelected
    ) -> None:
        """Handle sidebar navigation."""
        target_menu = event.menu

        self._menu_stack = [self.root_menu]
        self._cursor_stack = [0]
        self._find_path_to(self.root_menu, target_menu)

        panel = self.query_one(MenuListPanel)
        panel.set_menu(self.current_menu)
        self.query_one(MenuSidebar).set_active(self.current_menu)
        self._update_breadcrumb()

    def _find_path_to(self, current, target) -> bool:
        """Find the navigation path from current to target menu."""
        if current is target:
            return True
        for item in current.items:
            if item.submenu:
                self._menu_stack.append(item.submenu)
                self._cursor_stack.append(0)
                if self._find_path_to(item.submenu, target):
                    return True
                self._menu_stack.pop()
                self._cursor_stack.pop()
        return False

    def on_breadcrumb_bar_breadcrumb_navigate(
        self, event: BreadcrumbBar.BreadcrumbNavigate
    ) -> None:
        """Handle breadcrumb segment click."""
        level = event.level
        if level < len(self._menu_stack):
            self._menu_stack = self._menu_stack[:level + 1]
            self._cursor_stack = self._cursor_stack[:level + 1]

            panel = self.query_one(MenuListPanel)
            panel.set_menu(self.current_menu)
            panel.cursor_index = self._cursor_stack[-1]
            self.query_one(MenuSidebar).set_active(self.current_menu)
            self._update_breadcrumb()

    def on_search_bar_search_changed(
        self, event: SearchBar.SearchChanged
    ) -> None:
        """Handle search query change."""
        self.query_one(MenuListPanel).filter_items(event.query)

    # --- Actions ---

    def action_go_back(self) -> None:
        """Navigate back to parent menu."""
        search = self.query_one(SearchBar)
        from textual.widgets import Input
        inp = search.query_one(Input)
        if inp.has_focus:
            search.clear()
            self.query_one(MenuListPanel).focus()
            return

        if len(self._menu_stack) > 1:
            self._menu_stack.pop()
            self._cursor_stack.pop()

            panel = self.query_one(MenuListPanel)
            panel.set_menu(self.current_menu)
            panel.cursor_index = self._cursor_stack[-1]
            self.query_one(MenuSidebar).set_active(self.current_menu)
            self._update_breadcrumb()

    def action_focus_search(self) -> None:
        """Focus the search bar."""
        self.query_one(SearchBar).focus_input()

    def action_toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        if self._current_theme == "dark":
            self._apply_theme("light")
        else:
            self._apply_theme("dark")

    def _apply_theme(self, theme_name: str) -> None:
        """Apply a theme by loading its CSS."""
        self._current_theme = theme_name
        css_path = THEMES_DIR / f"{theme_name}.tcss"
        if css_path.exists():
            self.stylesheet.read(css_path)
            self.stylesheet.reparse()
            self.refresh(layout=True)
```

- [ ] **Step 4: Run app tests**

```bash
pytest tests/test_app.py -v
```

Expected: Tests pass. Some may need adjustments based on Textual's exact API — fix any issues before proceeding.

- [ ] **Step 5: Update Menu.display() to launch real TUI**

In `pymenu_cli/models/menu.py`, replace the temporary TUI fallback in `display()`:

Replace:
```python
        # TUI mode — will be implemented in Task 6
        # For now, fall back to classic
        from pymenu_cli.classic import classic_display
        classic_display(self)
```

With:
```python
        from pymenu_cli.app import MenuApp
        app = MenuApp(self, theme=theme)
        app.run()
```

- [ ] **Step 6: Run all tests**

```bash
pytest -v
```

Expected: All tests pass across all test files.

- [ ] **Step 7: Commit**

```bash
git add pymenu_cli/app.py tests/test_app.py pymenu_cli/models/menu.py
git commit -m "feat: add MenuApp TUI application, wire all widgets together"
```

---

### Task 7: CLI Flags and Entry Point Updates

Add `--classic` and `--theme` flags to the CLI entry point.

**Files:**
- Modify: `pymenu_cli/pymenu.py`
- Modify: `tests/test_pymenu.py`

- [ ] **Step 1: Write failing tests for new CLI flags**

Add these tests to `tests/test_pymenu.py`:

```python
def test_main_with_classic_flag(tmp_path, monkeypatch):
    """Test that --classic flag uses classic display mode."""
    menu_file = tmp_path / "menu.json"
    actions_file = tmp_path / "actions.py"

    menu_data = {"title": "Main Menu", "items": [{"title": "Item 1"}]}
    with open(menu_file, "w", encoding="utf-8") as f:
        json.dump(menu_data, f)
    with open(actions_file, "w", encoding="utf-8") as f:
        f.write("def action1(): pass")

    with patch.object(Menu, "display") as mock_display:
        monkeypatch.setattr(
            "argparse.ArgumentParser.parse_args",
            lambda self: Mock(
                menu=str(menu_file),
                actions=str(actions_file),
                classic=True,
                theme="dark",
            ),
        )
        main()
        mock_display.assert_called_once_with(classic=True, theme="dark")


def test_main_with_theme_flag(tmp_path, monkeypatch):
    """Test that --theme flag is passed through."""
    menu_file = tmp_path / "menu.json"
    actions_file = tmp_path / "actions.py"

    menu_data = {"title": "Main Menu", "items": [{"title": "Item 1"}]}
    with open(menu_file, "w", encoding="utf-8") as f:
        json.dump(menu_data, f)
    with open(actions_file, "w", encoding="utf-8") as f:
        f.write("def action1(): pass")

    with patch.object(Menu, "display") as mock_display:
        monkeypatch.setattr(
            "argparse.ArgumentParser.parse_args",
            lambda self: Mock(
                menu=str(menu_file),
                actions=str(actions_file),
                classic=False,
                theme="light",
            ),
        )
        main()
        mock_display.assert_called_once_with(classic=False, theme="light")
```

- [ ] **Step 2: Run to verify they fail**

```bash
pytest tests/test_pymenu.py::test_main_with_classic_flag tests/test_pymenu.py::test_main_with_theme_flag -v
```

Expected: FAIL — `display()` doesn't accept `classic` or `theme` args yet via CLI.

- [ ] **Step 3: Update pymenu.py with new flags**

Replace the `main()` function in `pymenu_cli/pymenu.py` (lines 112-132):

```python
def main() -> None:
    """Main function to parse arguments and display the menu."""
    parser = argparse.ArgumentParser(description='pymenu-cli - Create interactive CLI menus')
    parser.add_argument('-m', '--menu', type=str, help='Path to the menu JSON file')
    parser.add_argument('-a', '--actions', type=str, help='Path to the actions Python file')
    parser.add_argument('--classic', action='store_true', default=False,
                        help='Use classic input() display mode')
    parser.add_argument('--theme', type=str, default='dark', choices=['dark', 'light'],
                        help='Color theme (default: dark)')
    args = parser.parse_args()

    if args.menu and args.actions:
        try:
            main_menu = load_menu(args.menu, args.actions)
            main_menu.display(classic=args.classic, theme=args.theme)
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"Error: {str(e)}")
    else:
        parser.print_help()
```

- [ ] **Step 4: Update existing test_main_with_valid_args**

The existing test mocks `parse_args` without the new flags. Update the `monkeypatch.setattr` line in `test_main_with_valid_args`:

```python
        monkeypatch.setattr("argparse.ArgumentParser.parse_args",
                            lambda self: Mock(menu=str(menu_file), actions=str(actions_file),
                                              classic=False, theme="dark"))
```

And update the assertion:

```python
        mock_display.assert_called_once_with(classic=False, theme="dark")
```

- [ ] **Step 5: Run all pymenu tests**

```bash
pytest tests/test_pymenu.py -v
```

Expected: All tests PASS.

- [ ] **Step 6: Commit**

```bash
git add pymenu_cli/pymenu.py tests/test_pymenu.py
git commit -m "feat: add --classic and --theme CLI flags"
```

---

### Task 8: Update __init__.py Exports

Update the package's public API.

**Files:**
- Modify: `pymenu_cli/__init__.py`

- [ ] **Step 1: Update __init__.py**

```python
"""pymenu-cli: Interactive CLI menus from JSON configuration."""

from pymenu_cli.pymenu import load_menu, create_menu_from_data, load_actions_module
from pymenu_cli.models.menu import Menu
from pymenu_cli.models.menu_item import MenuItem
from pymenu_cli.app import MenuApp

__all__ = [
    "load_menu",
    "create_menu_from_data",
    "load_actions_module",
    "Menu",
    "MenuItem",
    "MenuApp",
]
```

- [ ] **Step 2: Verify imports work**

```bash
python -c "from pymenu_cli import load_menu, MenuApp, Menu, MenuItem; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add pymenu_cli/__init__.py
git commit -m "feat: update package exports with MenuApp"
```

---

### Task 9: Update Existing Tests for Compatibility

Fix any existing tests that break due to the refactoring.

**Files:**
- Modify: `tests/test_menu.py`

- [ ] **Step 1: Update test_menu.py imports and patches**

Update `test_menu_print_banner`:

```python
def test_menu_print_banner(capsys):
    """Test that the print_banner method delegates to classic module."""
    menu = Menu("Test Menu", i_config={"banner": {"title": "Banner Text", "font": "standard"}})

    with patch("pymenu_cli.classic.art.text2art", return_value="ASCII_ART"):
        menu.print_banner()
        captured = capsys.readouterr()
        assert captured.out == "ASCII_ART\n"
```

Update `test_menu_display` to use classic mode:

```python
def test_menu_display(monkeypatch):
    """Test that display in classic mode executes actions and submenus."""
    actions = Mock()
    mock_action1 = Mock()
    actions.action1 = mock_action1

    menu = Menu("Test Menu", i_config={"actions": actions})
    item1 = MenuItem("Item 1", i_action="action1")
    item2 = MenuItem("Item 2", i_submenu=Menu("Submenu"))
    menu.add_item(item1)
    menu.add_item(item2)

    user_inputs = iter(["1", "2", "B"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    mock_submenu_display = Mock()
    menu.items[1].submenu.display = mock_submenu_display

    menu.display(classic=True)

    mock_action1.assert_called_once()
    mock_submenu_display.assert_called_once()
```

- [ ] **Step 2: Run all tests**

```bash
pytest -v
```

Expected: All tests PASS across all files.

- [ ] **Step 3: Commit**

```bash
git add tests/test_menu.py
git commit -m "test: update existing tests for refactored display() and banner delegation"
```

---

### Task 10: Update Examples

Update the example JSON files to showcase new banner styles and verify they work.

**Files:**
- Modify: `examples/menus/colored_menu.json`
- Modify: `examples/menus/no_colored_menu.json`

- [ ] **Step 1: Read the no_colored_menu.json**

```bash
cat examples/menus/no_colored_menu.json
```

- [ ] **Step 2: Update colored_menu.json with gradient banner**

Update only the `banner` object at the top of `examples/menus/colored_menu.json`:

```json
{
  "banner": {
    "title": "Pymenu-cli",
    "style": "gradient",
    "colors": ["red", "magenta"],
    "subtitle": "v2.0 — Interactive TUI Menus"
  },
  ...rest stays the same...
}
```

- [ ] **Step 3: Update no_colored_menu.json with emoji banner**

Update the banner (if present) or add one:

```json
{
  "banner": {
    "title": "Pymenu-cli",
    "style": "emoji",
    "icon": "📋"
  },
  ...rest stays the same...
}
```

- [ ] **Step 4: Manual smoke test**

```bash
pymenu-cli --menu examples/menus/colored_menu.json --actions examples/actions/actions.py
```

Expected: Full TUI launches with gradient banner, sidebar, breadcrumbs, all menu items.

```bash
pymenu-cli --menu examples/menus/colored_menu.json --actions examples/actions/actions.py --classic
```

Expected: Classic numbered menu, same as v1.

- [ ] **Step 5: Commit**

```bash
git add examples/menus/colored_menu.json examples/menus/no_colored_menu.json
git commit -m "docs: update example menus with new banner styles"
```

---

### Task 11: Final Integration Test and CI Verification

Run the full test suite, lint check, and verify everything works end-to-end.

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

```bash
pytest -v --tb=short
```

Expected: All tests PASS.

- [ ] **Step 2: Run pylint**

```bash
pylint $(git ls-files '*.py' ':!examples/**' ':!tests/**')
```

Expected: No errors. Warnings are OK but no import errors or undefined names.

- [ ] **Step 3: Verify CLI entry point**

```bash
pymenu-cli --help
```

Expected: Shows help with `--menu`, `--actions`, `--classic`, `--theme` flags.

- [ ] **Step 4: Verify import works**

```bash
python -c "
from pymenu_cli import load_menu, MenuApp, Menu, MenuItem
from pymenu_cli.banner import render_banner
from pymenu_cli.classic import classic_display
print('All imports OK')
"
```

Expected: `All imports OK`

- [ ] **Step 5: Commit any remaining fixes**

```bash
git add -A
git status
# Only commit if there are changes
git commit -m "fix: final integration fixes"
```

- [ ] **Step 6: Create summary commit for the feature**

Review the commit history:

```bash
git log --oneline -15
```

Verify all tasks are captured.
