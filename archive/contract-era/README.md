# Archive: Contract Era

These artifacts are from the four-layer architecture (Flight Plan → hidden Mission
Contract → `/goal` files → Kanban tasks) that preceded the current system.

On 2026-06-10 we decided the hidden Mission Contract layer was MVP-unnecessary:
Hermes Kanban already encodes what the contract recorded — `parents=` for
sequencing, `goal_mode` for verification, `kanban_block()` for human gates, and
`task_runs` for the Agency Cost Ledger. The Flight Plan now compiles directly to
Kanban cards, and the After-Action Review is generated from `task_runs` after
execution.

## Contents

| File | What it was |
|---|---|
| `_template.md` | The full six-handoff Mission Contract template |
| `evolution-plan.md` | Plan to evolve pre-research skills into contract-authoring skills (superseded) |
| `landing-page-readme.flight-plan.md` | Demo Flight Plan (task-sized by the sizing guide; its goal — an accessible README — was fulfilled during the 2026-06-10 cleanup) |
| `landing-page-readme.contract.md` | Demo auto-generated Mission Contract |
| `landing-page-readme-builder.md` | Demo `/goal` file (goal text now lives in Kanban card bodies) |
| `landing-page-readme-reviewer.md` | Demo `/goal` file |
| `landing-page-readme-merge.md` | Demo `/goal` file |

The theory behind these documents (six handoffs, incomplete contracts,
principal-agent costs, residual control) is not abandoned — it informs how the
`launch-mission` skill designs Kanban cards. It just no longer lives in a
parallel artifact the operator has to maintain.
