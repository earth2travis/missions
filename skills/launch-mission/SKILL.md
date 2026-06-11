---
name: launch-mission
description: Compile an approved Flight Plan into Hermes Kanban cards and launch the mission. Runs automatic pre-flight Go/No-Go checks, presents the card graph for operator approval, then issues real kanban_create calls with dependencies, budgets, goal_mode verification, and human gates. The deep-integration skill of the missions.md system.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [missions, orchestration, kanban, launch, go-no-go]
    related_skills: [define-mission, debrief-mission, kanban-orchestrator, kanban-worker]
---

# Launch Mission — Flight Plan → Kanban Board

You are the launch director. The operator has an approved Flight Plan and says
"launch it" (or "/launch-mission <path>"). You run the pre-flight checks,
present the card graph, get one Go from the operator, and put the mission on
the board. From that point the Hermes dispatcher owns execution.

This skill builds nothing the Kanban runtime doesn't already provide. It is a
compiler: Flight Plan in, well-designed cards out.

## The contract of this skill

- **Input:** a Flight Plan in `missions/` (explicit path, else the most recent
  `status: ready` plan, else ask).
- **Output:** Kanban cards on the board, a Launch Record appended to the
  Flight Plan, frontmatter `status: launched`.
- **Out of scope:** doing any of the mission's work yourself, editing
  Commander's Intent or Success Criteria (that is the operator's page —
  if a check fails, report it and let them fix or override).

## Step 0 — Discover the fleet

Before anything else, find out what profiles exist. Run `hermes profile list`
through your terminal tool; if you can't, ask the operator. Cache the answer.

**The dispatcher silently drops cards assigned to unknown profiles** — no
error, no fallback, the card sits in `ready` forever. Never invent an assignee
name. If a lane has no fitting profile, ask the operator which profile to use
or whether to create one. This is the one mechanical rule with no override.

## Step 1 — Pre-flight Go/No-Go

Run every check, then report a single Go/No-Go poll. Two severities:

**NO-GO (mechanical — launching anyway would strand cards or burn budget blindly):**
| Check | Why it's mechanical |
|---|---|
| At least one profile exists and every planned assignee is on the list | Unknown assignees are silently dropped |
| Gateway/dispatcher is running (or operator confirms they'll start it) | Cards would sit unclaimed |
| Flight Plan has at least one Success Criterion | `goal_mode` judges against acceptance criteria; no criteria = blind judge |

**ADVISORY (intent quality — report specifically, operator may override with a word):**
| Check | What good looks like |
|---|---|
| Commander's Intent states a why, not just a what | An agent could make a judgment call from it |
| Intent is an outcome, not a step list | No "first… then… finally…" |
| Success Criteria are outcome-oriented and verifiable | A judge, test, or human can answer yes/no |
| Budget is set | Tokens/time/turns present in frontmatter |
| Pause conditions and human gates declared | Especially for anything irreversible |
| Plan status is `ready` | If `draft`, confirm the operator approved it |

Report format — terse, NASA-poll style:

```
PRE-FLIGHT: <mission name>
  fleet ......... GO (builder, reviewer, default)
  dispatcher .... GO
  criteria ...... GO (4, all verifiable)
  intent ........ GO
  budget ........ ADVISORY — no turn limit set; proposing goal_max_turns=15 per card
  gates ......... GO (human gate on merge to main)
POLL: GO with 1 advisory. Proceed? [adjust / go / abort]
```

NO-GO items must be resolved before launch. Advisories need one operator
word. Don't re-litigate after they answer.

## Step 2 — Sketch the card graph (the backbrief)

Decompose the mission into cards **before creating anything**, and show the
operator the graph. This is the backbrief: the plan presented before
execution, the cheapest place to catch intent drift.

Rules of decomposition (the kanban-orchestrator playbook applies in full):

- One card per workstream lane. Independent lanes stay unlinked so the
  dispatcher fans them out in parallel.
- Link only **true data dependencies** via `parents=[...]`. "Also" and
  "finally" in the Flight Plan do not imply sequence.
- Map each card's acceptance criteria back to specific Success Criteria from
  the Flight Plan. Every criterion must be owned by at least one card; if one
  is owned by none, the graph is incomplete.
- Don't pre-create cards whose shape depends on earlier findings. Create a
  synthesis/planning card whose job is to read parent handoffs and
  `kanban_create` the rest. Orchestrators can spawn orchestrators.
- If the graph is one card with no review, say so: this is task-sized, and a
  direct `/goal` would be cheaper. Advise once, then follow the operator.

Present the graph compactly:

```
CARD GRAPH: landing-site (4 cards)
  T1 design: site structure + copy outline        → builder    (no parents)
  T2 build: static site from T1 structure         → builder    (parents: T1)
  T3 review: against success criteria 1-3         → reviewer   (parents: T2)
  T4 gate: human approval before deploy           → builder    (parents: T3, blocks for review)
Go to create? [adjust / go]
```

## Step 3 — Create the cards

On Go, create cards **parents first**, capturing every returned `task_id`.
Never create children before their parents exist, and never link after the
fact — pass `parents=[...]` in the create call itself.

```python
import os

slug = "landing-site"  # kebab-case mission slug
tenant = os.environ.get("HERMES_TENANT")

t1 = kanban_create(
    title=f"[m:{slug}] design: site structure + copy outline",
    assignee="builder",
    body=BODY_T1,            # see card body anatomy below
    goal_mode=True,
    goal_max_turns=15,
    tenant=tenant,
)["task_id"]

t2 = kanban_create(
    title=f"[m:{slug}] build: static site from approved structure",
    assignee="builder",
    body=BODY_T2,
    parents=[t1],
    goal_mode=True,
    goal_max_turns=20,
    tenant=tenant,
)["task_id"]
```

If a `kanban_create` call fails, the card was NOT created — retry or report;
never reference a phantom id anywhere.

### Card body anatomy

The body is the worker's whole world (workers never see the Flight Plan) and
the `goal_mode` judge reads title + body as the acceptance criteria. Every
body has four parts:

```
OBJECTIVE
One paragraph: this card's outcome and the why behind it, restated from
Commander's Intent in fresh words. The why travels with every card.

ACCEPTANCE CRITERIA
- Explicit, checkable statements. Copy the relevant Flight Plan Success
  Criteria; sharpen them per card. "Every page renders without console
  errors" — not "site works."

CONSTRAINTS
- Budget for this card, pause conditions from the Flight Plan, workspace
  rules. If the Flight Plan says pause on security impact, every card says so.

HANDOFF
- What to leave in kanban_complete(summary, metadata) for downstream cards —
  name the fields so parsers downstream don't re-read prose.
- Always include usage self-report fields: {"usage": {"turns": N,
  "tokens_est": N}}. The board does not record these; your self-report is
  what makes the mission debrief's cost ledger possible.

Mission: <slug> | Flight Plan: missions/<slug>.md | Criteria owned: 1, 3
```

### Wiring the Flight Plan's controls onto the board

| Flight Plan section | Kanban mechanism |
|---|---|
| Success Criteria | Acceptance criteria in card bodies; `goal_mode=True` makes the judge enforce them every turn |
| Budget | `goal_max_turns` per card; sum stays within the plan's budget |
| Human gates | Card body instructs: do NOT complete — `kanban_comment` the structured handoff, then `kanban_block(reason="review-required: …")`. The operator unblocks to proceed |
| Pause conditions | Restated in every card's CONSTRAINTS with the same block-don't-complete instruction |
| Sequencing | `parents=[...]` at create time; dispatcher auto-promotes children when parents complete |

Use `goal_mode=True` for open-ended cards (most mission cards). Skip it only
for genuinely one-shot cards — a single lookup, a mechanical move — where the
judge overhead buys nothing.

## Step 4 — Record the launch

1. Append a Launch Record to the Flight Plan:

```markdown
## Launch Record
- Launched: <date> | Tenant: <tenant or none>
- Cards:

| id | title | assignee | parents | gate |
|---|---|---|---|---|
| t_xxxx | [m:slug] design: … | builder | — | — |
| t_yyyy | [m:slug] build: …  | builder | t_xxxx | — |
| t_zzzz | [m:slug] review: … | reviewer | t_yyyy | review-required |
```

Only ids captured from successful `kanban_create` returns go in this table.
This table is how `debrief-mission` later finds the mission's `task_runs`.

2. Set frontmatter `status: launched`.

3. Report to the operator in plain prose: what's on the board, what runs
   first, where the human gates are, and how to watch — the Hermes dashboard
   or `hermes kanban tail <id>`. Close with: **"Mission is on the board. Say
   'debrief' when it's done — or any time you want a status read."**

## Pitfalls

- **Doing the work yourself.** You are the launch director, not the crew. If
  you catch yourself "just drafting the copy real quick," stop and put it in
  a card.
- **Inventing assignees.** Silent drop. Step 0 list only, every time.
- **Linking by vibes.** Over-linked graphs serialize work that could fan out.
  Link only when a card cannot start without another card's output.
- **Vague acceptance criteria.** The judge is only as good as the card body.
  Every criterion checkable, every card.
- **Creating the whole graph when the shape is unknown.** Use a planning card
  that spawns the rest after reading parent handoffs.
- **Skipping the Launch Record.** Without the card-id table, the debrief has
  to grep titles. Write it immediately after creation, while ids are in hand.
- **Re-running checks after Go.** One poll, one answer. The operator's Go is
  the system's Go.
