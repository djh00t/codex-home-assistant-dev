---
name: ha-dev-cycle
description: Use when developing or modifying Home Assistant projects, including custom integrations, Lovelace dashboards, custom cards, packages, automations, blueprints, add-ons, tests, BDD coverage, local checks, and fast edit-test-deploy loops.
---

# Home Assistant Development Cycle

Start with repo classification, then keep the loop short and evidence-backed.

## Workflow

1. Resolve the plugin root as the directory two levels above this `SKILL.md`.
2. Inspect the repo shape with `<plugin-root>/scripts/classify_ha_repo.py` when useful.
3. Identify changed artifact types: integration, dashboard/card, package/automation/blueprint, add-on/image, release metadata, or docs.
4. Prefer the repo's existing Makefile and tests. Run `make check` as the default local gate.
5. Add or update BDD `.feature` coverage for user-visible or behavior-changing features.
6. Keep local changes scoped and reversible, especially in dirty worktrees.
7. For UI/dashboard/card work, plan cache busting and browser/HA UI verification before claiming the user will see the change.
8. If a repo module must run inside the Home Assistant Core runtime, use:

```bash
python <plugin-root>/scripts/run_ha_core_module.py underdog_ha.ha_quality_gate --host root@172.30.55.10 -- --polls 2 --interval-seconds 30
```

9. For live deploy, switch to `ha-live-deploy`; do not write to HA from this skill alone.

## Integration Review Checks

- For sensors, define key/name, source value, unit, icon, device class, state class, precision, and attributes before coding.
- Preserve unique IDs unless the migration is explicit.
- Keep recorder attributes small, stable, and free of secrets.
- Update docs and dashboards when a new operator-facing entity appears.

## References

- Read `../../references/artifact-types.md` when choosing validation by artifact type.
- Read `../../references/model-routing.md` when decomposing across agents/models.
- Read `../../references/lessons-underdog-ha.md` for UnderDog HA operational lessons.

## Useful Commands

```bash
python <plugin-root>/scripts/classify_ha_repo.py .
make check
python <plugin-root>/scripts/run_ha_core_module.py underdog_ha.ha_quality_gate --host root@172.30.55.10 -- --polls 2 --interval-seconds 30
```
