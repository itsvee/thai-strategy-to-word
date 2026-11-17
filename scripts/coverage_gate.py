"""Validate assignment and feedback coverage without judging prose quality."""
import argparse
import json
from pathlib import Path

VALID_STATUSES = {"covered", "partial", "blocked", "not_applicable"}
REQUIRED_FIELDS = ("id", "requirement", "report_location", "answer", "status")


def meaningful(value):
    return isinstance(value, str) and bool(value.strip())


def evaluate(coverage):
    if not isinstance(coverage, dict):
        raise ValueError("Coverage must be a JSON object.")
    items = coverage.get("items")
    if not isinstance(items, list):
        raise ValueError("items must be a list.")
    blockers = []
    seen = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"items[{index}] must be an object.")
        missing = [key for key in REQUIRED_FIELDS if key not in item]
        if missing:
            raise ValueError(f"items[{index}] is missing: {', '.join(missing)}")
        item_id = item["id"]
        if not meaningful(item_id):
            raise ValueError(f"items[{index}].id must be non-empty.")
        if item_id in seen:
            raise ValueError(f"Duplicate coverage id: {item_id}")
        seen.add(item_id)
        status = item["status"]
        if status not in VALID_STATUSES:
            raise ValueError(f"items[{index}].status is invalid.")
        required = item.get("required", True)
        if type(required) is not bool:
            raise ValueError(f"items[{index}].required must be boolean.")
        if required and status == "covered":
            for key in ("requirement", "report_location", "answer"):
                if not meaningful(item[key]):
                    blockers.append({"id": item_id, "reason": f"Covered item needs {key}."})
            if not isinstance(item.get("evidence_ids", []), list):
                raise ValueError(f"items[{index}].evidence_ids must be a list.")
            if not item.get("evidence_ids") and not meaningful(item.get("limitation")):
                blockers.append({"id": item_id, "reason": "Covered item needs evidence_ids or a stated limitation."})
        elif required and status in {"partial", "blocked"}:
            blockers.append({"id": item_id, "reason": f"Required item is {status}."})
        elif required and status == "not_applicable":
            if not meaningful(item.get("limitation")):
                blockers.append({"id": item_id, "reason": "Not-applicable item needs a reason."})
    if not items:
        blockers.append({"field": "items", "reason": "At least one assignment requirement is required."})
    status = "ready" if not blockers else "blocked"
    return {"ok": True, "status": status, "count": len(items), "blockers": blockers}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("coverage", type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.coverage.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
