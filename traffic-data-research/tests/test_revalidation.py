"""Guard scientific interpretation, annotation reconciliation and additive execution."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

SRC = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(SRC))
from revalidate_research import paired_contrast, reconcile_boxes

OUT = SRC.parent / 'reports/revalidation_2026_11_19_v2'


class RevalidationTests(unittest.TestCase):
    def test_renamed_track_ids_and_empty_tracks_are_not_geometry_errors(self):
        txt = pd.DataFrame([dict(frame=0, track_id=7, x=10, y=20, width=30, height=40)])
        objects = {'99': {'frames': ['000000.jpg'], 'boxes': [[10, 20, 30, 40]]},
                   '100': {'frames': [], 'boxes': []}}
        result = reconcile_boxes(txt, objects)
        self.assertTrue(result['identical_geometry_multisets'])
        self.assertTrue(result['matched_geometry_track_mapping_one_to_one'])
        self.assertEqual(result['json_empty_track_objects'], 1)
        self.assertEqual(result['matched_json_track_ids_with_different_txt_id'], 1)

    def test_geometry_comparison_preserves_duplicate_multiplicity(self):
        txt = pd.DataFrame([dict(frame=0, track_id=7, x=10, y=20, width=30, height=40)])
        obj = {'99': {'frames': ['000000.jpg', '000000.jpg'], 'boxes': [[10, 20, 30, 40]] * 2}}
        result = reconcile_boxes(txt, obj)
        self.assertFalse(result['identical_geometry_multisets'])
        self.assertEqual(result['shared_box_instances'], 1)
        self.assertEqual(result['json_only_box_instances'], 1)

    def test_malformed_annotation_arrays_fail_instead_of_silent_zip_truncation(self):
        txt = pd.DataFrame([dict(frame=0, track_id=1, x=1, y=1, width=1, height=1)])
        with self.assertRaises(ValueError):
            reconcile_boxes(txt, {'1': {'frames': ['0.jpg'], 'boxes': []}})

    def test_calendar_gaps_are_missing_not_zero_and_pairing_uses_local_time(self):
        rows = []
        for date in ['2020-01-01', '2020-01-03']:
            for hour, velocity in [('00', 10), ('05', 20)]:
                rows.append(dict(updated_at=f'{date}T{hour}:00:00Z', segment_id=1, velocity=velocity))
        status, pairs, days, coverage = paired_contrast(pd.DataFrame(rows))
        self.assertEqual(len(pairs), 2)
        self.assertTrue(pairs.difference.eq(-10).all())
        self.assertEqual(status.loc[0, 'hour'], 7)
        missing = coverage.loc[coverage.day.eq('2020-01-02')].iloc[0]
        self.assertTrue(pd.isna(missing.recorded_rows))
        self.assertFalse(missing.observed)

    def test_actual_rechecks_reproduce_old_numbers_without_promoting_inference(self):
        result = json.loads((OUT / 'measured_rechecks.json').read_text(encoding='utf-8'))
        g = result['GT07']
        self.assertTrue(all(g['reproduction'].values()))
        self.assertIn('DESCRIPTIVE_CONTRAST_ONLY', g['updated_inference_status'])
        self.assertAlmostEqual(g['equal_segment_day_mean'], -8/404)
        self.assertGreater(g['sensitivity'][3]['estimate'], 0)
        v = result['GT09']['VNTraffic']
        self.assertEqual(v['shared_box_instances'], 16036)
        self.assertEqual(v['json_empty_track_objects'], 120)
        self.assertTrue(v['identical_geometry_multisets'])

    def test_deliverable_counts_and_hypothesis_status(self):
        findings = json.loads((OUT / 'ten_traffic_discoveries_rechecked.json').read_text(encoding='utf-8'))
        candidates = json.loads((OUT / 'ten_candidate_ideas.json').read_text(encoding='utf-8'))
        self.assertEqual([f['id'] for f in findings], [f'T{i:02}' for i in range(1, 11)])
        self.assertEqual([c['id'] for c in candidates], [f'C{i:02}' for i in range(1, 11)])
        self.assertEqual({c['discovery_id'] for c in candidates}, {f['id'] for f in findings})
        for c in candidates:
            self.assertEqual(c['novelty_status'], 'NOT_ESTABLISHED')
            self.assertEqual(c['intervention_effect_status'], 'NOT_MEASURED')
            self.assertTrue(c['source_snapshot_provenance'])
            self.assertTrue(c['stop_rule_vi'])
            self.assertTrue(c['baseline_vi'])
        for c in candidates[:6]:
            self.assertIn('E0', c['evidence_grade_vi'])

    def test_all_original_data_and_old_findings_still_match_protected_hashes(self):
        manifest = json.loads((OUT / 'preservation_check.json').read_text(encoding='utf-8'))
        project = SRC.parents[1]
        self.assertEqual(manifest['changed_files'], [])
        for name, expected in manifest['before_sha256'].items():
            actual = hashlib.sha256((project / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)

    def test_existing_output_directory_is_refused_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            marker = folder / 'keep.txt'
            marker.write_text('preserve me', encoding='utf-8')
            result = subprocess.run([sys.executable, '-X', 'utf8', str(SRC / 'revalidate_research.py'),
                                     '--output', str(folder)], capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Output exists', result.stderr)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'preserve me')
            self.assertEqual(len(list(folder.iterdir())), 1)


if __name__ == '__main__':
    unittest.main()
