# Home Assistant Artifact Types

Use this reference when classifying a Home Assistant repository or choosing validation for a change.

## Custom Integrations

Signals:
- `custom_components/<domain>/manifest.json`
- `__init__.py`, `sensor.py`, `config_flow.py`, `coordinator.py`, `const.py`
- tests that import Home Assistant integration modules

Expected validation:
- Run the repo's `make check` first.
- Add or update BDD scenarios for user-visible behavior.
- Run focused pytest slices for the changed integration modules.
- For live deploy, sync the custom component path and restart or reload the affected integration only when supported.

Sensor-specific review:
- Keep unique IDs stable; changing them affects entity registry continuity.
- Confirm device class, state class, native unit, precision, and long-term-statistics eligibility are valid for the value.
- Keep attributes recorder-safe: avoid large nested payloads, secrets, and fast-changing noisy details.
- Check entity naming, icons, and dashboard/docs visibility for operator-facing sensors.

## Lovelace Dashboards, Storage, and Custom Cards

Signals:
- `examples/homeassistant/*.json`
- `.storage/lovelace.*` payload helpers
- generated JavaScript card assets
- dashboard/card validation commands in `Makefile`

Expected validation:
- Validate JSON storage envelopes and dashboard examples.
- Run `node --check` on generated card assets.
- Bust frontend/card caches after deploy with versioned resource URLs or changed filenames.
- Verify with browser or HA UI when a visual change is expected.

## Packages, Automations, Scripts, Scenes, and Blueprints

Signals:
- `packages/`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`, `blueprints/`
- YAML entity references, services, triggers, and selectors

Expected validation:
- Run local YAML parsing when available.
- Generate a HA config check command for the live host before restart.
- Prefer reloadable domains over full Core restart when the change is limited to automations/scripts/scenes.

## Add-ons and Container Images

Signals:
- `config.yaml`, `build.yaml`, `Dockerfile`, add-on repository layout, image publish workflows

Expected validation:
- Build locally when practical.
- Validate add-on metadata.
- Keep image tag, release notes, and GitHub/HACS metadata aligned.

## HACS and GitHub Releases

Signals:
- `hacs.json`, `manifest.json`, GitHub releases, tags, changelog entries

Expected validation:
- Ensure manifest version and tag match where the project uses versioned integration metadata.
- For HACS integrations, keep required runtime files inside `custom_components/<integration>/`.
- Check HACS-required manifest keys for integration repositories: `domain`, `documentation`, `issue_tracker`, `codeowners`, `name`, and `version`.
- Confirm release notes call out HA restart/reload needs.
- Confirm packaging excludes local caches, virtualenvs, and generated runtime data.
