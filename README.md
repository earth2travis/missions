# missions.md

**Write one page of intent. A fleet of agents executes it. A debrief shows you whether your intent survived.**

## Why

Every time you hand work to someone — a contractor, a teammate, an agent — some of what you meant gets lost. As agents take on more of the execution, that loss compounds silently across every handoff. Most agent tooling optimizes for *doing more*. missions.md optimizes for something different: **making sure what gets done is what you meant.**

The idea is old. Militaries call it mission command (Auftragstaktik): the commander states the intent and the constraints, and trusts the unit to choose the method. NASA runs the same pattern as Mission Control: a Flight Plan, Go/No-Go checks, telemetry, and a debrief. missions.md applies that pattern to agent fleets.

You command. The system coordinates. The agents execute.

## How It Works

```
IDEA ──▶ define-mission ──▶ Flight Plan (one page — the only thing you write)
                                │
                       launch-mission
                       ├─ pre-flight Go/No-Go checks (automatic)
                       └─ kanban_create ×N ──▶ Hermes fleet executes
                                │
                       debrief-mission
                       └─ task_runs ──▶ After-Action Review (the proof)
```

Two layers. No hidden machinery in between:

| Layer | Owned by | What it is |
|---|---|---|
| **Flight Plan** | You | One page: Commander's Intent, Constraints, Success Criteria, Context |
| **Hermes Kanban** | The system | Cards with dependencies, budgets, verification, and human gates |

The orchestration theory (intent cascades, verification gates, bounded delegation) lives in how the skills *design the cards*, not in extra artifacts you maintain.

## The Three Skills

| Skill | What it does | You say |
|---|---|---|
| `define-mission` | Turns raw intent into a Flight Plan | "I want to…", "We need to…" |
| `launch-mission` | Runs pre-flight checks, then compiles the Flight Plan into Kanban cards | "Launch it", "Run this mission" |
| `debrief-mission` | Reads `task_runs` and generates the After-Action Review | "Debrief", "How did it go?" |

Skills live in [`skills/`](skills/) (source of truth) and install into `~/.hermes/skills/` for the Hermes agent.

## Install the Skills

This repo is a Hermes **skills tap** (skills live under `skills/`, one directory per skill). On the machine where your Hermes fleet runs:

```bash
# Add the tap, then install each skill through the Skills Hub
# (quarantine + security scan included):
hermes skills tap add earth2travis/missions
hermes skills install earth2travis/missions/define-mission --category devops
hermes skills install earth2travis/missions/launch-mission --category devops
hermes skills install earth2travis/missions/debrief-mission --category devops

# Later: pick up new versions
hermes skills update
```

Or install manually from a clone:

```bash
git clone git@github.com:earth2travis/missions.git
cp -R missions/skills/* ~/.hermes/skills/devops/
```

One-time prep worth doing: `hermes profile describe --all --auto` generates a capability description for every profile from its installed skills — `launch-mission` routes mission lanes by matching against these.

## Your First Mission

1. Tell your Hermes agent what you want: *"I want every API route to return structured error codes, because silent auth failures are security incidents waiting to happen."*
2. `define-mission` drafts a Flight Plan in `missions/` and asks only what it cannot infer. You approve it.
3. Say *"launch it."* `launch-mission` runs the Go/No-Go checks, then creates Kanban cards assigned to your configured profiles. Dependencies gate the sequence; `goal_mode` judges each card against its acceptance criteria; human gates block where you said they should.
4. Watch the Hermes dashboard, or walk away. The board survives restarts.
5. Say *"debrief."* You get an After-Action Review: what ran, what it cost, what passed verification, and where intent drifted.

## What the System Leans On

missions.md builds no orchestration tech. It is a human-facing layer over primitives Hermes Kanban already ships:

| Mission need | Hermes primitive |
|---|---|
| Sequencing and parallelism | `kanban_create(parents=[...])` with dispatcher auto-promotion |
| Verification against acceptance criteria | `goal_mode=True` (judge re-checks each turn) |
| Human gates | `kanban_block()` / `/unblock` |
| Budgets | `goal_max_turns`, token/time limits |
| The audit trail and AAR data | `task_runs` in SQLite |
| Recovery from stuck workers | `reclaim` / `reassign` |

Any tool that speaks `/goal` can join a pipeline. There is no lock-in to defend, because there is no proprietary runtime to lock into.

## Repo Layout

```
missions/      Flight Plans — one file per mission
skills/        define-mission, launch-mission, debrief-mission (Hermes SKILL.md format)
concepts/      Sizing guidance and architecture notes
archive/       Earlier iterations, preserved with context
_packet.md     The Flight Plan template
```

## Sizing: Mission or Task?

A Mission is a bounded campaign: multiple agents, multiple sessions, real coordination, judgment calls about method. A Task is something one agent finishes in one session. If it's a task, a direct `/goal` or a single Kanban card is faster — and `define-mission` will tell you so. It will never block you. The operator decides; the system advises. See [`concepts/mission-sizing.md`](concepts/mission-sizing.md).

## The Deeper Theory

The design is grounded in mission command doctrine, incomplete contract theory (Grossman-Hart), and principal-agent economics (Holmstrom). Delegation always costs something; the goal is not to eliminate that cost but to make it bounded, observable, and improvable. The full treatment lives in the [Substrate knowledge base](https://github.com/earth2travis/substrate) and in [`concepts/`](concepts/).

## Status

MVP in active development. All three skills exist and are installed. Next: fleet setup (2–3 Hermes profiles), then the first real mission — building the public missions.md site with the system itself.
