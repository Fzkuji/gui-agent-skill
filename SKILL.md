---
name: gui-agent
description: "ALL interactions with ANY app — whether built-in (Finder, Safari, System Settings) or third-party (WeChat, Chrome, Slack) — MUST go through this skill. Clicking, typing, reading content, sending messages, navigating menus, filling forms: everything uses visual detection (screenshot → template match → click). This is the ONLY way to operate apps. Never bypass with CLI commands, AppleScript, or Accessibility APIs."
---

# GUI Agent Skill

You ARE the agent loop. Every GUI task follows this flow:

```
OBSERVE → ENSURE APP READY → ACT → VERIFY (auto) → RECORD TRANSITION → REPORT
```

## Sub-Skills (read on demand)

| Step | Skill | When to read |
|------|-------|-------------|
| **Observe** | `skills/gui-observe/SKILL.md` | Before any action — screenshot, detect state |
| **Learn** | `skills/gui-learn/SKILL.md` | App not in memory, or component not found |
| **Act** | `skills/gui-act/SKILL.md` | Clicking, typing, sending messages |
| **Memory** | `skills/gui-memory/SKILL.md` | Profiles, components, states, transitions |
| **Workflow** | `skills/gui-workflow/SKILL.md` | State graph navigation, workflow replay |
| **Setup** | `skills/gui-setup/SKILL.md` | First-time setup on a new machine |

## Core Commands

```bash
source ~/gui-actor-env/bin/activate
cd ~/.openclaw/workspace/skills/gui-agent

# Observe
python3 scripts/agent.py learn --app AppName        # Detect + save components
python3 scripts/agent.py detect --app AppName        # Match known components
python3 scripts/agent.py list --app AppName          # List saved components

# Act
python3 scripts/agent.py click --app AppName --component ButtonName
python3 scripts/agent.py open --app AppName
python3 scripts/agent.py cleanup --app AppName

# State graph
python3 scripts/app_memory.py transitions --app AppName     # View state graph
python3 scripts/app_memory.py path --app AppName --component from_state --contact to_state  # Find route

# Messaging (prints guidance, agent executes step by step)
python3 scripts/agent.py send_message --app WeChat --contact "小明" --message "明天见"
```

## Execution Flow

### STEP 0: OBSERVE
Take screenshot. Use `image` tool to **understand** current state (what app, what page, what's visible). First time only — subsequent steps use component detection.

### STEP 1: ENSURE APP READY
If app not in memory → `learn`. If component not found → `learn` current state.
Component not matching ≠ lower threshold. It means the component isn't on screen — re-learn to discover what IS on screen.

### STEP 2: ACT
`click_component` handles everything automatically:
1. Screenshot (one, shared for detection + matching)
2. Detect visible components (template match, no LLM)
3. Match target component → get precise coordinates
4. Click
5. Detect visible components again
6. Record state transition (from → click → to)
7. Report: appeared/disappeared components, current state

### STEP 3: VERIFY (automatic)
- **First click on X**: learns what appears/disappears → saves as `click:X` state
- **Repeat click on X**: verifies expected components appeared (no screenshot needed)
- **Mismatch**: agent should then screenshot + `image` tool to diagnose

### STEP 4: STATE TRANSITION (automatic)
Every click records `(from_state, click_component, to_state)` in the state graph.
Multiple clicks build a connected graph. Use `find_path()` to navigate between any two states.

### STEP 5: REPORT
```
⏱ 45.2s | 📊 +10k tokens | 🔧 3 clicks, 1 learn
```

---

## Key Principles

1. **Vision-driven, no shortcuts** — screenshot → detect → match → click. Only allowed system calls: `activate` (bring to front), `screencapture`, `platform_input.py` (pynput click/type).
2. **Coordinates from detection only:**
   - **Saved components** → template matching (conf≈1.0, pixel-precise)
   - **Dynamic content** (menus, search results) → YOLO/OCR detection → bbox center
   - **`image` tool = understanding only** ("what is this?", "which one?", "did it work?"). NEVER for coordinates.
3. **Not found = not on screen** — don't lower thresholds. Re-learn current state to discover new components.
4. **State graph drives navigation** — each click records a transition. Use `find_path()` to route between states.
5. **First time: screenshot + image. Repeat: detection only** — saves tokens on known workflows.
6. **Paste > Type** for CJK text
7. **Integer logical coordinates** — pynput uses screen logical pixels

## Safety Rules

1. **Full-screen search + window validation** — match on full screen, reject matches outside target app's window bounds
2. **App switch detection** — `click_component` checks frontmost app after every click
3. **No wrong-app learning** — validate frontmost app before learn
4. **Reject tiny templates** — <30×30 pixels produce false matches
5. **Never send screenshots to chat** — internal detection only
6. **NEVER quit the communication app** — if a dialog asks to quit apps (like CleanMyMac's "Quit All"), NEVER quit Discord/Telegram/WhatsApp or whatever channel you're communicating through. Instead: click individual Quit buttons for other apps, or click "Ignore" to skip. Quitting the comms app disconnects you from the user.
7. **Every click uses `click_and_record` or `click_component`** — never raw `click_at()`. Every click must record a state transition.

## Input Methods (platform_input.py)

```python
from platform_input import click_at, paste_text, key_press, key_combo, screenshot, 
    activate_app, get_clipboard, set_clipboard, mouse_right_click
```

No cliclick. No osascript for input. pynput only.

## File Structure

```
gui-agent/
├── SKILL.md              # This file
├── skills/               # Sub-skills (read on demand)
├── scripts/
│   ├── agent.py          # CLI entry point
│   ├── app_memory.py     # Components, states, transitions, matching
│   ├── platform_input.py # Cross-platform input (pynput)
│   ├── ui_detector.py    # YOLO + OCR detection
│   └── template_match.py # Legacy template matching
├── memory/               # Visual memory (gitignored)
│   ├── apps/<appname>/profile.json  # Components + states + transitions
│   └── meta_workflows/
└── README.md
```
