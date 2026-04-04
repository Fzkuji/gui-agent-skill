"""
gui_harness.tasks.read_messages — read messages from a messaging app.

High-level task: navigate → observe → extract messages.
compress=True hides sub-steps from summarize().
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_DIR = str(Path(__file__).parent.parent.parent)
if _REPO_DIR not in sys.path:
    sys.path.insert(0, _REPO_DIR)

from agentic.function import agentic_function
from gui_harness.runtime import GUIRuntime

_runtime: GUIRuntime | None = None


def _get_runtime() -> GUIRuntime:
    global _runtime
    if _runtime is None:
        _runtime = GUIRuntime()
    return _runtime


@agentic_function(compress=True)
def read_messages(app_name: str, contact: str = None,
                  runtime: GUIRuntime = None) -> dict:
    """Read messages from a messaging app.

    Steps:
      1. observe() — identify current state
      2. navigate() — go to conversation (if contact specified)
      3. observe() — read the chat content

    compress=True: callers see only the final result.

    Args:
        app_name: Messaging app (e.g., "WeChat", "Discord", "Telegram").
        contact:  Optional: specific contact/channel to read from.
        runtime:  Optional: GUIRuntime instance.

    Returns:
        dict with keys:
            app_name (str)
            contact (str | None)
            messages (list[str])
            screenshot_path (str)
            success (bool)
    """
    from gui_harness.functions.observe import observe
    from gui_harness.functions.navigate import navigate

    rt = runtime or _get_runtime()

    # 1. Navigate to conversation if contact specified
    if contact:
        obs = observe(
            task=f"Find conversation with {contact} in {app_name}",
            app_name=app_name,
            runtime=rt,
        )
        if not obs.get("target_visible"):
            navigate(
                target_state=f"conversation_{contact}",
                app_name=app_name,
                runtime=rt,
            )

    # 2. Read the chat content
    obs = observe(
        task=f"Read all visible messages in the current chat of {app_name}",
        app_name=app_name,
        runtime=rt,
    )

    return {
        "app_name": app_name,
        "contact": contact,
        "messages": obs.get("visible_text", []),
        "screenshot_path": obs.get("screenshot_path", ""),
        "success": True,
    }
