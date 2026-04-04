#!/usr/bin/env python3
"""
Run an OSWorld task using the Agentic Programming gui_harness framework.

Usage:
    python3 run_agentic.py <task_id_prefix> [--vm-ip IP]
"""

import argparse
import json
import os
import sys
import glob
import time

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def find_task(prefix: str) -> tuple[str, dict]:
    """Find task JSON by prefix."""
    pattern = f"evaluation_examples/examples/multi_apps/{prefix}*.json"
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No task matching {prefix}")
    path = matches[0]
    with open(path) as f:
        return path, json.load(f)


def setup_vm(task: dict, vm_ip: str):
    """Reset VM and apply task config using DesktopEnv."""
    from desktop_env.desktop_env import DesktopEnv
    env = DesktopEnv(
        action_space="pyautogui",
        headless=False,
        require_terminal=True,
        screen_size=(1920, 1080),
        path_to_vm="vmware_vm_data/Ubuntu0/Ubuntu.vmx",
        snapshot_name="init_state",
    )
    obs = env.reset(task_config=task)
    print(f"VM ready. IP: {env.vm_ip}")
    return env


def run_task(task: dict, vm_url: str):
    """Run the task using gui_harness functions."""
    # Patch primitives for VM
    from gui_harness.primitives.vm_adapter import patch_for_vm
    patch_for_vm(vm_url)

    # Import agentic functions
    from gui_harness.functions.observe import observe
    from gui_harness.functions.act import act
    from gui_harness.functions.verify import verify

    instruction = task["instruction"]
    print(f"\n{'='*60}")
    print(f"INSTRUCTION: {instruction[:200]}")
    print(f"{'='*60}\n")

    # Step 1: Observe
    print("[Step 1] Observing screen state...")
    obs = observe(task=instruction)
    print(f"  App: {obs.get('app_name', '?')}")
    print(f"  Description: {obs.get('page_description', '?')[:100]}")
    print(f"  Target visible: {obs.get('target_visible', '?')}")
    if obs.get("target_location"):
        loc = obs["target_location"]
        print(f"  Target at: ({loc.get('x')}, {loc.get('y')}) = {loc.get('label', '')}")
    print()

    # Step 2: The LLM-driven loop
    # For now, just do observe → let the human see what's happening
    # In a full implementation, the LLM would plan and execute actions

    print("[Step 2] Task execution would happen here...")
    print("  (The framework provides observe/act/verify primitives)")
    print("  (A planning layer would orchestrate them based on the instruction)")
    print()

    return obs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task_id", help="Task ID prefix")
    parser.add_argument("--vm-ip", default="172.16.105.128")
    parser.add_argument("--no-reset", action="store_true")
    args = parser.parse_args()

    task_path, task = find_task(args.task_id)
    print(f"Task: {os.path.basename(task_path)}")

    vm_url = f"http://{args.vm_ip}:5000"

    if not args.no_reset:
        setup_vm(task, args.vm_ip)
    
    time.sleep(2)  # Wait for VM to settle
    
    result = run_task(task, vm_url)
    
    print("\n[Done] Observation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])


if __name__ == "__main__":
    main()
