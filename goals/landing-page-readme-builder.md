# Goal: Rewrite missions README for accessibility

## Objective
Rewrite the missions repo README.md so a new visitor understands the system's purpose and how to run their first mission in under 60 seconds.

## Success Criteria
- [ ] README opens with a one-sentence purpose statement
- [ ] README includes a 30-second "your first mission" example with exact commands
- [ ] README links to the three operator skills (define-mission, plan-mission, validate-mission)
- [ ] Technical depth (six handoffs, agency theory, etc.) is moved to a secondary doc and linked
- [ ] All links are valid (no 404s)

## Constraints
- Budget: 15K tokens, 10 minutes
- Preserve all technical content: move, do not delete
- Do not change the repo structure (no moving existing files unless necessary)

## Context
- Current README: /home/sivart/missions/README.md
- Flight Plan: missions/landing-page-readme.md
- Mission Contract: missions/landing-page-readme.contract.md
- Operator skills: ~/.hermes/skills/devops/{define,plan,validate}-mission/
