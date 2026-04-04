"""
gui_harness.primitives.ocr — Apple Vision OCR.

Thin wrapper around the OCR parts of scripts/ui_detector.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).parent.parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


def detect_text(img_path: str, return_logical: bool = False) -> list[dict]:
    """Detect text using Apple Vision OCR.

    Args:
        img_path: Path to screenshot image.
        return_logical: DEPRECATED. Kept for backwards compatibility.

    Returns:
        List of dicts with keys: type, source, x, y, w, h, cx, cy, confidence, label
    """
    from ui_detector import detect_text as _detect_text
    return _detect_text(img_path, return_logical=return_logical)


def detect_text_from_screen(app_name: str = None, fullscreen: bool = True) -> tuple[list[dict], str]:
    """Take a screenshot and run OCR on it.

    Returns:
        (texts, img_path) — list of text elements and the screenshot path.
    """
    from gui_harness.primitives.screenshot import take, take_window
    if app_name and not fullscreen:
        img_path = take_window(app_name)
    else:
        img_path = take()
    texts = detect_text(img_path)
    return texts, img_path
