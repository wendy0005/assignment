#!/usr/bin/env bash
# Helper script to launch VS Code and open Wokwi diagram for SentinelSleep

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

echo "Opening SentinelSleep project in VS Code..."
code "$PROJECT_DIR" "$PROJECT_DIR/diagram.json"

echo "VS Code opened! In VS Code, open diagram.json and click 'Start Simulation' or press F1 -> Wokwi: Start Simulator."
