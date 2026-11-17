"""Build the report output bundle and optionally a checked DOCX."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import build_html


def validate_coverage(path):
    if not path:
        return
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "coverage_gate.py"), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    print(result.stdout, end="")
    if result.returncode:
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        raise SystemExit(result.returncode)


def write_registry(path, title, payload):
    path.write_text(build_html.registry_html(title, payload), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", default="รายงาน")
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--feedback", type=Path)
    parser.add_argument("--word", action="store_true")
    parser.add_argument("--word-name", default="report.docx")
    args = parser.parse_args()
    validate_coverage(args.coverage)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    html_path = args.output_dir / "report.html"
    build_html.main_from_values(args.source, html_path, args.title)
    manifest = {
        "source_report": str(args.source),
        "outputs": {"html": str(html_path), "coverage_html": None, "evidence_html": None, "feedback_html": None, "word": None},
        "word_requested": args.word,
    }

    for input_path, filename, title, manifest_key in (
        (args.coverage, "coverage.html", "Coverage", "coverage_html"),
        (args.evidence, "evidence.html", "Evidence Register", "evidence_html"),
        (args.feedback, "feedback.html", "Feedback Coverage", "feedback_html"),
    ):
        if input_path:
            payload = json.loads(input_path.read_text(encoding="utf-8"))
            output = args.output_dir / filename
            write_registry(output, title, payload)
            manifest["outputs"][manifest_key] = str(output)

    if args.word:
        source_for_word = args.source
        word_path = args.output_dir / args.word_name
        command = [sys.executable, str(ROOT / "scripts" / "export_word.py"), "build", str(source_for_word), str(word_path)]
        build = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        if build.returncode != 0:
            print(build.stdout, end="")
            print(build.stderr, file=sys.stderr, end="")
            return build.returncode
        check = subprocess.run([sys.executable, str(ROOT / "scripts" / "export_word.py"), "check", str(word_path)], capture_output=True, text=True, encoding="utf-8")
        print(build.stdout, end="")
        print(check.stdout, end="")
        if check.stderr:
            print(check.stderr, file=sys.stderr, end="")
        if check.returncode != 0:
            return check.returncode
        manifest["outputs"]["word"] = str(word_path)

    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "manifest": str(manifest_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
