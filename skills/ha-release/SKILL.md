---
name: ha-release
description: Use when preparing GitHub or HACS releases for Home Assistant projects, including version checks, manifest and hacs metadata, changelog/release notes, tags, packaging, PRs, CI monitoring, and release rollback notes.
---

# Home Assistant Release

Optimize first for HACS plus GitHub releases. Add-on and image publishing are extension points.

## Workflow

1. Resolve the plugin root as the directory two levels above this `SKILL.md`.
2. Run release readiness:

```bash
python <plugin-root>/scripts/check_release_readiness.py .
```

3. Ensure local gates pass before tagging or publishing.
4. Choose HACS mode: custom repository or default repository submission.
5. Align version metadata across `manifest.json`, `pyproject.toml`, `hacs.json`, changelog, tags, and release notes where those files exist.
6. For HACS integration releases, check that runtime files live under `custom_components/<domain>/` and required manifest keys are present.
7. For HACS default repository submission, verify brand requirements and repository metadata before treating the release as ready.
8. Document restart/reload requirements and cache-busting notes in release notes.
9. Open a PR with test evidence, wait for CI, and handle review feedback.
10. After merge, prepare the live HA deploy handoff when a target instance exists.

## Release Notes Should Include

- Behavior changes.
- HA restart/reload requirements.
- HACS or install instructions.
- Known backfill/cache limitations.
- Rollback instructions.

## HACS Distinctions

- Custom repository: users add the repo manually; still validate structure, manifest metadata, and install instructions.
- Default repository submission: also check HACS inclusion rules, brand assets, repository metadata, and stricter review expectations.
