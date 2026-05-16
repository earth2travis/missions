# missions/

> This directory holds Mission Contracts: orchestration manifests that define multi-agent work across heterogeneous tools.
>
> For the philosophy behind this system, see the Substrate knowledge base: [earth2travis/substrate](https://github.com/earth2travis/substrate)

## What This Is

A Mission Contract is a file that describes what must be done, why it matters, and how intent travels from human intention to machine execution without being lost along the way.

It is not a task list. It is not a project plan in the traditional sense. It is an incomplete contract: specific enough to evaluate, open enough to adapt. The human defines the outcome. The agents choose the method. The contract ensures the outcome and the method remain connected.

## What This Is Not

- **Not a replacement for /goal.** The `/goal` primitive is the execution leaf: session-scoped, autonomous, "work until done." The Mission Contract is the orchestration container: cross-session, intent-preserving, spanning multiple `/goal` invocations. They are complementary, not conflated.
- **Not a walled garden.** Any tool that implements `/goal` can participate in a Mission pipeline without adopting our format. The Mission Contract references `/goal` texts; it does not redefine them.
- **Not a guarantee.** Perfect delegation is theoretically impossible. The contract makes intent loss bounded and observable, not eliminated.

## The Architecture

```
missions/
  _template.md          # Start here. Copy, rename, remove guidance blockquotes.
  [mission-name].md     # Your Mission Contract: the orchestration manifest

goals/
  [goal-name].md        # /goal text files: tool-agnostic execution primitives
```

The Mission Contract lives in `missions/`. The `/goal` texts live in `goals/`. The orchestrator reads the Contract, maps each `goal_ref` to the appropriate agent and tool, and dispenses `/goal` texts as leaf-node instructions.

No agent receives the Mission Contract. Agents receive `/goal` texts in the standard syntax they already understand. The Contract is the orchestrator's map. The `/goal` is the agent's compass.

## The Six Handoffs

Every Mission Contract implements the six handoffs from the mission execution chain. Each handoff is a delegation point. Each delegation point is an agency relationship. Each agency relationship is a place where intent can be lost.

| Handoff | From → To | What the Contract Enforces |
|---------|-----------|---------------------------|
| 1 | Why → BHAG | Intent restatement: the Mission must serve the Why in fresh words |
| 2 | BHAG → Mission | Paragraph 2 Test: achieving the Mission must serve the BHAG |
| 3 | Mission → Objectives | Outcome orientation: every objective measures result, not activity |
| 4 | Objectives → Projects | Backbrief gate: plan presented and approved before /goal assignment |
| 5 | Projects → Tasks | Intent metadata: every task links to the objective it serves |
| 6 | Tasks → Execution | Verification stack: signals collected, human review gate, stop-the-line authority |

The template makes each handoff explicit. You cannot skip one accidentally. It is a required section.

## Residual Control

Per Grossman and Hart, residual control rights determine who has the incentive to enforce the contract. The Mission Contract specifies who holds pause, approve, override, and completion rights at each handoff.

This prevents two failure modes:
- **Human holds everything:** Initiative dies. The agent becomes a script.
- **Agent holds everything:** Accountability dies. The principal becomes a spectator.

The optimal allocation is contextual and configurable per Mission. The template provides the structure. You provide the decision.

## Agency Cost Ledger

Every Mission Contract includes a ledger table that is populated after execution. It tracks:

- Tokens consumed per handoff
- Turns used per agent
- Latency per delegation
- Verification signal coverage
- Estimated residual loss (false done detection, plan drift, rework)

This makes Holmstrom's agency costs observable. You cannot eliminate them. You can measure them and optimize their sum.

## How to Use This

1. **Copy the template.** `cp missions/_template.md missions/[your-mission-name].md`
2. **Remove guidance blockquotes.** Every `> ` line is instructions for you. Delete them.
3. **Fill the Mission Statement.** Pass the Bungay "Why" test. What must be true, and why does it matter?
4. **Define the cascade.** Walk through the six handoffs. Be explicit.
5. **Write the /goal files.** Create `goals/[goal-name].md` files for each execution leaf. Use standard `/goal` syntax.
6. **Assign residual control.** Who holds pause, approve, and override at each handoff?
7. **Execute.** The orchestrator reads the Contract, runs the backbrief protocol, dispenses `/goal` texts, and populates the ledger.
8. **Review.** After execution, the ledger tells you what the delegation cost. The contract tells you whether the intent survived.

## Related Knowledge

- Mission Execution Chain (Substrate)
- Principal-Agent Theory (Substrate)
- The /goal Primitive (Substrate)
- Kanban Doctrine (Substrate)
- Subagent Architecture (Substrate)

## The Commitment

A Mission Contract is a promise: from human to agent, from intent to execution, from what matters to what gets done. It is not a guarantee that the promise will be kept perfectly. It is a structure that makes broken promises visible, measurable, and improvable.

The goal is not perfect delegation. The goal is bounded, observable, and composable delegation across tools that share nothing except the will to build something that matters.
