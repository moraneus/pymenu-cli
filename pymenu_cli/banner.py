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
    title = config["title"]
    subtitle = config.get("subtitle", "")
    result = Text()
    result.append(f"◆ {title}", style="bold")
    if subtitle:
        result.append(f"  {subtitle}", style="dim")
    return result


def _render_box(config: dict) -> Text:
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
    title = config["title"]
    icon = config.get("icon", "◆")
    subtitle = config.get("subtitle", "")
    result = Text()
    result.append(f"{icon} ", style="bold")
    result.append(title, style="bold")
    if subtitle:
        result.append(f"  {subtitle}", style="dim")
    return result
