# HANDOFF: Mission Contract System — Session 2026-05-17

## SITREP

The Mission Contract system is live at `github.com/earth2travis/missions`.
Philosophy, architecture, and template are committed. Pre-research skills are
archived. Evolution plan is drafted. Ready for skill authoring and live test.

## What We Built This Session

1. **Mission Contract System**
   - `README.md` — Philosophy, architecture, six handoffs, residual control
   - `_template.md` — Container-leaf separation from `/goal`, Agency Cost Ledger,
     residual control allocation table
   - `concepts/structural-limits.md` — What the architecture makes possible
     and impossible (five possible, four impossible)

2. **Missions Repo**
   - Created `github.com/earth2travis/missions` (transferred from agent-sivart)
   - Committed all files. Repo is operational.

3. **Pre-Research Skills Archived**
   - Original sivart skills (commit `c9c5213`) preserved in
     `archive/sivart-skills-pre-research/`
   - `docs/kanban-mission-system.md` — Original four-phase workflow concept
   - `skills/define-mission/SKILL.md` — The "Strategist"
   - `skills/plan-mission/SKILL.md` — The "Operations Officer"
   - `skills/validate-mission/SKILL.md` — The "Inspector General"

4. **Evolution Plan**
   - `evolution-plan.md` — Maps old skills to new system
   - Defines three evolved skills: `mission-contract-author`,
     `mission-orchestrator`, `intent-cascade-linter`
   - Four-phase migration: authoring → integration → templates → public site

## Decisions Made

| Decision | Rationale |
|---|---|
| Missions repo is standalone, not in Substrate | Substrate is the brain (knowledge). Missions are OPORDs (execution). |
| `/goal` remains complementary, not conflated | `/goal` is session-scoped execution. Mission is cross-session orchestration. |
| Container-leaf separation | Mission Contract references `/goal` files; neither supersedes the other. |
| Agency Cost Ledger lives in `task_runs` | Hermes Kanban already captures runs, tokens, latency. Ledger is a view, not a new system. |
| Residual control is per-Mission configurable | Grossman-Hart says control rights determine investment incentives. Hardcoding destroys flexibility. |
| `missions.md` is the public brand | `.md` TLD signals markdown-native, AI-readable. SOUL.md established the pattern. |

## Key Concepts Established

- **Mission Contract** = incomplete contract made concrete. Human writes it. Agent reads it. Orchestrator verifies against it.
- **Six Handoffs** = Why → BHAG → Mission → Objectives → Projects → Tasks → Execution. Each has a preservation mechanism.
- **Residual Control** = who holds pause/clear/escalate at each handoff. Per Grossman-Hart.
- **Agency Cost Ledger** = tokens, turns, latency, verification signals, residual loss. Observable in `task_runs`.
- **Hermes Kanban** = the runtime. Durable SQLite-backed state machine. Worker lanes execute. Dispatcher routes.
- **Structural Limits** = five things made possible (intent-driven automation, persistent execution, observable agency costs, composability, human-in-loop governance) and four made impossible (opaque black boxes, unbounded delegation, single-tool lock-in, fire-and-forget automation).

## Where We Left Off

The evolution plan is drafted but not executed. Three skills need to be written
and registered in the Hermes skills system. No live test has been run.

## Next Steps (in priority order)

1. **Write `mission-contract-author` skill**
   - Teach the model to write a `mission.md` using the full Mission Contract Schema
   - Include `why`, `bhag`, `mission`, `objectives`, `cascade`, `residual_control`, `budget`, `related`
   - Include the Bungay "Why" test and the Paragraph 2 Test

2. **Write `intent-cascade-linter` skill**
   - Teach the model to check a Mission Contract against six failure modes
   - Output a structural integrity report, not a Go/No-Go
   - Catches intent degradation before execution

3. **Write `mission-orchestrator` skill**
   - Teach the model to read a Mission Contract and create Kanban tasks via `kanban_create`
   - Handle dependencies via `kanban_link`
   - Enforce backbrief gates
   - Apply budget constraints
   - Report to Agency Cost Ledger

4. **Live test: builder-reviewer-orchestrator pipeline**
   - Author a real Mission Contract
   - Run the linter on it
   - Use the orchestrator to create Kanban tasks
   - Execute end-to-end
   - Review the Agency Cost Ledger

5. **Template library**
   - Convert pre-research "Mission Packages" into Mission Contract templates
   - `templates/mission-security-audit/`
   - `templates/mission-research-sprint/`
   - `templates/mission-incident-response/`

6. **Open questions to resolve**
   - Should the orchestrator skill be a Hermes bundled skill or custom?
   - How to map the 5 Squad MOS names to the new flexible profile system?
   - Should the linter be a pre-commit hook, CI gate, or manual skill?
   - Where does the Agency Cost Ledger live: in the file, in `task_runs`, or separate?

## Files to Read on Resume

1. `README.md` — Orient first. Always.
2. `_template.md` — The canonical Mission Contract format.
3. `concepts/structural-limits.md` — The boundary conditions.
4. `evolution-plan.md` — The migration path.
5. `archive/sivart-skills-pre-research/` — Original inspiration (if needed).

## Context to Carry Forward

- The `.md` TLD is significant. `missions.md` is the brand.
- Hermes Kanban docs were fully consumed. Worker lanes, structured handoff,
  task_runs, and the eight collaboration patterns are understood.
- The `/goal` primitive research (Codex, Claude Code, Hermes) is committed to
  Substrate at `35dce23`. Cross-reference via `[[goal-primitive]]`.
- The user owns `missions.md` domain and wants to build a public system around it.
- Military metaphors are preferred but not forced.
- The user's 2026 word is "Relax." Do not grind.
