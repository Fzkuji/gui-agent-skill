---
name: gui-agent
description: "Control desktop GUI applications on macOS using Accessibility API, OCR, and cliclick. Use when asked to operate, click, type, or interact with any desktop application. NOT for web-only tasks (use browser tool) or simple file operations."
---

# GUI Agent Skill

## How It Works

You ARE the agent loop. Observe the screen → decide what to do → act → verify.

```
Observe (AX/OCR) → Plan actions → Execute (cliclick/osascript) → Verify (lightest method)
```

**Tools available** (from fastest to slowest):

| Tool | Speed | Use for |
|------|-------|---------|
| AppleScript/JXA | ~0.1s | App focus, window info, menu clicks, AX element discovery |
| cliclick | instant | Mouse clicks, keyboard input at precise coordinates |
| OCR (`gui_agent.py find`) | ~1.6s | Find text on screen with coordinates |
| Template match | ~1.3s | Find known UI elements (learned from prior use) |
| Screenshot + vision model | ~5-10s | Complex layout understanding (last resort) |

---

## Core Principles

### 1. Observe less, act more
```
BAD:  Screenshot → 1 action → Screenshot → 1 action → Screenshot
GOOD: AX scan → Plan 3-5 actions → Execute all → Verify once
```

### 2. AX first, OCR second, screenshot last
- **AX (`entireContents`)**: Precise positions, roles, titles. Best for buttons, fields, links
- **OCR**: When AX can't see content (WebViews, custom renders)
- **Screenshot + vision**: Only when you can't determine state otherwise

### 3. Hide before interact
```bash
osascript -e 'tell application "System Events" to set visible of every process whose name is not "TargetApp" to false'
```
Prevents mis-clicks on overlapping windows.

---

## Hard-Won Lessons

### Focus Management (最重要)
- **Any app can steal focus at any time** — especially auth/SSO pop-ups
- `osascript keystroke` sends to **current focus**, not the app you intended
- **Never assume focus** — use `cliclick c:x,y` to click the target element directly
- **Multi-app interaction**: finish the focus-stealing app first, then operate the passive one

### Coordinates
- **AX is the most reliable source**: `entireContents()` → find by role + title → position + size
- **Window moves invalidate coordinates** — always re-query AX before acting
- **cliclick only accepts integers**: `Math.round(pos + size/2)`
- **Retina**: OCR pixels ÷ 2 = logical coords. AX already returns logical coords

### Text Input
- **Cmd+V paste > cliclick t:** — `cliclick t:` truncates on special characters (`!@#` etc.)
- **For sensitive input**: copy to clipboard first, then Cmd+V into the field
- Clipboard sources (e.g. 1Password) may have TTL — copy as the **last step** before pasting

### 1Password Integration
- **Click password dots (●●●●) to copy** — simplest method, auto-copies to clipboard
- **Multiple entries with same name**: verify right panel shows correct username + website + password strength
- **90-second clipboard TTL**: copy immediately before pasting
- **`op` CLI needs Touch ID** — won't work headless; use GUI click-to-copy instead

### WebView Quirks
- `osascript keystroke` doesn't work inside WebViews
- `cliclick kp:return` may not trigger WebView buttons
- **Must use `cliclick c:x,y`** to click WebView buttons directly
- WebViews need load time — wait after navigation before interacting

### Debugging
- **Screenshot every step** when things go wrong: `/usr/sbin/screencapture -x path.png`
- **AX dump**: JXA `entireContents()` lists all elements with role/title/position
- **Never retry blindly** — observe current state first, then decide

---

## Quick Reference

### Observe
```bash
# AX scan (fastest, most reliable)
osascript -l JavaScript -e '
var se = Application("System Events");
var p = se.processes["AppName"];
var w = p.windows[0];
var all = w.entireContents();
var result = [];
for (var i = 0; i < all.length; i++) {
    try {
        var r = all[i].role();
        var t = all[i].title() || "";
        var p2 = all[i].position();
        var s = all[i].size();
        result.push(r + " \"" + t + "\" (" + p2[0] + "," + p2[1] + ") " + s[0] + "x" + s[1]);
    } catch(e) {}
}
result.join("\n");
'

# OCR (finds text with coordinates)
python3 scripts/gui_agent.py find "keyword"

# Full observation (structured)
python3 scripts/gui_agent.py observe --app AppName

# Screenshot (last resort)
/usr/sbin/screencapture -x /path/to/screenshot.png
```

### Act
```bash
# Click at coordinates
/opt/homebrew/bin/cliclick c:500,300

# Type text (simple ASCII only — use Cmd+V for special chars)
/opt/homebrew/bin/cliclick t:"hello"

# Keyboard shortcut
osascript -e 'tell application "System Events" to keystroke "v" using command down'

# Press special key
/opt/homebrew/bin/cliclick kp:return

# AX button click (reliable, doesn't need coordinates)
osascript -l JavaScript -e '
var se = Application("System Events");
se.processes["AppName"].windows[0].buttons.byName("OK").click();
'

# Menu bar action
osascript -l JavaScript -e '
var se = Application("System Events");
var p = se.processes["AppName"];
p.menuBars[0].menuBarItems.byName("Edit").menus[0].menuItems.byName("Copy").click();
'
```

### High-level tasks
```bash
python3 scripts/gui_agent.py task send_message --app WeChat --param contact="John" --param message="hi"
python3 scripts/gui_agent.py task read_messages --app WeChat --param contact="John"
python3 scripts/gui_agent.py task click_element --app Safari --param text="Downloads"
python3 scripts/gui_agent.py tasks  # list all available tasks
```

---

## App Profiles

App-specific configs in `apps/*.json`. Key profiles:

- **WeChat**: AX useless (5 elements), use OCR + templates. Enter to send. Don't use Cmd+F.
- **Discord**: AX excellent (1362 elements). Cmd+K for quick switcher.
- **Telegram**: Cmd+F for search. Enter to send.
- **GlobalProtect**: System tray app. WebView for SSO — must use cliclick, not keystroke. See TOOLS.md for VPN reconnect flow.

Create new profiles: copy any `apps/*.json`, adjust fields. Tasks work automatically.

---

## File Structure
```
gui-agent/
├── SKILL.md              # This file (agent instructions)
├── README.md             # Human documentation (detailed)
├── apps/                 # App profiles (layout, navigation, input, quirks)
├── scripts/
│   ├── gui_agent.py      # Main engine (observe/exec/task/find)
│   ├── template_match.py # Template learning & matching
│   ├── ocr_screen.sh     # OCR shell wrapper
│   └── ocr_screen.swift  # macOS Vision OCR
└── workflows/            # Legacy JSON workflows (reference only)
```

### Prerequisites
- macOS with Accessibility permissions
- `brew install cliclick`
- `pip install opencv-python-headless numpy`
- `/usr/sbin/screencapture` (full path required in headless environments)

---

*Last updated: 2026-03-10*
