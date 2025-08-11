import json
import os
from pathlib import Path


def load_rows_from_json(path: Path) -> list:
    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception:
        return []

    # Normalize to a list of dict rows
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        for key in ("colleges", "data", "items", "rows"):
            if key in data and isinstance(data[key], list):
                return [r for r in data[key] if isinstance(r, dict)]
    return []


def extract_name(row: dict) -> str:
    # Prefer 'college', fallback to 'name'
    name = (row.get("college") or row.get("name") or "").strip()
    # Normalize spacing/case
    return name


def main() -> None:
    data_dir = Path("data")
    if not data_dir.exists():
        print("data directory not found")
        return

    files = sorted(p for p in data_dir.glob("*.json"))
    overall_names: set[str] = set()
    per_file: list[tuple[str, int, int]] = []  # (filename, rows, unique_names)

    for path in files:
        rows = load_rows_from_json(path)
        names = {extract_name(r) for r in rows}
        names.discard("")
        per_file.append((path.name, len(rows), len(names)))
        # Use lowercase for overall uniqueness
        overall_names.update(n.lower() for n in names)

    print("Per file (rows, unique_colleges):")
    for name, rows, uniq in per_file:
        print(f"- {name}: rows={rows}, unique_colleges={uniq}")

    print(f"\nTotal unique colleges across all data/*.json: {len(overall_names)}")


if __name__ == "__main__":
    main()


