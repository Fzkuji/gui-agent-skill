"""
gui_harness.tasks.send_message — send a message in a messaging app.

High-level task: navigate → type → verify.
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
def send_message(app_name: str, recipient: str, message: str,
                 runtime: GUIRuntime = None) -> dict:
    """Send a message to a recipient in a messaging app.

    Steps:
      1. observe() — find current state
      2. navigate() — go to conversation with recipient
      3. act("type") — type the message
      4. act("click") — click send button
      5. verify() — confirm message was sent

    compress=True: callers see only this task's final result.

    Args:
        app_name:  Messaging app (e.g., "WeChat", "Messages", "Telegram").
        recipient: Name of the recipient/contact.
        message:   Message text to send.
        runtime:   Optional: GUIRuntime instance.

    Returns:
        dict with keys:
            app_name, recipient, message, success (bool), evidence (str)
    """
    from gui_harness.functions.observe import observe
    from gui_harness.functions.act import act
    from gui_harness.functions.navigate import navigate
    from gui_harness.functions.verify import verify

    rt = runtime or _get_runtime()

    # 1. Observe current state
    obs = observe(
        task=f"Find conversation with {recipient} in {app_name}",
        app_name=app_name,
        runtime=rt,
    )

    # 2. Navigate to conversation (if not already there)
    if not obs.get("target_visible"):
        navigate(
            target_state=f"conversation_{recipient}",
            app_name=app_name,
            runtime=rt,
        )

    # 3. Type the message
    act(
        action="click",
        target="message input field",
        app_name=app_name,
        runtime=rt,
    )
    act(
        action="type",
        target="message input field",
        text=message,
        app_name=app_name,
        runtime=rt,
    )

    # 4. Send
    act(
        action="click",
        target="send button",
        app_name=app_name,
        runtime=rt,
    )

    # 5. Verify
    result = verify(
        expected=f'Message "{message[:30]}..." appears in the conversation',
        runtime=rt,
    )

    return {
        "app_name": app_name,
        "recipient": recipient,
        "message": message,
        "success": result.get("verified", False),
        "evidence": result.get("evidence", ""),
    }
