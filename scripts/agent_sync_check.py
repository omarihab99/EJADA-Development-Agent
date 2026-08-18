#!/usr/bin/env python3
"""
agent_sync_check.py — upstream version check & update recommendation for the Development Agent Suite.

Compares every local `*.agent.md` against its upstream counterpart in the source repository
(default: github/awesome-copilot, `agents/` directory) and classifies drift.

Design rule: this tool RECOMMENDS. It never silently overwrites a customised agent.
  --apply   updates IDENTICAL-lineage files only (safe: they match upstream byte-for-byte,
            so an upstream change is a pure upgrade)
  --force   additionally overwrites DRIFTED files (destroys local customisation — requires a
            recorded human decision)

Usage:
    python scripts/agent_sync_check.py --report
    python scripts/agent_sync_check.py --report --out registry/UPSTREAM_SYNC_REPORT.md
    python scripts/agent_sync_check.py --apply
    python scripts/agent_sync_check.py --upstream-ref v2.1.0

Network: downloads a tarball from codeload.github.com (no API token, no rate limit).
Falls back to --upstream-dir for an already-extracted local copy (air-gapped use).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import urllib.request

DEFAULT_REPO = "github/awesome-copilot"
DEFAULT_REF = "main"
DEFAULT_UPSTREAM_SUBDIR = "agents"
LOCAL_AGENT_DIRS = [".github/agents"]          # non-dev-agents/ is deliberately excluded from routing
QUARANTINE_DIRS = ["non-dev-agents"]           # present locally, but intentionally NOT delegation targets
LOCK_FILE = "registry/.agentlock.json"


# ----------------------------------------------------------------------------- helpers

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_frontmatter(text: str) -> dict:
    """Minimal frontmatter reader — avoids a PyYAML dependency for four scalar fields."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm, out = m.group(1), {}
    for key in ("name", "description", "model", "version"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        if km:
            out[key] = km.group(1).strip().strip("'\"")
    return out


def fetch_upstream(repo: str, ref: str, subdir: str) -> dict[str, bytes]:
    """Return {filename: content_bytes} for *.agent.md under `subdir` in the upstream tarball."""
    url = f"https://codeload.github.com/{repo}/tar.gz/refs/heads/{ref}"
    print(f"[sync] fetching {url}", file=sys.stderr)
    try:
        with urllib.request.urlopen(url, timeout=180) as resp:
            blob = resp.read()
    except Exception as exc:                                   # tag rather than branch
        url = f"https://codeload.github.com/{repo}/tar.gz/refs/tags/{ref}"
        print(f"[sync] branch fetch failed ({exc}); trying {url}", file=sys.stderr)
        with urllib.request.urlopen(url, timeout=180) as resp:
            blob = resp.read()

    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        for member in tf.getmembers():
            parts = member.name.split("/")
            if len(parts) >= 3 and parts[1] == subdir and member.name.endswith(".agent.md"):
                fh = tf.extractfile(member)
                if fh:
                    files[parts[-1]] = fh.read()
    print(f"[sync] upstream agents found: {len(files)}", file=sys.stderr)
    return files


def load_upstream_dir(path: str) -> dict[str, bytes]:
    return {
        f: open(os.path.join(path, f), "rb").read()
        for f in os.listdir(path)
        if f.endswith(".agent.md")
    }


def collect_local(root: str) -> dict[str, tuple[str, bytes]]:
    """Return {filename: (relative_path, content_bytes)}."""
    out: dict[str, tuple[str, bytes]] = {}
    for d in LOCAL_AGENT_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if f.endswith(".agent.md"):
                rel = os.path.join(d, f)
                out[f] = (rel, open(os.path.join(root, rel), "rb").read())
    return out


def child_agent_refs(text: str, known_names: set[str]) -> list[str]:
    """Agent names this file references — sub-orchestrators embed their child lists."""
    return sorted({n for n in known_names if re.search(rf"`{re.escape(n)}`", text)})


# ----------------------------------------------------------------------------- core

def collect_quarantined(root: str) -> set[str]:
    """Filenames present locally but deliberately outside the delegation scope."""
    out: set[str] = set()
    for d in QUARANTINE_DIRS:
        full = os.path.join(root, d)
        if os.path.isdir(full):
            out |= {f for f in os.listdir(full) if f.endswith(".agent.md")}
    return out


def classify(local: dict, upstream: dict, quarantined: set[str] | None = None) -> list[dict]:
    rows = []
    all_names = {read_frontmatter(c.decode("utf-8", "replace")).get("name", "")
                 for _, c in local.values()} - {""}

    for fname, (rel, content) in sorted(local.items()):
        text = content.decode("utf-8", "replace")
        fm = read_frontmatter(text)
        lh = sha256_bytes(content)
        if fname in upstream:
            uh = sha256_bytes(upstream[fname])
            drift = "IDENTICAL" if uh == lh else "DRIFTED"
            usize = len(upstream[fname])
        else:
            drift, uh, usize = "LOCAL-ONLY", "", 0
        rows.append({
            "file": fname,
            "path": rel,
            "name": fm.get("name", ""),
            "model": fm.get("model", ""),
            "drift": drift,
            "local_sha": lh[:12],
            "upstream_sha": uh[:12],
            "local_bytes": len(content),
            "upstream_bytes": usize,
            "delta_bytes": len(content) - usize if usize else None,
            "references": child_agent_refs(text, all_names),
        })

    quarantined = quarantined or set()
    for fname in sorted(set(upstream) - set(local)):
        fm = read_frontmatter(upstream[fname].decode("utf-8", "replace"))
        rows.append({
            "file": fname, "path": "", "name": fm.get("name", ""), "model": fm.get("model", ""),
            "drift": "QUARANTINED" if fname in quarantined else "UPSTREAM-NEW", "local_sha": "", "upstream_sha": sha256_bytes(upstream[fname])[:12],
            "local_bytes": 0, "upstream_bytes": len(upstream[fname]), "delta_bytes": None,
            "references": [],
        })
    return rows


RECOMMENDATION = {
    "IDENTICAL":    "No action. Safe to auto-update on the next upstream change.",
    "DRIFTED":      "REVIEW — three-way diff required. Do not bulk-overwrite; local edits may be deliberate.",
    "LOCAL-ONLY":   "Exclude from sync. Confirm nothing upstream supersedes it.",
    "UPSTREAM-NEW": "Adopt only if it fills a real gap. Each added agent costs routing accuracy.",
    "QUARANTINED":  "Held in non-dev-agents/ by design. Do not move into .github/agents/.",
}


def render_report(rows: list[dict], repo: str, ref: str) -> str:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["drift"]] = counts.get(r["drift"], 0) + 1
    today = dt.date.today().isoformat()

    out = [
        "# Upstream Sync Report",
        "",
        f"**Generated:** {today}  ",
        f"**Upstream:** `{repo}` @ `{ref}` (`{DEFAULT_UPSTREAM_SUBDIR}/`)  ",
        f"**Local scope:** {', '.join(LOCAL_AGENT_DIRS)}",
        "",
        "## Summary",
        "",
        "| Drift class | Count | Recommendation |",
        "|---|---:|---|",
    ]
    for k in ("IDENTICAL", "DRIFTED", "LOCAL-ONLY", "UPSTREAM-NEW", "QUARANTINED"):
        if counts.get(k):
            out.append(f"| `{k}` | {counts[k]} | {RECOMMENDATION[k]} |")

    drifted = [r for r in rows if r["drift"] == "DRIFTED"]
    if drifted:
        out += ["", "## Requires human decision — DRIFTED", "",
                "| File | Agent name | Local bytes | Upstream bytes | Delta | References |",
                "|---|---|---:|---:|---:|---|"]
        for r in drifted:
            refs = ", ".join(f"`{x}`" for x in r["references"][:6]) or "—"
            out.append(f"| `{r['file']}` | {r['name']} | {r['local_bytes']} | "
                       f"{r['upstream_bytes']} | {r['delta_bytes']:+d} | {refs} |")
        out += ["", "> A large positive delta usually means local customisation or an older, more "
                "verbose upstream generation. Confirm the direction before taking upstream.", ""]

    local_only = [r for r in rows if r["drift"] == "LOCAL-ONLY"]
    if local_only:
        out += ["", "## Local-only agents (excluded from sync)", "",
                "| File | Agent name | Referenced by |", "|---|---|---|"]
        by_ref = {r["file"]: [o["file"] for o in rows if r["name"] and r["name"] in o["references"]]
                  for r in local_only}
        for r in local_only:
            refs = ", ".join(f"`{x}`" for x in by_ref[r["file"]]) or "— (orphan)"
            out.append(f"| `{r['file']}` | {r['name']} | {refs} |")

    new = [r for r in rows if r["drift"] == "UPSTREAM-NEW"]
    if new:
        out += ["", "## New upstream agents available", "", "| File | Agent name | Model pin |",
                "|---|---|---|"]
        for r in new:
            out.append(f"| `{r['file']}` | {r['name']} | `{r['model'] or '(none)'}` |")

    out += ["", "## Decision log", "",
            "| Date | File | Drift | Decision | Decided by |", "|---|---|---|---|---|",
            "| | | | | |", "",
            "> Record every take-upstream / keep-local / merge decision here before merging.",
            "", "## Post-sync checklist", "",
            "- [ ] Re-run `python scripts/model_audit.py --report` — upstream files carry upstream model pins",
            "- [ ] Verify no sub-orchestrator lost a child-agent reference",
            "- [ ] Verify agent `name:` uniqueness across the suite",
            "- [ ] Update `registry/AGENT_REGISTRY.csv`", ""]
    return "\n".join(out)


def write_lock(root: str, rows: list[dict], repo: str, ref: str) -> None:
    lock = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "upstream": {"repo": repo, "ref": ref, "subdir": DEFAULT_UPSTREAM_SUBDIR},
        "agents": {r["file"]: {"name": r["name"], "drift": r["drift"],
                               "local_sha": r["local_sha"], "upstream_sha": r["upstream_sha"]}
                   for r in rows if r["drift"] not in ("UPSTREAM-NEW", "QUARANTINED")},
    }
    path = os.path.join(root, LOCK_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(lock, open(path, "w", encoding="utf-8"), indent=1)
    print(f"[sync] wrote {LOCK_FILE}", file=sys.stderr)


def apply_updates(root: str, rows: list[dict], upstream: dict[str, bytes], force: bool) -> int:
    n = 0
    for r in rows:
        if r["drift"] == "IDENTICAL":
            continue                                    # already current
        if r["drift"] == "DRIFTED" and not force:
            print(f"[skip] {r['file']} — DRIFTED, needs --force + recorded decision", file=sys.stderr)
            continue
        if r["drift"] in ("LOCAL-ONLY", "UPSTREAM-NEW", "QUARANTINED"):
            continue                                    # never auto-add or auto-delete
        dest = os.path.join(root, r["path"])
        shutil.copyfile(dest, dest + ".bak")
        open(dest, "wb").write(upstream[r["file"]])
        print(f"[apply] {r['file']} updated (backup: {r['file']}.bak)", file=sys.stderr)
        n += 1
    return n


def main() -> int:
    p = argparse.ArgumentParser(description="Upstream agent version check and update recommendation.")
    p.add_argument("--root", default=".", help="repository root")
    p.add_argument("--repo", default=DEFAULT_REPO)
    p.add_argument("--upstream-ref", default=DEFAULT_REF, help="branch or tag")
    p.add_argument("--upstream-dir", help="use an already-extracted upstream agents/ dir (offline)")
    p.add_argument("--report", action="store_true", help="print a Markdown report")
    p.add_argument("--out", help="write the report to this path")
    p.add_argument("--json", help="write raw classification JSON to this path")
    p.add_argument("--apply", action="store_true", help="update IDENTICAL-lineage files")
    p.add_argument("--force", action="store_true", help="also overwrite DRIFTED files (destructive)")
    a = p.parse_args()

    local = collect_local(a.root)
    if not local:
        print(f"[error] no *.agent.md found under {LOCAL_AGENT_DIRS} in {a.root}", file=sys.stderr)
        return 2

    upstream = (load_upstream_dir(a.upstream_dir) if a.upstream_dir
                else fetch_upstream(a.repo, a.upstream_ref, DEFAULT_UPSTREAM_SUBDIR))

    rows = classify(local, upstream, collect_quarantined(a.root))
    write_lock(a.root, rows, a.repo, a.upstream_ref)

    if a.json:
        json.dump(rows, open(a.json, "w", encoding="utf-8"), indent=1)

    if a.report or a.out:
        report = render_report(rows, a.repo, a.upstream_ref)
        if a.out:
            os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
            open(a.out, "w", encoding="utf-8").write(report)
            print(f"[sync] wrote {a.out}", file=sys.stderr)
        else:
            print(report)

    if a.apply:
        n = apply_updates(a.root, rows, upstream, a.force)
        print(f"[sync] {n} file(s) updated. Re-run model_audit.py.", file=sys.stderr)

    return 1 if any(r["drift"] == "DRIFTED" for r in rows) else 0   # non-zero for CI visibility


if __name__ == "__main__":
    raise SystemExit(main())
