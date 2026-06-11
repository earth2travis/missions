---
title: "Flight Plan: Public missions.md Site"
status: complete # draft → ready → launched → complete
priority: normal
budget:
  tokens: 500000
  time: "48h"
---

# Flight Plan: Public missions.md Site

## Sizing Check (Informational)
Mission. Passes all five criteria: multiple objectives (content, build,
install path, deploy), ambiguous method (framework and hosting are judgment
calls), real coordination between content and build work, multi-session,
multi-agent. A single `/goal` could not hold this.

## Commander's Intent

missions.md exists so that delegated intent survives execution, but today the
system is invisible outside its own repo. There must be a public site where a
stranger from the open-source or Hermes community understands, within the
first screen, what missions.md is and why intent loss matters, and can travel
from that first screen to working skills on their own fleet without leaving
the site's instructions. The site is the system's public face: until it
exists, the tool stays private and the ideas stay locked in a README.

## Constraints

- Budget: 500,000 tokens / 48 hours wall-clock (operator-proposed; adjust at approval)
- Pause conditions:
  - Build break that survives one repair attempt
  - Anything requiring credentials the operator has not provided (Cloudflare
    deploy token expected in the Operations vault)
  - Any irreversible action not covered by a human gate
- Human gates:
  - Operator approves content and design before anything deploys
  - Any push to the default branch of a public repo
  - The deploy itself (site going live at a public URL)
  - Any DNS change

## Success Criteria

1. First-screen comprehension: a reviewer who has never seen the missions
   repo, shown only the landing page's first screen, can state what
   missions.md is and why intent loss matters. Verified by a fresh-context
   judge with no access to the repo.
2. The install path works end to end: following only the site's
   instructions, a Hermes agent on a host without the skills reaches all
   three skills installed and verified. Verified by an actual run, not a
   read-through.
3. Every claim on the site traces to the missions repo (README.md,
   docs/install-prompt.md, _packet.md, concepts/) and none contradicts it.
   Verified by side-by-side review against those four sources.
4. The site builds clean (zero errors, zero warnings treated as errors) and
   is live at its public URL returning HTTP 200 after the gated deploy.
5. Lighthouse performance and accessibility scores of 90+ on the landing
   page. (proxy for: low-friction)
6. The rendered site is strictly monochrome: computed styles resolve to
   black, white, and grays only, with no chromatic color anywhere.
   (proxy for: cyberpunk minimalist aesthetic)

## Context

- Content source of truth: local clone at `/home/sivart/missions/` —
  `README.md` (the story), `docs/install-prompt.md` (onboarding),
  `_packet.md` (Flight Plan template), `concepts/` (deeper thinking).
  The site distills these; it never contradicts them.
- Site code: new repo `earth2travis/missions-site` (operator to confirm
  name). Create private; flipping public is covered by the deploy gate.
- Framework: `cloudflare/vinext` — a Vite plugin reimplementing the Next.js
  API surface. Operator-directed; do not substitute another framework. It is
  young software: if it breaks, repair or work around it within budget, and
  pause rather than swap frameworks silently.
- Hosting: Cloudflare (Workers, via vinext's deploy path). Deploys need a
  Cloudflare API token from the Operations vault; the deploy itself is
  human-gated. The VPS stays untouched.
- Tone: NASA Mission Control told in Le Guin x Gibson — contemplative,
  anthropological depth with high-tech, low-life precision. Poetic but not
  flowery; every sentence earns its place. The story of why leads; the
  architecture follows. The README's voice is the floor, not the ceiling.
- Aesthetic: cyberpunk minimalist, black and white only. Strive for
  simplicity — best practices and industry standards, no decoration that
  does not carry meaning. This direction guides workers; criterion 6 is its
  verifiable floor.
- Custom domain: exists, will be attached to the Cloudflare deployment
  after mission completion. Out of scope for this mission; the site must be
  domain-ready (no hardcoded URLs). The DNS gate covers it if scope changes.
- The missions repo archive (`archive/contract-era/`) contains an earlier
  landing-page effort; useful as a record of what the operator has already
  rejected or evolved past, not as content.

## Launch Record
- Launched: 2026-06-11 | Tenant: none
- Dispatcher: embedded in hermes-gateway.service (systemd user unit,
  enabled, Linger=yes; `kanban.dispatch_in_gateway: true`, 60s interval).
  No separate daemon needed.
- Shared workspace: /home/sivart/workspaces/missions-site
- Cards:

| id | title | assignee | parents | gate |
|---|---|---|---|---|
| t_c84e9778 | [m:missions-site] content: distill repo into site copy + IA | campaign_scribe | — | — |
| t_feb28a30 | [m:missions-site] scaffold: vinext app + monochrome design system | combat_engineer | — | — |
| t_62fc052c | [m:missions-site] build: integrate copy into site | combat_engineer | t_c84e9778, t_feb28a30 | — |
| t_95b5dcd0 | [m:missions-site] review: criteria 1,3,5,6 + content/design gate | inspector_general | t_62fc052c | review-required: content+design approval |
| t_862f3c59 | [m:missions-site] verify install path end-to-end (criterion 2) | intelligence_officer | t_62fc052c | — |
| t_340d7b29 | [m:missions-site] gate + deploy: repo public, Cloudflare live (criterion 4) | combat_engineer | t_95b5dcd0, t_862f3c59 | review-required ×2: repo public, deploy |
| t_70409598 | [m:missions-site] rework: install page matches corrected install docs | combat_engineer | — | — |
| t_3a5d08a9 | [m:missions-site] re-verify install path end-to-end (criterion 2, second attempt) | intelligence_officer | t_70409598 | — |
| t_3e071f9c | [m:missions-site] repair: vinext hydration — site must render, not just build | combat_engineer | — | pause-on-fail: framework decision returns to operator |
| t_3de4be1a | [m:missions-site] repair: deploy must ship the SSR worker — site live with HTTP 200 | combat_engineer | — | — (deploy authority pre-granted) |
