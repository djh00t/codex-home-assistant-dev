---
name: ha-quality-gates
description: Use when validating Home Assistant changes with make check, BDD scenarios, pytest, dashboard/card validation, HA logs, Supervisor jobs, disk/memory checks, or post-deploy health gates.
---

# Home Assistant Quality Gates

Use local gates before deploy and live gates after deploy.

## Local Gates

1. Run `make check` unless the repo has a documented narrower gate for the change.
2. Confirm BDD `.feature` coverage for user-visible behavior.
3. Validate dashboard JSON and generated JavaScript card assets where present.
4. If using a tarball snapshot, handle `git diff --check` failures caused by missing `.git` as a validation-mode caveat.

## Live Gates

1. Run the repo's HA quality gate when available.
2. Check HA logs, Supervisor jobs, disk usage, memory, and deployed artifact state.
3. Baseline existing log warnings separately from new findings.
4. Re-poll after Core restart before treating active restart jobs as failures.

## Restart Warning Table

- `home_assistant_core_restart` only on first poll: pending restart, not enough evidence to call the deploy bad.
- Restart job still active after the configured polling window: investigate before handoff.
- Restart job plus new errors or resource pressure: treat as a likely deploy or host health problem.
- Warnings should not fail normal gates unless `--fail-on-warning` is explicitly used.

## UnderDog HA Example

```bash
python -m underdog_ha.ha_quality_gate --ssh-target root@172.30.55.10 --polls 2 --interval-seconds 30
rtk .venv/bin/python -m underdog_ha.ha_quality_gate --ssh-target root@172.30.55.10 --polls 2 --interval-seconds 30
```
