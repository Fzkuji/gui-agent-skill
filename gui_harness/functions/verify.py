"""
gui_harness.functions.verify — verify the result of a previous action.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_DIR = str(Path(__file__).parent.parent.parent)
if _REPO_DIR not in sys.path:
    sys.path.insert(0, _REPO_DIR)

from agentic.function import agentic_function
from gui_harness.runtime import GUIRuntime
from gui_harness.primitives import screenshot, ocr

_runtime: GUIRuntime | None = None


def _get_runtime() -> GUIRuntime:
    global _runtime
    if _runtime is None:
        _runtime = GUIRuntime()
    return _runtime


@agentic_function
def verify(expected: str, runtime: GUIRuntime = None) -> dict:
    """Verify whether a previous action produced the expected result.

    Args:
        expected: A description of what should be visible/true after the action.
        runtime:  Optional: GUIRuntime instance.

    Returns:
        dict with keys:
            expected (str)
            actual (str)
            verified (bool)
            evidence (str)
            screenshot_path (str)
    """
    rt = runtime or _get_runtime()

    img_path = screenshot.take()
    ocr_results = ocr.detect_text(img_path)
    ocr_lines = "\n".join(
        f"  '{el.get('label', '')}'"
        for el in ocr_results[:40]
    )

    prompt = f"""Verify that the expected outcome was achieved.

Expected: {expected}

OCR text visible on screen:
{ocr_lines if ocr_lines else '(none)'}

Look at the screenshot and determine if the expected outcome is visible.

Return JSON:
{{
  "expected": "{expected}",
  "actual": "what you actually see on screen",
  "verified": true/false,
  "evidence": "specific text or element that confirms/denies the expectation",
  "screenshot_path": "{img_path}"
}}"""

    reply = rt.exec(content=[
        {"type": "text", "text": prompt},
        {"type": "image", "path": img_path},
    ])

    try:
        result = _parse_json(reply)
        result.setdefault("screenshot_path", img_path)
    except Exception:
        result = {
            "expected": expected,
            "actual": reply[:300],
            "verified": False,
            "evidence": "Failed to parse LLM response",
            "screenshot_path": img_path,
        }

    return result


def _parse_json(reply: str) -> dict:
    text = reply.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return json.loads(text)
