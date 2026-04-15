# OSWorld Benchmark Results — GUI Agent Harness

> Last updated: 2026-04-15

## Overview

**GUI Agent Harness** is evaluated on [OSWorld](https://github.com/xlang-ai/OSWorld), a real-computer benchmark for multimodal agents with 369 tasks across 10 domains.

## Results Summary

| Domain | Pass | Total | Rate | Status |
|--------|------|-------|------|--------|
| **Chrome** | 43 | 46 | **93.5%** | ✅ Complete |
| **Multi-Apps** | 72.6 | 91 | **79.8%** | ✅ Complete |
| **OS** | 24 | 24 | **100%** | ✅ Complete |
| GIMP | — | 26 | — | Not tested |
| LibreOffice Calc | — | 47 | — | Not tested |
| LibreOffice Impress | — | 47 | — | Not tested |
| LibreOffice Writer | — | 23 | — | Not tested |
| Thunderbird | — | 15 | — | Not tested |
| VLC | — | 17 | — | Not tested |
| VS Code | — | 23 | — | Not tested |
| **Total** | **139.6** | **369** | — | 3/10 domains |

> Notes: Multi-Apps has 10 blocked tasks (Google Drive credentials), 91 evaluated. OS includes 7 manual 1.0 (5 infeasible + 2 eval mismatch).

## Test Environment

- **Host**: Mac (Apple Silicon)
- **VM**: Ubuntu ARM (aarch64), VMware Fusion
- **Resolution**: 1920x1080
- **LLM**: Claude Opus 4.6 via Claude Code CLI
- **Framework**: [Agentic Programming](https://github.com/Fzkuji/Agentic-Programming)

## Architecture

```
gui-agent "task description"
    │
    ▼
gui_agent()                    ← @agentic_function, drives the loop
    │
    ├── for step in 1..max_steps:
    │       │
    │       ▼
    │   gui_step()             ← @agentic_function, orchestration
    │       │
    │       ├── 1. Observe     (Python) — screenshot + detect + match + state ID
    │       ├── 2. Verify      (LLM)   — check previous action's result
    │       ├── 3. Plan        (LLM)   — decide next action
    │       └── 4. Dispatch    (Python) — execute: click/type/scroll/general
    │
    └── return result summary
```

## Domain Results

- [Chrome](chrome.md) — 43/46 (93.5%)
- [Multi-Apps](multi_apps.md) — 72.6/91 (79.8%)
- [OS](os.md) — 24/24 (100%)
