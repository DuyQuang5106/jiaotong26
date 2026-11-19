"""Tests for inference boundaries and transformations used in idea discovery."""
import json
import sys
import unittest
from pathlib import Path
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from discover_opportunities import (OUT, PROJECT, education_title_mask,
                                   normalize, province_changes, read_ideas)

class DiscoveryTests(unittest.TestCase):
    def test_idea_schema_and_unique_ids(self):
        ideas,sources=read_ideas(PROJECT/'data/traffic_contest_ideas_2022_2025.xlsx')
        self.assertEqual(len(ideas),73)
        self.assertEqual(ideas.idea_id.nunique(),73)
        self.assertEqual(len(sources),15)

    def test_whitespace_normalization_does_not_merge_boundaries(self):
        self.assertEqual(normalize('Thái  Nguyên'),'Thái Nguyên')
        self.assertNotEqual(normalize('Hải Dương'),normalize('Hải Phòng'))

    def test_elearning_regex_does_not_capture_machine_learning(self):
        titles=pd.Series(['ứng dụng Machine Learning','trò chơi E-learning','môn học ở cấp THCS'])
        self.assertEqual(education_title_mask(titles).tolist(),[False,True,True])

    def test_zero_base_is_not_infinite_or_zero_growth(self):
        fixture=[]
        for i in range(63):
            for year in [2023,2024]:
                for metric in ['crashes','deaths','injuries']:
                    fixture.append({'region':f'Fixture-{i:02}','year':year,'metric':metric,'value':0 if year==2023 else 2})
        result=province_changes(pd.DataFrame(fixture))
        self.assertTrue(result.crashes_pct_change.isna().all())
        self.assertTrue(result.crashes_delta.eq(2).all())

    def test_exactly_ten_each_with_traceable_evidence(self):
        patterns=json.loads((OUT/'idea_patterns.json').read_text(encoding='utf-8'))
        findings=json.loads((OUT/'traffic_findings.json').read_text(encoding='utf-8'))
        self.assertEqual([r['id'] for r in patterns],[f'I{i:02}' for i in range(1,11)])
        self.assertEqual([r['id'] for r in findings],[f'T{i:02}' for i in range(1,11)])
        for r in findings:
            self.assertTrue(r['source_snapshot_provenance'])
            self.assertTrue(r['limitation_vi'])
            self.assertIn('denominator',r)

    def test_no_implicit_upgrade_of_proposals(self):
        candidates=json.loads((OUT/'opportunity_bridge.json').read_text(encoding='utf-8'))
        for c in candidates:
            self.assertEqual(c['novelty_status'],'NOT ESTABLISHED')
            self.assertEqual(c['market_status'],'NO VERIFIED DEMAND OR WILLINGNESS-TO-PAY')
        q=next(c for c in candidates if c['opportunity_id']=='O01')
        self.assertIn('không tự phù hợp chủ đề 2',q['competition_fit'])

    def test_all_63_regions_remain_available(self):
        full=pd.read_csv(OUT/'tables/province_changes_2023_2024.csv')
        self.assertEqual(full.region_as_recorded_2023_2024.nunique(),63)
        self.assertNotIn('TỔNG SỐ',full.region_as_recorded_2023_2024.tolist())

if __name__=='__main__': unittest.main()
