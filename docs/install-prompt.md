# Hermes Install Prompt

Copy everything below the line and paste it to your Hermes agent. It contains
everything she needs to install the missions.md skill package, prep the
fleet, verify the install, and report back — without starting any missions.

Steps that depend on host state come with a probe command, the expected
result, and the remedy when they differ — so the agent never has to read
Hermes source to recover.

---

# Install the missions.md skill package

## What you are installing

missions.md is a mission orchestration system that runs on your Kanban board.
Three skills: `define-mission` (turns operator intent into a one-page Flight
Plan), `launch-mission` (compiles a Flight Plan into Kanban cards with
dependencies, budgets, goal_mode verification, and human gates), and
`debrief-mission` (reads task_runs and generates an After-Action Review).
They build on tools you already have — kanban_create, goal_mode, kanban_block
— and add no new runtime.

Source repo: github.com/earth2travis/missions (it is a Hermes skills tap:
skills live under `skills/`, one directory per skill).

## Step 1 — Check for superseded skills

Probe: `ls ~/.hermes/skills/devops/`

If you find any of these from earlier iterations of this system, they are
**superseded by this package**: `mission-contracts`, `plan-mission`,
`validate-mission`, or a `define-mission` installed before this package.
The boundary: `launch-mission` replaces both `plan-mission` and
`validate-mission` (validation now runs automatically at launch);
`mission-contracts` is retired entirely.

Remove them so routing is unambiguous — "plan a mission" must resolve to
exactly one skill. Two things to know about removal before you start:

- Probe: `hermes skills uninstall <name>` — **interactive terminal only.**
  In a non-interactive terminal the confirm prompt cannot be answered and
  auto-cancels with a quiet "Cancelled." (uninstall has no `--yes` flag,
  unlike install). Expected on success: an "Uninstalled" confirmation.
- **If it reports "not a hub-installed skill":** the skill is local and was
  never Hub-tracked. Remedy: remove the directory directly
  (`rm -rf ~/.hermes/skills/devops/<name>`) and note the supersession in
  your report so the lineage is recorded somewhere durable.

List anything you removed in your report. Do not touch skills outside this
list.

## Step 2 — Install via the tap

Use `--yes` on installs so the quarantine confirmation does not hang waiting
for a TTY.

```
hermes skills tap add earth2travis/missions
hermes skills install earth2travis/missions/define-mission --category devops --yes
hermes skills install earth2travis/missions/launch-mission --category devops --yes
hermes skills install earth2travis/missions/debrief-mission --category devops --yes
```

**Fallback** — only if the Hub cannot fetch the repo (auth or rate limit):

```
git clone https://github.com/earth2travis/missions.git /tmp/missions
mkdir -p ~/.hermes/skills/devops
cp -R /tmp/missions/skills/* ~/.hermes/skills/devops/
rm -rf /tmp/missions
```

Know what the fallback costs: a manual copy bypasses Hub metadata, so
`hermes skills check` and `hermes skills update` will not track these skills.
If you used the fallback, say so prominently in your report and recommend
retrying the tap path later to restore update tracking.

## Step 3 — Fleet prep (profile descriptions)

`launch-mission` routes mission lanes by matching against the `description`
in each profile.yaml. Generate them — but probe with a single profile first,
because this is the step most sensitive to host config:

Probe: `hermes profile describe default --auto`

- **Expected:** a 1–2 sentence description is written and echoed.
- **If `AuthenticationError`:** the describe command routes through Hermes'
  auxiliary LLM client, and `auxiliary.profile_describer` defaults to
  `provider: auto`, which can resolve to nothing. Remedy: in
  `~/.hermes/config.yaml`, set `auxiliary.profile_describer.provider`,
  `model`, `base_url`, and `api_key` explicitly to match your main provider,
  then re-run the probe.

Once the probe passes, run the full fleet:

```
hermes profile describe --all --auto
```

- **If any profile returns "LLM returned an empty response":** known batch
  flakiness, not a config problem. Retry just those profiles individually
  (`hermes profile describe <name> --auto`); they typically succeed on the
  second attempt.

Tell the operator which descriptions were auto-generated so they can review
and edit (they are marked `description_auto: true`).

## Step 4 — Verify

1. `hermes skills list` shows define-mission, launch-mission, and
   debrief-mission under devops — and none of the superseded skills from
   Step 1.
2. Read the `version:` field from each installed SKILL.md frontmatter
   (`hermes skills list` does not display versions) and confirm `name:`
   matches its directory.
3. `hermes profile list` shows the fleet; every profile has a description.
4. Gateway and dispatcher:
   - Probe: `hermes gateway status` — expected: running.
   - The Kanban dispatcher runs embedded in the gateway when
     `kanban.dispatch_in_gateway` is true, which is the default. Probe:
     `grep dispatch_in_gateway ~/.hermes/config.yaml` — expected: `true`
     or absent (absent means default true). If it is `false`, cards will
     sit in `ready` with nothing to claim them — report this; do not
     change config or restart services without asking.
   - Optional board health check: `hermes kanban diagnostics`.

## Report back

When done, report:

- Which install path you used (tap or manual fallback — and if fallback,
  the update-tracking caveat)
- Superseded skills found and removed in Step 1, if any
- The three skills' versions (from SKILL.md frontmatter)
- The profile roster with descriptions, noting any that needed the
  auxiliary-client remedy or individual retries
- Gateway status and the dispatch_in_gateway value
- Anything that failed and what you did about it

Do not create any Kanban cards or start a mission — installation only. The
operator will initiate the first mission with "define a mission" when ready.
