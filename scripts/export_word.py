"""Build and check a Word file through the vendored thai-docx runtime."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_RUNTIME = ROOT / "vendor" / "thai-docx-upstream" / "scripts" / "thai_docx"
JS_RUNTIME = ROOT / "vendor" / "thai-docx-upstream" / "scripts" / "thai_docx.js"


def runtime_command():
    if PY_RUNTIME.is_dir() and sys.version_info >= (3, 11):
        return [sys.executable, str(PY_RUNTIME)]
    node = shutil.which("node")
    if JS_RUNTIME.is_file() and node:
        return [node, str(JS_RUNTIME)]
    raise RuntimeError("No compatible vendored thai-docx runtime is available.")


def run(*args):
    return subprocess.run(runtime_command() + list(map(str, args)), capture_output=True, text=True, encoding="utf-8")


def json_line(output):
    for line in reversed(output.splitlines()):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("source", type=Path)
    build.add_argument("output", type=Path)
    build.add_argument("flags", nargs=argparse.REMAINDER)
    check = sub.add_parser("check")
    check.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        runtime_command()
    except RuntimeError as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    if args.command == "build":
        result = run("build", args.source, args.output, *args.flags)
    else:
        result = run("check", args.document)
    payload = json_line(result.stdout)
    if payload is None:
        payload = {"ok": False, "error": result.stderr.strip() or "thai-docx returned no JSON result."}
    print(json.dumps({"exit_code": result.returncode, "result": payload}, ensure_ascii=False, indent=2))
    if result.stderr.strip():
        print(result.stderr, file=sys.stderr, end="")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
