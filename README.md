# Codex Home Assistant Dev

Codex plugin for developing, validating, deploying, packaging, and releasing Home Assistant projects.

The plugin ID is `home-assistant-dev`. It provides skills for:

- Home Assistant development loops
- Home Assistant Core runtime execution for repo Python modules
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

Clone the repository into a stable local path that you want Codex to load from, for example:

```bash
mkdir -p ./plugins
git clone https://github.com/djh00t/codex-home-assistant-dev.git \
  ./plugins/codex-home-assistant-dev
cd ./plugins/codex-home-assistant-dev
```

Install the plugin into the home-local marketplace layout that Codex expects by linking that checkout into the local plugin bundle directory:

```bash
mkdir -p ~/.agents/plugins/plugins
ln -s "$(pwd)" ~/.agents/plugins/plugins/home-assistant-dev
```

If the symlink already exists and points somewhere stale, replace it first:

```bash
rm -f ~/.agents/plugins/plugins/home-assistant-dev
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
