"""Static integrity checks for the Development Agent Suite.

Run from the repository root:  python -m pytest -q tests
Requires: pytest, pyyaml.
"""
import csv
import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT_DIRS = [ROOT / ".github" / "agents", ROOT / "non-dev-agents"]
FILES = sorted(p for d in AGENT_DIRS for p in d.glob("*.agent.md"))
DELEGATION_TOOLS = {"runSubagent", "agent", "agent/runSubagent"}
# Keys seen in the suite; confirm against current GitHub Copilot custom-agent documentation before extending.
ALLOWED_KEYS = {
    "name", "description", "tools", "model", "target", "mcp-servers", "handoffs", "argument-hint",
    "user-invocable", "disable-model-invocation", "agents", "mode", "hidden", "agent",
    "version", "owner", "last-reviewed",
}


def load(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name}: missing or unterminated front matter"
    return yaml.safe_load(m.group(1)), text


def registry():
    with open(ROOT / "registry" / "AGENT_REGISTRY.csv", encoding="utf-8", newline="") as f:
        return {r["file"]: r for r in csv.DictReader(f)}


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_frontmatter_is_valid(path):
    fm, text = load(path)
    assert isinstance(fm, dict)
    assert fm.get("name"), "name required"
    assert fm.get("description"), "description required"
    unknown = set(fm) - ALLOWED_KEYS
    assert not unknown, f"unsupported/corrupt keys: {unknown}"
    assert not re.search(r"&lt;|&gt;|&amp;|&quot;|<br\s*/?>|Show more lines", text), "chat-UI residue"


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_model_is_single_scalar(path):
    fm, _ = load(path)
    model = fm.get("model")
    assert model is None or (isinstance(model, str) and not re.search(r"[|\[\],]", model))


def test_names_unique():
    names = [load(p)[0]["name"] for p in FILES]
    assert len(names) == len(set(names))


def test_registry_matches_files():
    reg = registry()
    files = {p.name: load(p)[0]["name"] for p in FILES}
    assert set(reg) == set(files), f"registry-only={set(reg) - set(files)} file-only={set(files) - set(reg)}"
    assert {f: r["name"] for f, r in reg.items()} == files


def test_index_targets_exist():
    idx = (ROOT / ".github" / "agents" / "AGENT_INDEX.md").read_text(encoding="utf-8")
    listed = re.findall(r"^\| `[^`]+` \| `([^`]+\.agent\.md)` \|", idx, re.M)
    missing = [f for f in listed if not (ROOT / ".github" / "agents" / f).exists()]
    assert not missing, f"index lists missing files: {missing}"
    on_disk = {p.name for p in (ROOT / ".github" / "agents").glob("*.agent.md")}
    assert on_disk == set(listed), f"index/disk mismatch: {on_disk ^ set(listed)}"


def test_only_registered_t0_t1_agents_can_delegate():
    reg = registry()
    offenders = []
    for p in FILES:
        fm, _ = load(p)
        tools = fm.get("tools") or []
        tools = tools if isinstance(tools, list) else [tools]
        if DELEGATION_TOOLS & set(map(str, tools)) and reg[p.name]["tier"] not in {"T0", "T1"}:
            offenders.append(p.name)
    assert not offenders, offenders


def test_t1_agents_declare_child_allowlist():
    reg = registry()
    for p in FILES:
        if reg[p.name]["tier"] == "T1":
            fm, _ = load(p)
            assert fm.get("agents"), f"{p.name}: T1 requires an `agents:` allowlist"


def test_only_one_t0():
    assert [f for f, r in registry().items() if r["tier"] == "T0"] == ["universal-orchestrator.agent.md"]


def test_shared_instructions_exist_and_restore_script_has_no_embedded_copy():
    assert (ROOT / ".github" / "copilot-instructions.md").exists()
    src = (ROOT / "scripts" / "restore_copilot_instructions.py").read_text(encoding="utf-8")
    assert "CONTENT = r'''" not in src and 'CONTENT = r"""' not in src


def test_response_contract_defines_agent_line_and_delegation_plan():
    rc = (ROOT / "governance" / "RESPONSE_CONTRACT_AND_VALIDATION.md").read_text(encoding="utf-8")
    assert "🤖 Agent:" in rc and "Delegation Plan" in rc


def test_approval_token_is_defined_consistently():
    for rel in ["governance/AGENT_GOVERNANCE.md", ".github/agents/universal-orchestrator.agent.md"]:
        assert "APPROVE" in (ROOT / rel).read_text(encoding="utf-8"), rel


def test_readme_links_exist():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for ref in re.findall(r"\]\(([^)#]+)\)", readme):
        if not ref.startswith("http"):
            assert (ROOT / ref).exists(), f"README link broken: {ref}"
