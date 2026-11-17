import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_outputs.py"


class OutputChainTests(unittest.TestCase):
    def test_html_bundle_without_word(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "report.md"
            source.write_text("# รายงาน\n\nเนื้อหาทดสอบ\n", encoding="utf-8")
            coverage = root / "coverage.json"
            coverage.write_text(json.dumps({"items": [{
                "id": "Q1", "requirement": "โจทย์", "required": True,
                "report_location": "บทนำ", "answer": "คำตอบ",
                "evidence_ids": ["E1"], "status": "covered"
            }]}, ensure_ascii=False), encoding="utf-8")
            evidence = root / "evidence.json"
            evidence.write_text(json.dumps({"items": [{"id": "E1", "claim": "ข้อมูล", "status": "user_reported", "source": "ผู้ใช้"}]}, ensure_ascii=False), encoding="utf-8")
            output = root / "output"
            result = subprocess.run([sys.executable, str(BUILDER), str(source), str(output), "--coverage", str(coverage), "--evidence", str(evidence)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("รายงาน", (output / "report.html").read_text(encoding="utf-8"))
            self.assertTrue((output / "coverage.html").is_file())
            self.assertTrue((output / "evidence.html").is_file())
            self.assertEqual(json.loads((output / "manifest.json").read_text(encoding="utf-8"))["word_requested"], False)

    def test_blocked_coverage_stops_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "report.md"
            source.write_text("# รายงาน\n", encoding="utf-8")
            coverage = root / "coverage.json"
            coverage.write_text(json.dumps({"items": [{"id": "Q1", "requirement": "โจทย์", "required": True, "report_location": "ยังไม่มี", "answer": "ยังไม่มี", "status": "blocked"}]}, ensure_ascii=False), encoding="utf-8")
            output = root / "output"
            result = subprocess.run([sys.executable, str(BUILDER), str(source), str(output), "--coverage", str(coverage)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((output / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
