"""Main TUI application for pymenu-cli."""

import contextlib
import io
import traceback
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Static

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
        self._app_theme = theme

    @property
    def current_menu(self):
        return self._menu_stack[-1]

    @property
    def app_theme(self) -> str:
        return self._app_theme

    def compose(self) -> ComposeResult:
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
        self._update_breadcrumb()
        if self._app_theme == "light":
            self._apply_theme("light")
        # Focus the menu list so keyboard navigation works immediately
        self.query_one(MenuListPanel).focus()

    def _update_breadcrumb(self) -> None:
        path = [m.title for m in self._menu_stack]
        self.query_one(BreadcrumbBar).set_path(path)

    def _navigate_to(self, menu) -> None:
        panel = self.query_one(MenuListPanel)
        if len(self._cursor_stack) == len(self._menu_stack):
            self._cursor_stack[-1] = panel.cursor_index

        self._menu_stack.append(menu)
        self._cursor_stack.append(0)

        panel.set_menu(menu)
        panel.focus()
        self.query_one(MenuSidebar).set_active(menu)
        self._update_breadcrumb()

    def _execute_action(self, item) -> None:
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
        finally:
            self.query_one(MenuListPanel).focus()

    def on_menu_list_panel_menu_item_selected(self, event: MenuListPanel.MenuItemSelected) -> None:
        item = event.item
        if item.submenu:
            self._navigate_to(item.submenu)
        elif item.action:
            self._execute_action(item)

    def on_menu_sidebar_sidebar_item_selected(self, event: MenuSidebar.SidebarItemSelected) -> None:
        target_menu = event.menu
        self._menu_stack = [self.root_menu]
        self._cursor_stack = [0]
        self._find_path_to(self.root_menu, target_menu)

        panel = self.query_one(MenuListPanel)
        panel.set_menu(self.current_menu)
        self.query_one(MenuSidebar).set_active(self.current_menu)
        self._update_breadcrumb()

    def _find_path_to(self, current, target) -> bool:
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

    def on_breadcrumb_bar_breadcrumb_navigate(self, event: BreadcrumbBar.BreadcrumbNavigate) -> None:
        level = event.level
        if level < len(self._menu_stack):
            self._menu_stack = self._menu_stack[:level + 1]
            self._cursor_stack = self._cursor_stack[:level + 1]

            panel = self.query_one(MenuListPanel)
            panel.set_menu(self.current_menu)
            panel.cursor_index = self._cursor_stack[-1]
            self.query_one(MenuSidebar).set_active(self.current_menu)
            self._update_breadcrumb()

    def on_search_bar_search_changed(self, event: SearchBar.SearchChanged) -> None:
        self.query_one(MenuListPanel).filter_items(event.query)

    def action_go_back(self) -> None:
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
            panel.focus()
            self.query_one(MenuSidebar).set_active(self.current_menu)
            self._update_breadcrumb()

    def action_focus_search(self) -> None:
        self.query_one(SearchBar).focus_input()

    def action_toggle_theme(self) -> None:
        if self._app_theme == "dark":
            self._apply_theme("light")
        else:
            self._apply_theme("dark")

    def _apply_theme(self, theme_name: str) -> None:
        self._app_theme = theme_name
        css_path = THEMES_DIR / f"{theme_name}.tcss"
        if css_path.exists():
            self.stylesheet.read(css_path)
            self.stylesheet.reparse()
            self.refresh(layout=True)
