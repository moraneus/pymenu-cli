"""Real working actions for the pymenu-cli example.

These actions demonstrate practical functionality that works
in both TUI mode (output captured in panel) and classic mode.
"""

import datetime
import json
import os
import platform
import random
import string
import sys
import textwrap
import time

# ─── State ────────────────────────────────────────────────

_clipboard = ""
_workspace_dir = os.path.join(os.path.dirname(__file__), ".workspace")


def _ensure_workspace():
    os.makedirs(_workspace_dir, exist_ok=True)


# ─── File Operations ─────────────────────────────────────

def create_new_file():
    _ensure_workspace()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{timestamp}.txt"
    filepath = os.path.join(_workspace_dir, filename)
    content = f"# New Note\nCreated: {datetime.datetime.now().isoformat()}\n\nWrite your content here.\n"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✓ Created: {filepath}")
    print(f"  Size: {len(content)} bytes")


def open_file():
    _ensure_workspace()
    files = sorted(os.listdir(_workspace_dir))
    if not files:
        print("No files in workspace. Use 'New' to create one first.")
        return
    print(f"Workspace: {_workspace_dir}")
    print(f"{'─' * 50}")
    for i, f in enumerate(files, 1):
        path = os.path.join(_workspace_dir, f)
        size = os.path.getsize(path)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        print(f"  {i}. {f}  ({size}B, modified {mtime:%Y-%m-%d %H:%M})")
    print(f"{'─' * 50}")
    print(f"Total: {len(files)} file(s)")


def save_file():
    _ensure_workspace()
    filepath = os.path.join(_workspace_dir, "quicksave.txt")
    content = f"Quicksave at {datetime.datetime.now().isoformat()}\nClipboard: {_clipboard or '(empty)'}\n"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✓ Saved quicksave.txt ({len(content)} bytes)")


def save_as_text():
    _ensure_workspace()
    filepath = os.path.join(_workspace_dir, "export.txt")
    lines = [
        "pymenu-cli Export",
        "=" * 40,
        f"Date: {datetime.datetime.now().isoformat()}",
        f"Platform: {platform.system()} {platform.release()}",
        f"Python: {sys.version.split()[0]}",
        f"Clipboard: {_clipboard or '(empty)'}",
    ]
    content = "\n".join(lines) + "\n"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✓ Exported as text: {filepath}")


def save_as_json():
    _ensure_workspace()
    filepath = os.path.join(_workspace_dir, "export.json")
    data = {
        "exported_at": datetime.datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "clipboard": _clipboard,
        "workspace_files": os.listdir(_workspace_dir),
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✓ Exported as JSON: {filepath}")
    print(f"  Keys: {', '.join(data.keys())}")


def save_as_xml():
    _ensure_workspace()
    filepath = os.path.join(_workspace_dir, "export.xml")
    content = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <export>
            <timestamp>{datetime.datetime.now().isoformat()}</timestamp>
            <platform>{platform.platform()}</platform>
            <python>{sys.version.split()[0]}</python>
            <clipboard>{_clipboard}</clipboard>
        </export>
    """)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✓ Exported as XML: {filepath}")


def exit_program():
    print("Goodbye!")
    sys.exit(0)


# ─── Edit Operations ─────────────────────────────────────

def cut_text():
    global _clipboard
    _clipboard = f"[cut-{datetime.datetime.now().strftime('%H:%M:%S')}]"
    print(f"✂ Cut to clipboard: {_clipboard}")


def copy_text():
    global _clipboard
    _clipboard = f"Copied content at {datetime.datetime.now().strftime('%H:%M:%S')}"
    print(f"📋 Copied to clipboard: {_clipboard}")


def paste_text():
    if _clipboard:
        print(f"📌 Pasted from clipboard: {_clipboard}")
    else:
        print("Clipboard is empty. Use Copy or Cut first.")


def select_all_text():
    _ensure_workspace()
    files = os.listdir(_workspace_dir)
    total_size = sum(
        os.path.getsize(os.path.join(_workspace_dir, f))
        for f in files
    )
    print(f"Selected all content in workspace:")
    print(f"  Files: {len(files)}")
    print(f"  Total size: {total_size:,} bytes")


# ─── Settings ────────────────────────────────────────────

def open_general_settings():
    print("General Settings")
    print("=" * 40)
    print(f"  Working directory : {os.getcwd()}")
    print(f"  Workspace        : {_workspace_dir}")
    print(f"  Python executable : {sys.executable}")
    print(f"  Python version    : {sys.version.split()[0]}")
    print(f"  Platform          : {platform.system()} {platform.release()}")
    print(f"  Architecture      : {platform.machine()}")
    print(f"  User              : {os.environ.get('USER', 'unknown')}")


def open_advanced_settings():
    print("Advanced Settings")
    print("=" * 40)
    print(f"  PID              : {os.getpid()}")
    print(f"  Encoding         : {sys.getdefaultencoding()}")
    print(f"  Max recursion     : {sys.getrecursionlimit()}")
    print(f"  Path entries      : {len(sys.path)}")
    env_count = len(os.environ)
    print(f"  Environment vars  : {env_count}")
    print(f"  Terminal          : {os.environ.get('TERM', 'unknown')}")
    print(f"  Shell             : {os.environ.get('SHELL', 'unknown')}")


# ─── Plugins ─────────────────────────────────────────────

def install_plugin():
    plugins = ["syntax-highlighter", "auto-formatter", "spell-checker", "git-integration"]
    chosen = random.choice(plugins)
    print(f"Installing plugin: {chosen}")
    for step in ["Downloading", "Verifying", "Extracting", "Configuring"]:
        print(f"  ✓ {step}...")
    print(f"✓ Plugin '{chosen}' installed successfully!")


def manage_plugins():
    plugins = [
        ("syntax-highlighter", "1.2.0", "active"),
        ("auto-formatter", "0.9.1", "active"),
        ("spell-checker", "2.0.3", "disabled"),
        ("git-integration", "1.0.0", "active"),
    ]
    print("Installed Plugins")
    print("=" * 50)
    print(f"  {'Name':<25} {'Version':<10} {'Status'}")
    print(f"  {'─' * 25} {'─' * 10} {'─' * 10}")
    for name, ver, status in plugins:
        icon = "●" if status == "active" else "○"
        print(f"  {icon} {name:<23} {ver:<10} {status}")
    print(f"\n  Total: {len(plugins)} plugins, {sum(1 for _, _, s in plugins if s == 'active')} active")


# ─── Utilities ───────────────────────────────────────────

def perform_backup():
    _ensure_workspace()
    files = os.listdir(_workspace_dir)
    backup_dir = os.path.join(_workspace_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest = {
        "backup_id": timestamp,
        "created": datetime.datetime.now().isoformat(),
        "files": files,
        "file_count": len(files),
    }
    manifest_path = os.path.join(backup_dir, f"backup_{timestamp}.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✓ Backup created: backup_{timestamp}")
    print(f"  Files backed up: {len(files)}")
    print(f"  Manifest: {manifest_path}")


def perform_restore():
    _ensure_workspace()
    backup_dir = os.path.join(_workspace_dir, "backups")
    if not os.path.exists(backup_dir):
        print("No backups found. Run Backup first.")
        return
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith(".json")])
    if not backups:
        print("No backups found. Run Backup first.")
        return
    latest = backups[-1]
    with open(os.path.join(backup_dir, latest)) as f:
        manifest = json.load(f)
    print(f"Latest backup: {manifest['backup_id']}")
    print(f"  Created: {manifest['created']}")
    print(f"  Files: {manifest['file_count']}")
    print(f"  ✓ Restore point available")


# ─── Help ────────────────────────────────────────────────

def open_user_guide():
    print("pymenu-cli User Guide")
    print("=" * 50)
    print()
    print("Navigation:")
    print("  ↑/↓ or j/k  Move through menu items")
    print("  Enter        Select item (enter submenu or run action)")
    print("  Esc          Go back to parent menu")
    print("  /            Search/filter menu items")
    print("  T            Toggle dark/light theme")
    print("  Q            Quit application")
    print()
    print("Mouse:")
    print("  Click        Select menu items or sidebar nodes")
    print("  Scroll       Scroll menu list or output panel")
    print()
    print("Classic Mode:")
    print("  Run with --classic flag for numbered menu input")


def open_faq():
    print("Frequently Asked Questions")
    print("=" * 50)
    print()
    print("Q: How do I create a menu?")
    print("A: Define your menu structure in a JSON file and")
    print("   your actions in a Python file. Then run:")
    print("   pymenu-cli --menu menu.json --actions actions.py")
    print()
    print("Q: Can I use the old-style numbered menus?")
    print("A: Yes! Add the --classic flag to use the v1 style.")
    print()
    print("Q: How do I change the theme?")
    print("A: Press 'T' in the TUI, or start with --theme light")
    print()
    print("Q: What banner styles are available?")
    print("A: rich, box, figlet, gradient, emoji")


def show_about():
    print("pymenu-cli v2.0.0")
    print("=" * 40)
    print()
    print("A Python library for creating interactive")
    print("CLI menus from JSON configuration files.")
    print()
    print("Author  : Moraneus")
    print("License : MIT")
    print("Homepage: github.com/moraneus/pymenu-cli")
    print()
    print(f"Python  : {sys.version.split()[0]}")
    print(f"Platform: {platform.system()} {platform.machine()}")


# ─── Password Generator (bonus utility) ─────────────────

def generate_password():
    length = 16
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    password = "".join(random.choice(chars) for _ in range(length))
    strength = "Strong" if length >= 16 else "Medium"
    print(f"Generated Password ({length} chars, {strength}):")
    print(f"  {password}")


def show_system_info():
    print("System Information")
    print("=" * 50)
    print(f"  OS          : {platform.system()} {platform.release()}")
    print(f"  Machine     : {platform.machine()}")
    print(f"  Processor   : {platform.processor() or 'N/A'}")
    print(f"  Python      : {sys.version.split()[0]}")
    print(f"  Executable  : {sys.executable}")
    print(f"  CWD         : {os.getcwd()}")
    print(f"  Home        : {os.path.expanduser('~')}")
    print(f"  User        : {os.environ.get('USER', 'unknown')}")
