---
title: "Mission Contract Template: Builder-Reviewer-Orchestrator Pipeline"
tags: [mission, contract, template, goal, orchestration, auftragstaktik, intent-cascade]
related:
  - goal-primitive
  - mission-execution-chain
  - principal-agent-theory
  - kanban-doctrine
  - subagent-architecture
  - workflow-as-contract
  - centaur-principle
source: concepts/goal-primitive.md, concepts/mission-execution-chain.md, concepts/principal-agent-theory.md
created: 2026-05-16
---

# Mission Contract Template

> Copy this file, rename it, and remove all `> ` blockquotes before committing.
> This template demonstrates the container-leaf relationship between Mission Contracts and /goal primitives.
> The Mission Contract is the orchestration manifest. The /goal files are the execution leaves.
> No tool that implements /goal needs to know this format exists.

## Mission Statement

> Write the Bungay "Why" test here: what must be true, and why does it matter?
> Example: "Refactor the authentication module so all API routes return structured error codes with request IDs, because silent failures in auth are security incidents waiting to happen."

**What:**
**Why:**
**Who cares if this fails:**

## Cascade: The Six Handoffs

> Each handoff is a delegation point. Each delegation point is an agency relationship.
> The Mission Contract does not replace /goal. It references it.

### Handoff 1: Why → BHAG

| Field | Value |
|-------|-------|
| BHAG reference | [[ ]] |
| Alignment check | Does this Mission serve the BHAG, or has it drifted? |
| Preservation mechanism | Intent restatement: write the Why in fresh words, not copy-paste |

### Handoff 2: BHAG → Mission

| Field | Value |
|-------|-------|
| Mission owner | Human operator |
| Mission authority | Who can edit, pause, or kill this Mission |
| Paragraph 2 Test | If the agent achieves this Mission but misses the BHAG, the Mission was written wrong |

### Handoff 3: Mission → Objectives

| Field | Value |
|-------|-------|
| Objective 1 | Outcome-oriented, not activity-oriented |
| Verification criteria | How do we know this objective is met? |
| Verification method | test-pass / judge-verdict / human-review / build-success |

> Add Objectives 2-N as needed. Each objective must link upward to the Mission statement.

### Handoff 4: Objectives → Projects (The Backbrief Gate)

| Field | Value |
|-------|-------|
| Backbrief required | true / false |
| Backbrief reviewer | agent-id or human-id |
| Backbrief approval method | auto / human-signoff / judge-verdict |

> The backbrief is the plan of action presented before /goal assignment.
> It answers: what will you do, how does each step serve the objective, and what is your estimated budget?

### Handoff 5: Projects → Tasks

| Field | Value |
|-------|-------|
| Task source | kanban-card / delegate_task / direct /goal |
| Intent metadata | Every task must carry a link to the objective it serves |
| Deviation authority | Can the agent abandon the plan when conditions change? |

### Handoff 6: Tasks → Execution

| Field | Value |
|-------|-------|
| Verification stack | Which signals are collected? |
| Human review gate | Required / optional / none |
| Stop-the-line authority | Who can block when intent is unclear? |

## Execution: /goal References

> Each row is a leaf node. The agent receives the /goal text, not the Mission Contract.
> The orchestrator maps goal_ref to the actual /goal invocation.

| # | Agent | Tool | goal_ref | backbrief | verification | budget | residual_control |
|---|-------|------|----------|-----------|--------------|--------|------------------|
| 1 | builder | codex | `goals/build-auth-refactor.md` | required | test-pass, build-success | token: 50K, time: 30m | human |
| 2 | reviewer | claude-code | `goals/review-auth-refactor.md` | required | judge-verdict, human-review | none | human |
| 3 | orchestrator | hermes | `goals/verify-and-merge.md` | none | build-success, test-pass, human-signoff | turn: 20 | human |

> The goal_ref files live in `goals/` and are written in standard /goal syntax.
> They are tool-agnostic. Any agent that implements /goal can execute them.
> The Mission Contract is the only thing that knows the full pipeline.

## Agency Cost Ledger

> Populated after execution. Tracks the price of delegation.

| mission_id | handoff | agent | tool | tokens | turns | latency | signals | residual_loss |
|------------|---------|-------|------|--------|-------|---------|---------|---------------|
| | | | | | | | | |

> Residual loss is estimated cost of imperfect delegation: false done detection, plan drift, rework.
> This makes Holmstrom's agency costs observable.

## Residual Control Allocation

> Per Grossman-Hart: who holds the residual control rights at each handoff?
> This determines who has the incentive to enforce the contract.

| Handoff | Controller | Rights |
|---------|-----------|--------|
| Mission edit | human | Edit, pause, kill |
| Backbrief approval | human or judge | Approve, reject, request revision |
| /goal pause/resume | human or agent | Pause, resume, clear, subgoal |
| Verification override | human | Accept despite failing signals, reject despite passing |
| Mission completion | human | Archive, promote, spawn child |

## Related

- Mission Execution Chain (Substrate)
- Principal-Agent Theory (Substrate)
- The /goal Primitive (Substrate)
- Kanban Doctrine (Substrate)
- Subagent Architecture (Substrate)
