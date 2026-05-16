# Codex Home Assistant Dev

Codex plugin for developing, validating, deploying, packaging, and releasing Home Assistant projects.

The plugin ID is `home-assistant-dev`. It provides skills for:

- Home Assistant development loops
- backup-first live deploy planning
- Lovelace and frontend cache busting
- local and live quality gates
- HACS and GitHub release readiness
- reviewable self-improvement of HA runbooks

## Repository Layout

- `.codex-plugin/plugin.json` - plugin manifest
- `skills/` - Codex skills
- `references/` - skill support references
- `scripts/` - deterministic helper scripts

## Validation

```bash
make check
make quality-gates
```
