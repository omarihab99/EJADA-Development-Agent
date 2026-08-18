"""Tests that the agent-identification guideline is enforced."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
AGENTS_DIR = ROOT / ".github" / "agents"


def test_copilot_instructions_contains_agent_identification_rule():
    """The shared guidelines must include the agent identification directive."""
    text = INSTRUCTIONS.read_text(encoding="utf-8")
    assert "Agent identification" in text
    assert "🤖 Agent:" in text


def test_agent_files_have_yaml_frontmatter_with_name():
    """Every .agent.md must have YAML frontmatter containing a name field."""
    agent_files = sorted(AGENTS_DIR.glob("*.agent.md"))
    assert len(agent_files) > 0, "No agent files found"

    missing_name = []
    for path in agent_files:
        content = path.read_text(encoding="utf-8")
        # Must start with YAML frontmatter delimiters
        if not content.startswith("---"):
            missing_name.append(path.name)
            continue
        # Extract frontmatter block
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            missing_name.append(path.name)
            continue
        frontmatter = match.group(1)
        if "name:" not in frontmatter:
            missing_name.append(path.name)

    assert missing_name == [], f"Agents missing 'name:' in frontmatter: {missing_name}"
