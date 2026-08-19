@echo off
echo [Setup] Configuring git hooks...
git config core.hooksPath .githooks
echo [Setup] Checking project integrity...
python scripts\restore_copilot_instructions.py
echo [Setup] Done. Future git pull/checkout will auto-restore missing files.
pause
