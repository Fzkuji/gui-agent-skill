"""
gui_harness.primitives.vm_adapter — VM-based backend for GUI primitives.

Monkey-patches the primitives to work with a remote VM via HTTP API
instead of local macOS operations.

Usage:
    from gui_harness.primitives.vm_adapter import patch_for_vm
    patch_for_vm("http://172.16.105.128:5000")
"""

from __future__ import annotations

import base64
import os
import requests
import time

_VM_URL: str | None = None


def patch_for_vm(vm_url: str):
    """Monkey-patch all primitives to use the VM HTTP API."""
    global _VM_URL
    _VM_URL = vm_url.rstrip("/")

    import gui_harness.primitives.screenshot as _ss
    import gui_harness.primitives.input as _inp

    # Patch screenshot
    _ss.take = vm_screenshot
    _ss.take_window = lambda app, out=None: vm_screenshot(out or "/tmp/gui_agent_screen.png")

    # Patch input functions
    _inp.mouse_click = vm_mouse_click
    _inp.mouse_double_click = vm_mouse_double_click
    _inp.mouse_right_click = vm_mouse_right_click
    _inp.key_press = vm_key_press
    _inp.key_combo = vm_key_combo
    _inp.type_text = vm_type_text
    _inp.paste_text = vm_paste_text
    _inp.get_frontmost_app = lambda: "VM Desktop"


def _vm_exec(command: str, timeout: int = 30) -> dict:
    """Execute a command on the VM."""
    r = requests.post(f"{_VM_URL}/execute", json={"command": command}, timeout=timeout)
    return r.json()


def vm_screenshot(path: str = "/tmp/gui_agent_screen.png") -> str:
    """Take a screenshot from the VM and save locally."""
    r = requests.get(f"{_VM_URL}/screenshot", timeout=15)
    with open(path, "wb") as f:
        f.write(r.content)
    return path


def vm_mouse_click(x: int, y: int, button: str = "left", clicks: int = 1):
    btn = "left" if button == "left" else "right"
    cmd = f"python3 -c \"import pyautogui; pyautogui.click({x}, {y}, button='{btn}', clicks={clicks})\""
    _vm_exec(cmd)
    time.sleep(0.3)


def vm_mouse_double_click(x: int, y: int):
    vm_mouse_click(x, y, clicks=2)


def vm_mouse_right_click(x: int, y: int):
    vm_mouse_click(x, y, button="right")


def vm_key_press(key_name: str):
    cmd = f"python3 -c \"import pyautogui; pyautogui.press('{key_name}')\""
    _vm_exec(cmd)
    time.sleep(0.2)


def vm_key_combo(*keys: str):
    key_list = "', '".join(keys)
    cmd = f"python3 -c \"import pyautogui; pyautogui.hotkey('{key_list}')\""
    _vm_exec(cmd)
    time.sleep(0.3)


def vm_type_text(text: str):
    """Type text character by character (slow, for typewrite)."""
    escaped = text.replace("'", "\\'").replace('"', '\\"')
    cmd = f'python3 -c "import pyautogui; pyautogui.typewrite(\'{escaped}\', interval=0.02)"'
    _vm_exec(cmd)
    time.sleep(0.3)


def vm_paste_text(text: str):
    """Paste text via xdotool on the VM."""
    # Use xdotool to type text (handles unicode better)
    b64 = base64.b64encode(text.encode()).decode()
    cmd = f"python3 -c \"import base64,subprocess; t=base64.b64decode('{b64}').decode(); subprocess.run(['xdotool','type','--clearmodifiers','--delay','20',t])\""
    _vm_exec(cmd)
    time.sleep(0.3)
