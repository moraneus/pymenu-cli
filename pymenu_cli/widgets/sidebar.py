"""Sidebar widget displaying the menu tree hierarchy."""

# pylint: disable=import-outside-toplevel
from textual import on
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Tree


class MenuSidebar(Vertical):
    """A sidebar that displays the full menu tree."""

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
        for item in menu.items:
            if item.submenu:
                child = node.add(item.title, data=item.submenu)
                self._build_tree(child, item.submenu)
            else:
                node.add_leaf(item.title, data=item)

    def set_active(self, menu) -> None:
        """Update the currently active menu reference in the sidebar."""
        self._active_menu = menu

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Post SidebarItemSelected when a menu node is clicked in the tree."""
        from pymenu_cli.models.menu import Menu  # Lazy import to avoid circular dependency

        if isinstance(event.node.data, Menu):
            self.post_message(self.SidebarItemSelected(event.node.data))
