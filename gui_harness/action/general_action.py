"""
gui_harness.action.general_action — general-purpose action executed by the agent.

Unlike GUI actions (click, type, etc.) which are specific operations,
general_action gives the agent a sub-task description and lets it use
any available tools to complete it: shell commands, file I/O, keyboard
shortcuts, web browsing, etc.

The agent runs in interactive mode with full tool access (Bash, Read,
Write, etc.) and reports the result when done.

IMPORTANT: general_action uses its own separate runtime instance to
avoid context pollution with the main loop's runtime (which accumulates
screenshot history). Each general_action call starts with a fresh process.
"""

from __future__ import annotations

from agentic import agentic_function


def _create_fresh_runtime():
    """Create a fresh runtime for general_action.

    Uses a separate instance so that the main loop's accumulated
    context (screenshots, detection results) doesn't interfere.
    """
    from gui_harness.runtime import GUIRuntime
    return GUIRuntime()


@agentic_function(summarize={"depth": 0, "siblings": 0})
def general_action(sub_task: str, runtime=None) -> dict:
    """Execute a sub-task using any available tools.

    You are given a specific sub-task to complete. You have full freedom
    to use any tools and methods available to you:
    - Run shell commands (bash)
    - Read and write files
    - Use keyboard shortcuts via pyautogui
    - Browse the web
    - Install packages
    - Anything else you need

    Complete the sub-task and report the result.

    Return JSON:
    {
      "success": true/false,
      "output": "what you did and the result",
      "error": null or "error description"
    }
    """
    from gui_harness.utils import parse_json

    # Always use a fresh runtime to avoid context pollution
    rt = _create_fresh_runtime()

    reply = rt.exec(content=[
        {"type": "text", "text": f"Sub-task: {sub_task}\n\nComplete this and return JSON with success/output/error."},
    ])

    # Clean up the runtime's process after use
    if hasattr(rt, '_inner') and hasattr(rt._inner, 'reset'):
        rt._inner.reset()

    try:
        return parse_json(reply)
    except Exception:
        return {"success": True, "output": reply[:500]}
