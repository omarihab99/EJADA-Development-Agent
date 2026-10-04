#!/usr/bin/env python3
"""registry_build.py - regenerate registry/AGENT_REGISTRY.csv and .github/agents/AGENT_INDEX.md from disk.

The agent files are the source; the registry is the machine-readable routing source of truth and
AGENT_INDEX.md is a generated human view. Curated columns (domain, provenance, drift, routing_priority,
model_strategy, benchmark_key, notes, supported_tasks, unsupported_tasks, requires_approval_for) are
preserved from the existing registry; everything derivable from the files is recomputed.

Usage:
    python scripts/registry_build.py           # rewrite registry + index
    python scripts/registry_build.py --check   # exit 1 if registry/index are out of date (CI)
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_audit as ma  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "registry", "AGENT_REGISTRY.csv")
INDEX = os.path.join(ROOT, ".github", "agents", "AGENT_INDEX.md")
COLUMNS = [
    "file", "name", "tier", "scope", "domain", "model_declared", "model_status", "tools_count",
    "provenance", "drift", "sha256", "description", "routing_priority", "model_strategy",
    "benchmark_key", "supported_tasks", "unsupported_tasks", "requires_approval_for", "notes",
]
CURATED = ["domain", "provenance", "drift", "routing_priority", "model_strategy", "benchmark_key",
           "supported_tasks", "unsupported_tasks", "requires_approval_for", "notes"]
DELEGATION_TOOLS = {"runSubagent", "agent", "agent/runSubagent"}

# Tiers (AGENT_GOVERNANCE.md section 3). T0 = Universal Orchestrator. T1 = approved bounded sub-orchestrators.
T0 = {"universal-orchestrator.agent.md"}
T1 = {"react18-commander.agent.md", "react19-commander.agent.md", "rug-orchestrator.agent.md"}
# Domain for agents that are not in a previous registry.
NEW_DOMAIN = {
    "universal-orchestrator.agent.md": "Orchestration & Governance",
    "ef-core-expert.agent.md": "Backend - .NET",
    "customer-faq-agent.agent.md": "Documentation",
}
NEW_PROVENANCE = {"customer-faq-agent.agent.md": "UNKNOWN"}  # origin not recorded; do not guess


def sha12(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def load_existing() -> dict[str, dict]:
    if not os.path.exists(REGISTRY):
        return {}
    with open(REGISTRY, encoding="utf-8", newline="") as f:
        return {r["file"]: r for r in csv.DictReader(f)}


def build_rows() -> list[dict]:
    old = load_existing()
    rows = []
    for scope_dir, scope in ((".github/agents", "dev"), ("non-dev-agents", "non-dev")):
        full = os.path.join(ROOT, scope_dir)
        for fname in sorted(os.listdir(full)):
            if not fname.endswith(".agent.md"):
                continue
            path = os.path.join(full, fname)
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            fm = yaml.safe_load(m.group(1)) if m else {}
            raw = fm.get("model")
            declared = "" if raw is None else (raw if isinstance(raw, str) else str(raw))
            status, _ = ma.classify(declared)
            tools = fm.get("tools")
            prev = old.get(fname, {})
            digest = sha12(path)
            if fname in T0:
                tier = "T0"
            elif fname in T1:
                tier = "T1"
            else:
                tier = "T2" if scope == "dev" else "T3"
            row = {c: prev.get(c, "") for c in COLUMNS}
            row.update({
                "file": fname, "name": fm.get("name", ""), "tier": tier, "scope": scope,
                "model_declared": declared, "model_status": status,
                "tools_count": len(tools) if isinstance(tools, list) else (1 if tools else 0),
                "sha256": digest, "description": " ".join(str(fm.get("description", "")).split()),
            })
            if not prev:  # new agent
                row["domain"] = NEW_DOMAIN.get(fname, "")
                row["provenance"] = NEW_PROVENANCE.get(fname, "LOCAL-ONLY")
                row["drift"] = NEW_PROVENANCE.get(fname, "LOCAL-ONLY")
                row["routing_priority"] = "normal"
                row["model_strategy"] = "adaptive"
            elif prev.get("sha256") != digest and prev.get("drift") == "IDENTICAL":
                row["drift"] = "DRIFTED"  # local edit of an upstream-identical file; needs a sync decision record
            # `scope` replaces the old dev/non-dev meaning of `tier`
            rows.append(row)
    return rows


def write_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def build_index(rows: list[dict], generated: str) -> str:
    dev = [r for r in rows if r["scope"] == "dev"]
    t0 = [r for r in dev if r["tier"] == "T0"]
    targets = [r for r in dev if r["tier"] != "T0"]
    non_dev = [r for r in rows if r["scope"] == "non-dev"]
    by_domain: dict[str, list[dict]] = {}
    for r in targets:
        by_domain.setdefault(r["domain"], []).append(r)
    order = sorted(by_domain, key=lambda d: (-len(by_domain[d]), d))
    status_label = lambda r: "unpinned" if r["model_status"] == "UNPINNED" else r["model_status"]  # noqa: E731
    out = [
        "# Agent Routing Index", "",
        f"**Generated:** {generated}  ",
        f"**Delegation targets:** {len(targets)} agents in `.github/agents/` (plus the Universal Orchestrator entry point)  ",
        f"**Excluded:** {len(non_dev)} agents in `non-dev-agents/` are not delegation targets.", "",
        "> Generated by `python scripts/registry_build.py` from the agent files. The machine source of truth is",
        "> `registry/AGENT_REGISTRY.csv`; this index is a navigation view of it. Delegate by the exact `Agent name`",
        "> column - filenames and agent names differ for most entries. Domain grouping is heuristic and is a",
        "> navigation aid, not a constraint: if a better-matching agent sits in another domain, use it.", "",
        "## Domain summary", "", "| Domain | Agents |", "|---|---:|",
    ]
    out += [f"| {d} | {len(by_domain[d])} |" for d in order]
    out += [f"| **Total** | **{len(targets)}** |", ""]
    header = ["| Agent name (delegate by this) | File | Model status | Drift |", "|---|---|---|---|"]
    out += ["## Entry point (T0, not a delegation target)", ""] + header
    out += [f"| `{r['name']}` | `{r['file']}` | {status_label(r)} | {r['drift']} |" for r in t0] + [""]
    for d in order:
        out += [f"## {d}", ""] + header
        for r in sorted(by_domain[d], key=lambda x: x["name"].lower()):
            out.append(f"| `{r['name']}` | `{r['file']}` | {status_label(r)} | {r['drift']} |")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def strip_generated(s: str) -> str:
    return re.sub(r"^\*\*Generated:\*\*.*$", "", s, flags=re.M)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rows = build_rows()
    csv_text = write_csv(rows)
    if args.check:
        cur_csv = open(REGISTRY, encoding="utf-8", newline="").read() if os.path.exists(REGISTRY) else ""
        cur_idx = open(INDEX, encoding="utf-8").read() if os.path.exists(INDEX) else ""
        ok = cur_csv.replace("\r\n", "\n") == csv_text and \
            strip_generated(cur_idx.replace("\r\n", "\n")) == strip_generated(build_index(rows, ""))
        print("registry/index up to date" if ok else "registry/index are OUT OF DATE: run python scripts/registry_build.py")
        return 0 if ok else 1
    with open(REGISTRY, "w", encoding="utf-8", newline="") as f:
        f.write(csv_text)
    with open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(build_index(rows, dt.date.today().isoformat()))
    print(f"wrote {len(rows)} registry rows and the index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
