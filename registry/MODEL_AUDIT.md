# Model Policy Audit

**Generated:** 2026-08-17  
**Model tables verified:** 2026-08-17  
**Files scanned:** 225 across .github/agents, non-dev-agents

## Summary

| Status | Count | Meaning |
|---|---:|---|
| `RETIRED` | 56 | Pin is dead — Copilot falls back silently |
| `SUNSET` | 17 | Breaks on 2026-09-01 |
| `UTILITY-ONLY` | 2 | Not selectable in the model picker |
| `MALFORMED` | 4 | Not a single scalar value |
| `UNPINNED` | 142 | No pin — depends on the user's picker |
| `OK` | 4 | Valid and current |

## P1 — breaks on 2026-09-01

| File | Agent | Declared | Issue | Proposed | Task class |
|---|---|---|---|---|---|
| `ai-readiness-reporter.agent.md` | ai-readiness-reporter | `'Claude Sonnet 4.5'` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |
| `aws-cloud-expert.agent.md` | aws-cloud-expert | `claude-sonnet-4-6` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Opus 5` | architecture |
| `aws-principal-architect.agent.md` | aws-principal-architect | `'Claude Sonnet 4.6'` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Opus 5` | architecture |
| `azure-iac-exporter.agent.md` | azure-iac-exporter | `'Claude Sonnet 4.5'` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5.3-Codex` | codex-autonomy |
| `azure-iac-generator.agent.md` | azure-iac-generator | `'Claude Sonnet 4.5'` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5.3-Codex` | codex-autonomy |
| `custom-agent-foundry.agent.md` | Custom Agent Foundry | `Claude Sonnet 4.5` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5.3-Codex` | codex-autonomy |
| `defender-scout-kql.agent.md` | Defender Scout KQL | `'claude-sonnet-4-5'` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |
| `insiders-a11y-tracker.agent.md` | VS Code Insiders Accessibility Tracker | `Claude Sonnet 4.5` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5 mini` | tests |
| `markdown-accessibility-assistant.agent.md` | Markdown Accessibility Assistant | `'Claude Sonnet 4.6'` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5 mini` | tests |
| `nuxt-expert.agent.md` | Expert Nuxt Developer | `'Claude Sonnet 4.5'` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |
| `oracle-to-postgres-migration-expert.agent.md` | Oracle-to-PostgreSQL Migration Expert | `'Claude Sonnet 4.6 (copilot)'` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5.3-Codex` | codex-autonomy |
| `sast-sca-security-analyzer.agent.md` | sast-sca-security-analyzer | `"Claude Sonnet 4.6"` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Opus 5` | architecture |
| `taxcore-technical-writer.agent.md` | TaxCore Technical Writer | `"claude-sonnet-4.6"` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5 mini` | docs-boilerplate |
| `technical-content-evaluator.agent.md` | technical-content-evaluator | `Claude Sonnet 4.5 (copilot)` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5 mini` | docs-boilerplate |
| `terraform-aws-planning.agent.md` | terraform-aws-planning | `'Claude Sonnet 4.6'` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |
| `vuejs-expert.agent.md` | Expert Vue.js Frontend Engineer | `'Claude Sonnet 4.5'` | retires 2026-09-01 → use Claude Sonnet 5 | `GPT-5 mini` | tests |
| `droid.agent.md` | droid | `"claude-sonnet-4-5-20250929"` | retires 2026-09-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |

## P1 — already retired

| File | Agent | Declared | Issue | Proposed | Task class |
|---|---|---|---|---|---|
| `accessibility-runtime-tester.agent.md` | Accessibility Runtime Tester | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `GPT-5 mini` | tests |
| `accessibility.agent.md` | Accessibility Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `GPT-5 mini` | tests |
| `aem-frontend-specialist.agent.md` | AEM Front-End Specialist | `'GPT-4.1'` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `arch-linux-expert.agent.md` | Arch Linux Expert | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `centos-linux-expert.agent.md` | CentOS Linux Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `context-architect.agent.md` | Context Architect | `'GPT-5'` | retired 2026-02-17 → use GPT-5.5 | `Claude Opus 5` | architecture |
| `csharp-mcp-expert.agent.md` | C# MCP Server Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `debian-linux-expert.agent.md` | Debian Linux Expert | `Claude Sonnet 4` | retired 2026-05-01 → use Claude Sonnet 5 | `Claude Opus 5` | architecture |
| `declarative-agents-architect.agent.md` | Declarative Agents Architect | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Opus 5` | architecture |
| `devtools-regression-investigator.agent.md` | DevTools Regression Investigator | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `drupal-expert.agent.md` | Drupal Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Opus 5` | architecture |
| `expert-embedded-c-engineer.agent.md` | expert-embedded-c-engineer | `'claude-sonnet-4'` | retired 2026-05-01 → use Claude Sonnet 5 | `Claude Sonnet 5` | coding |
| `expert-nextjs-developer.agent.md` | Next.js Expert | `"GPT-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Opus 5` | orchestration |
| `fedora-linux-expert.agent.md` | Fedora Linux Expert | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `frontend-performance-investigator.agent.md` | Frontend Performance Investigator | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `go-mcp-expert.agent.md` | Go MCP Server Development Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `hlbpa.agent.md` | High-Level Big Picture Architect (HLBPA) | `'claude-sonnet-4'` | retired 2026-05-01 → use Claude Sonnet 5 | `GPT-5 mini` | docs-boilerplate |
| `java-mcp-expert.agent.md` | Java MCP Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `kotlin-mcp-expert.agent.md` | Kotlin MCP Server Development Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `kubestellar-console.agent.md` | KubeStellar Console | `gpt-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `mcp-m365-agent-expert.agent.md` | MCP M365 Agent Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `meta-agentic-project-scaffold.agent.md` | Meta Agentic Project Scaffold | `"GPT-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `GPT-5.3-Codex` | codex-autonomy |
| `modernization.agent.md` | Modernization Agent | `'GPT-5'` | retired 2026-02-17 → use GPT-5.5 | `GPT-5.3-Codex` | codex-autonomy |
| `openapi-to-application.agent.md` | OpenAPI to Application Generator | `'GPT-4.1'` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `php-mcp-expert.agent.md` | PHP MCP Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `playwright-tester.agent.md` | Playwright Tester Mode | `Claude Sonnet 4` | retired 2026-05-01 → use Claude Sonnet 5 | `GPT-5 mini` | tests |
| `power-bi-data-modeling-expert.agent.md` | Power BI Data Modeling Expert Mode | `"gpt-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `power-bi-dax-expert.agent.md` | Power BI DAX Expert Mode | `"gpt-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `power-bi-performance-expert.agent.md` | Power BI Performance Expert Mode | `"gpt-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `power-bi-visualization-expert.agent.md` | Power BI Visualization Expert Mode | `"gpt-4.1"` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `power-platform-expert.agent.md` | Power Platform Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `power-platform-mcp-integration-expert.agent.md` | Power Platform MCP Integration Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `project-architecture-planner.agent.md` | Project Architecture Planner | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Opus 5` | architecture |
| `python-mcp-expert.agent.md` | Python MCP Server Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `repo-architect.agent.md` | Repo Architect Agent | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Opus 5` | architecture |
| `ruby-mcp-expert.agent.md` | Ruby MCP Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `rust-mcp-expert.agent.md` | Rust MCP Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `salesforce-apex-triggers.agent.md` | Salesforce Apex & Triggers Development | `claude-3.5-sonnet` | retired 2025-11-06 → use Claude Haiku 4.5 | `Claude Sonnet 5` | coding |
| `salesforce-aura-lwc.agent.md` | Salesforce UI Development (Aura & LWC) | `claude-3.5-sonnet` | retired 2025-11-06 → use Claude Haiku 4.5 | `Claude Sonnet 5` | coding |
| `salesforce-expert.agent.md` | Salesforce Expert Agent | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `GPT-5.3-Codex` | codex-autonomy |
| `salesforce-flow.agent.md` | Salesforce Flow Development | `claude-3.5-sonnet` | retired 2025-11-06 → use Claude Haiku 4.5 | `Claude Sonnet 5` | coding |
| `salesforce-visualforce.agent.md` | Salesforce Visualforce Development | `claude-3.5-sonnet` | retired 2025-11-06 → use Claude Haiku 4.5 | `Claude Opus 5` | architecture |
| `se-gitops-ci-specialist.agent.md` | SE: DevOps/CI | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `se-responsible-ai-code.agent.md` | SE: Responsible AI | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `GPT-5 mini` | tests |
| `se-security-reviewer.agent.md` | SE: Security | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Opus 5` | architecture |
| `se-system-architecture-reviewer.agent.md` | SE: Architect | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Opus 5` | architecture |
| `se-technical-writer.agent.md` | SE: Tech Writer | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `GPT-5 mini` | docs-boilerplate |
| `shopify-expert.agent.md` | Shopify Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `swift-mcp-expert.agent.md` | Swift MCP Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `terminal-helper.agent.md` | terminal-helper | `GPT-4.1 (copilot)` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Haiku 4.5` | fast-interactive |
| `terratest-module-testing.agent.md` | Terratest Module Testing | `"gpt-5"` | retired 2026-02-17 → use GPT-5.5 | `GPT-5 mini` | tests |
| `trojan-skill-hunter.agent.md` | Trojan Skill Hunter | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `typescript-mcp-expert.agent.md` | TypeScript MCP Server Expert | `GPT-4.1` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Sonnet 5` | coding |
| `mentoring-juniors.agent.md` | Sensei - Junior Mentor | `'gpt-4.1'` | retired 2026-06-01 → use GPT-5.5 (also a utility model — never selectable in the picker) | `Claude Haiku 4.5` | fast-interactive |
| `se-product-manager-advisor.agent.md` | SE: Product Manager | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |
| `se-ux-ui-designer.agent.md` | SE: UX Designer | `GPT-5` | retired 2026-02-17 → use GPT-5.5 | `Claude Sonnet 5` | coding |

## P2 — utility-only pins

| File | Agent | Declared | Issue | Proposed | Task class |
|---|---|---|---|---|---|
| `agent-governance-reviewer.agent.md` | Agent Governance Reviewer | `'gpt-4o'` | utility model — not selectable in the picker | `Claude Opus 5` | architecture |
| `azure-logic-apps-expert.agent.md` | Azure Logic Apps Expert Mode | `"gpt-4"` | utility model — not selectable in the picker | `Claude Sonnet 5` | coding |

## P3 — malformed values

| File | Agent | Declared | Issue | Proposed | Task class |
|---|---|---|---|---|---|
| `dotnet-self-learning-architect.agent.md` | .NET Self-Learning Architect | `["GPT-5.3-Codex", "Claude Sonnet 4.6 (copilot)", "Claude Opus 4.6 (copilot)", "Claude Haiku 4.5 (copilot)"]` | not a single scalar value; parsed as 'gpt-5.3-codex' | `Claude Opus 5` | architecture |
| `laravel-expert-agent.agent.md` | Laravel Expert Agent | `GPT-4.1 | 'gpt-5' | 'Claude Sonnet 4.5'` | not a single scalar value; parsed as 'gpt-4.1' | `GPT-5 mini` | tests |
| `new-relic-incident-response.agent.md` | New Relic Incident Response Agent | `- GPT-4.1` | not a single scalar value; parsed as 'gpt-4.1' | `Claude Sonnet 5` | coding |
| `pimcore-expert.agent.md` | Pimcore Expert | `GPT-4.1 | 'gpt-5' | 'Claude Sonnet 4.5'` | not a single scalar value; parsed as 'gpt-4.1' | `Claude Sonnet 5` | coding |

## P2 — unpinned agents, by proposed task class

| Task class | Count | Proposed model |
|---|---:|---|
| coding | 60 | `Claude Sonnet 5` |
| tests | 23 | `GPT-5 mini` |
| architecture | 21 | `Claude Opus 5` |
| orchestration | 12 | `Claude Opus 5` |
| docs-boilerplate | 10 | `GPT-5 mini` |
| codex-autonomy | 10 | `GPT-5.3-Codex` |
| fast-interactive | 6 | `Claude Haiku 4.5` |

> Apply with `python scripts/model_audit.py --fix --dry-run` first, then review the proposed diff before writing.
