"""
gui_harness.platform_info.dpi — cross-platform display scale + DPI awareness.

The agent captures a screenshot in *image* pixels and clicks at *click-space*
coordinates. On HiDPI displays the two differ by a scale factor:

    scale = image_pixels_per_click_unit
          = screenshot_width_px / click_space_width

- macOS Retina : screencapture is 2x logical points -> scale = backingScaleFactor (~2.0)
- Windows      : PIL ImageGrab always captures *physical* pixels; pynput's
                 SetCursorPos uses the process DPI-awareness space. We make the
                 process per-monitor DPI-aware so click-space == physical, giving
                 scale = 1.0. If awareness can't be set, scale = physical/logical
                 (e.g. 1.5 @ 150% scaling), which still maps correctly.
- Linux / X11  : usually 1:1 -> scale = 1.0.

detector.ImageContext divides image coords by this scale to get click coords,
so a correct cross-platform scale here makes clicks land on every OS.
"""
from __future__ import annotations

import os
import platform

SYSTEM = platform.system()

_aware_done = False
_cached_scale = None


def ensure_dpi_aware() -> None:
    """Make the process per-monitor DPI-aware (Windows). Idempotent,
    best-effort, no-op on macOS/Linux. Run before any screenshot/click so
    ImageGrab (physical px) and pynput (SetCursorPos) share one coordinate
    space. Set ``OPENPROGRAM_GUI_NO_DPI_AWARE=1`` to opt out.
    """
    global _aware_done
    if _aware_done or SYSTEM != "Windows":
        return
    _aware_done = True
    if os.environ.get("OPENPROGRAM_GUI_NO_DPI_AWARE"):
        return
    import ctypes
    # Win10 1703+: DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = (HANDLE)-4
    try:
        if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
            return
    except Exception:
        pass
    # Win8.1+: PROCESS_PER_MONITOR_DPI_AWARE = 2
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    # Vista+ legacy (system-DPI aware only)
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def screen_scale() -> float:
    """Image-pixels per click-unit for the primary display (cached)."""
    global _cached_scale
    if _cached_scale is None:
        _cached_scale = _compute_scale()
    return _cached_scale


def reset_cache() -> None:
    """Forget the cached scale (call after a resolution / scaling change)."""
    global _cached_scale
    _cached_scale = None


def _compute_scale() -> float:
    if SYSTEM == "Darwin":
        import subprocess
        try:
            r = subprocess.run(
                ["swift", "-e",
                 "import AppKit; print(NSScreen.main!.backingScaleFactor)"],
                capture_output=True, text=True, timeout=10)
            return float(r.stdout.strip()) or 2.0
        except Exception:
            return 2.0
    if SYSTEM == "Windows":
        ensure_dpi_aware()  # MUST precede the measurement (and any click)
        try:
            import ctypes
            u = ctypes.windll.user32
            g = ctypes.windll.gdi32
            hdc = u.GetDC(0)
            try:
                DESKTOPHORZRES = 118  # true physical width, awareness-independent
                physical = g.GetDeviceCaps(hdc, DESKTOPHORZRES)
                logical = u.GetSystemMetrics(0)  # SM_CXSCREEN in current awareness
            finally:
                u.ReleaseDC(0, hdc)
            if physical and logical:
                return physical / logical
        except Exception:
            pass
        return 1.0
    return 1.0  # Linux / other
