#!/usr/bin/env python3
"""Classify Home Assistant project artifacts in a repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def classify_repo(root: Path) -> dict[str, Any]:
    root = root.resolve()
    custom_components = sorted(
        path.parent.name
        for path in root.glob("custom_components/*/manifest.json")
        if path.is_file()
    )
    dashboard_files = sorted({
        str(path.relative_to(root))
        for pattern in (
            "examples/homeassistant/*.json",
            "**/lovelace*.yaml",
            "**/dashboard*.json",
        )
        for path in root.glob(pattern)
        if path.is_file()
    })
    card_files = sorted({
        str(path.relative_to(root))
        for path in root.glob("**/*.js")
        if "card" in path.name.lower() and ".venv" not in path.parts
    })
    package_files = sorted({
        str(path.relative_to(root))
        for pattern in (
            "packages/**/*.yaml",
            "automations.yaml",
            "scripts.yaml",
            "scenes.yaml",
            "blueprints/**/*.yaml",
        )
        for path in root.glob(pattern)
        if path.is_file()
    })
    addon_files = sorted({
        str(path.relative_to(root))
        for pattern in ("**/config.yaml", "**/build.yaml", "**/Dockerfile")
        for path in root.glob(pattern)
        if path.is_file() and ".venv" not in path.parts
    })
    release_files = [
        str(path.relative_to(root))
        for path in (root / "hacs.json", root / "CHANGELOG.md", root / "custom_components")
        if path.exists()
    ]
    checks = {
        "make_check": (root / "Makefile").exists(),
        "bdd_features": (root / "features").exists()
        and any((root / "features").glob("**/*.feature")),
        "pytest": (root / "tests").exists(),
    }
    return {
        "root": str(root),
        "custom_integrations": custom_components,
        "dashboards": dashboard_files,
        "custom_cards": card_files,
        "packages_automations_blueprints": package_files,
        "addons_or_images": addon_files,
        "release_metadata": release_files,
        "checks": checks,
        "recommended_local_gate": (
            "make check"
            if checks["make_check"]
            else "pytest -q"
            if checks["pytest"]
            else "manual validation required"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to inspect.")
    args = parser.parse_args()
    print(json.dumps(classify_repo(Path(args.root)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
