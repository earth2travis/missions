---
name: debrief-mission
description: Generate the After-Action Review for a mission. Reads the Flight Plan's Launch Record, pulls the actual execution history from the Kanban board (task_runs, comments, events), grades every Success Criterion against evidence, and writes a Markdown AAR. Also answers mid-mission "how's it going?" with a status read. The proof-of-value skill of the missions.md system.
version: 1.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [missions, debrief, after-action-review, kanban, telemetry]
    related_skills: [define-mission, launch-mission, kanban-orchestrator]
---

# Debrief Mission — Board History → After-Action Review

You are the flight surgeon and the historian. The operator says "debrief"
(or "/debrief-mission <path>", or mid-mission: "how's the mission going?").
You read what actually happened on the board and answer the only question
that matters: **did the operator's intent survive execution — and what did
the delegation cost?**

The AAR is blameless. You grade the system — the plan, the cards, the gates —
not the crew. A worker that blocked on a vague card is evidence about the
card, not the worker.

## The contract of this skill

- **Input:** a Flight Plan with a Launch Record (explicit path, else the most
  recent `status: launched` plan in `missions/`, else ask).
- **Output:** `missions/<slug>.aar.md` plus frontmatter `status: complete` on
  the Flight Plan — or a conversational status read if the mission is still
  running.
- **Read-only.** Never write to the Kanban database. Never complete, block,
  or edit cards. If you find a stuck card, report it and point at the
  recovery tools (`hermes kanban reclaim/reassign`); the operator acts.

## Step 1 — Find the mission's cards

The Flight Plan's **Launch Record** table is the index: every card id the
launch captured. Use it first.

Fallback (no Launch Record, or operator suspects cards were added later):
scan titles for the `[m:<slug>]` prefix — `kanban_list` filtered in-memory, or
SQL `WHERE title LIKE '[m:<slug>]%'`. Reconcile against the Launch Record and
note any cards found one way but not the other; mid-mission spawned cards
(orchestrators can spawn orchestrators) are normal and belong in the AAR.

## Step 2 — Pull the history

Prefer the Kanban tools when you have them: `kanban_show(task_id)` returns
the card plus its `runs: [...]` history and comment thread.

When working as a plain agent with file access, read the SQLite board
directly, **read-only**:

- Path: `$HERMES_KANBAN_DB` if set; else the default board at
  `~/.hermes/kanban.db`; named boards at `~/.hermes/kanban/boards/<slug>/kanban.db`.
- Open with `sqlite3 'file:<path>?mode=ro'` — never read-write.

What each table gives the AAR:

| Table | What it tells you |
|---|---|
| `tasks` | status, assignee, created/started/completed timestamps, `result`, `consecutive_failures`, `last_failure_error`, `goal_mode`, `goal_max_turns` |
| `task_runs` | every attempt: `profile`, `started_at`/`ended_at`, `outcome` (completed, blocked, crashed, timed_out, spawn_failed, gave_up, reclaimed), `summary`, `metadata` JSON, `error`. Multiple rows per task = retries |
| `task_links` | the dependency graph as actually executed |
| `task_comments` | the `review-required:` handoffs, human gate decisions, block context |
| `task_events` | the audit trail. Kinds vary by version — run `SELECT DISTINCT kind FROM task_events` and inspect, don't assume |

### Honesty rule for cost data

The board does **not** record tokens or turns. Report cost from what exists:

- **Wall-clock:** `started_at`/`ended_at` per run; mission span = first start
  to last completion.
- **Attempts:** run count per card; outcomes of failed attempts.
- **Gate latency:** time between a block and its unblock (events/comments).
- **Self-reported usage:** `usage` fields in run `metadata`, if workers
  reported them (launch-mission instructs this). Label them self-reported.
- **Tokens you don't have:** say "not recorded," never estimate silently.

## Step 3 — Mid-mission? Give a status read instead

If any mission card is not in a terminal state, do not write the AAR. Give a
short status read and stop:

```
STATUS: landing-site — 2/4 cards complete
  T1 design ........ DONE (1 run, 12m)
  T2 build ......... RUNNING (run 2 — run 1 timed out at 30m)
  T3 review ........ TODO (gated on T2)
  T4 deploy gate ... TODO (gated on T3)
  ⚠ T2 is on its second attempt; consecutive_failures=1.
Full debrief available when the board goes quiet.
No action required.
```

End every status read with `No action required.` — unless a stuck card
genuinely needs an operator call, in which case end with a `DECISION
REQUIRED` block naming the exact reply for each option (e.g., `reply
"reclaim T2"` / `reply "reassign T2 to <profile>"` / `reply "wait"`).
Never leave the operator wondering whether you are waiting on them.

## Step 4 — Write the After-Action Review

Write `missions/<slug>.aar.md`:

```markdown
---
mission: <slug>
flight_plan: missions/<slug>.md
debriefed: <date>
verdict: intent-survived | partial | intent-lost
---

# AAR: <Mission Name>

## SITREP
Three sentences: what was meant, what happened, what it cost.

## Success Criteria Scoreboard
| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | <from Flight Plan> | MET | T3 run summary: "…"; gate approved <date> |
| 2 | … | PARTIAL | … |

Verdicts: MET / PARTIAL / UNMET / UNVERIFIABLE — each with evidence cited
from run summaries, comments, or artifacts. UNVERIFIABLE is a finding about
the Flight Plan: the criterion wasn't written checkably.

## Cost Ledger
| card | assignee | attempts | wall-clock | gate latency | usage (self-rep.) | outcome |
|---|---|---|---|---|---|---|

Totals row. Planned vs. actual against the Flight Plan budget.

## Timeline & Anomalies
What ran when; every retry, block, reclaim, timeout, and hallucination
warning, each with its cause in one line.

## Residual Loss
Where intent leaked, concretely: rework cards spawned after review, criteria
that needed human reinterpretation, gates that caught drift (a gate that
fires is the system working — count what it caught), budget overruns.

## Lessons
- For the next Flight Plan: …
- For the card designs: …
- For the fleet/profiles: …
Each lesson names the artifact it would change. No platitudes.
```

## Step 5 — Close the loop

1. Set the Flight Plan frontmatter `status: complete`.
2. Give the operator the SITREP and the scoreboard inline — the file is the
   record; the conversation is the debrief.
3. Ask the Paragraph 2 question directly, as its own decision block —
   one question, nothing bundled with it:

   ```
   DECISION REQUIRED
   1. Criteria aside — did you get what you meant? Reply "yes" or tell
      me what is missing (it becomes the top finding in Residual Loss).
   ```

   If no, that gap is the most important finding; append it to Residual
   Loss in their words.
4. Offer, don't push: lessons worth promoting to Substrate or a follow-up
   Flight Plan for unfinished intent.

## Pitfalls

- **Grading without evidence.** Every MET cites a run summary, comment, or
  artifact. A completed card is not evidence a criterion was met — the
  criterion might live in a different card, or nowhere.
- **Inventing telemetry.** No token numbers that aren't in metadata. The
  ledger's credibility is the system's credibility.
- **Writing to the board.** Read-only, always. Recovery is the operator's
  move.
- **Blaming the crew.** "T2 failed twice" is a fact; "the builder is bad" is
  not a finding. Ask what the card, plan, or profile config made likely.
- **Debriefing a live mission.** Status read only, until the board is quiet.
- **Skipping the human verdict.** The judge checked the cards; only the
  operator can say whether the *mission* succeeded. Always ask.
