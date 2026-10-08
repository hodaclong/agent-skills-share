#!/usr/bin/env python3
"""Validate the small, source-grounded knowledge-pack contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = (
    "manifest.json",
    "sources.jsonl",
    "claims.jsonl",
    "entities.jsonl",
    "relations.jsonl",
    "chatbot.jsonl",
    "content-map.jsonl",
    "quality.json",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{line_no} is not a JSON object")
        rows.append(value)
    return rows


def validate(pack_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    counts: dict[str, int] = {}
    ids: dict[str, set[str]] = {}

    if not pack_dir.is_dir():
        return {"ok": False, "errors": [f"pack directory not found: {pack_dir}"]}

    for filename in REQUIRED_FILES:
        if not (pack_dir / filename).is_file():
            errors.append(f"missing required file: {filename}")

    manifest: dict[str, Any] = {}
    if (pack_dir / "manifest.json").is_file():
        try:
            manifest = read_json(pack_dir / "manifest.json")
            if not isinstance(manifest, dict):
                errors.append("manifest.json is not an object")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"manifest.json: {exc}")

    for filename in REQUIRED_FILES:
        path = pack_dir / filename
        if not path.is_file() or filename in {"manifest.json", "quality.json"}:
            continue
        try:
            rows = read_jsonl(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{filename}: {exc}")
            continue
        key = path.stem
        counts[key] = len(rows)
        id_values = []
        for row in rows:
            record_id = next((row.get(field) for field in row if field.endswith("_id")), None)
            if not isinstance(record_id, str) or not record_id:
                errors.append(f"{filename}: record has no *_id")
                continue
            id_values.append(record_id)
        ids[key] = set(id_values)
        if len(id_values) != len(set(id_values)):
            errors.append(f"{filename}: duplicate record ID")

    for filename in ("manifest.json", "quality.json"):
        path = pack_dir / filename
        if path.is_file():
            try:
                value = read_json(path)
                if not isinstance(value, dict):
                    errors.append(f"{filename} is not an object")
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{filename}: {exc}")

    if manifest:
        for field in ("dataset_id", "schema_version", "entrypoints"):
            if field not in manifest:
                errors.append(f"manifest.json missing {field}")
        declared = manifest.get("counts")
        if isinstance(declared, dict):
            for key, count in counts.items():
                if key in declared and declared[key] != count:
                    errors.append(f"manifest count mismatch for {key}: {declared[key]} != {count}")

    source_ids = ids.get("sources", set())
    for filename in ("claims.jsonl", "entities.jsonl", "relations.jsonl", "chatbot.jsonl", "content-map.jsonl"):
        path = pack_dir / filename
        if not path.is_file():
            continue
        try:
            rows = read_jsonl(path)
        except Exception:
            continue
        for row_number, row in enumerate(rows, 1):
            for ref in row.get("source_refs", []):
                if isinstance(ref, dict) and ref.get("source_id") not in source_ids:
                    errors.append(f"{filename}:{row_number} references unknown source_id")

    return {"ok": not errors, "errors": errors, "counts": counts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack_dir", type=Path)
    args = parser.parse_args()
    result = validate(args.pack_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
