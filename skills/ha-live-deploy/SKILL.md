---
name: ha-live-deploy
description: Use when preparing or performing live Home Assistant deploys, backup-first writes, SSH syncs, reload/restart decisions, post-restart checks, HA quality gates, rollback planning, or merged-PR deploy handoffs.
---

# Home Assistant Live Deploy

Live writes default to plan-then-apply. Generate a deploy plan first and apply it only after explicit confirmation.

## Workflow

1. Resolve the plugin root as the directory two levels above this `SKILL.md`.
2. Read `../../references/live-guardrails.md`.
3. Run local validation before any live write, normally `make check`.
4. Generate the deploy plan:

```bash
python <plugin-root>/scripts/generate_deploy_plan.py . --host root@172.30.55.10
```

5. Include backup, sync, reload/restart, cache-bust, quality-gate, and rollback commands.
6. If the user approves applying the plan, take the HA backup first and record the backup slug/id.
7. After restart, wait for active Supervisor restart jobs to clear before judging the quality gate.
8. Verify live artifacts directly. For split repos, validate both support code and `custom_components/<domain>`.

## Guardrails

- Never write to `/config` before a backup.
- Prefer targeted reloads when safe; restart Core for Python integration code or manifest changes.
- Treat immediate `home_assistant_core_restart` warnings as pending restart evidence until a re-poll confirms persistence.
- Separate daily catch-up and historical backfill in status reports.
