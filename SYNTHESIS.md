# Missions System Synthesis

## What Exists Now

### The Three Operator Skills

| Skill | What It Does | What the User Sees |
|-------|-------------|-------------------|
| **`define-mission`** | Turns raw intent into a Flight Plan + auto-generated Contract | "Here is your mission. Go for pre-flight checks?" |
| **`plan-mission`** | Reads the Contract, creates Kanban tasks, generates `/goal` files | "3 tasks created. Builder → Reviewer → Orchestrator. Ready." |
| **`validate-mission`** | Runs six intent checks + mechanical checks | "GO" or specific "NO-GO: fix X" |

### The Flight Plan Template

`_packet.md` is the only thing a human writes. It fits on one screen:

```yaml
---
status: draft
priority: normal
budget: { tokens: 25000, time: "15m" }
---

# Flight Plan: [MISSION NAME]

## Commander's Intent
What must be true, and why does it matter?

## Constraints
Budget, pause conditions, human gates

## Success Criteria
1. Outcome-oriented
2. Verifiable

## Context
Links, refs, notes
```

### What the System Generates (Hidden)

From that one file, the system produces:
- `missions/<name>.contract.md` — the full six-handoff Contract
- `goals/<name>-*.md` — tool-agnostic `/goal` files for each execution leaf
- Kanban tasks with dependencies and budget metadata

### The End-to-End Demo We Just Ran

We created a real mission ("Rewrite README for accessibility") and ran the full pipeline:

**Step 1: define-mission** → Generated Flight Plan + Contract automatically.

**Step 2: validate-mission** → Caught a real failure:
```
[✗] Check 6: Residual control — All handoffs default to human.
STATUS: NO-GO
Suggested fix: Assign execution rights to builder agent.
```

**Step 3: Fix + Re-run** → Patched the Contract. All six checks passed. STATUS: GO.

**Step 4: plan-mission** → Would create 3 Kanban tasks with dependency links.

## The User Experience

```
User: "I want to rewrite the README so new visitors get it in 60 seconds."
   ↓
define-mission: Generates Flight Plan + Contract
   ↓
validate-mission: [✓][✓][✓][✓][✓][✗] → fix → [✓][✓][✓][✓][✓][✓] GO
   ↓
plan-mission: Tasks created. Builder → Reviewer → Orchestrator.
   ↓
User sees: "MISSION STATUS: GO FOR LAUNCH"
```

The human writes intent. The system handles the architecture. The pre-flight checks catch intent degradation before execution. The dashboard is Hermes itself.

## What Remains

1. **Wire the skills to actual `kanban_create()` calls.** Right now `plan-mission` describes what to do; it needs to call the tools.
2. **Implement the After-Action Review generator.** A markdown report auto-populated from `task_runs`.
3. **Build template library.** Security audit, research sprint, incident response packets ready to copy.
4. **Test with real Kanban execution.** Run a builder-reviewer-orchestrator pipeline against a real codebase.

The architecture is sound. The abstraction works. The complexity is buried. The operator sees NASA, not mechanism design.
