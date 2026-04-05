"""
Component Memory — Phase 1-5 locate_target workflow.

This module implements the core loop for finding a target element on screen
by combining GPA detection, template matching against saved memory, and
LLM-driven labeling of unknown components.

Design (from DESIGN doc):
  Phase 1: GPA detection + OCR → N components (sorted by confidence)
  Phase 2: Template match against memory → known components list
  Phase 3: LLM sees known components → found target? → return coordinates
  Phase 4: Label unknown components one-by-one (stop when target found)
  Phase 5: Cleanup (delete unlabeled screenshots)

This module is called by execute_task.py whenever an action needs
screen coordinates (click, double_click, right_click, drag).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

from agentic import agentic_function

from gui_harness.perception import screenshot, ocr, detector
from gui_harness.memory import app_memory

# ═══════════════════════════════════════════
# Phase 1: Detection
# ═══════════════════════════════════════════

def detect_components(img_path: str, conf: float = 0.1) -> dict:
    """Run GPA-GUI-Detector + OCR on a screenshot.

    Returns a dict with:
      - icons: list[dict] — GPA-detected UI components, sorted by confidence desc
      - texts: list[dict] — OCR text elements with coordinates
      - img_w, img_h: image dimensions
    """
    icons, texts, _merged, img_w, img_h = detector.detect_all(img_path, conf=conf)

    # Sort icons by confidence descending — higher confidence = more likely interactive
    icons = sorted(icons, key=lambda e: e.get("confidence", 0), reverse=True)

    return {
        "icons": icons,
        "texts": texts,
        "img_w": img_w,
        "img_h": img_h,
    }


# ═══════════════════════════════════════════
# Phase 2: Memory Matching
# ═══════════════════════════════════════════

def match_memory_components(
    app_name: str,
    img_path: str,
    threshold: float = 0.8,
) -> list[dict]:
    """Match saved component templates against the current screenshot.

    For each saved component, run template matching on the full screenshot.
    Returns a list of matched components with their labels and click-space
    coordinates.

    Returns:
        list[dict]: Each dict has keys:
            - name: str — component label
            - cx, cy: int — click-space center coordinates
            - confidence: float — match confidence
            - source: "memory"
    """
    app_dir = app_memory.get_app_dir(app_name)
    components_dir = app_dir / "components"

    if not components_dir.exists():
        return []

    screen_img = cv2.imread(img_path)
    if screen_img is None:
        return []

    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    matched = []

    for icon_file in components_dir.glob("*.png"):
        template = cv2.imread(str(icon_file))
        if template is None:
            continue

        th, tw = template.shape[:2]
        if th < 10 or tw < 10 or th > screen_gray.shape[0] or tw > screen_gray.shape[1]:
            continue

        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            cx = max_loc[0] + tw // 2
            cy = max_loc[1] + th // 2
            matched.append({
                "name": icon_file.stem,
                "cx": cx,
                "cy": cy,
                "w": tw,
                "h": th,
                "confidence": round(float(max_val), 3),
                "source": "memory",
            })

    # Sort by confidence descending
    matched.sort(key=lambda m: m["confidence"], reverse=True)
    return matched


# ═══════════════════════════════════════════
# Phase 3: LLM decides from known components
# ═══════════════════════════════════════════

@agentic_function(summarize={"depth": 0, "siblings": 0})
def find_target_in_known(
    task: str,
    target: str,
    known_components: list[dict],
    texts: list[dict],
    runtime=None,
) -> dict:
    """Given a list of known (labeled) UI components and OCR text, decide if the
    target element is among them.

    You receive:
    - The task being performed
    - The target element description
    - Known components: labeled UI elements with exact coordinates
    - OCR text: all visible text on screen with coordinates

    If you can identify the target, return its coordinates.
    Coordinates MUST come from the provided lists — never estimate.

    Return JSON:
    {
      "found": true/false,
      "name": "component name or text label",
      "cx": <x coordinate>,
      "cy": <y coordinate>,
      "reasoning": "why this is the target"
    }
    """
    from gui_harness.utils import parse_json
    from gui_harness.runtime import GUIRuntime

    rt = runtime or GUIRuntime()

    comp_lines = "\n".join(
        f"  [{c['name']}] at ({c['cx']}, {c['cy']}) conf={c.get('confidence', 0):.2f}"
        for c in known_components
    ) or "(none)"

    text_lines = "\n".join(
        f"  '{t.get('label', '')}' at ({t.get('cx', 0)}, {t.get('cy', 0)})"
        for t in texts[:60]
    ) or "(none)"

    context = f"""Task: {task}
Target: {target}

Known UI components (labeled, with coordinates):
{comp_lines}

OCR text on screen:
{text_lines}

If the target is in the lists above, return its coordinates.
If not found, return {{"found": false}}.
Return ONLY valid JSON."""

    reply = rt.exec(content=[{"type": "text", "text": context}])

    try:
        return parse_json(reply)
    except Exception:
        return {"found": False, "reasoning": f"Parse failed: {reply[:200]}"}


# ═══════════════════════════════════════════
# Phase 4: Label unknown components one by one
# ═══════════════════════════════════════════

@agentic_function(summarize={"depth": 0, "siblings": 0})
def label_single_component(
    task: str,
    target: str,
    component_crop_path: str,
    component_index: int,
    component_bbox: dict,
    runtime=None,
) -> dict:
    """Identify a single UI component from its cropped screenshot.

    You will see a cropped image of one UI component detected on screen.

    Decide:
    1. What is this component? (button, icon, text field, menu item, etc.)
    2. Give it a descriptive snake_case label, or "skip" if it's blank/meaningless
    3. Is this the target we're looking for?

    Return JSON:
    {
      "label": "descriptive_name" or "skip",
      "is_target": true/false,
      "reasoning": "what this component appears to be"
    }
    """
    from gui_harness.utils import parse_json
    from gui_harness.runtime import GUIRuntime

    rt = runtime or GUIRuntime()

    context = f"""Task: {task}
Target element: {target}

This is component #{component_index} at position ({component_bbox['cx']}, {component_bbox['cy']}), size {component_bbox['w']}x{component_bbox['h']}.

What is this UI element? Give it a snake_case name (e.g., "search_bar", "close_button").
If it's blank, decorative, or meaningless, return "skip" as the label.
Also determine if this is the target element described above.

Return ONLY valid JSON."""

    reply = rt.exec(content=[
        {"type": "text", "text": context},
        {"type": "image", "path": component_crop_path},
    ])

    try:
        return parse_json(reply)
    except Exception:
        return {"label": "skip", "is_target": False, "reasoning": f"Parse failed: {reply[:200]}"}


def label_unknown_components(
    task: str,
    target: str,
    icons: list[dict],
    known_names: set[str],
    img_path: str,
    app_name: str,
    runtime=None,
) -> Optional[dict]:
    """Phase 4: Label unknown components one by one until target is found.

    Iterates through detected icons (sorted by confidence descending).
    For each unknown component:
      1. Crop it from the screenshot
      2. Send to LLM for labeling
      3. If labeled (not "skip"), save to memory
      4. If it's the target, stop and return coordinates

    Args:
        task: The overall task description
        target: Description of the target element
        icons: GPA-detected components, sorted by confidence desc
        known_names: Set of component names already matched from memory
        img_path: Path to the full screenshot
        app_name: App name for memory storage
        runtime: GUIRuntime instance

    Returns:
        dict with {cx, cy, name} if target found, None otherwise.
    """
    screen_img = cv2.imread(img_path)
    if screen_img is None:
        return None

    app_dir = app_memory.get_app_dir(app_name)
    components_dir = app_dir / "components"
    components_dir.mkdir(parents=True, exist_ok=True)

    # Track temporary crop files for cleanup (Phase 5)
    temp_crops = []

    for i, icon in enumerate(icons):
        # Skip tiny elements
        if icon.get("w", 0) < 25 or icon.get("h", 0) < 25:
            continue

        # Skip already-known components (matched in Phase 2)
        # We check by approximate position overlap with known components
        # (A more sophisticated check could use IoU)

        # Crop this component from the screenshot
        x = icon.get("x", 0)
        y = icon.get("y", 0)
        w = icon.get("w", 0)
        h = icon.get("h", 0)

        # Add padding
        pad = 4
        y1 = max(0, y - pad)
        x1 = max(0, x - pad)
        y2 = min(screen_img.shape[0], y + h + pad)
        x2 = min(screen_img.shape[1], x + w + pad)

        crop = screen_img[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        # Check if this crop duplicates an existing saved component
        is_dup, dup_name = app_memory.is_duplicate_icon(crop, components_dir)
        if is_dup:
            continue

        # Save temporary crop for LLM to see
        crop_path = str(components_dir / f"_unlabeled_{i:03d}.png")
        cv2.imwrite(crop_path, crop)
        temp_crops.append(crop_path)

        # Ask LLM to label this component
        result = label_single_component(
            task=task,
            target=target,
            component_crop_path=crop_path,
            component_index=i,
            component_bbox={
                "cx": icon.get("cx", 0),
                "cy": icon.get("cy", 0),
                "w": w,
                "h": h,
            },
            runtime=runtime,
        )

        label = result.get("label", "skip")
        is_target = result.get("is_target", False)

        if label and label != "skip":
            # Rename temporary crop to proper label
            safe_label = label.replace("/", "-").replace(" ", "_").replace(":", "")[:50]
            final_path = str(components_dir / f"{safe_label}.png")

            # Don't overwrite existing components
            if not os.path.exists(final_path):
                os.rename(crop_path, final_path)
                temp_crops.remove(crop_path)

                # Save to components.json
                components = app_memory.load_components(app_dir)
                components[label] = {
                    "type": icon.get("type", "icon"),
                    "source": "gpa_detector",
                    "cx": icon.get("cx", 0),
                    "cy": icon.get("cy", 0),
                    "w": w,
                    "h": h,
                    "icon_file": f"components/{safe_label}.png",
                    "label": label,
                    "confidence": icon.get("confidence", 0),
                    "learned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "seen_count": 1,
                    "consecutive_misses": 0,
                }
                app_memory.save_components(app_dir, components)

        if is_target:
            # Phase 5: Cleanup before returning
            _cleanup_temp_crops(temp_crops)
            return {
                "cx": icon.get("cx", 0),
                "cy": icon.get("cy", 0),
                "name": label if label != "skip" else f"component_{i}",
            }

    # Phase 5: Cleanup all remaining temp crops
    _cleanup_temp_crops(temp_crops)
    return None


# ═══════════════════════════════════════════
# Phase 5: Cleanup
# ═══════════════════════════════════════════

def _cleanup_temp_crops(temp_crops: list[str]):
    """Delete temporary unlabeled crop files."""
    for path in temp_crops:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


# ═══════════════════════════════════════════
# Main entry point: locate_target
# ═══════════════════════════════════════════

def locate_target(
    task: str,
    target: str,
    img_path: str,
    app_name: str = "desktop",
    runtime=None,
) -> Optional[dict]:
    """Complete Phase 1-5 flow to find a target element on screen.

    This is the single entry point called by execute_task when an action
    needs coordinates.

    Phase 1: Detect all components (GPA + OCR)
    Phase 2: Match against saved memory
    Phase 3: Ask LLM if target is among known components
    Phase 4: Label unknown components (stop when target found)
    Phase 5: Cleanup

    Args:
        task: Natural language task description
        target: Description of the element to locate
        img_path: Path to the current screenshot
        app_name: App name for memory lookup/storage
        runtime: GUIRuntime instance

    Returns:
        dict with {cx, cy, name} if found, None if not found.
    """
    # Phase 1: Detection
    detection = detect_components(img_path)
    icons = detection["icons"]
    texts = detection["texts"]

    # Phase 2: Memory matching
    known_components = match_memory_components(app_name, img_path)
    known_names = {c["name"] for c in known_components}

    # Also include OCR texts as "known" elements (they have labels + coordinates)
    # OCR texts are always available and don't need labeling
    all_known = list(known_components)
    for t in texts:
        all_known.append({
            "name": t.get("label", ""),
            "cx": t.get("cx", 0),
            "cy": t.get("cy", 0),
            "w": t.get("w", 0),
            "h": t.get("h", 0),
            "confidence": 1.0,
            "source": "ocr",
        })

    # Phase 3: Ask LLM to find target in known components
    if all_known:
        result = find_target_in_known(
            task=task,
            target=target,
            known_components=all_known,
            texts=texts,
            runtime=runtime,
        )
        if result.get("found"):
            return {
                "cx": result.get("cx", 0),
                "cy": result.get("cy", 0),
                "name": result.get("name", target),
            }

    # Phase 4: Label unknown components one by one
    found = label_unknown_components(
        task=task,
        target=target,
        icons=icons,
        known_names=known_names,
        img_path=img_path,
        app_name=app_name,
        runtime=runtime,
    )

    return found
