#!/usr/bin/env python3
"""Validate catalogue metadata and inline local Markdown links, without network I/O."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"specifications", "learning", "skills", "distribution", "onboarding", "debugging", "orchestration", "evaluation"}
ENTRY_FIELDS = {"id", "name", "category", "repository", "summary", "publisher_type", "license", "license_evidence", "availability", "installation", "bob_relation", "review_status", "reviewed_on", "runtime_evidence", "notes", "sources"}
REPORT_FIELDS = {"date", "bob_version", "surface", "platform", "source_revision", "task", "result", "evidence_url"}


def is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_date(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def is_url(value: object) -> bool:
    if not is_text(value) or any(ch.isspace() or ord(ch) < 32 for ch in value):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme == "https" and bool(parts.hostname) and "." in parts.hostname and not parts.username and not parts.password
    except ValueError:
        return False


def validate_catalog(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or set(data) != {"schema_version", "reviewed_on", "review_timezone", "entries"}:
        return ["catalogue: unexpected or missing top-level fields"]
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        errors.append("catalogue: schema_version must be 1")
    if not is_date(data["reviewed_on"]) or not is_text(data["review_timezone"]):
        errors.append("catalogue: invalid review date or timezone")
    entries = data["entries"]
    if not isinstance(entries, list) or not entries:
        return errors + ["catalogue: entries must be a nonempty list"]
    seen_ids: set[str] = set()
    seen_repositories: set[str] = set()
    for number, entry in enumerate(entries, 1):
        where = f"entry {number}"
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            errors.append(f"{where}: unexpected or missing fields")
            continue
        text_fields = ENTRY_FIELDS - {"runtime_evidence", "notes", "sources"}
        if any(not is_text(entry[key]) for key in text_fields):
            errors.append(f"{where}: text fields must contain nonempty strings")
            continue
        where = entry["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
            errors.append(f"{where}: invalid ID")
        if entry["id"] in seen_ids or entry["repository"].rstrip("/") in seen_repositories:
            errors.append(f"{where}: duplicate ID or repository")
        seen_ids.add(entry["id"])
        seen_repositories.add(entry["repository"].rstrip("/"))
        enums = {
            "category": CATEGORIES,
            "publisher_type": {"organization", "community"},
            "availability": {"public-source"},
            "installation": {"documented", "not-assessed"},
            "bob_relation": {"explicit-integration", "bob-example", "bob-extension"},
            "review_status": {"documentation-reviewed", "runtime-report-linked"},
        }
        for field, allowed in enums.items():
            if entry[field] not in allowed:
                errors.append(f"{where}: invalid {field}")
        if not is_date(entry["reviewed_on"]):
            errors.append(f"{where}: invalid review date")
        elif is_date(data["reviewed_on"]) and entry["reviewed_on"] > data["reviewed_on"]:
            errors.append(f"{where}: entry review is newer than catalogue review")
        if len(entry["summary"]) > 300:
            errors.append(f"{where}: summary exceeds 300 characters")
        if not is_url(entry["repository"]) or not is_url(entry["license_evidence"]):
            errors.append(f"{where}: repository and license evidence must be public HTTPS URLs without credentials")
        if not isinstance(entry["notes"], list) or any(not is_text(note) for note in entry["notes"]):
            errors.append(f"{where}: notes must be a list of nonempty strings")
        sources = entry["sources"]
        source_urls: set[str] = set()
        if not isinstance(sources, list) or not sources:
            errors.append(f"{where}: at least one primary source is required")
        else:
            for source in sources:
                if not isinstance(source, dict) or set(source) != {"url", "supports"} or not is_url(source["url"]) or not is_text(source["supports"]):
                    errors.append(f"{where}: invalid source record")
                else:
                    source_urls.add(source["url"])
        if not {entry["repository"], entry["license_evidence"]}.issubset(source_urls):
            errors.append(f"{where}: sources must include repository and license evidence")
        reports = entry["runtime_evidence"]
        if not isinstance(reports, list):
            errors.append(f"{where}: runtime_evidence must be a list")
            continue
        if bool(reports) != (entry["review_status"] == "runtime-report-linked"):
            errors.append(f"{where}: review status contradicts runtime evidence")
        for report in reports:
            if not isinstance(report, dict) or set(report) != REPORT_FIELDS or any(not is_text(value) for value in report.values()):
                errors.append(f"{where}: incomplete runtime report")
                continue
            if not is_date(report["date"]) or not is_url(report["evidence_url"]) or report["result"] not in {"passed", "partial", "failed"}:
                errors.append(f"{where}: invalid runtime date, URL, or result")
            if report["bob_version"].lower() in {"latest", "current", "unknown"} or report["source_revision"].lower() in {"main", "master", "head", "latest", "unknown"}:
                errors.append(f"{where}: runtime report needs an exact version and source revision")
    return errors


def headings(text: str) -> set[str]:
    result: set[str] = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if not match:
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", match[1])
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        suffix = counts.get(slug, 0)
        counts[slug] = suffix + 1
        result.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return result


def validate_markdown(root: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    local_links = 0
    documents = 0
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.relative_to(root).parts):
            continue
        documents += 1
        text = re.sub(r"(?ms)^```.*?^```\s*$", "", path.read_text(encoding="utf-8"))
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", text):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            local_links += 1
            resolved = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            label = str(path.relative_to(root))
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f"{label}: missing or out-of-repository local target {target}")
            elif parts.fragment:
                if not resolved.is_file() or resolved.suffix != ".md" or unquote(parts.fragment) not in headings(resolved.read_text(encoding="utf-8")):
                    errors.append(f"{label}: missing local heading {target}")
    return errors, documents, local_links


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    try:
        data = json.loads((ROOT / "catalog/projects.json").read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
        errors = validate_catalog(data)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        if not errors:
            for entry in data["entries"]:
                if entry["repository"] not in readme:
                    errors.append(f"{entry['id']}: repository is absent from README")
        link_errors, documents, local_links = validate_markdown(ROOT)
        errors.extend(link_errors)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(data['entries'])} project entries, {documents} Markdown files, and {local_links} local links.")
    print("External sources and Bob runtime behavior were not tested by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
