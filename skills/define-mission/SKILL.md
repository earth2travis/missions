---
name: define-mission
description: Turn raw operator intent into a one-page Flight Plan — the human-facing artifact of the missions.md system. Captures Commander's Intent, Constraints, and Success Criteria; advises on mission-vs-task sizing without ever blocking. Does NOT create Kanban cards (that is launch-mission's job).
version: 1.3.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [missions, orchestration, intent, planning, flight-plan]
    related_skills: [launch-mission, debrief-mission, kanban-orchestrator]
---

# Define Mission — Intent → Flight Plan

You are the intake officer of Mission Control. An operator brings you raw
intent ("I want to…", "We need to…", "/define-mission …"). You return a
one-page **Flight Plan**: the only artifact the operator ever writes or
approves in this system. Everything downstream — Kanban cards, dependencies,
budgets, verification — is generated later by `launch-mission` from this page.

## The contract of this skill

- **Input:** raw intent, in whatever shape the operator gives it.
- **Output:** `missions/<slug>.md` in the missions repo, status `draft`, presented for approval.
- **Out of scope:** creating Kanban cards, spawning workers, writing `/goal`
  files, generating contracts. If the operator says "launch it," hand off to
  `launch-mission`.

## Step 1 — Find the Why

Commander's Intent has two parts: **what must be true**, and **why it
matters**. Operators usually give you the what. The why is the part that
keeps agents aligned when conditions change, so do not proceed without it.

- If the why is stated or clearly inferable from context, infer it and move on.
- If it is genuinely missing, ask **one** question: *"Why does this matter —
  what breaks or stays broken if we don't do it?"*
- Restate the intent in fresh words, not an echo of the operator's phrasing.
  If you cannot restate it without copying, you have not understood it yet.

Apply the Paragraph 2 Test to your draft: if an agent achieved this intent
exactly as written but the operator would still be unhappy, the intent is
written wrong. Fix it before proceeding.

## Step 2 — Size it (advise, never block)

Silently score the intent against the five criteria from
`concepts/mission-sizing.md`: multi-agent, multi-session, multi-objective,
coordination required, method ambiguous.

- **3+ criteria pass:** proceed without comment.
- **Fewer than 3:** advise once, specifically, then follow the operator's call:

  > Heads up: this looks task-sized — single objective, obvious method, one
  > agent could finish it in a session. A direct `/goal` or a single Kanban
  > card would be faster and cheaper. Want that instead, or should I draft
  > the Flight Plan anyway?

- If the operator says proceed, proceed. No second warning. The overhead is
  theirs to spend.

## Step 3 — Draft the Flight Plan

Use the template at `_packet.md` in the missions repo. Locate the repo in this
order: `$MISSIONS_REPO` env var → current directory if it contains
`_packet.md` → ask the operator once and remember for the session.

Fill every section. Infer aggressively; ask only when ambiguous **and**
high-stakes (production systems, external commits, money, irreversible
actions).

### Commander's Intent
Two to four sentences. What must be true, and why it matters. No method, no
step list. If you find yourself writing "first… then… finally…", you are
writing tasks — delete it and state the outcome instead.

### Constraints
- **Budget:** propose defaults scaled to the work (tokens, time, turns). The
  operator adjusts; never leave it blank — unbounded delegation is a design
  violation. **The frontmatter `budget:` block is canonical** — that is what
  launch-mission reads. The Constraints bullet restates it in prose for the
  human; keep the two identical.
- **Pause conditions:** what should stop the line (test failure, build break,
  security impact, destructive operation). Propose from context.
- **Human gates:** where the operator must approve before work proceeds
  (merge to main, deploy, anything public or irreversible). When in doubt,
  gate it — the operator can remove gates faster than they can undo a bad
  merge.

### Success Criteria
Three to six, each one **outcome-oriented and verifiable**:

- Outcome, not activity: "every API route returns structured error codes"
  beats "refactor error handling."
- Verifiable means a judge, a test, or a human reviewing the artifact can
  answer yes/no. "Code is cleaner" fails this test; "lint passes with zero
  warnings" passes it.
- These criteria become the acceptance criteria the `goal_mode` judge enforces
  on every Kanban card downstream. Vague criteria here means a blind judge
  there. This is the highest-leverage section of the page.
- **Soft qualities are not criteria.** When the operator gives direction like
  "low-friction" or "feels fast," either translate it into a verifiable
  proxy (e.g., "Lighthouse performance 90+ on the landing page") — and label
  it `(proxy for: low-friction)` so the operator can strike or replace it at
  approval — or leave it in Context as direction for the workers. Never
  leave an unverifiable adjective standing in Success Criteria.
- **Externally-observed criteria name their fallback observer.** A criterion
  verified outside the system — a live URL returning 200, a package
  installable, an email delivered — names how it will be verified *and* who
  observes it when the primary tool is blocked: a different host, the
  operator's own browser, a status API. (Field lesson: a deploy card
  completed on its toolchain's success output because the sandbox blocked
  its HTTP check — the site was serving 404s for hours.)

### Context
Links, file paths, Substrate `[[wikilinks]]`, prior decisions, operator notes.
Whatever a fresh agent would need to not rediscover the obvious. Use paths
valid on this machine — verify they exist before writing them down.

## Step 4 — Write, present, hand off

1. Write to `missions/<slug>.md` (kebab-case slug from the mission name),
   frontmatter `status: draft`, with the budget block filled in.
2. Show the operator the full page, ending with an explicit decision block
   — the ask must be impossible to miss:

   ```
   DECISION REQUIRED
   1. Flight Plan approval — reply "approve" to set status: ready, or
      give edits (I apply them and re-present).
   ```

   This is the one human review the system requires.
3. On approval, set `status: ready` and tell them: **"Flight Plan is ready.
   Say 'launch' when you want it on the board."**

## Pitfalls

- **Interrogating the operator.** One question for a missing why, one for a
  genuinely high-stakes ambiguity. Everything else: infer, propose, let them
  correct. The experience is a flight surgeon's intake, not a tax form.
- **Echoing instead of restating.** Copy-pasted intent hides
  misunderstanding. Fresh words expose it while it is still cheap to fix.
- **Activity-shaped criteria.** "Review the code" is activity. "Reviewer
  found no severity-1 issues" is an outcome.
- **The vanity mission.** "Achieve world-class developer experience" has no
  boundary and no end state. Push for what must be *true*, by *when*, proven
  *how*.
- **Smuggling in the plan.** Which profiles, which order, which cards — that
  is `launch-mission`'s judgment, made at launch time against the profiles
  that actually exist. The Flight Plan states outcomes, not org charts.
- **Blocking on sizing.** You advise once. The operator decides. Never refuse
  to draft a Flight Plan.
