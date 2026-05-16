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

## Install

### Home-local install

Install the plugin into the home-local marketplace layout that Codex expects:

```bash
mkdir -p ~/.agents/plugins/plugins
ln -s "$(pwd)" ~/.agents/plugins/plugins/home-assistant-dev
```

Create or update `~/.agents/plugins/marketplace.json` so the plugin entry points at the canonical relative path:

```json
{
  "name": "local",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "home-assistant-dev",
      "source": {
        "source": "local",
        "path": "./plugins/home-assistant-dev"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Then fully restart Codex and open `Marketplace`. The plugin should appear under `Local Plugins` as `Home Assistant Dev`.

If the marketplace entry points anywhere else, for example `./home-assistant-dev`, Codex may list the plugin but fail to load its details or install it.

## Validation

```bash
make check
make quality-gates
```
