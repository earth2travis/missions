# HANDOFF: missions.md MVP — Session 2026-06-10 (supersedes prior handoff)

## SITREP

The architecture was simplified from four layers to two. The hidden Mission
Contract layer is gone; Flight Plans now compile directly to Hermes Kanban
cards. The skill trio was renamed and re-scoped. The repo was cleaned up to
match. The `define-mission` skill is written and installed. `launch-mission`
and `debrief-mission` are next.

**Correction to the prior handoff:** it claimed three skills lived in
`~/.hermes/skills/devops/`. They did not — that directory contained only the
bundled kanban skills. The only prior versions were the archived pre-research
drafts. Verify claims like this on disk before building on them.

---

## What We Are Building

A mission orchestration system: the human writes a one-page Flight Plan, a
Hermes agent fleet executes it via Kanban automation, and an After-Action
Review proves whether intent survived. NASA Mission Control feel: clean,
decisive, low-friction.

### The Architecture (Two Layers)

```
IDEA ──▶ define-mission ──▶ Flight Plan (one page — the only thing you write)
                                │
                       launch-mission
                       ├─ pre-flight Go/No-Go checks (automatic)
                       └─ kanban_create ×N ──▶ Hermes fleet executes
                                │
                       debrief-mission
                       └─ task_runs ──▶ After-Action Review
```

| Layer | Owned by | What it is |
|---|---|---|
| Flight Plan | Human | Commander's Intent, Constraints, Success Criteria, Context |
| Hermes Kanban | System | Cards with `parents=`, `goal_mode`, budgets, `kanban_block()` gates |

There is no hidden Mission Contract and no separate `goals/` directory. Goal
text lives in Kanban card bodies, where the `goal_mode` judge reads it.

---

## Decisions Made (2026-06-10, user-approved)

| Decision | Supersedes |
|---|---|
| No hidden Mission Contract — Flight Plan compiles directly to Kanban cards | Four-layer architecture in prior handoff |
| Trio is `define-mission` / `launch-mission` / `debrief-mission` | `define/plan/validate` naming |
| Validation folds into `launch-mission` as automatic pre-flight Go/No-Go checks | Standalone `validate-mission` skill |
| After-Action Review is the third skill (`debrief-mission`), generated from `task_runs` | "AAR as later subcommand" open question |
| First real mission: build the missions.md public site (genuinely mission-sized) | README demo as first run |
| Minimal fleet (builder + reviewer + default-as-orchestrator) set up as part of MVP | — |
| Skills live in repo `skills/` (source of truth), installed to `~/.hermes/skills/devops/` | — |
| Prove on personal OS first; target open-source + Hermes communities second | — |
| Sizing is advisory, never enforced (unchanged, now consistent across all docs) | Contradictory "reject" language in `concepts/mission-sizing.md` |

Standing preferences (unchanged): operator-first; no enforcement gates; NASA
flavor with military terminology welcome; no separate app — Hermes is the
dashboard; minimal human interaction; "Relax" — do not over-engineer.

---

## What We Did This Session

1. **Repo cleanup**
   - Rewrote `README.md` around the operator-first story and two-layer architecture
   - Archived contract-era artifacts to `archive/contract-era/` with an explanatory README: `_template.md`, `evolution-plan.md`, the demo contract, the demo `/goal` files, and the demo Flight Plan (its goal — an accessible README — was fulfilled by the rewrite)
   - Removed the now-empty `goals/` directory
   - Fixed `concepts/mission-sizing.md`: sizing advice is advisory, never a rejection
   - Rewrote `concepts/structural-limits.md` for the direct-to-Kanban architecture
   - Refreshed `_packet.md` (Flight Plan template): sizing check reworded as informational, status lifecycle documented
2. **`define-mission` skill** — written at `skills/define-mission/SKILL.md`
   (source of truth) and installed to `~/.hermes/skills/devops/define-mission/`
3. **`launch-mission` skill** — written at `skills/launch-mission/SKILL.md`,
   installed alongside. Pre-flight Go/No-Go poll (mechanical NO-GOs vs.
   advisories), backbrief card graph, parents-first creation with captured
   ids, four-part card body anatomy, gates via `review-required:` blocks,
   Launch Record appended to the Flight Plan (the card-id table
   `debrief-mission` will read), workers instructed to self-report usage
4. **`debrief-mission` skill** — written at `skills/debrief-mission/SKILL.md`,
   installed alongside. Launch Record as card index (title-prefix scan as
   fallback), read-only board access (tools or `sqlite3 mode=ro`), honest
   cost ledger (wall-clock/attempts/gate-latency from the board; usage only
   if self-reported), Success Criteria scoreboard graded against cited
   evidence, blameless residual-loss analysis, mid-mission status-read mode,
   closes with the operator's Paragraph 2 verdict

---

## Hermes Reality Check (verified on this machine)

- `hermes profile list` shows a single profile: `default`. Gateway stopped.
- `~/.hermes/skills/devops/` bundles `kanban-orchestrator`, `kanban-worker`,
  `webhook-subscriptions` — read these before writing `launch-mission`; they
  document the real tool contracts.
- Key primitives: `kanban_create(parents=[...], goal_mode=True, goal_max_turns=N)`,
  `kanban_block()`, `kanban_complete(summary, metadata)`, `task_runs` in SQLite,
  `hermes kanban reclaim/reassign`.
- The dispatcher **silently drops** cards assigned to unknown profiles. Always
  discover profiles (`hermes profile list`) before assigning. Never invent names.

---

## Next Steps (Priority Order)

1. **Configure the minimal fleet** — 2–3 profiles (builder, reviewer; `default`
   as orchestrator), gateway running. User said to check in before touching
   profiles.
2. **First real mission: the missions.md public site** — write its Flight Plan
   with `define-mission`, launch it, debrief it. The AAR is the proof of value
   and the launch story for the Hermes community.

**Schema reality (verified in `hermes_cli/kanban_db.py`):** the board records
no tokens or turns. `task_runs` has per-attempt outcome, timestamps, summary,
metadata JSON, error. So: `launch-mission` instructs workers to self-report
`usage` in handoff metadata; `debrief-mission` computes wall-clock, attempts,
and gate latency from the board, labels usage as self-reported, and says
"not recorded" rather than estimating. DB path: `$HERMES_KANBAN_DB`, else
`~/.hermes/kanban.db` (default board), else
`~/.hermes/kanban/boards/<slug>/kanban.db`. Read-only access only.

---

## Files to Read on Resume

1. `README.md` — the story and architecture, current
2. `_packet.md` — the Flight Plan template
3. `skills/define-mission/SKILL.md` — the first skill
4. `concepts/mission-sizing.md` — advisory sizing rules the skills follow
5. `~/.hermes/skills/devops/kanban-orchestrator/SKILL.md` — real Kanban tool contracts
6. `archive/contract-era/README.md` — why the contract layer was retired

---

## Context to Carry Forward

- The user is **Ξ2T (Travis)**, earth2travis. Operator-first, minimal friction,
  clean abstractions. 2026 word: **"Relax."** Ship working things.
- `missions.md` is the brand. Substrate = knowledge; missions repo = operations.
  Strict separation.
- The system suggests; it never blocks. The operator decides.
- The ecosystem goal: skills contributable upstream to Hermes; missions.md as
  the methodology home.

## The Commitment

Build the simplest thing that works. Two layers, three skills, one real
mission. The goal is a system that makes multi-agent orchestration feel as
simple as writing a one-page Flight Plan — and proves it with a debrief.
