#!/usr/bin/env bash
# Helper script to launch VS Code and open Wokwi diagram for SentinelSleep

PROJECT_DIR="/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/project"

echo "Opening SentinelSleep project in VS Code..."
code "$PROJECT_DIR" "$PROJECT_DIR/diagram.json"

echo "VS Code opened! In VS Code, open diagram.json and click 'Start Simulation' or press F1 -> Wokwi: Start Simulator."
