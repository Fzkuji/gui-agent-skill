---
name: gui-agent
description: "GUI automation via Agentic Programming. Give it a task, it handles the rest — screenshot, detect, act, verify, all automatic."
---

# GUI Agent

## Usage

```python
from gui_harness.tasks.execute_task import execute_task
from gui_harness.runtime import GUIRuntime

runtime = GUIRuntime()  # auto-detects provider
result = execute_task("Open Firefox and go to google.com", runtime=runtime)
```

Or from CLI:

```bash
python3 {baseDir}/gui_harness/main.py "Open Firefox and go to google.com"
python3 {baseDir}/gui_harness/main.py --vm http://VM_IP:5000 "Click the OK button"
```

## Architecture: Phase 0-5 Loop

Each step in `execute_task()` follows this flow:

```
Phase 0: Screenshot → LLM sees image → decides action
  ├─ No coordinates needed (type / key_press / shortcut / paste / scroll)
  │   → Execute directly, next step
  │
  └─ Coordinates needed (click / double_click / right_click / drag)
      → Enter Phase 1-5 (locate_target)

Phase 1: GPA-GUI-Detector + OCR → N components (sorted by confidence)
Phase 2: Template match saved memory → known components with labels
Phase 3: LLM sees known components list → target found? → execute
Phase 4: Label unknown components one-by-one
         → LLM identifies each → save to memory → stop when target found
Phase 5: Cleanup (delete unlabeled temporary crops)
```

### Key Design Points

- **Phase 0 is visual**: LLM sees the full screenshot to understand context
- **Non-coordinate actions skip detection entirely** — no wasted compute
- **Phase 3 is text-only**: LLM sees a list of labels + coordinates, no image needed
- **Phase 4 stops early**: once the target is found, remaining components are skipped
- **Memory accumulates**: labeled components persist across steps and tasks
- **Drag uses two locate_target calls**: one for start position, one for end

## Available Actions

| Action | Needs Coordinates | Description |
|--------|:-:|---|
| `click` | Yes | Single click on an element |
| `double_click` | Yes | Double-click (open files, edit cells) |
| `right_click` | Yes | Right-click (context menus) |
| `drag` | Yes (x2) | Drag from start to end |
| `type` | No | Type text at current focus |
| `key_press` | No | Press a key (return, escape, tab, etc.) |
| `shortcut` | No | Keyboard shortcut (ctrl+s, ctrl+c, etc.) |
| `paste` | No | Paste text via clipboard |
| `scroll` | No | Scroll up or down |
| `done` | No | Task is complete |

## For VMs (OSWorld)

```python
from gui_harness.adapters.vm_adapter import patch_for_vm
patch_for_vm("http://VM_IP:5000")
# Then use execute_task() normally — routes through VM HTTP API
```

## First-Time Setup

```bash
cd {baseDir}
git submodule update --init --recursive          # pull Agentic Programming
pip install -e ./libs/agentic-programming        # install Agentic Programming
pip install -e .                                 # install GUI Agent Harness
```

## Core Rules

- **Coordinates from detection only** — OCR or GPA-GUI-Detector, never guessed
- **Look before you act** — every action justified by what was observed
- **Memory saves automatically** — labeled components persist for future use
