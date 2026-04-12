"""Tests for the banner rendering system."""

from pymenu_cli.banner import render_banner


def test_render_banner_rich():
    config = {"title": "My App", "style": "rich"}
    result = render_banner(config)
    assert "My App" in result.plain

def test_render_banner_rich_with_subtitle():
    config = {"title": "My App", "style": "rich", "subtitle": "v1.0"}
    result = render_banner(config)
    assert "My App" in result.plain
    assert "v1.0" in result.plain

def test_render_banner_box():
    config = {"title": "My App", "style": "box"}
    result = render_banner(config)
    text = result.plain
    assert "My App" in text
    assert "╔" in text
    assert "╗" in text

def test_render_banner_figlet():
    config = {"title": "Hi", "style": "figlet", "font": "standard"}
    result = render_banner(config)
    assert len(result.plain.strip().split("\n")) > 1

def test_render_banner_figlet_backward_compat():
    config = {"title": "Hi", "font": "standard"}
    result = render_banner(config)
    assert len(result.plain.strip().split("\n")) > 1

def test_render_banner_gradient():
    config = {"title": "My App", "style": "gradient", "colors": ["red", "blue"]}
    result = render_banner(config)
    assert "My App" in result.plain

def test_render_banner_gradient_default_colors():
    config = {"title": "My App", "style": "gradient"}
    result = render_banner(config)
    assert "My App" in result.plain

def test_render_banner_emoji():
    config = {"title": "My App", "style": "emoji", "icon": "🚀"}
    result = render_banner(config)
    assert "My App" in result.plain
    assert "🚀" in result.plain

def test_render_banner_emoji_default_icon():
    config = {"title": "My App", "style": "emoji"}
    result = render_banner(config)
    assert "My App" in result.plain

def test_render_banner_no_style_no_font():
    config = {"title": "My App"}
    result = render_banner(config)
    assert "My App" in result.plain

def test_render_banner_empty_config():
    result = render_banner({})
    assert result.plain.strip() == ""

def test_render_banner_none():
    result = render_banner(None)
    assert result.plain.strip() == ""
