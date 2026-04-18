# OSWorld Benchmark — GUI Agent Harness

> Last updated: 2026-04-15

## Overview

**GUI Agent Harness** is evaluated on [OSWorld](https://github.com/xlang-ai/OSWorld), a real-computer benchmark for multimodal agents with 369 tasks across 10 domains.

## Results Summary

| Domain | Pass | Total | Rate | Status |
|--------|------|-------|------|--------|
| **Chrome** | 43 | 46 | **93.5%** | Complete |
| **Multi-Apps** | 72.6 | 91 | **79.8%** | Complete |
| **OS** | 24 | 24 | **100%** | Complete |
| GIMP | — | 26 | — | In progress |
| LibreOffice Calc | — | 47 | — | Not tested |
| LibreOffice Impress | — | 47 | — | Not tested |
| LibreOffice Writer | — | 23 | — | Not tested |
| Thunderbird | — | 15 | — | Not tested |
| VLC | — | 17 | — | Not tested |
| VS Code | — | 23 | — | Not tested |
| **Total** | **139.6** | **369** | — | 3/10 domains |

> Notes: Multi-Apps has 10 blocked tasks (Google Drive credentials), 91 evaluated. OS includes 7 manual 1.0 (5 infeasible + 2 eval mismatch).

## How to Run

### Prerequisites

1. **GUI Agent Harness** installed (`pip install -e .`)
2. **OSWorld** cloned at `~/OSWorld` (`git clone https://github.com/xlang-ai/OSWorld.git`)
3. **VMware Fusion** installed with Ubuntu ARM VM
4. VM has an `init_state` snapshot (the script reverts to this before each task)
5. **Claude Code CLI** logged in (`npm install -g @anthropic-ai/claude-code && claude login`)
6. **Surge proxy** (optional) running on port 6152 for VM internet access

### Run a Single Task

```bash
cd GUI-Agent-Harness
python benchmarks/osworld/run_osworld_task.py <task_number> [options]
```

Examples:

```bash
# Multi-Apps task 88
python benchmarks/osworld/run_osworld_task.py 88 --max-steps 15

# GIMP domain task 4, more steps
python benchmarks/osworld/run_osworld_task.py 4 --domain gimp --max-steps 20

# Custom VM IP
python benchmarks/osworld/run_osworld_task.py 44 --vm 172.16.82.132
```

Options:

```
task_num              Task number (1-indexed within the domain)
--domain DOMAIN       Task domain (default: multi_apps)
                      Options: multi_apps, chrome, gimp, os, libreoffice_calc,
                      libreoffice_impress, libreoffice_writer, thunderbird, vlc, vscode
--vm VM_IP            VM IP address (default: 172.16.82.132)
--max-steps N         Max agent steps (default: 15)
--no-setup            Skip VM revert (useful for retrying without reset)
--no-eval             Skip official evaluation (just run the agent)
```

### Run a Batch

```bash
bash benchmarks/osworld/run_batch.sh <start> <end> [domain]
```

Examples:

```bash
# Run all 101 Multi-Apps tasks
bash benchmarks/osworld/run_batch.sh 1 101 multi_apps

# Run GIMP tasks 1-26
bash benchmarks/osworld/run_batch.sh 1 26 gimp

# Run Multi-Apps tasks 81-90
bash benchmarks/osworld/run_batch.sh 81 90 multi_apps
```

Logs are saved to `/tmp/osworld_batch_<domain>/task<N>.log`. A summary is printed at the end.

### Run Official Evaluation Only

If you already ran the agent and just want to re-evaluate:

```bash
python benchmarks/osworld/eval_osworld_task.py <task_number> --vm <VM_IP>
```

## What the Script Does

For each task, `run_osworld_task.py` performs:

1. **Revert VM** — `vmrun revertToSnapshot` to `init_state`
2. **Setup** — Run OSWorld's official setup steps (download files, launch apps, open URLs)
3. **Configure** — Install Chromium proxy wrapper, set system-wide proxy, set resolution to 1920x1080
4. **Run agent** — `gui_agent()` executes the task autonomously (observe → verify → plan → dispatch loop)
5. **Evaluate** — Run OSWorld's official evaluator to score the result
6. **Report** — Print score, steps, timing, and per-step action history

## File Structure

```
benchmarks/osworld/
├── run_osworld_task.py    # Main runner: setup VM → run agent → evaluate
├── run_batch.sh           # Batch runner: loop over task range
├── eval_osworld_task.py   # Standalone evaluator (calls OSWorld's eval)
├── cache/                 # Cached evaluation files (auto-created)
├── multi_apps.md          # Multi-Apps domain results (101 tasks)
├── chrome.md              # Chrome domain results
├── gimp.md                # GIMP domain results
├── os.md                  # OS domain results
├── libreoffice_calc.md    # LibreOffice Calc results
├── libreoffice_impress.md
├── libreoffice_writer.md
├── thunderbird.md
├── vlc.md
└── vscode.md
```

## Hardcoded Paths

If your setup differs from the defaults, check these in `run_osworld_task.py`:

```python
OSWORLD_DIR = os.path.expanduser("~/OSWorld")           # OSWorld repo location
VMRUN = "/Applications/VMware Fusion.app/.../vmrun"      # VMware Fusion CLI
VMX = os.path.expanduser("~/OSWorld/vmware_vm_data/Ubuntu-arm/Ubuntu.vmx")  # VM file
VM_IP = "172.16.82.132"                                  # Default VM IP (--vm flag)
PROXY_URL = "http://172.16.82.1:6152"                    # Surge proxy on host
```

## Test Environment

- **Host**: macOS (Apple Silicon)
- **VM**: Ubuntu ARM (aarch64), VMware Fusion
- **Resolution**: 1920x1080
- **LLM**: Claude Opus 4.6 via Claude Code CLI
- **Framework**: [OpenProgram](https://github.com/Fzkuji/OpenProgram) (Agentic Programming paradigm)

## Domain Results

- [Chrome](chrome.md) — 43/46 (93.5%)
- [Multi-Apps](multi_apps.md) — 72.6/91 (79.8%)
- [OS](os.md) — 24/24 (100%)
- [GIMP](gimp.md) — In progress
