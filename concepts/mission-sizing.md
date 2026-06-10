# Mission Sizing Guide

## The Rule

A Mission is a **bounded campaign**, not a chore. If it can be done by one agent in one session with one `/goal`, it is a task. Not a mission.

## Mission Qualification Criteria

A candidate must satisfy **at least 3 of 5** to qualify as a Mission:

| # | Criterion | What It Means | Litmus Test |
|---|-----------|-------------|-------------|
| 1 | **Multi-agent** | Requires 2+ distinct profiles/tools | Would a single agent choke on this? |
| 2 | **Multi-session** | Expected to span multiple chat sessions or Kanban lifecycles | Would it realistically survive a human going to sleep and returning? |
| 3 | **Multi-objective** | Has 2+ distinct outcomes that must be achieved | Can you describe "done" in 3+ independent statements? |
| 4 | **Coordination required** | Outcomes have dependencies, sequencing, or parallel paths | Does order matter? Can some work run in parallel? |
| 5 | **Method ambiguous** | The "how" is not obvious; Auftragstaktik is needed | Would a competent builder need to make significant judgment calls? |

## Examples

### NOT Missions (Tasks)

| Submission | Why It Fails | What To Use Instead |
|---|---|---|
| "Rewrite the README" | Single agent, one session, one objective | Direct `/goal` to a builder |
| "Fix the auth bug" | Single objective, method is obvious (find bug, patch, test) | Direct `/goal` or single Kanban task |
| "Review this PR" | One reviewer, one session, one outcome | Direct `/goal` to a reviewer |
| "Research OAuth2 best practices" | Research has no execution; no coordination needed | Research query or Substrate finding |
| "Update dependencies" | Single objective, mechanical, no judgment calls | Direct `/goal` or CI job |

### REAL Missions

| Mission | Why It Qualifies |
|---|---|
| **Harden authentication end-to-end** | Builder (implement) + Reviewer (audit) + Verifier (pen-test). 3 objectives: OAuth flow, error handling, rate limiting. Method is ambiguous (which OAuth library? which rate limit strategy?). |
| **Migrate from Express to Fastify** | Assessment (researcher) + Pilot (builder) + Rollout (orchestrator) + Validation (reviewer). Multi-session. Sequencing required. Method is ambiguous. |
| **Security audit and remediation** | Scanner (find vulns) + Analyst (prioritize) + Builder (patch) + Reviewer (verify). 4+ objectives. Parallel + sequential work. Method is ambiguous per vulnerability. |
| **Build the public missions.md site** | Designer (UX) + Builder (frontend) + Content (author) + Reviewer (QA) + Orchestrator (deploy). Multi-session. 5+ objectives. Coordination heavy. |
| **Implement observability stack** | Builder (metrics) + Builder (logs) + Builder (traces) + Reviewer (integration) + Orchestrator (dashboard). Three parallel workstreams plus integration. Method is ambiguous (which tools? how to correlate?). |

## The Flight Plan Sizing Gate

Every Flight Plan must answer this question explicitly:

> **Why is this a Mission and not a Task?**

If the answer is "because it sounded important" or "it involves multiple steps," it is a task. A task with steps is still a task.

A mission involves **uncertainty at the method level** that requires delegation of judgment, not just delegation of labor.

## Anti-Patterns

### Anti-Pattern 1: The Step-List Mission

```
BAD: "Mission: Rewrite README"
  Step 1: Draft new README
  Step 2: Review for clarity
  Step 3: Merge

WHY: This is a task list, not a mission. The method is obvious.
```

### Anti-Pattern 2: The Vanity Mission

```
BAD: "Mission: Achieve World-Class Developer Experience"

WHY: No boundaries. No end state. Not a mission; a vision statement.
```

### Anti-Pattern 3: The Single-Agent Mission

```
BAD: "Mission: Refactor auth module"
  Agent: builder only

WHY: If one agent can do it, it is a task. The orchestration overhead is waste.
```

## The Test

Before creating a Flight Plan, run this test:

```
If I gave this to one agent with one /goal, would they succeed?
  → YES: This is a task. Use /goal directly.
  → NO, because they lack expertise: Add a reviewer. Still a task.
  → NO, because it requires coordination across systems/sessions/tools: This is a Mission.
```

## Mission vs. Task Decision Tree

```
Does it require 2+ distinct agent profiles?
  NO → Task
  YES → Does it span multiple sessions?
    NO → Large task (still a task)
    YES → Does it have 2+ independent objectives?
      NO → Large sequential task (still a task)
      YES → Is the method ambiguous?
        NO → Well-defined project (maybe a mission)
        YES → MISSION
```

## For the define-mission Skill

When a user submits intent, the skill must:

1. **Apply the 5-criterion test silently.**
2. **If 3+ criteria pass:** Proceed to Flight Plan generation.
3. **If <3 criteria pass:** Reject with specificity:
   ```
   This looks like a task, not a Mission. Here's why:
   - Single objective (fails criterion 3)
   - Method is obvious: rewrite README, review, merge (fails criterion 5)
   - One agent can handle this (fails criterion 1)

   RECOMMENDATION: Use /goal directly, or create a single Kanban task.
   If you believe this IS a mission, explain why the method is ambiguous
   or why coordination is required.
   ```
4. **Never** let a task masquerade as a mission. The overhead is not free. Respect the operator's time.

## Related

- [[mission-execution-chain]] — The six handoffs (missions have all six; tasks have 1-2)
- [[mission-command]] — Auftragstaktik (missions require commander's intent; tasks require instructions)
- [[goal-primitive]] — /goal is for tasks. Mission Contracts are for missions.
