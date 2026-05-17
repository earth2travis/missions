# Structural Limits: What the Architecture Makes Possible and Impossible

## What It Makes Structurally Possible

### 1. Intent-Driven Automation
A human writes a Mission Contract in `missions/`. The orchestrator reads it and fans out into Kanban tasks with explicit parent-child dependencies, backbrief requirements, and verification signal requirements. The human never writes a task card. The human writes intent. The system decomposes.

### 2. Persistent Multi-Session Execution
Unlike ephemeral chat sessions that die when context compresses, a Mission Contract spans sessions, restarts, and tool boundaries. A builder uses Codex `/goal` for three hours, crashes, and the dispatcher reclaims the task. A reviewer uses Claude Code `/goal` the next day. The orchestrator uses Hermes `/goal` to synthesize. All three sessions are linked by the same Mission Contract and the same Kanban task history.

### 3. Observable Agency Costs
Every handoff in the Mission Contract generates a row in `task_runs`. Tokens consumed, turns used, latency, verification signals, residual loss. The Agency Cost Ledger is not a separate document. It is a view of the database. For the first time, the cost of delegation is measurable in real time.

### 4. Composability Without Lock-In
Because the leaf execution is standard `/goal`, any tool that adopts it joins our pipeline automatically. We do not ask Codex to adopt our Mission format. We do not ask Claude Code to adopt our Kanban system. We ask them to keep doing what they are already doing. The Mission Contract is the Rosetta Stone.

### 5. Human-in-the-Loop Governance
The "blocked" state in Kanban is the operationalization of residual control. The Mission Contract specifies who holds pause rights at each handoff. The Kanban system enforces it. A worker cannot proceed past a verification gate without human unblock. Intent is preserved because control is preserved.

## What It Makes Structurally Impossible

### 1. Opaque Black Boxes
You cannot have a Mission Contract that hides its decomposition. Every handoff is explicit, verifiable, and linted by the Intent Cascade Linter before execution. Ambiguity is caught at the keyboard, not in production.

### 2. Unbounded Delegation
The Mission Contract's budget constraints (token limits, turn limits, time limits, max runtime) mean agency costs are bounded. A runaway agent hits a circuit breaker and the task blocks. The human is notified. No unlimited spend.

### 3. Single-Tool Lock-In
Because we use the standard `/goal` primitive, we cannot be trapped in a single vendor's ecosystem. If Codex changes its API, we swap the worker lane. The Mission Contract does not change. The Kanban runtime does not change. Only the lane adapter changes.

### 4. Fire-and-Forget Automation
The Kanban runtime's durability means every task has history, retry logic, and human intervention points. You cannot "launch and ignore." The system expects supervision. The Mission Contract makes that expectation explicit.

## The Architecture

```
Human writes Mission Contract (missions/)
    → Orchestrator reads Contract, decomposes into Kanban tasks (kanban_create)
    → Dispatcher claims tasks, spawns workers (via worker lanes)
    → Workers execute via /goal (Codex, Claude, Hermes)
    → Structured handoff (kanban_complete with metadata)
    → Agency Cost Ledger populated (task_runs + events)
    → Human reviews via dashboard or /kanban commands
```

This is a shift from "I ask an AI to do something" to "I define a mission, and the system orchestrates execution across specialized agents, preserving my intent and giving me control."

## The missions.md Synthesis

`missions.md` is the public face of this system. It is the brand that says: mission-driven project management is how humans direct agent ecosystems. The site explains the philosophy, shares templates, validates contracts, and shows live execution.

The Hermes Kanban system is the runtime that makes it real. The Mission Contract is the manifest that makes it intentional. The `/goal` primitive is the standard that makes it universal.