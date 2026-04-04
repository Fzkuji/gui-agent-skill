"""
gui_harness.primitives.detector — GPA-GUI-Detector and merged detection.

Thin wrapper around the detection parts of scripts/ui_detector.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).parent.parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


def detect_icons(img_path: str, conf: float = 0.1, iou: float = 0.3) -> tuple[list[dict], int, int]:
    """Detect UI elements using Salesforce/GPA-GUI-Detector.

    Args:
        img_path: Path to screenshot image.
        conf: YOLO confidence threshold.
        iou: YOLO NMS IoU threshold.

    Returns:
        (elements, img_w, img_h) — list of elements in detection-space coords.
    """
    from ui_detector import detect_icons as _detect_icons
    return _detect_icons(img_path, conf=conf, iou=iou)


def detect_all(img_path: str, conf: float = 0.1, iou: float = 0.3) -> tuple:
    """Unified detection: GPA + OCR + merge + coordinate conversion.

    Returns:
        (icons, texts, merged, img_w, img_h) — merged in click-space coordinates.
    """
    from ui_detector import detect_all as _detect_all
    return _detect_all(img_path, conf=conf, iou=iou)


def merge_elements(icon_elements: list, text_elements: list,
                   ax_elements: list = None, iou_threshold: float = 0.3) -> list[dict]:
    """Merge and deduplicate elements from different sources."""
    from ui_detector import merge_elements as _merge
    return _merge(icon_elements, text_elements, ax_elements, iou_threshold)


def detect_all_mac(app_name: str = None, fullscreen: bool = False,
                   include_ax: bool = False,
                   gpa_conf: float = 0.1, gpa_iou: float = 0.3,
                   merge_iou: float = 0.3) -> tuple:
    """Full Mac detection pipeline: screenshot + detect.

    Returns:
        (elements, img_path, annotated_path)
    """
    from ui_detector import detect_all_mac as _detect_all_mac
    return _detect_all_mac(app_name=app_name, fullscreen=fullscreen,
                           include_ax=include_ax,
                           gpa_conf=gpa_conf, gpa_iou=gpa_iou,
                           merge_iou=merge_iou)


def annotate_image(img_path: str, elements: list, out_path: str = None) -> str | None:
    """Draw bounding boxes on image. Returns annotated image path."""
    from ui_detector import annotate_image as _annotate
    return _annotate(img_path, elements, out_path)


def get_screen_info() -> dict:
    """Return current screen scale info."""
    from ui_detector import get_screen_info as _get_info
    return _get_info()
