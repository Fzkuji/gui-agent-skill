"""
gui_harness.primitives — pure Python tools (no @agentic_function decorator).

These are thin wrappers around the original scripts/ modules.
They re-export the same interfaces for backward compatibility.
"""

from gui_harness.primitives import screenshot, ocr, detector, input, template_match

__all__ = ["screenshot", "ocr", "detector", "input", "template_match"]
