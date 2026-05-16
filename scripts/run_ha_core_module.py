#!/usr/bin/env python3
"""Run a repo Python module inside the Home Assistant Core container."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path


REMOTE_SCRIPT = textwrap.dedent(
    """
    set -eu

    container_name="${CONTAINER_NAME:-}"
    remote_repo="${REMOTE_REPO:?REMOTE_REPO is required}"
    python_bin="${PYTHON_BIN:-python3}"
    module_name="${MODULE_NAME:?MODULE_NAME is required}"

    if [ -z "$container_name" ] && command -v docker >/dev/null 2>&1; then
      container_name="$(
        docker ps \
          --filter label=io.hass.type=core \
          --format '{{.Names}}' \
          | head -n 1
      )"
    fi

    if [ -z "$container_name" ] && command -v docker >/dev/null 2>&1; then
      for candidate in homeassistant home-assistant; do
        if docker ps --format '{{.Names}}' | grep -Fx "$candidate" >/dev/null 2>&1; then
          container_name="$candidate"
          break
        fi
      done
    fi

    if [ -z "$container_name" ]; then
      echo "Could not detect the Home Assistant Core container. Set --container-name explicitly." >&2
      exit 1
    fi

    exec docker exec \
      -w "$remote_repo" \
      "$container_name" \
      "$python_bin" \
      -m "$module_name" \
      "$@"
    """
).strip()


def build_remote_command(
    *,
    host: str,
    remote_repo: str,
    module_name: str,
    module_args: list[str],
    python_bin: str,
    container_name: str | None,
) -> list[str]:
    command = [
        "ssh",
        host,
        "env",
        f"REMOTE_REPO={remote_repo}",
        f"PYTHON_BIN={python_bin}",
        f"MODULE_NAME={module_name}",
    ]
    if container_name:
        command.append(f"CONTAINER_NAME={container_name}")
    command.extend(["sh", "-s", "--", *module_args])
    return command


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", help="Python module to run with `python -m` inside HA Core.")
    parser.add_argument("--host", default="root@172.30.55.10", help="SSH target for Home Assistant.")
    parser.add_argument(
        "--remote-repo",
        default="/config/underdog_ha_shadow/repo",
        help="Repo path on the HA host that is mounted inside the Core container.",
    )
    parser.add_argument(
        "--python-bin",
        default="python3",
        help="Python binary inside the Home Assistant Core container.",
    )
    parser.add_argument(
        "--container-name",
        default=None,
        help="Explicit Home Assistant Core container name. Auto-detect by default.",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the SSH command that would run instead of executing it.",
    )
    args, module_args = parser.parse_known_args()
    args.module_args = module_args
    return args


def main() -> int:
    args = _parse_args()
    module_args = list(args.module_args)
    if module_args and module_args[0] == "--":
        module_args = module_args[1:]

    command = build_remote_command(
        host=args.host,
        remote_repo=args.remote_repo,
        module_name=args.module,
        module_args=module_args,
        python_bin=args.python_bin,
        container_name=args.container_name,
    )

    if args.print_command:
        print(" ".join(shlex.quote(part) for part in command))
        print("# remote script")
        print(REMOTE_SCRIPT)
        return 0

    completed = subprocess.run(command, input=REMOTE_SCRIPT, text=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
