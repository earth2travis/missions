---
title: "Flight Plan"
status: ready
priority: normal
budget:
  tokens: 25000
  time: "15m"
---

# Flight Plan: Landing Page README

## Commander's Intent
A visitor to the missions repo should understand what the system does and how to use it in under 60 seconds. The current README is architecture-heavy and assumes deep context.

## Constraints
- Budget: 25K tokens, 15 minutes
- Pause on: build break (if we add CI), factual errors about the system
- Human gate: Final approval before commit to main

## Success Criteria
1. A new visitor can read the README and understand the system's purpose without reading Substrate
2. The README includes a 30-second "your first mission" example
3. The README links to the three operator skills (define, plan, validate)
4. Existing technical depth is preserved in a secondary doc, not lost

## Context
- Current README: /home/sivart/missions/README.md
- Substrate refs: [[mission-execution-chain]], [[mission-command]], [[goal-primitive]]
- Operator skills live in ~/.hermes/skills/devops/{define,plan,validate}-mission/
