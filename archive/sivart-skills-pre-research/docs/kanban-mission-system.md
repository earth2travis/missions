# The Kanban Mission System

## Why: From Craft to Factory
Previously, every Kanban board was hand-crafted. We manually defined tasks, linked dependencies, and assigned agents one by one. This was slow, error-prone, and impossible to reproduce.

The **Kanban Mission System** turns board creation into a **manufacturing process**. By scripting the deployment, we gain:
1.  **Reproducibility:** A "Mission Package" (Manifest + Script) can be saved in the Substrate. We can re-run a security audit or a research sprint in six months with a single command.
2.  **Complexity Management:** We can build complex, multi-stage swarms with dynamic dependencies that would be too fragile to create manually.
3.  **Versioned Workflows:** Missions are code. They can be reviewed, branched, and improved like any other part of the Factory.

## How: The Four-Phase Workflow

### 1. Define (The Strategist)
*   **Skill:** `define-mission`
*   **Action:** Translates a high-level goal into a `mission-manifest.md`.
*   **Output:** Strategic Intent, Success Criteria, and Required Specialists.

### 2. Plan (The Operations Officer)
*   **Skill:** `plan-mission`
*   **Action:** Decomposes the manifest into a `deploy-mission.sh` script.
*   **Output:** A bash script with `hermes kanban create` commands and dynamic dependency chaining.

### 3. Validate (The Inspector General)
*   **Skill:** `validate-mission`
*   **Action:** Audits the script for logic errors, circular dependencies, and invalid assignees.
*   **Output:** A Go/No-Go verdict.

### 4. Deploy (The Squad)
*   **Action:** Run `bash deploy-mission.sh`.
*   **Output:** The Kanban board is populated, and the Squad begins work.

## What This Makes Possible

### Mission Packages
We can now create "Mission Packages" for common workflows:
*   `mission-security-audit/`
*   `mission-research-sprint/`
*   `mission-incident-response/`

Each package contains the manifest and the deployment script. To start a mission, we simply run the script.

### Multi-Agent Swarms
By using variables for dependencies, we can orchestrate complex swarms where:
*   Three researchers work in parallel.
*   A scribe waits for all three to finish.
*   An inspector audits the scribe's work.
*   An engineer indexes the final result.

All of this happens automatically, with no human intervention required after deployment.

### The Factory OS
This system is the core of the **Factory OS**. It moves us from "using tools" to "building systems." We are no longer just managing tasks; we are **manufacturing outcomes**.
