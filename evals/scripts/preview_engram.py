#!/usr/bin/env python3
"""Render a disabled project-only Engram MCP preview without writing or running it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "qualifications" / "engram-v0.11.0" / "profile.json"


def absolute_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path")
    return path


def build_preview(project: Path, binary: Path) -> dict[str, object]:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    database = project / ".engram" / "graph.db"
    configuration_path = project / ".bob" / "mcp.json"
    server_name = profile["bob_trial_contract"]["server_name"]
    configuration = {
        "mcpServers": {
            server_name: {
                "command": str(binary),
                "args": ["mcp", "--db", str(database)],
                "cwd": str(project),
                "alwaysAllow": [],
                "disabled": True,
            }
        }
    }
    return {
        "qualification_id": profile["qualification_id"],
        "evidence_level": profile["evidence_level"],
        "configuration_path": str(configuration_path),
        "configuration": configuration,
        "first_tool_call": {
            "server": server_name,
            "tool": "brief",
            "arguments": {},
        },
        "writes_performed": False,
        "processes_started": False,
        "next_decision": "review paths and digest; a separate disposable runtime trial remains required",
    }


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="absolute disposable project path")
    parser.add_argument("--binary", required=True, help="absolute reviewed Engram binary path")
    return parser.parse_args(arguments)


def main(arguments: list[str] | None = None) -> int:
    options = parse_arguments(arguments)
    try:
        project = absolute_path(options.project, "project")
        binary = absolute_path(options.binary, "binary")
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(build_preview(project, binary), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
