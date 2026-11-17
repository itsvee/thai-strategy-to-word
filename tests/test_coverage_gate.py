import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "coverage_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("coverage_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CoverageGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_ready_when_required_item_has_answer_and_evidence(self):
        coverage = {"items": [{
            "id": "Q1", "requirement": "อธิบายกลยุทธ์", "required": True,
            "report_location": "บทที่ 2", "answer": "เลือกกลยุทธ์ A",
            "evidence_ids": ["E1"], "status": "covered"
        }]}
        self.assertEqual(self.module.evaluate(coverage)["status"], "ready")

    def test_partial_required_item_blocks(self):
        coverage = {"items": [{
            "id": "Q1", "requirement": "อธิบายกลยุทธ์", "required": True,
            "report_location": "", "answer": "", "status": "partial"
        }]}
        self.assertEqual(self.module.evaluate(coverage)["status"], "blocked")

    def test_covered_item_can_state_limitation_without_evidence(self):
        coverage = {"items": [{
            "id": "Q1", "requirement": "ประเมินผลกระทบ", "required": True,
            "report_location": "บทที่ 4", "answer": "ยังประเมินไม่ได้",
            "evidence_ids": [], "limitation": "ไม่มีข้อมูลภายใน",
            "status": "covered"
        }]}
        self.assertEqual(self.module.evaluate(coverage)["status"], "ready")

    def test_duplicate_ids_are_invalid(self):
        coverage = {"items": [
            {"id": "Q1", "requirement": "a", "report_location": "b", "answer": "c", "status": "covered", "evidence_ids": ["E1"]},
            {"id": "Q1", "requirement": "a", "report_location": "b", "answer": "c", "status": "covered", "evidence_ids": ["E1"]},
        ]}
        with self.assertRaises(ValueError):
            self.module.evaluate(coverage)

    def test_cli_returns_success_for_ready_coverage(self):
        coverage = {"items": [{
            "id": "Q1", "requirement": "อธิบายองค์กร", "required": True,
            "report_location": "บทที่ 1", "answer": "องค์กรมีสองหน่วยธุรกิจ",
            "evidence_ids": ["E1"], "status": "covered"
        }]}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "coverage.json"
            path.write_text(json.dumps(coverage, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "ready")


if __name__ == "__main__":
    unittest.main()
