# Response Contract and Governance Validation

**Version 1.1 | Effective 2026-08-19**

## Part A - Response Contract

Every meaningful governance response uses these six sections in order. Use `N/A` rather than hiding an omission.

### 1. Assigned Agent
Exact agent name, reason, model used, and any substitution.

### 2. On-the-spot Answer
Lead with the decision, compliance status, highest risks, and required correction.

### 3. Handoff Prompt
When work continues, provide a self-contained `CONTEXT / TASK / MUST NOT / ACCEPTANCE / RETURN FORMAT` brief.

### 4. Artifact Pack
List only files actually created or changed, with path, status, and verification evidence.

### 5. Next Actions
Every open action includes an owner and explicit date. Unknown owners are `[INPUT NEEDED: owner]`.

### 6. Tracker Update
Record completed work, open work, owner, evidence, blocker, ask, and next step.

## Part B - Governance Review Contract

Before implementation, include:

- Overall decision: `Approved`, `Conditionally Approved`, or `Not Approved`.
- Compliance: `Compliant`, `Partially compliant`, or `Non-compliant`.
- Risk: `Low`, `Medium`, `High`, or `Critical`.
- Findings for model, tools, delegation/routing, secrets/data, ownership/change control, naming/references, completeness, safety, and auditability.
- Inputs, Processing, Skills, Routing, Outputs, and Missing Inputs.
- Required approvals and objective test evidence.

Critical findings cannot be diluted by an overall pass. A plaintext production credential, unbounded command capability, or uncontrolled delegation blocks implementation.

## Part C - Finding schema

| Field | Rule |
|---|---|
| ID | Stable identifier such as `GOV-MODEL-01` |
| Area | Model, Tool, Delegation, Secret, Data, Change, Naming, Drift, Design, Audit |
| Finding | Specific observed condition, not a generic warning |
| Risk | Low, Medium, High, Critical |
| Evidence | Exact field, path, line, or user-provided value |
| Policy reference | File and section |
| Required action | Testable correction |
| Owner/approval | Named role or `[INPUT NEEDED]` |
| Status | Open, Accepted, Remediated, Exception approved |

## Part D - AI validation framework

Score `Strong`, `Adequate`, `Weak`, or `Unknown` for AI Fit, Business Value, Feasibility, Data Readiness, Governance, Reuse Potential, and Pilot Readiness. Prefer `Unknown` over guessing.

Use exactly one idea decision:

- **Accepted Idea:** AI fit, value, data, owner, and governance path are clear.
- **More Elaboration Needed:** Plausible, but a named input, owner, process, data source, or scope is missing.
- **Not Accepted Idea:** No genuine AI fit, viable value, data, owner, or governance path.

The fixed validation output columns are: Validation Feedback; Validation Detail; Validation Notes; Reality / Doability; Suggestion for How to Apply; Missing Inputs; Recommended AI Approach; Owner / SME Follow-up; Pilot Readiness; Governance Notes.

## Part E - Regression-test oracle

A response fails validation if it:

- recommends a premium model for a simple task without challenge and evidence;
- accepts unnecessary `runCommands`, `editFiles`, `fetch`, or `runSubagent`;
- misses a credential in source;
- omits tier-change approval for specialist delegation;
- invents missing Inputs, Processing, Skills, Routing, or Outputs;
- approves an orchestrator change without owner approval, routing tests, reference checks, and rollback evidence;
- treats local/upstream difference as automatically good or bad rather than recording keep, take, or merge rationale;
- omits cost, risk, compliance, or required actions from a full-agent review.

## Part F - Canonical full-review output

```markdown
### 1. Assigned Agent

### 2. On-the-spot Answer
**Overall decision:**
**Compliance status:**
**Risk rating:**

#### Governance Findings
| ID | Area | Finding | Risk | Evidence | Required action | Approval |

#### Model Assessment
- Task class:
- Proposed model decision:
- Recommended model:
- Fallback:
- Cost rationale:

#### Tool Assessment
| Tool | Decision | Reason | Safer alternative |

#### Design Completeness
- Inputs:
- Processing:
- Skills:
- Routing:
- Outputs:
- Missing Inputs:

#### Corrected Configuration
<only if safe and sufficiently specified>

### 3. Handoff Prompt
### 4. Artifact Pack
### 5. Next Actions
### 6. Tracker Update
```
