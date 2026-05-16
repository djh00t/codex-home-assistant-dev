---
name: ha-core-runtime
description: Use when a Home Assistant repo Python module must run inside the live Home Assistant Core Python environment on the remote host, especially when the SSH add-on shell cannot execute synced repo code directly.
---

# Home Assistant Core Runtime

Use this skill when local validation is not enough and a repo module must execute inside the Home Assistant Core container on the target host.

## Workflow

1. Resolve the plugin root as the directory two levels above this `SKILL.md`.
2. Confirm the repo has already been synced to the HA host path you plan to execute from.
3. Prefer explicit `--remote-repo` paths rather than assuming the default if the target host differs from UnderDog HA.
4. Run the module inside HA Core with:

```bash
python <plugin-root>/scripts/run_ha_core_module.py underdog_ha.ha_quality_gate --host root@172.30.55.10 --remote-repo /config/underdog_ha_shadow/repo -- --polls 2 --interval-seconds 30
```

5. If auto-detection misses the Core container, retry with `--container-name`.
6. Report stdout, stderr, exit status, and the exact remote repo path used.

## Guardrails

- Do not assume the SSH add-on shell can run Python from the synced repo.
- Do not use this skill as a substitute for syncing code first.
- Do not treat host-shell Python and HA Core Python as equivalent runtimes.
