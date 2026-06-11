# Evolution Plan: Pre-Research Skills → Mission Contract System

## Status: Draft
## Created: 2026-05-17

## Context

The pre-research skills (archived in `archive/sivart-skills-pre-research/`) were
brainstormed before the deep research on:

- The `/goal` primitive across Codex CLI, Claude Code, and Hermes Agent
- Auftragstaktik (mission command) and its six handoffs
- Principal-agent theory (Grossman-Hart, Holmstrom)
- The Mission Contract as an incomplete contract
- Hermes Kanban as the runtime for multi-agent collaboration

They are preserved as inspiration but must evolve to align with the current
architecture. This plan defines that evolution.

---

## Assessment Summary

### What the Pre-Research Skills Got Right

1. **Four-Phase Workflow:** Define → Plan → Validate → Deploy maps cleanly to
the Mission Contract lifecycle.
2. **Specialist Roles as Worker Lanes:** The five Squad MOS names are early
versions of what Hermes worker lanes formalize.
3. **Reproducibility Through Code:** "Missions are code" is the same principle
behind versioned Mission Contracts in a repo.

### What Needs to Evolve

| Pre-Research Element | Problem | Evolution |
|---|---|---|
| **Manifest Format** | No `why`, no BHAG, no cascading intent, no residual control, no budget | Adopt full Mission Contract Schema from `_template.md` |
| **Success Criteria** | No verification method; just 3-5 checkboxes | Add `verification_signals` and `verification_method` fields |
| **Deployment Script** | Static bash script; no runtime feedback, no backbrief, no circuit breaker | Replace with orchestrator skill using `kanban_create` tool calls |
| **Specialist Names** | 5 fixed names; hardcoded and narrow | Replace with `/goal` reference table: any profile, any tool |
| **Validation** | Static bash linting; no intent preservation check | Replace with Intent Cascade Linter: structural integrity per handoff |

---

## The Evolved Skill Set

### 1. `define-mission` → `mission-contract-author`

**Identity:** The Strategist. Commander's Intent.

**What it teaches the model:** How to write a `mission.md` file using the full
Mission Contract Schema (`_template.md`). Not the lightweight pre-research format.
The full schema with:
- `why`: the moral claim
- `bhag`: the horizon
- `mission`: the `/goal` text with Bungay "Why" test
- `objectives`: with verification criteria and method
- `cascade`: the six handoffs with preservation mechanisms
- `residual_control`: who holds pause/clear/escalate per Grossman-Hart
- `budget`: token limit, turn limit, time limit
- `related`: parent and child missions

**Key change:** The manifest format is now the Mission Contract Schema, not the
pre-research template.

---

### 2. `plan-mission` → `mission-orchestrator`

**Identity:** The Operations Officer. Translates strategic intent into Kanban tasks.

**What it teaches the model:** How to read a Mission Contract and use
`kanban_create` tool calls (not bash scripts) to populate the Kanban board.

**Capabilities:**
- Reads the Mission Contract's `/goal` reference table
- Creates Kanban tasks with correct dependencies via `kanban_link`
- Enforces backbrief gates before execution
- Applies budget constraints (token limit, turn limit, time limit)
- Assigns tasks to the correct worker lanes (Codex builder, Claude reviewer,
  Hermes orchestrator)
- Monitors execution via `kanban_show` and `kanban_list`
- Reports to the Agency Cost Ledger (reads `task_runs`)

**Key change:** No bash scripts. Dynamic tool calls. Runtime awareness.

---

### 3. `validate-mission` → `intent-cascade-linter`

**Identity:** The Inspector General. Ensures intent preservation across handoffs.

**What it teaches the model:** How to read a Mission Contract and check each
handoff against the six failure modes from the military research:

1. Is `mission` a restatement of `bhag`?
2. Is `mission` a task list disguised as intent?
3. Does `mission` pass the Bungay "Why" test?
4. Are `objectives` activity-oriented or outcome-oriented?
5. Does every `objective` link upward to `mission`?
6. Is `residual_control` assigned or defaulted to human?

**Output:** Not a Go/No-Go verdict on bash syntax. A structural integrity report
on intent preservation across the cascade.

**Key change:** Validates the Mission Contract, not a bash script.

---

## Migration Path

### Phase 1: Skill Authoring (Immediate)
- Write `mission-contract-author/SKILL.md` in the Hermes skills system
- Write `mission-orchestrator/SKILL.md`
- Write `intent-cascade-linter/SKILL.md`
- Register them in `~/.hermes/skills/`

### Phase 2: Integration Testing (Next)
- Author a real Mission Contract using the new `mission-contract-author` skill
- Run the `intent-cascade-linter` on it
- Use the `mission-orchestrator` to create Kanban tasks
- Execute a builder-reviewer-orchestrator pipeline end-to-end
- Populate the Agency Cost Ledger

### Phase 3: Template Library (Later)
- Convert pre-research "Mission Packages" (security audit, research sprint,
  incident response) into Mission Contract templates
- Each template is a directory in `missions/templates/`
- Contains `mission.md`, `goals/`, and optional `artifacts/`

### Phase 4: missions.md Public Site (Future)
- Publish the philosophy, templates, and validator
- Build a web-based Mission Contract author
- Show live execution via Kanban dashboard integration

---

## Files to Create

### In `missions/` repo:
- `skills/mission-contract-author/SKILL.md`
- `skills/mission-orchestrator/SKILL.md`
- `skills/intent-cascade-linter/SKILL.md`
- `templates/mission-security-audit/mission.md`
- `templates/mission-research-sprint/mission.md`

### In `~/.hermes/skills/` (Hermes skills system):
- `mission-contract-author/SKILL.md`
- `mission-orchestrator/SKILL.md`
- `intent-cascade-linter/SKILL.md`

---

## Acceptance Criteria

1. A human can write a Mission Contract using the `mission-contract-author` skill
2. The `intent-cascade-linter` catches intent degradation before execution
3. The `mission-orchestrator` creates Kanban tasks that execute end-to-end
4. The Agency Cost Ledger shows measurable data for each handoff
5. Residual control is configurable per Mission, not hardcoded
6. Any tool that speaks `/goal` can join the pipeline without format changes

---

## Open Questions

1. Should the orchestrator skill be a Hermes bundled skill or a custom skill?
2. How do we map the 5 Squad MOS names to the new flexible profile system?
   (Option A: Keep them as default profiles. Option B: Retire them in favor of
   tool-based assignment.)
3. Should the linter be a pre-commit hook, a CI gate, or a manual skill?
4. Where does the Agency Cost Ledger live: in the Mission Contract file,
   in `task_runs`, or a separate file?

---

## Related

- `../README.md` — Mission Contract system overview
- `../_template.md` — Mission Contract Schema
- `../concepts/structural-limits.md` — What the architecture makes possible
- `../archive/sivart-skills-pre-research/` — Original skills (preserved)
