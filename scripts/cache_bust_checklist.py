#!/usr/bin/env python3
"""Generate a Home Assistant frontend cache-busting checklist."""

from __future__ import annotations

import argparse
from pathlib import Path


def find_frontend_artifacts(root: Path) -> list[str]:
    root = root.resolve()
    patterns = (
        "examples/homeassistant/*.json",
        "**/lovelace*.yaml",
        "**/*.js",
        "**/www/**/*",
        "**/*.html",
    )
    artifacts: list[str] = []
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file() and ".venv" not in path.parts and ".git" not in path.parts:
                artifacts.append(str(path.relative_to(root)))
    return sorted(set(artifacts))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    args = parser.parse_args()
    root = Path(args.root)
    artifacts = find_frontend_artifacts(root)
    print("# Home Assistant Cache-Busting Checklist")
    print()
    print("- Identify whether changed frontend resources are dashboard storage, custom card JS, `/www` assets, report HTML, or images.")
    print("- Version custom card resource URLs or filenames when practical.")
    print("- Sync generated JS/assets and Lovelace storage/dashboard references together.")
    print("- Reload Lovelace/resources or restart Core according to artifact type.")
    print("- Hard-refresh the HA browser session or verify with browser automation.")
    print("- If the user said they cannot see a difference, inspect the first-screen UI and active resource URL.")
    print()
    print("## Artifact action map")
    print("- Dashboard JSON or `.storage/lovelace.*`: sync payloads and reload Lovelace or restart Core.")
    print("- Custom card JS: version the resource URL or filename, sync the JS, reload resources, hard-refresh browser.")
    print("- `/www` assets, HTML, images, CSS: sync assets and verify with a no-cache browser request.")
    print("- HACS frontend assets: check HACS, HA frontend, and browser cache layers.")
    print()
    print("## Browser verification")
    print("- Confirm the loaded URL includes the expected cache key or filename.")
    print("- Confirm the browser fetched the new asset rather than using a stale cache entry.")
    print("- Inspect the first viewport when the user reports no visible difference.")
    print()
    print("## Candidate frontend artifacts")
    for artifact in artifacts:
        print(f"- {artifact}")
    if not artifacts:
        print("- No obvious frontend artifacts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
