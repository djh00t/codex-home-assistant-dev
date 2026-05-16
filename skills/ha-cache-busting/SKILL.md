---
name: ha-cache-busting
description: Use when Home Assistant Lovelace dashboards, custom cards, frontend resources, static assets, browser-visible reports, or generated JavaScript changed and the user needs the live UI to show the update reliably.
---

# Home Assistant Cache Busting

Use this skill for UI changes where the code may deploy but the browser still shows old assets.

## Workflow

1. Resolve the plugin root as the directory two levels above this `SKILL.md`.
2. Identify changed frontend artifacts: Lovelace storage, dashboard JSON, custom card JS, `www/` assets, report HTML/JSON, images, or CSS.
3. Generate a checklist:

```bash
python <plugin-root>/scripts/cache_bust_checklist.py .
```

4. Version custom card resource URLs or filenames when practical.
5. Sync dashboard/card assets and Lovelace storage payloads together when they depend on each other.
6. Reload Lovelace/resources or restart Core according to the changed artifact type.
7. Verify through HA UI or browser automation when the user-visible shell changed.

## Artifact Action Map

- Dashboard JSON or `.storage/lovelace.*`: sync storage/dashboard payload and reload Lovelace or restart Core when storage reload is unavailable.
- Custom card JavaScript: change the resource URL query string or filename, sync the JS, reload Lovelace resources, then hard-refresh the browser.
- `/www` assets, report HTML, images, or CSS: sync assets and verify with a no-cache browser request.
- HACS-installed frontend assets: confirm whether HACS, HA frontend, and the browser each have a cached copy before declaring the update live.

## Browser Verification

- Confirm the active resource URL includes the expected version/cache key.
- Check the browser fetched the new JS/HTML asset with no stale cache hit.
- Inspect the first viewport when the user says the UI does not look different.

## Do Not Do

- Do not claim a visual update is live based only on tests.
- Do not change cache keys without syncing the generated asset that key references.
- Do not ignore first-screen hierarchy complaints; treat "I don't see any difference" as a UI delivery failure.
