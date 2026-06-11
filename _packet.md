---
title: "Flight Plan"
status: draft # draft → ready → launched → complete
priority: normal
budget:
  tokens: 50000
  time: "30m"
---

# Flight Plan: [MISSION NAME]

## Sizing Check (Informational)
Is this a Mission or a Task?

A **Mission** is a bounded campaign: multiple agents, multiple sessions, real
coordination, judgment calls about method.
A **Task** is work one agent can complete in one session with one `/goal`.

If this is a task, a direct `/goal` or a single Kanban card is faster and
cheaper. Your call either way — this check never blocks a launch.

## Commander's Intent
What must be true, and why does it matter?

## Constraints
- Budget: [tokens / time / turns — mirror of the frontmatter `budget:` block, which is canonical]
- Pause conditions: [e.g., test failure, security impact, build break]
- Human gates: [e.g., merge approval, production deploy, external commit]

## Success Criteria
1. [Outcome-oriented: what result proves this succeeded?]
2. [Outcome-oriented: what else must be true?]

## Context
[Any relevant links, Substrate references, or operator notes]
