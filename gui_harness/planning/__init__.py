"""
gui_harness.planning — @agentic_function decorated decision functions.

Core module: component_memory.py implements Phase 1-5 locate_target workflow.
Legacy modules (observe, act, verify, learn, navigate, remember) are retained
for backward compatibility but the primary flow is now through execute_task
which calls locate_target directly.
"""

from gui_harness.planning.component_memory import (
    locate_target,
    detect_components,
    match_memory_components,
    find_target_in_known,
    label_unknown_components,
)
from gui_harness.planning.observe import observe
from gui_harness.planning.act import act
from gui_harness.planning.verify import verify
from gui_harness.planning.learn import learn
from gui_harness.planning.navigate import navigate
from gui_harness.planning.remember import remember

__all__ = [
    "locate_target",
    "detect_components",
    "match_memory_components",
    "find_target_in_known",
    "label_unknown_components",
    "observe", "act", "verify", "learn", "navigate", "remember",
]
