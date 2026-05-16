# Live Home Assistant Guardrails

Use this reference before any action that writes to a live Home Assistant instance.

## Default Policy

Live writes are plan-then-apply. Generate the exact backup, sync, reload/restart, cache-busting, and verification commands first. Apply them only after explicit user confirmation.

## Required Flow

1. Identify the target host, auth method, deploy paths, changed artifact types, and rollback path.
2. Run local validation first, normally `make check`.
3. Generate a backup command and require the resulting backup slug/id to be recorded before any write.
4. Sync only the needed paths.
5. Prefer targeted reloads when Home Assistant supports them; use Core restart when Python integration code or manifest metadata changes.
6. After restart, wait for Supervisor jobs to clear before judging health.
7. Run HA quality gates and report baseline log issues separately from new findings.
8. Verify the deployed tree or live artifact, not just the local checkout.

## Restart Warning Interpretation

- Restart job only on first poll: pending restart, wait and re-poll.
- Restart job persists after the planned polling window: investigate Supervisor jobs and Core logs.
- Restart job plus new errors, high memory, disk pressure, or failed commands: likely bad deploy or unhealthy host.
- Warnings normally remain warnings unless the gate is run with `--fail-on-warning`.
- Use the repo's default polling window first; for UnderDog HA that is two polls with a 30 second interval.

## Do Not Do

- Do not write to `/config` before taking a backup.
- Do not treat an active `home_assistant_core_restart` job immediately after restart as a code failure without a re-poll.
- Do not confuse daily rolling collection with complete historical backfill.
- Do not claim a visual dashboard/card change landed until cache-busting and UI verification are complete.
- Do not use destructive git or HA cleanup commands as rollback unless the user explicitly asks.

## UnderDog HA Examples

- Live host: `root@172.30.55.10`
- Repo mirror: `/config/underdog_ha_shadow/repo`
- Custom component: `/config/custom_components/underdog_ha`
- AEMO actuals marker: `/config/underdog_ha_shadow/weather/aemo-rooftop-pv-actual.jsonl.maintenance.json`
- Known quality gate: `python -m underdog_ha.ha_quality_gate --ssh-target root@172.30.55.10 --polls 2 --interval-seconds 30`
- Repo-local variant used on this host: `rtk .venv/bin/python -m underdog_ha.ha_quality_gate --ssh-target root@172.30.55.10 --polls 2 --interval-seconds 30`
