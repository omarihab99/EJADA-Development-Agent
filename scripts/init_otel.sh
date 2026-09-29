#!/usr/bin/env bash
# Ensures Node.js and npm are available before running
command -v npm >/dev/null 2>&1 || { echo "Error: npm is required but not installed." >&2; exit 1; }

# Download and run the standalone Aspire dashboard directly
npx -y @microsoft/aspire-cli dashboard run
