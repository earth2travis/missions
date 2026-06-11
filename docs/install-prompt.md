# Hermes Install Prompt

Copy everything below the line and paste it to your Hermes agent. It contains
everything she needs to install the missions.md skill package, prep the
fleet, verify the install, and report back — without starting any missions.

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

## Install steps

Run these through your terminal tool. Use `--yes` on installs so the
quarantine confirmation does not hang waiting for a TTY.

1. Add the tap:

   ```
   hermes skills tap add earth2travis/missions
   ```

2. Install all three skills into the devops category:

   ```
   hermes skills install earth2travis/missions/define-mission --category devops --yes
   hermes skills install earth2travis/missions/launch-mission --category devops --yes
   hermes skills install earth2travis/missions/debrief-mission --category devops --yes
   ```

3. If the Hub cannot fetch the repo (private repo or GitHub rate limit),
   fall back to a manual install:

   ```
   git clone git@github.com:earth2travis/missions.git /tmp/missions
   mkdir -p ~/.hermes/skills/devops
   cp -R /tmp/missions/skills/* ~/.hermes/skills/devops/
   rm -rf /tmp/missions
   ```

## One-time fleet prep

launch-mission routes mission lanes by matching against profile descriptions
in each profile.yaml. Generate them for the whole fleet:

```
hermes profile describe --all --auto
```

Tell the operator which descriptions were auto-generated so they can review
and edit (they are marked `description_auto: true`).

## Verify

1. `hermes skills list` shows define-mission, launch-mission, and
   debrief-mission under devops.
2. Read each installed SKILL.md frontmatter and confirm `name:` matches its
   directory.
3. `hermes profile list` shows the fleet, and each profile has a description.
4. Confirm the gateway/dispatcher is running (cards cannot be claimed
   otherwise). Report its status; do not restart anything without asking.

## Report back

When done, report: which install path you used (tap or manual), the three
skills' versions, the profile roster with descriptions, gateway status, and
anything that failed. Do not create any Kanban cards or start a mission —
installation only. The operator will initiate the first mission with
"define a mission" when ready.
