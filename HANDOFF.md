# HANDOFF: missions.md — Session 2026-06-11 (supersedes prior handoff)

## SITREP

The first real mission has been flown end to end and the system survived
contact with reality. `missions-site` launched 03:10 UTC, ran 17 runs across
10 cards, hit honest failures at exactly the places the theory predicted —
and every loss was caught, bounded, and fixed in minutes. The site is live:
**https://missions-site.sivart-36d.workers.dev** (all six criteria verified
on the deployed artifact, Lighthouse P97/A96 on the edge). The After-Action
Review exists (`missions/missions-site.aar.md`, verdict: intent-survived,
operator-confirmed), and its Lessons are already compiled into the skills.
The AAR is the proof-of-value artifact this project was built to produce.

---

## What This Is

A mission orchestration system on Hermes Kanban. The operator writes a
one-page **Flight Plan** (Commander's Intent, Constraints, Success Criteria,
Context); `launch-mission` compiles it directly to Kanban cards;
`debrief-mission` proves whether intent survived. Two layers, no hidden
contract (`archive/contract-era/` explains the retired layer). The repo
doubles as a Hermes skills tap: `hermes skills tap add earth2travis/missions`.

| Skill | Version | Job |
|---|---|---|
| define-mission | 1.3.0 | intent → Flight Plan (advisory sizing, proxy-labeled criteria, fallback observers for external criteria) |
| launch-mission | 1.5.0 | Flight Plan → cards: Go/No-Go poll, backbrief graph, verification discipline, workspaces, gates |
| debrief-mission | 1.2.0 | board history → AAR (evidence-graded, ledger reconciles, artifacts observed not trusted) |

Source of truth: `skills/` in this repo. Installed at `~/.hermes/skills/devops/`
locally and on the fleet. All three scan **safe** with the Hub scanner — keep
it that way (see Conventions).

## The Cast

- **Operator: Travis (Ξ2T, earth2travis).** 2026 word: "Relax" — ship working
  things, never over-engineer. Operator-first, minimal friction, NASA Mission
  Control flavor. The system advises; the operator decides; never block.
- **Architect (you, on Travis's Mac).** Repo at `/Users/earth/Sites/missions`.
  Full Hermes source at `~/.hermes/hermes-agent` — **verify every claim about
  Hermes behavior against that source before patching anything.** You design
  and patch skills, audit field reports, commit and push.
- **Sivart:** Hermes agent on the VPS "alchemist" (user `sivart`), running a
  7-profile fleet (default/orchestrator, campaign_scribe, combat_engineer,
  inspector_general, intelligence_officer, signal_analyst, +1). Travis relays
  between you and her by pasting. She has her own GitHub account
  (collaborator on earth2travis repos, pushes over SSH — **never PATs in
  chat; credentials go in the 1Password vault, reached via `op` under the
  Hermes env**). She also pushes to this repo's main —
  **always `git pull --rebase` before pushing.**

## Conventions (non-negotiable — each one came from a field failure)

- Every operator ask ends in a `DECISION REQUIRED` block: numbered decisions,
  each naming the literal reply and its effect. Never bundle a NO-GO remedy
  into a launch word. Status-only messages end `No action required.`
- Host-dependent instructions ship probe / expected output / named remedy.
- **Probes pasted to terminals are single-line or repo files — never
  heredocs, never long one-liners** (terminal paste mangles both). The kit:
  `tools/board-probe.py` — board overview per mission slug, `--runs <id>`
  for full run history + metadata + comments. Read-only at the SQLite layer.
- **Verification discipline** (now in launch-mission 1.5.0): can't-verify ⇒
  block, never complete on a toolchain's success output; deploy cards verify
  from outside the toolchain with a named fallback observer; verification
  cards whose verdict is FAIL block instead of completing.
- Blameless analysis: grade the plan and the cards, not the crew.
- Skill text must pass `tools/skills_guard.py` (in hermes-agent): never write
  literal Hermes-config or agent-config file paths in a SKILL.md — the
  scanner grades them dangerous and blocks the tap install. Rescan all three
  skills before every push that touches them.

## Hermes Facts (verified against source — don't re-derive)

- `task_runs` holds per-attempt outcome/timestamps/summary/metadata/error;
  **no tokens or turns recorded** — cards make the `usage` self-report part
  of acceptance criteria; debrief labels it self-reported, never estimates.
  Run metadata lives on runs, not the task object.
- `kanban_create` params: parents, goal_mode, goal_max_turns,
  workspace_kind/workspace_path, skills, max_runtime_seconds, tenant.
  **No metadata param** — mission identity = `[m:<slug>]` title prefix +
  body footer + Launch Record table in the Flight Plan.
- Orchestrator-created cards do NOT inherit workspaces; pass explicitly.
  Scratch workspaces are GC'd at archive — no path-shaped handoffs on
  scratch cards (the scratch consistency rule).
- Dispatcher runs **embedded in the gateway** when
  `kanban.dispatch_in_gateway` is true-or-absent — no daemon process exists
  and that absence is healthy. Block reason → last run's summary; review
  packets → `task_comments`. Heartbeat staleness threshold: 3600s.
- `hermes skills update <name>` is surgical; `uninstall` needs a TTY (no
  `--yes` — upstream issue drafted, NOT filed) and only knows Hub skills.
- `hermes profile describe <name> --text "..."` sets a description with no
  LLM; `--auto` needs the `auxiliary.*` client configured in config.yaml.
- Worker sandboxes filter networks (one blocked all `.dev` domains) — this
  is why verification discipline exists.
- Default board DB: `~/.hermes/kanban.db`; read-only access only.

## Field Findings With Shelf Life (from the missions-site mission)

- **wrangler 3 cannot statically detect vinext 0.1.1's re-exported default
  fetch handler** — uploads `handlers: []`, Cloudflare never activates the
  deployment, workers.dev serves its placeholder. wrangler 4 fixes it.
- `run_worker_first: true` (bare bool) routes static assets into the SSR
  worker → asset 404s. Use a rule array with at least one positive rule:
  `["/*", "!/_next/static/*", "!/favicon.svg"]`.
- vinext App Router mode with wrangler.toml present requires
  `@cloudflare/vite-plugin`; a stray root `index.html` makes Vite serve `/`
  as a static SPA shell, bypassing SSR entirely.
- "In the vault" is not "usable from this host" — probe credentials
  (reachable AND valid for the target API) before launch, one curl each.

## Next Steps (operator's word required for each)

1. **File the upstream issues** (both drafted in spirit, neither filed):
   `hermes skills uninstall --yes` to NousResearch/hermes-agent; the
   wrangler-3 handler-detection finding to cloudflare/vinext.
2. **Custom domain** — attach to the Cloudflare deployment (DNS was gated
   out of mission scope; site is domain-ready, no hardcoded URLs).
3. **Community launch story** — the material exists: a live site built by
   the system it describes, plus an AAR proving what delegation cost.
4. **Template library** — candidate next iteration once a second mission
   has flown.
5. Long-term: contribute the skills to the Hermes ecosystem.

## Files to Read on Resume

1. `README.md` — story and architecture
2. `missions/missions-site.md` + `missions/missions-site.aar.md` — the first
   mission's Flight Plan, Launch Record, and AAR (the system's best
   self-documentation)
3. `skills/*/SKILL.md` — current contracts, post-AAR versions
4. `docs/install-prompt.md` — onboarding path, verified end-to-end in a
   clean environment
5. `~/.hermes/skills/devops/kanban-orchestrator/SKILL.md` +
   `kanban-worker/SKILL.md` — the runtime's real contracts
6. `git log --oneline -20` — the session-by-session record

## The Commitment

Build the simplest thing that works. Two layers, three skills — and now one
real mission flown, debriefed, and compiled back into the system. The loss
was visible, bounded, and small. Keep it that way.
