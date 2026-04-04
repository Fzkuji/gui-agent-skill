"""
gui_harness.functions.act — perform a GUI action.

act() is an @agentic_function that:
  1. Uses summarize() to see what observe() found (via Context tree)
  2. Takes a before screenshot
  3. Asks the LLM to locate the target and determine coordinates
  4. Executes the action via primitives
  5. Returns a structured result
"""

from __future__ import annotations

import json
import time
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
def act(action: str, target: str, text: str = None,
        app_name: str = None, runtime: GUIRuntime = None) -> dict:
    """Perform a GUI action on a target element.

    The Context tree (via summarize()) provides what observe() found,
    so the LLM has full situational awareness without re-observing.

    Args:
        action: One of "click", "double_click", "right_click", "type", "shortcut".
        target: Description of the element to interact with.
        text:   Text to type (for "type" action).
        app_name: Optional: override frontmost app detection.
        runtime: Optional: GUIRuntime instance.

    Returns:
        dict with keys:
            action (str)
            target (str)
            coordinates (dict | None) — {x, y}
            success (bool)
            screen_changed (bool)
            before_state (str | None)
            after_state (str | None)
            error (str | None)
    """
    rt = runtime or _get_runtime()

    if not app_name:
        app_name = _input.get_frontmost_app()

    # 1. Before screenshot + detection
    img_path = screenshot.take()
    ocr_results = ocr.detect_text(img_path)

    try:
        _, _, elements, _, _ = detector.detect_all(img_path)
    except Exception:
        elements = ocr_results

    ocr_lines = "\n".join(
        f"  '{el.get('label', '')}' at ({el.get('cx', 0)}, {el.get('cy', 0)})"
        for el in ocr_results[:60]
    )
    det_lines = "\n".join(
        f"  [{el.get('label', 'UI element')}] id={el.get('id', '?')} "
        f"at ({el.get('cx', 0)}, {el.get('cy', 0)}) "
        f"size={el.get('w', 0)}x{el.get('h', 0)}"
        for el in elements[:50]
    )

    prompt = f"""Action: {action}
Target: {target}
{f'Text to type: {text}' if text else ''}
App: {app_name}

OCR text on screen:
{ocr_lines if ocr_lines else '(none)'}

Detected UI elements:
{det_lines if det_lines else '(none)'}

Find the target "{target}" in the lists above and return its EXACT coordinates.
Do NOT estimate from the image — use only coordinates from the lists.

Return JSON:
{{
  "action": "{action}",
  "target": "{target}",
  "coordinates": {{"x": 0, "y": 0}} or null if not found,
  "success": true/false,
  "error": null or "reason why not found"
}}"""

    # 2. LLM decides where to click
    reply = rt.exec(content=[
        {"type": "text", "text": prompt},
        {"type": "image", "path": img_path},
    ])

    try:
        data = _parse_json(reply)
    except Exception:
        data = {
            "action": action, "target": target,
            "coordinates": None, "success": False,
            "error": f"Failed to parse LLM response: {reply[:200]}"
        }

    # 3. Execute the action
    if data.get("success") and data.get("coordinates"):
        coords = data["coordinates"]
        cx, cy = int(coords.get("x", 0)), int(coords.get("y", 0))

        try:
            if action.lower() in ("click", "single_click"):
                _input.mouse_click(cx, cy)
            elif action.lower() == "double_click":
                _input.mouse_double_click(cx, cy)
            elif action.lower() == "right_click":
                _input.mouse_right_click(cx, cy)
            elif action.lower() == "type":
                _input.mouse_click(cx, cy)
                time.sleep(0.3)
                _input.paste_text(text or "")
            elif action.lower() == "shortcut":
                keys = [k.strip() for k in target.split("+")]
                _input.key_combo(*keys)

            time.sleep(0.5)

            # Check if screen changed
            after_path = screenshot.take("/tmp/gui_act_after.png")
            after_ocr = ocr.detect_text(after_path)
            before_texts = {el.get("label", "") for el in ocr_results}
            after_texts = {el.get("label", "") for el in after_ocr}
            data["screen_changed"] = before_texts != after_texts
            data["before_state"] = img_path
            data["after_state"] = after_path

        except Exception as e:
            data["success"] = False
            data["error"] = str(e)
            data["screen_changed"] = False

    else:
        data["screen_changed"] = False
        data["before_state"] = img_path
        data["after_state"] = None

    data.setdefault("action", action)
    data.setdefault("target", target)
    return data


def _parse_json(reply: str) -> dict:
    text = reply.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return json.loads(text)
