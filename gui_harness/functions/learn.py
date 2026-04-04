"""
gui_harness.functions.learn — learn an app's UI for the first time.

learn() screenshots an app, runs full detection, and asks the LLM
to label all components so they can be saved to visual memory.
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
from gui_harness.primitives import screenshot, ocr, detector, input as _input

_runtime: GUIRuntime | None = None


def _get_runtime() -> GUIRuntime:
    global _runtime
    if _runtime is None:
        _runtime = GUIRuntime()
    return _runtime


@agentic_function
def learn(app_name: str, runtime: GUIRuntime = None) -> dict:
    """Learn the UI of an app by labeling its components.

    Takes a screenshot, runs full detection, and uses the LLM to:
    - Name each detected UI component
    - Identify the current page/state
    - Filter out decorative elements

    The result can be saved to app_memory for future template matching.

    Args:
        app_name: Name of the app to learn.
        runtime:  Optional: GUIRuntime instance.

    Returns:
        dict with keys:
            app_name (str)
            page_name (str)
            components_found (int)
            components_saved (int)
            component_names (list[str])
            already_known (bool)
    """
    rt = runtime or _get_runtime()

    img_path = screenshot.take()

    # Run full detection
    ocr_results = ocr.detect_text(img_path)

    try:
        _, _, elements, _, _ = detector.detect_all(img_path)
    except Exception:
        elements = ocr_results

    det_lines = "\n".join(
        f"  Component {el.get('id', i)}: "
        f"at ({el.get('cx', 0)}, {el.get('cy', 0)}) "
        f"size={el.get('w', 0)}x{el.get('h', 0)} "
        f"label={el.get('label') or 'unknown'}"
        for i, el in enumerate(elements[:50])
    )
    ocr_lines = "\n".join(
        f"  '{el.get('label', '')}' at ({el.get('cx', 0)}, {el.get('cy', 0)})"
        for el in ocr_results[:60]
    )

    prompt = f"""You are learning the UI of "{app_name}" for the first time.

Detected UI components (need labels):
{det_lines if det_lines else '(none)'}

OCR text visible on screen:
{ocr_lines if ocr_lines else '(none)'}

For each interactive component:
1. Assign a descriptive snake_case name (e.g., search_bar, send_button)
2. Skip purely decorative or background elements
3. Identify the current page name

Return JSON:
{{
  "app_name": "{app_name}",
  "page_name": "current_page_name",
  "component_names": ["search_bar", "send_button", ...],
  "components_found": <total detected count>,
  "components_saved": <count of non-decorative, interactive ones>,
  "already_known": false
}}"""

    reply = rt.exec(content=[
        {"type": "text", "text": prompt},
        {"type": "image", "path": img_path},
    ])

    try:
        result = _parse_json(reply)
        result.setdefault("app_name", app_name)
        result.setdefault("components_found", len(elements))
        result.setdefault("components_saved", 0)
        result.setdefault("component_names", [])
        result.setdefault("page_name", "unknown")
        result.setdefault("already_known", False)

        # Optionally save to app_memory if available
        try:
            _SCRIPTS_DIR = str(Path(_REPO_DIR) / "scripts")
            if _SCRIPTS_DIR not in sys.path:
                sys.path.insert(0, _SCRIPTS_DIR)
            from app_memory import learn_from_screenshot
            saved = learn_from_screenshot(img_path, app_name, result["page_name"])
            result["components_saved"] = saved.get("saved", 0)
        except Exception:
            pass  # app_memory is optional

    except Exception:
        result = {
            "app_name": app_name,
            "page_name": "unknown",
            "component_names": [],
            "components_found": len(elements),
            "components_saved": 0,
            "already_known": False,
        }

    return result


def _parse_json(reply: str) -> dict:
    text = reply.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return json.loads(text)
