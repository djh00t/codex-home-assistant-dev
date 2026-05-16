#!/usr/bin/env python3
"""Check HACS and GitHub release readiness for a Home Assistant project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib


def _load_json(path: Path) -> tuple[dict[str, object] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as err:
        return None, str(err)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument(
        "--hacs-mode",
        choices=("custom", "default"),
        default="custom",
        help="HACS release target. Default repository submission has stricter checks.",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[str] = []
    warnings: list[str] = []
    project_version = _load_pyproject_version(root / "pyproject.toml")

    hacs, hacs_error = _load_json(root / "hacs.json")
    if hacs_error:
        findings.append(f"hacs.json is invalid JSON: {hacs_error}")
    elif hacs is None:
        warnings.append("hacs.json not found; HACS release checks are informational only.")

    manifests = sorted(root.glob("custom_components/*/manifest.json"))
    if not manifests:
        warnings.append("No custom_components/*/manifest.json files found.")
    for manifest_path in manifests:
        manifest, manifest_error = _load_json(manifest_path)
        label = str(manifest_path.relative_to(root))
        if manifest_error:
            findings.append(f"{label} is invalid JSON: {manifest_error}")
            continue
        if manifest is None:
            continue
        for key in ("domain", "documentation", "issue_tracker", "codeowners", "name", "version"):
            if key not in manifest:
                warnings.append(f"{label} is missing HACS integration metadata key `{key}`.")
        manifest_version = manifest.get("version")
        if project_version and manifest_version and manifest_version != project_version:
            warnings.append(
                f"{label} version `{manifest_version}` differs from pyproject.toml version `{project_version}`."
            )
        domain = manifest_path.parent.name
        runtime_files = [path for path in manifest_path.parent.rglob("*") if path.is_file()]
        if not runtime_files:
            warnings.append(f"{label} has no runtime files beside the manifest.")
        if _custom_component_references_repo_src(manifest_path.parent):
            warnings.append(
                f"{domain} appears to load runtime code from outside custom_components; HACS packages require runtime files inside the integration directory."
            )
        if args.hacs_mode == "default" and not _has_local_brand_evidence(root, domain):
            warnings.append(
                f"{domain} has no local brand evidence; HACS default repositories require Home Assistant brands."
            )

    if not (root / "CHANGELOG.md").exists():
        warnings.append("CHANGELOG.md not found; release notes must come from commits or PR body.")
    if not (root / "Makefile").exists():
        warnings.append("Makefile not found; document the release validation command explicitly.")

    print("# Home Assistant Release Readiness")
    print()
    if findings:
        print("## Blocking findings")
        for finding in findings:
            print(f"- {finding}")
    else:
        print("## Blocking findings")
        print("- None detected.")
    print()
    print("## Warnings")
    for warning in warnings:
        print(f"- {warning}")
    if not warnings:
        print("- None detected.")
    print()
    print("## Required evidence before release")
    print("- Local `make check` output.")
    print("- BDD scenario coverage for changed behavior.")
    print("- Restart/reload and cache-busting notes.")
    print("- GitHub PR/CI status.")
    print("- HACS/GitHub release notes and rollback notes.")
    print("- Tag naming, draft/prerelease choice, and release asset decision.")
    return 1 if findings else 0


def _load_pyproject_version(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return None
    project = payload.get("project")
    if isinstance(project, dict):
        version = project.get("version")
        if isinstance(version, str):
            return version
    return None


def _custom_component_references_repo_src(component_dir: Path) -> bool:
    for path in component_dir.glob("**/*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "sys.path" in text or "/repo/src" in text or "parents[" in text and "/src" in text:
            return True
    return False


def _has_local_brand_evidence(root: Path, domain: str) -> bool:
    candidates = (
        root / "brands" / domain,
        root / "custom_components" / domain / "icon.png",
        root / "custom_components" / domain / "logo.png",
    )
    return any(path.exists() for path in candidates)


if __name__ == "__main__":
    raise SystemExit(main())
