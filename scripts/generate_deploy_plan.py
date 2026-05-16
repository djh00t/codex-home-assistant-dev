#!/usr/bin/env python3
"""Generate a backup-first Home Assistant deploy plan."""

from __future__ import annotations

import argparse
from pathlib import Path

from classify_ha_repo import classify_repo


def _component_domains(root: Path) -> list[str]:
    return classify_repo(root).get("custom_integrations", [])


def build_plan(root: Path, host: str, remote_repo: str, remote_custom_components: str) -> str:
    root = root.resolve()
    domains = _component_domains(root)
    lines = [
        "# Home Assistant Deploy Plan",
        "",
        "Live writes are plan-then-apply. Do not run these commands until the user approves.",
        "",
        "## 1. Local validation",
        "",
        "```bash",
        "make check",
        "```",
        "",
        "## 2. Backup",
        "",
        "```bash",
        f"ssh {host} 'ha backups new --name codex-pre-deploy-$(date +%Y%m%d-%H%M%S)'",
        "```",
        "",
        "Record the backup slug/id before syncing files.",
        "",
        "## 3. Sync",
        "",
        "```bash",
        f"rsync -az --delete --exclude .git --exclude .venv --exclude __pycache__ {root}/ {host}:{remote_repo}/",
    ]
    for domain in domains:
        lines.append(
            f"rsync -az --delete {root}/custom_components/{domain}/ {host}:{remote_custom_components}/{domain}/"
        )
    lines.extend(
        [
            "```",
            "",
            "## 4. Reload or restart",
            "",
            "Use targeted reloads for YAML-only automation/script/scene changes. Restart Core for Python integration or manifest changes.",
            "",
            "```bash",
            f"ssh {host} 'ha core restart'",
            "```",
            "",
            "## 5. Post-restart verification",
            "",
            "Wait for active Supervisor restart jobs to clear, then run the HA quality gate.",
            "",
            "```bash",
            f"ssh {host} 'ha jobs info --raw-json'",
            f"python -m underdog_ha.ha_quality_gate --ssh-target {host} --polls 2 --interval-seconds 30",
            "```",
            "",
            "## 6. Cache and UI verification",
            "",
            "Run the cache-busting checklist for dashboard/card changes and verify the live UI when visual behavior changed.",
            "",
            "## 7. Rollback",
            "",
            "Restore from the recorded backup or sync the previous known-good tree. Do not run destructive cleanup commands without explicit approval.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument("--host", default="root@172.30.55.10", help="SSH target for Home Assistant.")
    parser.add_argument("--remote-repo", default="/config/underdog_ha_shadow/repo")
    parser.add_argument("--remote-custom-components", default="/config/custom_components")
    args = parser.parse_args()
    print(build_plan(Path(args.root), args.host, args.remote_repo, args.remote_custom_components))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
