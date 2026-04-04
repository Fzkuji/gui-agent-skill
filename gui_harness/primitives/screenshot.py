"""
gui_harness.primitives.screenshot — screenshot capture utilities.

Thin wrapper around scripts/platform_input.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure scripts/ is importable
_SCRIPTS_DIR = str(Path(__file__).parent.parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


def take(path: str = "/tmp/gui_agent_screen.png") -> str:
    """Take a full-screen screenshot. Returns the file path."""
    from platform_input import screenshot as _screenshot
    return _screenshot(path)


def take_window(app_name: str, out_path: str = None) -> str:
    """Capture a specific app window. Returns the file path."""
    from platform_input import capture_window
    return capture_window(app_name, out_path)


def take_region(out_path: str, x1=None, y1=None, x2=None, y2=None,
                method: str = "auto", **kwargs) -> str:
    """Capture a region of the screen. Returns the file path."""
    from platform_input import screenshot_region
    return screenshot_region(out_path, method=method, x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)


# Re-export original functions for direct access
def fullscreen(path: str = "/tmp/gui_agent_screen.png") -> str:
    """Alias for take()."""
    return take(path)
