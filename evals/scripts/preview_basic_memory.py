#!/usr/bin/env python3
"""Render a disabled, isolated Basic Memory MCP preview without writing or running it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "qualifications" / "basic-memory-v1.0.0" / "profile.json"


def absolute_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path")
    return path


def build_preview(project: Path, uvx: Path, wheel: Path) -> dict[str, object]:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    state = project / ".basic-memory-state"
    project_name = "project-alpha"
    server_name = profile["bob_trial_contract"]["server_name"]
    def project_value(value: str) -> str:
        prefix = "<project>/"
        if value.startswith(prefix):
            return str(project / value.removeprefix(prefix))
        return value.replace("<project>", str(project))

    environment = {
        key: project_value(value)
        for key, value in profile["bob_trial_contract"]["environment"].items()
    }
    basic_memory_config = {
        "projects": {project_name: {"path": str(project), "mode": "local"}},
        "default_project": None,
        "project_root": str(project.parent),
        "database_backend": "sqlite",
        "default_search_type": "text",
        "logfire_enabled": False,
        "logfire_send_to_logfire": False,
        "enable_project_delete": False,
        "auto_update": False,
        "cloud_promo_opt_out": True,
    }
    bob_configuration = {
        "mcpServers": {
            server_name: {
                "command": str(uvx),
                "args": ["--from", str(wheel), "basic-memory", "mcp", "--project", project_name],
                "cwd": str(project),
                "env": environment,
                "alwaysAllow": [],
                "disabled": True,
            }
        }
    }
    return {
        "qualification_id": profile["qualification_id"],
        "evidence_level": profile["evidence_level"],
        "configuration_path": str(project / ".bob" / "mcp.json"),
        "configuration": bob_configuration,
        "basic_memory_config_path": str(state / "config.json"),
        "basic_memory_config": basic_memory_config,
        "first_tool_call": {
            "server": server_name,
            "tool": "bm_project",
            "arguments": {"command": "list"},
        },
        "writes_performed": False,
        "processes_started": False,
        "next_decision": "verify the wheel and review both files; a separate disposable runtime trial remains required",
    }


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="absolute disposable project path")
    parser.add_argument("--uvx", required=True, help="absolute reviewed uvx executable path")
    parser.add_argument("--wheel", required=True, help="absolute reviewed Basic Memory wheel path")
    return parser.parse_args(arguments)


def main(arguments: list[str] | None = None) -> int:
    options = parse_arguments(arguments)
    try:
        project = absolute_path(options.project, "project")
        uvx = absolute_path(options.uvx, "uvx")
        wheel = absolute_path(options.wheel, "wheel")
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(build_preview(project, uvx, wheel), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
