"""
gui_harness.primitives.template_match — template matching utilities.

Thin wrapper around scripts/template_match.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).parent.parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


def find_template(app_name: str, template_name: str,
                  screen_path: str = None, threshold: float = 0.8) -> dict:
    """Find a template on screen.

    Returns:
        dict with keys: found (bool), x, y, confidence
    """
    import importlib
    tm = importlib.import_module("template_match")
    return tm.find_template(app_name, template_name, screen_path=screen_path,
                            threshold=threshold)


def save_template(app_name: str, template_name: str, region: tuple,
                  click_offset: tuple = None):
    """Save a template from the current screen.

    Args:
        app_name: App name.
        template_name: Template identifier.
        region: (x1, y1, x2, y2) in logical pixels.
        click_offset: (x, y) click offset within template.
    """
    import importlib
    tm = importlib.import_module("template_match")
    tm.save_template(app_name, template_name, region, click_offset=click_offset)


def click_template(app_name: str, template_name: str) -> bool:
    """Find and click a template. Returns True if found and clicked."""
    import importlib
    tm = importlib.import_module("template_match")
    return tm.click_template(app_name, template_name)


def list_templates(app_name: str = None) -> list[dict]:
    """List saved templates."""
    import importlib
    tm = importlib.import_module("template_match")
    return tm.list_templates(app_name)
