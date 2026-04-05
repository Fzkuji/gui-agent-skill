"""
gui_harness — GUI automation powered by Agentic Programming.

Primary entry point: execute_task()
Architecture: Phase 0-5 loop (see SKILL.md)
"""

from gui_harness.runtime import GUIRuntime
from gui_harness.tasks.execute_task import execute_task
from gui_harness.planning.component_memory import locate_target

__all__ = [
    "GUIRuntime",
    "execute_task",
    "locate_target",
]
