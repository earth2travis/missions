# HANDOFF: Operator-First Mission System — Session 2026-06-10

## SITREP

The operator-first mission system is in active development. Three Hermes skills are written and live in `~/.hermes/skills/devops/`. The missions repo at `github.com/earth2travis/missions` contains the Flight Plan template, a demo mission, generated `/goal` files, and a system synthesis. The architecture is defined. What remains is wiring the skills to actual tools and running a real end-to-end pipeline.

---

## What We Are Building

A **Mission orchestration system** that makes multi-agent, multi-session work as simple as writing a one-page Flight Plan. The complexity (six handoffs, residual control, agency cost tracking, incomplete contract theory, Auftragstaktik, principal-agent economics) is buried in the system. The human writes intent. The system handles the architecture.

The experience should feel like **NASA Mission Control** or a **Special Operations mission packet**: clean, decisive, low-friction. Military terminology is fine; NASA uses it too.

### The Three-Layer Architecture

| Layer | What the Human Sees | What the System Handles |
|-------|-------------------|------------------------|
| **Flight Plan** | One-page markdown: Commander's Intent, Constraints, Success Criteria | Nothing; human writes this |
| **Mission Contract** | Nothing (hidden) | Auto-generated: six handoffs, cascade, residual control, Agency Cost Ledger |
| **`/goal` Files** | Nothing (hidden) | Auto-generated: tool-agnostic execution leaves |
| **Kanban Tasks** | Hermes dashboard | Auto-created with dependencies, budgets, metadata |

### The Three Skills

| Skill | What It Does | Trigger |
|-------|-------------|---------|
| `define-mission` | Turns raw intent into Flight Plan + auto-generated Contract | "I want to...", "We need to...", explicit `/define-mission` |
| `plan-mission` | Reads Contract, creates `/goal` files, produces pre-launch telemetry | "Let's run this", "Deploy the mission", explicit `/plan-mission` |
| `validate-mission` | Pre-flight checks: six intent checks + mechanical checks | Before execution, explicit `/validate-mission` |

### The Flight Plan Template

The only human-facing artifact. Lives at `_packet.md` in the repo. Contains:
- Sizing Gate (informational self-assessment, **not enforced**)
- Commander's Intent
- Constraints (budget, pause conditions, human gates)
- Success Criteria (outcome-oriented, verifiable)
- Context (links, refs, notes)

### Key Design Decisions (User-Approved)

1. **Operator-first, not architecture-first.** The human writes intent; the system generates structure.
2. **No enforcement gates.** If a user wants to run a task through the full mission pipeline, let them. The sizing guide is informational, not a barrier.
3. **NASA-flavored with military terminology.** Mission Control, Flight Plan, Pre-Launch Telemetry, Go/No-Go.
4. **No separate app.** Leverage Hermes as the dashboard. `/goal` and Kanban are the runtime.
5. **Minimal human interaction.** Auto-generate everything possible. Ask for confirmation only when ambiguous or high-stakes.
6. **After-Action Review is a Markdown report.** Auto-populated from `task_runs`.
7. **Skills are named `define-mission`, `plan-mission`, `validate-mission`.** User finds these intuitive.

---

## What We Built This Session

1. **Three Operator Skills**
   - `~/.hermes/skills/devops/define-mission/SKILL.md` — Intent → Flight Plan + Contract
   - `~/.hermes/skills/devops/plan-mission/SKILL.md` — Contract → `/goal` files + Kanban tasks
   - `~/.hermes/skills/devops/validate-mission/SKILL.md` — Pre-flight Go/No-Go checks

2. **Flight Plan Template**
   - `missions/_packet.md` — The one-page human-facing artifact
   - Includes informational sizing gate (not enforced)

3. **Demo Mission (End-to-End)**
   - `missions/landing-page-readme.md` — Flight Plan
   - `missions/landing-page-readme.contract.md` — Auto-generated Contract
   - `goals/landing-page-readme-builder.md` — Builder `/goal`
   - `goals/landing-page-readme-reviewer.md` — Reviewer `/goal`
   - `goals/landing-page-readme-merge.md` — Orchestrator `/goal`

4. **Mission Sizing Guide**
   - `concepts/mission-sizing.md` — Educational reference for what makes a mission vs. a task
   - **Not enforced by skills.** Informational only.

5. **System Synthesis**
   - `SYNTHESIS.md` — Overview of the system for quick reference

---

## Decisions Made

| Decision | Rationale |
|---|---|
| Three skills: define, plan, validate | User finds these intuitive. Maps to natural workflow. |
| No enforcement gates | User decides what qualifies as a mission. System helps, does not block. |
| Flight Plan is the only human-facing file | Operator-first: one page of intent, not a 6-handoff contract. |
| Contract is auto-generated and hidden | The system needs the structure; the human does not. |
| `/goal` files auto-generated | Tool-agnostic execution leaves. No manual authoring. |
| Informational sizing gate | Nudges user toward `/goal` for simple tasks, but never blocks. |
| Sizing guide lives in `concepts/` | Reference material, not runtime policy. |
| NASA flavor + military terminology | User preference. Clean, decisive, familiar. |
| Hermes as dashboard | No separate app. Leverage existing tools. |

---

## Where We Left Off

The architecture is defined. The skills are written. The demo mission exists. What remains is **execution and wiring**:

### Next Steps (Priority Order)

1. **Wire `plan-mission` to actual Kanban tools**
   - Replace descriptive "would create" with actual `kanban_create()` calls
   - Test dependency linking via `kanban_link()`
   - Verify task metadata propagation (mission_id, handoff_number, budget)

2. **Implement After-Action Review generator**
   - Read `task_runs` from `kanban.db`
   - Generate Markdown AAR: runtime, tokens, turns, residual loss, lessons
   - Wire to a new `aar-mission` command or skill

3. **Run a real end-to-end pipeline**
   - Pick a real codebase (not a demo)
   - Execute builder → reviewer → orchestrator via Kanban
   - Populate the Agency Cost Ledger
   - Generate the first real AAR

4. **Build template library**
   - `templates/mission-security-audit/`
   - `templates/mission-refactor-migration/`
   - `templates/mission-research-sprint/`
   - Each contains a Flight Plan with pre-filled constraints and criteria

5. **Refine the Flight Plan → Contract generation**
   - Currently manual/skilled generation. Consider automating via script or model call.
   - Ensure backbrief gates are correctly set based on mission complexity

6. **Connect to Substrate knowledge graph**
   - Flight Plans should be able to reference `[[wikilinks]]` to Substrate insights
   - Ensure `WIKI_PATH` resolution works for context injection

7. **Open questions to resolve**
   - Should AAR be a skill (`aar-mission`) or a subcommand?
   - Should templates be repo directories or a separate `templates/` repo?
   - How to handle mission abort/cleanup (Kanban tasks in running state)?

---

## Files to Read on Resume

1. `README.md` — Original architecture philosophy. Still valid.
2. `_packet.md` — The Flight Plan template. What the human writes.
3. `SYNTHESIS.md` — System overview written this session.
4. `concepts/mission-sizing.md` — Reference material on mission vs. task.
5. `missions/landing-page-readme.md` — Example Flight Plan (note: this is a task-sized demo; real missions should be bigger).
6. `missions/landing-page-readme.contract.md` — Example auto-generated Contract.
7. `~/.hermes/skills/devops/define-mission/SKILL.md` — The skill the next agent will use.
8. `~/.hermes/skills/devops/plan-mission/SKILL.md` — The skill that needs Kanban wiring.
9. `~/.hermes/skills/devops/validate-mission/SKILL.md` — Pre-flight linter.

---

## Context to Carry Forward

- The user is **Ξ2T (Travis)**. He values operator-first thinking, minimal friction, and clean abstractions.
- He explicitly rejected enforcement gates. The system suggests; it does not block.
- He wants NASA-flavored language but military terminology is fine.
- His 2026 word is **"Relax."** Do not over-engineer. Ship working things.
- The `.md` TLD is significant. `missions.md` is the brand.
- Substrate (the Brain) is separate from operational artifacts (missions repo).
- Hermes Kanban is the runtime. `/goal` is the execution primitive.
- The user maintains strict separation: Substrate = knowledge, missions repo = operations.

---

## The Commitment

Build the simplest thing that works. Wire the skills to the tools. Run a real pipeline. Generate a real AAR. Then iterate.

The goal is not a perfect system on paper. The goal is a system that makes multi-agent orchestration feel as simple as writing a one-page Flight Plan.
