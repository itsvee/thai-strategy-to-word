import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'readiness_gate.py'


def ready_state():
    brief = {
        'company': 'บริษัทสมมติ ก',
        'business': 'รับผลิตอาหารแช่เย็นตามคำสั่งซื้อ',
        'customers': 'ร้านค้าปลีกในจังหวัดที่ส่งถึงภายในหนึ่งวัน',
        'user_role': 'ผู้จัดการปฏิบัติการ เสนอแผนได้แต่อนุมัติงบไม่ได้',
        'strategy_scope': 'หน่วยธุรกิจโรงงานหนึ่งแห่ง เฉพาะส่งมอบ',
        'audience': 'กรรมการผู้จัดการและฝ่ายการเงิน',
        'decision': 'เลือกแนวทางลดสินค้าส่งคืนและอนุมัติการทดลอง',
        'problem': 'ลูกค้าสามร้านส่งคืนสินค้าจากอุณหภูมิปลายทางในเดือนที่ผ่านมา',
        'desired_outcome': 'ลดการคืนโดยรักษาความปลอดภัยอาหาร ใช้ทะเบียนคืนติดตาม',
        'horizon': 'ทดลองในไตรมาสหน้า',
        'constraints': 'ใช้ทีมเดิมและยังเปลี่ยนผู้ขนส่งไม่ได้',
        'tradeoffs': 'ยอมลดจำนวนเส้นทางทดลอง แต่ห้ามลดมาตรฐานอาหาร',
        'non_goals': 'ไม่ขยายโรงงานหรือพัฒนาสินค้าใหม่',
    }
    return {
        'brief_revision': 1, 'confirmed_revision': 1, 'brief': brief,
        'evidence': [{'claim': brief['problem'], 'status': 'user_reported',
                      'source': 'ผู้จัดการปฏิบัติการ รายงานเดือนก่อน'}],
        'gaps': [], 'contradictions': [],
    }


class ReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('readiness_gate', SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_unknown_problem_blocks_drafting(self):
        state = ready_state()
        state['brief']['problem'] = 'ไม่ทราบ'
        self.assertEqual(self.module.evaluate(state)['status'], 'needs_interview')

    def test_hypothesis_only_is_not_observed_problem_evidence(self):
        state = ready_state()
        state['evidence'][0]['status'] = 'hypothesis'
        self.assertEqual(self.module.evaluate(state)['status'], 'needs_interview')

    def test_collection_plan_cannot_replace_unknown_core_problem(self):
        state = ready_state()
        state['brief']['problem'] = ''
        state['gaps'] = [{'field': 'problem', 'treatment': 'collection_plan',
                         'owner': 'Operations', 'method': 'สัมภาษณ์',
                         'deadline': 'เดือนหน้า', 'accepted': True}]
        self.assertEqual(self.module.evaluate(state)['status'], 'needs_interview')

    def test_explicitly_accepted_baseline_collection_can_proceed(self):
        state = ready_state()
        state['gaps'] = [{'field': 'baseline', 'treatment': 'collection_plan',
                         'owner': 'Operations', 'method': 'ตรวจทะเบียนคืน',
                         'deadline': 'ก่อนเปิดทดลอง', 'accepted': True}]
        self.assertEqual(self.module.evaluate(state)['status'], 'ready_for_analysis')

    def test_collection_plan_without_user_acceptance_blocks(self):
        state = ready_state()
        state['gaps'] = [{'field': 'cost', 'treatment': 'collection_plan',
                         'owner': 'Finance', 'method': 'ประเมินต้นทุน',
                         'deadline': 'ก่อนอนุมัติ', 'accepted': False}]
        self.assertEqual(self.module.evaluate(state)['status'], 'needs_interview')

    def test_unresolved_contradiction_blocks_even_with_confirmation(self):
        state = ready_state()
        state['contradictions'] = ['ฝ่ายขายกับโรงงานระบุสาเหตุคนละอย่าง']
        self.assertEqual(self.module.evaluate(state)['status'], 'needs_interview')

    def test_changed_scope_invalidates_previous_confirmation(self):
        state = ready_state()
        state['brief_revision'] = 2
        self.assertEqual(self.module.evaluate(state)['status'], 'ready_for_confirmation')

    def test_no_confirmation_cannot_start_analysis(self):
        state = ready_state()
        state['confirmed_revision'] = None
        self.assertEqual(self.module.evaluate(state)['status'], 'ready_for_confirmation')

    def test_malformed_collection_types_are_rejected(self):
        state = ready_state()
        state['evidence'] = 'มีหลักฐาน'
        with self.assertRaises(ValueError):
            self.module.evaluate(state)

    def test_boolean_is_not_a_revision(self):
        state = ready_state()
        state['brief_revision'] = True
        with self.assertRaises(ValueError):
            self.module.evaluate(state)

    def test_cli_blocks_unfilled_template_and_accepts_confirmed_case(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'state.json'
            path.write_text(json.dumps(ready_state(), ensure_ascii=False), encoding='utf-8')
            ok = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(json.loads(ok.stdout)['status'], 'ready_for_analysis')
            blocked = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / 'templates' / 'state.example.json')], capture_output=True, text=True)
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(json.loads(blocked.stdout)['status'], 'needs_interview')

    def test_cli_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'state.json'
            path.write_text('{', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['ok'])


if __name__ == '__main__':
    unittest.main()
