---
mission_id: landing-page-readme
parent_mission: null
generated_from: missions/landing-page-readme.md
generated_at: 2026-06-10
---

# Mission Contract: Landing Page README

## Mission Statement

**What:** Rewrite the missions repo README so a new visitor understands the system's purpose and how to run their first mission in under 60 seconds.

**Why:** The current README is architecture-heavy and assumes the reader has already read Substrate. It describes what the system is without showing why someone would use it.

**Who cares if this fails:** Every future user who bounces from the repo because they cannot figure out what to do.

## Cascade: The Six Handoffs

### Handoff 1: Why → BHAG

| Field | Value |
|-------|-------|
| BHAG reference | [[mission-execution-chain]] — make intent-driven multi-agent orchestration accessible to any operator |
| Alignment check | Does this Mission serve the BHAG? Yes: lowering the barrier to entry serves the goal of making the system usable. |
| Preservation mechanism | Intent restatement: the BHAG is about accessible orchestration; this Mission makes it accessible by simplifying the README. |

### Handoff 2: BHAG → Mission

| Field | Value |
|-------|-------|
| Mission owner | Human operator (Travis) |
| Mission authority | Human operator can edit, pause, or kill |
| Paragraph 2 Test | If the agent achieves this Mission (simple README) but misses the BHAG (no one uses it because they still cannot figure out how to run a mission), the Mission was written wrong. |

### Handoff 3: Mission → Objectives

| Objective | Verification Criteria | Verification Method |
|-----------|---------------------|---------------------|
| New visitor understands purpose in <60s | Time-to-comprehension test | human-review |
| README includes 30-second "first mission" example | Example exists and is runnable | test-pass |
| README links to define/plan/validate skills | Links present and valid | build-success |
| Technical depth preserved in secondary doc | Architecture doc exists and is linked | human-review |

### Handoff 4: Objectives → Projects (The Backbrief Gate)

| Field | Value |
|-------|-------|
| Backbrief required | true |
| Backbrief reviewer | human |
| Backbrief approval method | human-signoff |

### Handoff 5: Projects → Tasks

| Field | Value |
|-------|-------|
| Task source | kanban-card |
| Intent metadata | Each task carries mission_id + objective_id |
| Deviation authority | Agent can restructure README layout; cannot remove technical content without preservation |

### Handoff 6: Tasks → Execution

| Field | Value |
|-------|-------|
| Verification stack | human-review (readability), build-success (links valid), test-pass (example runnable) |
| Human review gate | Required |
| Stop-the-line authority | Human operator |

## Execution: /goal References

| # | Agent | Tool | goal_ref | backbrief | verification | budget | residual_control |
|---|-------|------|----------|-----------|--------------|--------|------------------|
| 1 | builder | hermes | `goals/landing-page-readme-builder.md` | required | human-review, build-success | token: 15K, time: 10m | agent (execution), human (pause/abort) |
| 2 | reviewer | hermes | `goals/landing-page-readme-reviewer.md` | none | human-review | token: 5K, time: 3m | human |
| 3 | orchestrator | hermes | `goals/landing-page-readme-merge.md` | none | build-success, human-signoff | token: 5K, time: 2m | human |

## Agency Cost Ledger

| mission_id | handoff | agent | tool | tokens | turns | latency | signals | residual_loss |
|------------|---------|-------|------|--------|-------|---------|---------|---------------|
| | | | | | | | | |

## Residual Control Allocation

| Handoff | Controller | Rights |
|---------|-----------|--------|
| Mission edit | human | Edit, pause, kill |
| Backbrief approval | human | Approve, reject, request revision |
| Builder execution (Handoff 5) | agent | Execute, adapt plan, report complete |
| Builder pause/abort (Handoff 5) | human | Pause, resume, clear, subgoal |
| Reviewer verification (Handoff 6) | human | Accept despite failing signals, reject despite passing |
| Mission completion | human | Archive, promote, spawn child |

## Related

- Flight Plan: missions/landing-page-readme.md
- Parent BHAG: [[mission-execution-chain]]
- Skills: define-mission, plan-mission, validate-mission
