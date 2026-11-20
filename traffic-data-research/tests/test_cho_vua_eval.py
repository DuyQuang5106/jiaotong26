"""Evaluation of CHỞ VỪA photo measurements against tape-measure values."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(SRC))
from cho_vua_eval import HEADER, evaluate  # noqa: E402


def row(**kw):
    r = {k: '' for k in HEADER}
    r.update({'id': 'r1', 'at': '2026-11-20T08:00:00Z', 'vehicle': 'motorbike', 'item': 'thung_carton', 'overall': 'green'})
    r.update({k: str(v) for k, v in kw.items()})
    return r


class EvaluateTest(unittest.TestCase):
    def test_false_green_counted(self):
        rows = [row(ref_kind='plate', rear_min=40, rear_max=48, tape_rear=55)]
        self.assertEqual(evaluate(rows)['plate']['false_green'], 1)

    def test_coverage_and_mae(self):
        rows = [row(ref_kind='aruco', side_left_min=35, side_left_max=45, tape_side_left=42)]
        r = evaluate(rows)['aruco']
        self.assertEqual(r['coverage'], 1.0)
        self.assertAlmostEqual(r['mae_cm'], 2.0)

    def test_missing_tape_skipped(self):
        self.assertEqual(evaluate([row(ref_kind='plate', rear_min=10, rear_max=20)])['plate']['skipped'], 1)

    def test_yellow_rate_uses_motorbike_limits(self):
        rows = [row(ref_kind='plate', side_left_min=25, side_left_max=35, tape_side_left=31),
                row(ref_kind='plate', side_left_min=5, side_left_max=10, tape_side_left=8)]
        self.assertEqual(evaluate(rows)['plate']['yellow_rate'], 0.5)

    def test_non_motorbike_rows_skip_light_metrics(self):
        r = evaluate([row(ref_kind='aruco', vehicle='non_motorized', rear_min=40, rear_max=48, tape_rear=55)])['aruco']
        self.assertEqual(r['false_green'], 0)
        self.assertIsNone(r['yellow_rate'])
        self.assertEqual(r['pairs'], 1)

    def test_groups_by_reference(self):
        rows = [row(ref_kind='plate', rear_min=1, rear_max=2, tape_rear=1), row(ref_kind='aruco', rear_min=1, rear_max=2, tape_rear=1)]
        self.assertEqual(set(evaluate(rows)), {'plate', 'aruco'})

    def test_cli_writes_reports(self):
        with tempfile.TemporaryDirectory() as d:
            csv_path = Path(d) / 'c.csv'
            csv_path.write_text(','.join(HEADER) + '\n' + ','.join(row(ref_kind='plate', rear_min=40, rear_max=48, tape_rear=55)[k] for k in HEADER) + '\n', encoding='utf-8-sig')
            out = Path(d) / 'out'
            subprocess.run([sys.executable, '-X', 'utf8', str(SRC / 'cho_vua_eval.py'), str(csv_path), '--out', str(out)], check=True)
            self.assertEqual(json.loads((out / 'eval.json').read_text(encoding='utf-8'))['plate']['false_green'], 1)
            self.assertIn('false_green', (out / 'eval_vi.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
