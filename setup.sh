#!/usr/bin/env bash
echo "[Setup] Configuring git hooks..."
git config core.hooksPath .githooks
chmod +x .githooks/*
echo "[Setup] Checking project integrity..."
python3 scripts/restore_copilot_instructions.py
echo "[Setup] Done. Future git pull/checkout will auto-restore missing files."
