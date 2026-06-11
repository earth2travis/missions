---
name: launch-mission
description: Compile an approved Flight Plan into Hermes Kanban cards and launch the mission. Runs automatic pre-flight Go/No-Go checks, presents the card graph for operator approval, then issues real kanban_create calls with dependencies, budgets, goal_mode verification, and human gates. The deep-integration skill of the missions.md system.
version: 1.4.0
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

## Asking the operator: the decision block

Every time you stop for operator input — the poll, the card graph, a NO-GO
remedy — end the message with exactly one block in this shape, and put
nothing the operator must act on outside it:

```
DECISION REQUIRED
1. <decision> — reply "<word>" to <effect>, or <alternative>.
2. <decision> — ...
```

- One numbered line per decision. Each names the **literal reply** that
  proceeds and what it causes.
- Distinct decisions stay distinct. **Never bundle a NO-GO remedy into the
  launch word** — clear the NO-GO as its own decision, show the re-probe
  result, then ask for launch separately.
- Pure status reports end with `No action required.`

(Field lesson: a pre-flight that said a NO-GO "resolves at your word" left
the operator unsure what to say. The ask must be impossible to miss.)

## Step 0 — Discover and read the fleet

Before anything else, build a **roster with capabilities**, not just a name
list. Three signals, in order of strength:

1. **Names and models:** `hermes profile list` via your terminal tool (ask
   the operator if you can't run it).
2. **Descriptions:** each profile's `profile.yaml`
   (`~/.hermes/profiles/<name>/profile.yaml`; the `default` profile lives at
   the root) may carry a `description` of what it is good at. This is the
   same signal Hermes' native `kanban decompose` routes by — match against
   it and you are speaking the platform's own routing convention.
   - **If profiles are undescribed**, offer to fix it once for the whole
     fleet: `hermes profile describe --all --auto` has the auxiliary LLM
     generate each description from the profile's installed skills, model,
     and name. One command, and every future mission routes better. The
     operator can review/edit afterward (`description_auto: true` marks
     them).
3. **Track record:** the board knows what each assignee has actually
   finished. When two profiles look equally fit on paper, check recent
   completed cards per assignee (`kanban_list` / run summaries) —
   demonstrated competence beats described competence.

Cache the roster for the conversation.

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
| Dispatcher is running | Cards would sit unclaimed. Probe correctly: `kanban.dispatch_in_gateway` in `~/.hermes/config.yaml` true-or-absent **plus** the gateway service active means the dispatcher runs **embedded in the gateway** — confirm via the `kanban dispatcher: embedded in gateway` line in gateway.log. Do NOT grep for a standalone daemon process; an embedded dispatcher shows none, and that absence is not a NO-GO |
| Flight Plan has at least one Success Criterion | `goal_mode` judges against acceptance criteria; no criteria = blind judge |

**ADVISORY (intent quality — report specifically, operator may override with a word):**
| Check | What good looks like |
|---|---|
| Commander's Intent states a why, not just a what | An agent could make a judgment call from it |
| Intent is an outcome, not a step list | No "first… then… finally…" |
| Success Criteria are outcome-oriented and verifiable | A judge, test, or human can answer yes/no |
| Budget is set | Tokens/time/turns present in frontmatter |
| Frontmatter budget matches Constraints prose | The frontmatter `budget:` block is canonical (it is what you read); if the prose drifted, flag the mismatch and have the operator confirm which number stands |
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
POLL: GO with 1 advisory.

DECISION REQUIRED
1. Budget advisory — reply "accept turns" to use goal_max_turns=15 per
   card, or give your own numbers.
2. Proceed — reply "go" to see the card graph, or "abort".
```

If the poll had a NO-GO, it becomes decision #1 with its remedy ("reply
'fix dispatcher' and I will …"), and the proceed question waits until you
have shown the NO-GO cleared. Advisories need one operator word. Don't
re-litigate after they answer.

## Step 2 — Sketch the card graph (the backbrief)

Decompose the mission into cards **before creating anything**, and show the
operator the graph. This is the backbrief: the plan presented before
execution, the cheapest place to catch intent drift.

Rules of decomposition (the kanban-orchestrator playbook applies in full):

- One card per workstream lane. Independent lanes stay unlinked so the
  dispatcher fans them out in parallel.
- Assign each lane by matching it against the roster's **descriptions and
  track record**, and show your reasoning in the graph — the operator should
  see *why* each profile got its lane, so a bad match dies in the backbrief,
  not on the board.
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
     why builder: "front-end implementation and static sites" + 6 done cards in this domain
  T2 build: static site from T1 structure         → builder    (parents: T1)
  T3 review: against success criteria 1-3         → reviewer   (parents: T2)
     why reviewer: description names QA/code review; only profile with review history
  T4 gate: human approval before deploy           → builder    (parents: T3, blocks for review)

DECISION REQUIRED
1. Card graph — reply "launch" to create these cards exactly as shown,
   or name the change (card, assignee, parent, gate, workspace).
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
    workspace_kind="dir",                       # persistent artifact → shared dir
    workspace_path="/srv/missions-site",        # same path on every collaborating card
    tenant=tenant,
)["task_id"]

t2 = kanban_create(
    title=f"[m:{slug}] build: static site from approved structure",
    assignee="builder",
    body=BODY_T2,
    parents=[t1],
    goal_mode=True,
    goal_max_turns=20,
    workspace_kind="dir",                       # repeat explicitly — orchestrator-created
    workspace_path="/srv/missions-site",        # cards do NOT inherit workspaces
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

### Workspaces: where the work product lives

`kanban_create` defaults to `workspace_kind="scratch"` — a throwaway tmp dir,
garbage-collected when the task archives. **Scratch is wrong for any mission
that produces a persistent artifact.** Decide the workspace per card before
creating anything:

| Mission shape | Workspace |
|---|---|
| Research / analysis (artifact is the handoff text) | `scratch` (default) is fine |
| Cards collaborating on files (site, codebase, docs) | `workspace_kind="dir"`, `workspace_path=<absolute shared path>` — same path on every card in the lane |
| Code changes that should land as commits/PRs | `workspace_kind="worktree"` — workers commit on a task branch |

The shared path must exist (or be a repo clone) before launch; verify it in
pre-flight when the graph needs one. State the workspace in the card graph
you present — the operator should see where the work product will live.

**The scratch consistency rule:** scratch is legal only when the handoff
*contains* the artifact — findings in the summary, data in metadata, prose
in a comment. **If any HANDOFF field asks for a path (`*_path`, "where you
wrote X"), the card cannot be scratch** — scratch workspaces are deleted
when the task completes, so the path dangles the moment a downstream card
reads it. Either give the card a persistent workspace (`dir`/`worktree`,
usually the lane's shared path), or rewrite the handoff to carry the
content itself. Check every card for this before the backbrief: a card
whose handoff names a path while its workspace is scratch is a graph bug,
not a style choice. (Field lesson: a content card "completed" into a
scratch dir and its six pages of copy nearly evaporated before the build
card could read them.)

Two more per-card controls worth using when they fit:
- `max_runtime_seconds` — wall-clock circuit breaker alongside `goal_max_turns`.
- `skills=[...]` — force-load specific skills into the worker for that card
  (appended to the dispatcher's built-in `kanban-worker`).

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
- **Burying the ask.** If the operator has to re-read your message to find
  what you need from them, the message failed. Every stop ends in a
  DECISION REQUIRED block; everything else is briefing.
