#!/usr/bin/env python3
"""
model_audit.py — audit and remediate `model:` pins across the Development Agent Suite.

Checks every `*.agent.md` frontmatter `model:` value against the GitHub Copilot supported-model
tables and classifies it. With --fix, proposes a compliant replacement based on the task class
inferred from the agent's filename and description.

Model tables verified 2026-08-17 against:
  docs.github.com → Copilot → Reference → AI models → Supported models
KEEP SECTION `MODEL TABLES` IN SYNC WITH governance/MODEL_POLICY.md — they must not diverge.

Usage:
    python scripts/model_audit.py --report
    python scripts/model_audit.py --report --out registry/MODEL_AUDIT.md
    python scripts/model_audit.py --csv registry/model_audit.csv
    python scripts/model_audit.py --fix --dry-run
    python scripts/model_audit.py --fix                # writes frontmatter, creates .bak files

Exit codes: 0 = clean, 1 = retired/invalid pins found (use in CI).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import shutil
import sys

SCAN_DIRS = [".github/agents", "non-dev-agents"]
TABLE_VERIFIED = "2026-08-17"

# ----------------------------------------------------------------- MODEL TABLES

SUPPORTED = {
    "claude opus 5", "claude sonnet 5", "claude opus 4.7", "claude opus 4.8", "claude haiku 4.5",
    "claude opus 4.8 (fast mode)", "gpt-5.5", "gpt-5.6 luna", "gpt-5.6 sol", "gpt-5.6 terra",
    "gpt-5.4", "gpt-5.4 mini", "gpt-5 mini", "gpt-5.3-codex", "gemini 3.5 flash",
    "gemini 3.6 flash", "gemini 3.7 flash", "mai-code-1-flash", "mai-code-1.1-flash",
    "grok 4.5", "grok 4.6", "auto",
}

APPROVAL_GATED = {                       # usable, but require a named approval
    "claude fable 5": "distinct data-retention posture; not eligible for default enablement",
    "kimi k2.7 code": "open weight; not eligible for default enablement",
    "kimi k3": "open weight; not eligible for default enablement",
}

SUNSET = {                               # retiring 2026-09-01
    "claude sonnet 4.5": "Claude Sonnet 5", "claude sonnet 4.6": "Claude Sonnet 5",
    "claude opus 4.5": "Claude Opus 5", "claude opus 4.6": "Claude Opus 5",
    "gemini 3.1 pro": "Gemini 3.6 Flash", "raptor mini": "MAI-Code-1-Flash",
}
SUNSET_DATE = "2026-09-01"

RETIRED = {                              # model -> (retirement date, successor)
    "gpt-4.1": ("2026-06-01", "GPT-5.5"),
    "gpt-5.2": ("2026-06-01", "GPT-5.5"),
    "gpt-5.2-codex": ("2026-06-01", "GPT-5.3-Codex"),
    "grok code fast 1": ("2026-05-15", "GPT-5 mini"),
    "claude sonnet 4": ("2026-05-01", "Claude Sonnet 5"),
    "gpt-5.1": ("2026-04-15", "GPT-5.3-Codex"),
    "gpt-5.1-codex": ("2026-04-01", "GPT-5.3-Codex"),
    "gpt-5.1-codex-max": ("2026-04-01", "GPT-5.3-Codex"),
    "gpt-5.1-codex-mini": ("2026-04-01", "GPT-5.3-Codex"),
    "gemini 3 pro": ("2026-03-26", "Gemini 3.6 Flash"),
    "gpt-5": ("2026-02-17", "GPT-5.5"),
    "gpt-5-codex": ("2026-02-17", "GPT-5.3-Codex"),
    "claude opus 4.1": ("2026-02-17", "Claude Opus 5"),
    "claude sonnet 3.5": ("2025-11-06", "Claude Haiku 4.5"),
    "claude opus 4": ("2025-10-23", "Claude Opus 5"),
    "claude sonnet 3.7": ("2025-10-23", "Claude Sonnet 5"),
    "claude sonnet 3.7 thinking": ("2025-10-23", "Claude Sonnet 5"),
    "gemini 2.0 flash": ("2025-10-23", "Gemini 3.6 Flash"),
    "gemini 2.5 pro": ("2026-07-31", "Gemini 3.6 Flash"),
    "gemini 3 flash": ("2026-07-31", "Gemini 3.6 Flash"),
    "o1-mini": ("2025-10-23", "GPT-5 mini"), "o3": ("2025-10-23", "GPT-5.5"),
    "o3-mini": ("2025-10-23", "GPT-5 mini"), "o4-mini": ("2025-10-23", "GPT-5 mini"),
}

UTILITY_ONLY = {"gpt-4o", "gpt-4o mini", "gpt-4", "gpt-4.1", "gpt-5.4 nano"}

# API-style aliases → canonical picker names
ALIASES = {
    "claude-sonnet-4-5": "claude sonnet 4.5", "claude-sonnet-4.5": "claude sonnet 4.5",
    "claude-sonnet-4-5-20250929": "claude sonnet 4.5",
    "claude-sonnet-4-6": "claude sonnet 4.6", "claude-sonnet-4.6": "claude sonnet 4.6",
    "claude-sonnet-4": "claude sonnet 4", "claude-3.5-sonnet": "claude sonnet 3.5",
    "claude-3-5-sonnet": "claude sonnet 3.5", "claude-opus-4.7": "claude opus 4.7",
    "claude-opus-4-7": "claude opus 4.7", "claude-opus-4.6": "claude opus 4.6",
    "claude-opus-5": "claude opus 5", "claude-sonnet-5": "claude sonnet 5",
    "gpt5": "gpt-5", "gpt4.1": "gpt-4.1", "gpt-4-1": "gpt-4.1",
}

# ----------------------------------------------------------------- TASK CLASSES

# Matched against the FILENAME first (a strong, stable signal), then the description as fallback.
# Order matters — the first match wins. Proposals are advisory: always review --fix output.
TASK_CLASSES = [
    ("orchestration",    r"orchestrat|umbrella|commander|coordinator|router",      "Claude Opus 5"),
    ("tests",            r"test|\bqa\b|playwright|\btdd\b|coverage|diffblue|a11y|accessib",
                                                                                  "GPT-5 mini"),
    ("docs-boilerplate", r"writer|\bdocs?\b|documentation|readme|changelog|tour|markdown|content",
                                                                                  "GPT-5 mini"),
    ("architecture",     r"architect|\badr\b|blueprint|threat|security|governance|principal|sentinel|policy",
                                                                                  "Claude Opus 5"),
    ("codex-autonomy",   r"scaffold|generator|foundry|migration|moderniz|upgrade|implementer|exporter",
                                                                                  "GPT-5.3-Codex"),
    ("fast-interactive", r"terminal|helper|cheat|mentor|study|prep|lookup",        "Claude Haiku 4.5"),
]
DEFAULT_MODEL = "Claude Sonnet 5"          # day-to-day coding — the majority class


def normalise(raw: str) -> str:
    if not raw:
        return ""
    v = raw.strip()
    v = re.sub(r"^-\s*", "", v)                       # YAML list item: "- GPT-4.1"
    v = v.split("|")[0]                               # pipe-delimited alternatives
    v = v.strip().strip("[]").split(",")[0]           # list literal
    v = v.strip().strip("'\"").strip()
    v = re.sub(r"\s*\(copilot\)\s*$", "", v, flags=re.I)
    v = v.lower()
    return ALIASES.get(v, v)


def is_malformed(raw: str) -> bool:
    return bool(raw) and bool(re.search(r"^\s*[-\[]|\||,", raw))


def classify(raw: str) -> tuple[str, str]:
    """Return (status, note)."""
    if not raw:
        return "UNPINNED", "no model declared — behaviour depends on the user's picker"
    v = normalise(raw)
    if is_malformed(raw):
        return "MALFORMED", f"not a single scalar value; parsed as '{v}'"
    if v in RETIRED:
        d, succ = RETIRED[v]
        extra = " (also a utility model — never selectable in the picker)" if v in UTILITY_ONLY else ""
        return "RETIRED", f"retired {d} → use {succ}{extra}"
    if v in UTILITY_ONLY:
        return "UTILITY-ONLY", "utility model — not selectable in the picker"
    if v in SUNSET:
        return "SUNSET", f"retires {SUNSET_DATE} → use {SUNSET[v]}"
    if v in APPROVAL_GATED:
        return "APPROVAL-GATED", APPROVAL_GATED[v]
    if v in SUPPORTED:
        return "OK", ""
    return "UNKNOWN", "not present in the verified supported-model table"


def task_class(fname: str, desc: str) -> tuple[str, str]:
    """Filename is the primary signal; description is a weaker fallback."""
    stem = fname.replace(".agent.md", "").lower()
    for name, pat, model in TASK_CLASSES:
        if re.search(pat, stem):
            return name, model
    d = (desc or "").lower()
    for name, pat, model in TASK_CLASSES:
        if re.search(pat, d):
            return name, model
    return "coding", DEFAULT_MODEL


def frontmatter_span(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), m.start(1), m.end(1)) if m else (None, 0, 0)


def scan(root: str) -> list[dict]:
    rows = []
    for d in SCAN_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if not f.endswith(".agent.md"):
                continue
            rel = os.path.join(d, f)
            text = open(os.path.join(root, rel), encoding="utf-8").read()
            fm, _, _ = frontmatter_span(text)
            fm = fm or ""
            get = lambda k: (re.search(rf"^{k}:\s*(.+)$", fm, re.M).group(1).strip().strip("'\"")
                             if re.search(rf"^{k}:", fm, re.M) else "")
            raw = re.search(r"^model:\s*(.+)$", fm, re.M)
            raw = raw.group(1).strip() if raw else ""
            status, note = classify(raw)
            tc, proposed = task_class(f, get("description"))
            rows.append({
                "path": rel, "file": f, "name": get("name"), "scope":
                    "dev" if d == ".github/agents" else "non-dev",
                "declared": raw, "normalised": normalise(raw), "status": status, "note": note,
                "task_class": tc, "proposed": "" if status in ("OK", "APPROVAL-GATED") else proposed,
            })
    return rows


def apply_fix(root: str, rows: list[dict], dry: bool) -> int:
    n = 0
    for r in rows:
        if not r["proposed"]:
            continue
        p = os.path.join(root, r["path"])
        text = open(p, encoding="utf-8").read()
        fm, s, e = frontmatter_span(text)
        if fm is None:
            print(f"[skip] {r['file']} — no frontmatter", file=sys.stderr)
            continue
        if re.search(r"^model:", fm, re.M):
            new_fm = re.sub(r"^model:.*$", f"model: '{r['proposed']}'", fm, count=1, flags=re.M)
        else:
            new_fm = fm + f"\nmodel: '{r['proposed']}'"
        new_text = text[:s] + new_fm + text[e:]
        verb = "would set" if dry else "set"
        print(f"[{verb}] {r['file']}: '{r['declared'] or '(none)'}' -> "
              f"'{r['proposed']}' [{r['task_class']}]")
        if not dry:
            shutil.copyfile(p, p + ".bak")
            open(p, "w", encoding="utf-8").write(new_text)
        n += 1
    return n


ORDER = ["RETIRED", "SUNSET", "UTILITY-ONLY", "MALFORMED", "UNKNOWN",
         "UNPINNED", "APPROVAL-GATED", "OK"]


def render(rows: list[dict]) -> str:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    out = ["# Model Policy Audit", "",
           f"**Generated:** {dt.date.today().isoformat()}  ",
           f"**Model tables verified:** {TABLE_VERIFIED}  ",
           f"**Files scanned:** {len(rows)} across {', '.join(SCAN_DIRS)}", "",
           "## Summary", "", "| Status | Count | Meaning |", "|---|---:|---|"]
    meaning = {
        "RETIRED": "Pin is dead — Copilot falls back silently",
        "SUNSET": f"Breaks on {SUNSET_DATE}",
        "UTILITY-ONLY": "Not selectable in the model picker",
        "MALFORMED": "Not a single scalar value",
        "UNKNOWN": "Not in the verified supported table",
        "UNPINNED": "No pin — depends on the user's picker",
        "APPROVAL-GATED": "Usable, but requires a named approval",
        "OK": "Valid and current",
    }
    for k in ORDER:
        if counts.get(k):
            out.append(f"| `{k}` | {counts[k]} | {meaning[k]} |")

    for k in ("SUNSET", "RETIRED", "UTILITY-ONLY", "MALFORMED", "UNKNOWN"):
        sel = [r for r in rows if r["status"] == k]
        if not sel:
            continue
        title = {"SUNSET": f"P1 — breaks on {SUNSET_DATE}", "RETIRED": "P1 — already retired",
                 "UTILITY-ONLY": "P2 — utility-only pins", "MALFORMED": "P3 — malformed values",
                 "UNKNOWN": "P3 — unrecognised values"}[k]
        out += ["", f"## {title}", "",
                "| File | Agent | Declared | Issue | Proposed | Task class |",
                "|---|---|---|---|---|---|"]
        for r in sel:
            out.append(f"| `{r['file']}` | {r['name']} | `{r['declared']}` | {r['note']} | "
                       f"`{r['proposed']}` | {r['task_class']} |")

    unp = [r for r in rows if r["status"] == "UNPINNED"]
    if unp:
        by: dict[str, int] = {}
        for r in unp:
            by[r["task_class"]] = by.get(r["task_class"], 0) + 1
        out += ["", "## P2 — unpinned agents, by proposed task class", "",
                "| Task class | Count | Proposed model |", "|---|---:|---|"]
        for tc, c in sorted(by.items(), key=lambda x: -x[1]):
            model = next(r["proposed"] for r in unp if r["task_class"] == tc)
            out.append(f"| {tc} | {c} | `{model}` |")
        out += ["", "> Apply with `python scripts/model_audit.py --fix --dry-run` first, "
                "then review the proposed diff before writing.", ""]
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Audit model pins against GitHub Copilot model status.")
    p.add_argument("--root", default=".")
    p.add_argument("--report", action="store_true")
    p.add_argument("--out")
    p.add_argument("--csv")
    p.add_argument("--fix", action="store_true", help="write compliant model pins")
    p.add_argument("--dry-run", action="store_true", help="with --fix, print changes only")
    a = p.parse_args()

    rows = scan(a.root)
    if not rows:
        print(f"[error] no *.agent.md found under {SCAN_DIRS} in {a.root}", file=sys.stderr)
        return 2

    if a.csv:
        os.makedirs(os.path.dirname(a.csv) or ".", exist_ok=True)
        with open(a.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"[audit] wrote {a.csv}", file=sys.stderr)

    if a.report or a.out:
        rep = render(rows)
        if a.out:
            os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
            open(a.out, "w", encoding="utf-8").write(rep)
            print(f"[audit] wrote {a.out}", file=sys.stderr)
        else:
            print(rep)

    if a.fix:
        n = apply_fix(a.root, rows, a.dry_run)
        print(f"[audit] {n} file(s) {'would be' if a.dry_run else ''} updated.", file=sys.stderr)

    bad = sum(1 for r in rows
              if r["status"] in ("RETIRED", "SUNSET", "UTILITY-ONLY", "MALFORMED", "UNKNOWN"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
