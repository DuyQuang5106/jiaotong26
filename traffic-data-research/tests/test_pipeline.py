import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from parse_inventory import parse
from spatial import normalize_region,chainage_metres,require_metric_crs,rate_per_100k
from build_evidence_matrix import score
class ProtocolTests(unittest.TestCase):
    def test_inventory(self):
        root=Path(__file__).resolve().parents[1]; sheets,rows=parse(next((root/'input').glob('*.xlsx')))
        self.assertEqual(len(rows),22); self.assertTrue(all(len(x)==13 for x in rows)); self.assertTrue(sheets)
    def test_rate(self):
        self.assertEqual(rate_per_100k(10,200000),5)
        with self.assertRaises(ValueError): rate_per_100k(1,0)
    def test_region_normalization(self): self.assertEqual(normalize_region('  Khánh  Hòa '),'Khánh Hòa')
    def test_chainage(self):
        self.assertEqual(chainage_metres('Km22+280'),22280)
        with self.assertRaises(ValueError): chainage_metres('Km26+00')
    def test_crs(self):
        self.assertEqual(require_metric_crs(32648),32648)
        with self.assertRaises(ValueError): require_metric_crs(4326)
    def test_scores(self):
        self.assertAlmostEqual(score([5]*6),5)
        self.assertEqual(score([0]*6),0)
        with self.assertRaises(ValueError): score([6]*6)
    def test_historical_rates_only(self):
        import pandas as pd
        p=Path(__file__).resolve().parents[1]/'data/processed/GT-01_GT-17_population_rates.csv'
        d=pd.read_csv(p); self.assertEqual(d.year.tolist(),[2022,2023,2024]); self.assertTrue((d.population_million>0).all())
    def test_raw_integrity(self):
        import hashlib,json
        root=Path(__file__).resolve().parents[1]
        for e in json.loads((root/'registry/raw_manifest.json').read_text(encoding='utf-8')): self.assertEqual(hashlib.sha256((root/e['path']).read_bytes()).hexdigest(),e['sha256'])
    def test_date_timezone(self):
        import pandas as pd
        self.assertEqual(pd.Timestamp('2020-07-03T18:00:00Z').tz_convert('Asia/Ho_Chi_Minh').strftime('%Y-%m-%d'),'2020-07-04')
    def test_provider_archive_checksums(self):
        import hashlib,json
        root=Path(__file__).resolve().parents[1]
        es=[json.loads(x) for x in (root/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
        for sid,label in [('GT-09','Vehicle_Tracking.zip'),('GT-17','vietnam_transport_dataset.xlsx')]:
            md=next(e for e in es if e['source_id']==sid and e['label']=='api_metadata' and e['status']==200)
            provider=json.loads((root/md['path']).read_text(encoding='utf-8'))['files'][0]['checksum'].split(':')[1]
            actual=next(e for e in es if e['source_id']==sid and e['label']==label and e['status']==200)
            self.assertEqual(hashlib.md5((root/actual['path']).read_bytes()).hexdigest(),provider)
if __name__=='__main__': unittest.main()
