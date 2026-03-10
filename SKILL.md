---
name: gui-agent
description: "Control desktop GUI applications on macOS using Accessibility API, OCR, and cliclick. Use when asked to operate, click, type, or interact with any desktop application. NOT for web-only tasks (use browser tool) or simple file operations."
---

# GUI Agent Skill

You ARE the agent loop: Observe → Decide → Act → Verify.

## Scene Index

Tasks are modeled as **hierarchical scenes**, organized by app. Each scene decomposes into meta actions → atomic actions. Read only what you need.

| Scene | File | Goal |
|-------|------|------|
| **Atomic Actions** | `scenes/_actions.yaml` | Shared primitives (click, type, paste, AX scan...) |
| **WeChat** | `scenes/wechat.yaml` | Send/read messages, scroll history in WeChat |
| **Discord** | `scenes/discord.yaml` | Send/read messages in Discord |
| **Telegram** | `scenes/telegram.yaml` | Send/read messages in Telegram |
| **1Password** | `scenes/1password.yaml` | Retrieve credentials from 1Password GUI |
| **VPN Reconnect** | `scenes/vpn-reconnect.yaml` | Reconnect GlobalProtect VPN (depends on: 1password) |
| **App Exploration** | `scenes/app-explore.yaml` | Map an unfamiliar app's UI for automation |

### How scenes compose

```
VPN Reconnect (big scene)
├── Restart GP (meta action)
│   ├── quit app (action)
│   ├── open app (action)
│   └── wait (action)
├── SSO Login (meta action)
│   ├── Click Next (action)
│   ├── Get Password → ref: 1password.yaml#get_password (sub-scene)
│   │   ├── Focus 1Password (action)
│   │   ├── Select Entry (meta action)
│   │   │   ├── Cmd+F (action)
│   │   │   ├── Type search (action)
│   │   │   └── Enter (action)
│   │   ├── Verify Entry (meta action)
│   │   └── Click Dots to Copy (action)
│   ├── Click Password Field (action)
│   ├── Cmd+V Paste (action)
│   └── Click Verify (action)
└── Verify Connection (meta action)
    └── SSH test (action)
```

## Quick Decision Tree

```
What do you need to do?
│
├── WeChat (发消息/读消息)? → read scenes/wechat.yaml
├── Discord? → read scenes/discord.yaml
├── Telegram? → read scenes/telegram.yaml
├── VPN/SSH down? → read scenes/vpn-reconnect.yaml
├── Need a password? → read scenes/1password.yaml
├── New app, unknown UI? → read scenes/app-explore.yaml
├── Just need one atomic op? → read scenes/_actions.yaml
└── Core principles/lessons? → read docs/core.md
```

## Key Principles (always apply)

1. **AX first, OCR second, screenshot last** — AX is fastest and most precise
2. **Never assume focus** — click target before typing
3. **Paste > Type** for passwords/special chars
4. **Integer coordinates only** for cliclick
5. **Re-query AX positions** every time — window moves invalidate coords

## File Structure
```
gui-agent/
├── SKILL.md              # This index
├── scenes/               # Scenes organized by app (load on demand)
│   ├── _actions.yaml     # Atomic action catalog (shared by all scenes)
│   ├── wechat.yaml       # WeChat: send/read/scroll
│   ├── discord.yaml      # Discord: send/read
│   ├── telegram.yaml     # Telegram: send/read
│   ├── 1password.yaml    # 1Password: get credentials
│   ├── vpn-reconnect.yaml  # GlobalProtect VPN (refs 1password)
│   └── app-explore.yaml  # Explore unknown apps
├── docs/                 # Detailed reference docs
│   └── core.md           # Core principles & hard-won lessons
├── apps/                 # App profiles (JSON)
├── scripts/              # Automation scripts
└── README.md             # Human documentation
```
