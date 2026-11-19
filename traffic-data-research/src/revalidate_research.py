"""Additive checkpoint: audit existing snapshots without reacquisition or mutation.

Run from repository root with Python's UTF-8 mode. Output must be a NEW directory.
The six analytics skills are loaded from --skill-root; hashes record their versions.
This runner never invokes skill demonstration entry points or fits award predictors.
"""
import argparse
from collections import Counter
import contextlib
import datetime as dt
import hashlib
import html
import importlib.util
import io
import json
import platform
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from discover_opportunities import (EXCLUDED_REGIONS, PROJECT, RESEARCH,
    education_title_mask, normalize, province_changes, read_ideas)

NEW_SKILLS = ['programmatic-eda', 'data-quality-audit', 'analysis-assumptions-log',
              'time-series-analysis', 'root-cause-investigation', 'analysis-qa-checklist']
OTHER_SKILLS = ['statistical-analysis', 'scientific-critical-thinking',
                'experimental-design', 'scientific-visualization', 'literature-review',
                'geopandas', 'statsmodels']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, (np.ndarray, pd.Series)):
        return clean(value.tolist())
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, (pd.Timestamp, dt.datetime, dt.date)):
        return value.isoformat()
    return value


def write_json(path, value):
    path.write_text(json.dumps(clean(value), ensure_ascii=False, indent=2,
                               allow_nan=False) + '\n', encoding='utf-8')


def paired_contrast(status):
    """Recompute from status rows, not previously calculated paired summaries."""
    s = status.copy()
    ts = pd.to_datetime(s.updated_at, utc=True, errors='raise').dt.tz_convert('Asia/Ho_Chi_Minh')
    s['day'], s['hour'] = ts.dt.strftime('%Y-%m-%d'), ts.dt.hour
    s['window'] = np.select([s.hour.isin([7, 8, 16, 17]), s.hour.between(10, 14)],
                            ['peak', 'midday'], default='exclude')
    pairs = s[s.window.ne('exclude')].groupby(['day', 'segment_id', 'window']).velocity.median().unstack().dropna()
    pairs['difference'] = pairs.peak - pairs.midday
    days = pairs.groupby(level='day').difference.agg(['mean', 'median', 'size'])
    days.index.name = 'day'
    daily = s.groupby('day').size().rename('recorded_rows')
    calendar = pd.date_range(ts.min().normalize(), ts.max().normalize(), freq='D')
    coverage = daily.reindex(calendar.strftime('%Y-%m-%d')).rename_axis('day').reset_index()
    coverage['observed'] = coverage.recorded_rows.notna()
    return s, pairs, days, coverage


def box_counter(frame):
    """Keep multiplicity; do not let dictionary keys silently overwrite boxes."""
    columns = ['frame', 'x', 'y', 'width', 'height']
    return Counter(tuple(float(v) for v in row) for row in frame[columns].itertuples(index=False, name=None))


def reconcile_boxes(txt, objects):
    rows = []
    for tid, obj in objects.items():
        if len(obj['frames']) != len(obj['boxes']):
            raise ValueError('JSON frame/box array length mismatch')
        for f, box in zip(obj['frames'], obj['boxes']):
            if len(box) != 4:
                raise ValueError('Expected x,y,width,height')
            rows.append({'frame': int(Path(f).stem), 'track_id': str(tid),
                         **dict(zip(['x', 'y', 'width', 'height'], box))})
    js = pd.DataFrame(rows)
    a, b = box_counter(txt), box_counter(js)
    txt_ids = {tuple(float(getattr(r, c)) for c in ['frame', 'x', 'y', 'width', 'height']): str(int(r.track_id))
               for r in txt.itertuples()}
    mapping = {}
    for r in js.itertuples():
        key = tuple(float(getattr(r, c)) for c in ['frame', 'x', 'y', 'width', 'height'])
        if key in txt_ids:
            mapping.setdefault(r.track_id, set()).add(txt_ids[key])
    one_to_one = (all(len(v) == 1 for v in mapping.values()) and
                  len({next(iter(v)) for v in mapping.values()}) == len(mapping))
    return {
        'txt_rows': len(txt), 'json_rows': len(js), 'shared_box_instances': sum((a & b).values()),
        'txt_only_box_instances': sum((a - b).values()), 'json_only_box_instances': sum((b - a).values()),
        'identical_geometry_multisets': a == b,
        'txt_duplicate_geometry_instances': len(txt) - len(a),
        'json_duplicate_geometry_instances': len(js) - len(b),
        'txt_track_ids': txt.track_id.nunique(), 'json_track_ids': js.track_id.nunique(),
        'json_track_objects_including_empty': len(objects),
        'json_empty_track_objects': sum(not obj['boxes'] for obj in objects.values()),
        'matched_geometry_track_mapping_one_to_one': one_to_one,
        'matched_json_track_ids_with_different_txt_id': sum(v != {k} for k, v in mapping.items()),
        'txt_duplicate_frame_track_extra_rows': int(txt.duplicated(['frame', 'track_id']).sum()),
        'comparison_key': 'frame,x,y,width,height; exact numeric equality; multiplicity retained; track ID ignored',
        'scope': 'representation audit, not validation against video or independently annotated truth',
    }


class Checkpoint:
    def __init__(self, out, skill_root):
        self.out, self.skill_root = out, skill_root
        self.modules, self.calls, self.inputs, self.results = {}, [], {}, {}
        (out / 'tables').mkdir(parents=True, exist_ok=False)
        (out / 'skill_outputs').mkdir()
        self.skill_records = []
        for name in NEW_SKILLS + OTHER_SKILLS:
            p = skill_root / name / 'SKILL.md'
            self.skill_records.append({'skill': name, 'available': p.is_file(),
                                       'skill_md_sha256': sha(p) if p.is_file() else None,
                                       'use': 'pending'})
        missing = [r['skill'] for r in self.skill_records[:6] if not r['available']]
        if missing:
            write_json(out / 'skills_available.json', self.skill_records)
            raise RuntimeError('Required skills unavailable: ' + ', '.join(missing))

    def module(self, skill, script):
        key = skill + '/' + script
        if key not in self.modules:
            p = self.skill_root / skill / 'scripts' / (script + '.py')
            spec = importlib.util.spec_from_file_location(script, p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.modules[key] = mod
        return self.modules[key]

    def call(self, skill, script, function, *args, **kwargs):
        """Import functions to avoid demo-only __main__ branches in installed helpers."""
        p = self.skill_root / skill / 'scripts' / (script + '.py')
        buf = io.StringIO()
        record = {'skill': skill, 'script': script, 'function': function, 'sha256': sha(p)}
        with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            result = getattr(self.module(skill, script), function)(*args, **kwargs)
        record.update(status='EXECUTED', warnings=list(dict.fromkeys(str(w.message) for w in caught)))
        self.calls.append(record)
        text = buf.getvalue()
        if text:
            log = self.out / 'skill_outputs' / (script + '.txt')
            with log.open('a', encoding='utf-8') as f:
                f.write(text + '\n')
        return result

    def load(self, relative, **kwargs):
        p = RESEARCH / relative
        self.inputs[str(p.relative_to(PROJECT)).replace('\\', '/')] = sha(p)
        return pd.read_csv(p, **kwargs)

    def table(self, df, name):
        df.to_csv(self.out / 'tables' / (name + '.csv'), index=False, encoding='utf-8-sig')

    def profile(self, df, name, keys, rules=None, numeric=None):
        p = 'programmatic-eda'
        self.call(p, 'data_overview', 'overview', df, sample_n=3)
        self.table(self.call(p, 'null_profiler', 'profile_nulls', df).rename_axis('column').reset_index(), name + '_eda_nulls')
        numeric_df = df[numeric] if numeric is not None else df.select_dtypes(include='number')
        if numeric_df.shape[1]:
            self.table(self.call(p, 'outlier_detector', 'detect_outliers', numeric_df), name + '_outlier_screen')
            self.call(p, 'distribution_summary', 'distribution_summary', numeric_df)
        if numeric_df.shape[1] >= 2:
            # Installed helper raises KeyError when there are no strong pairs.
            # Keep unmodified helper; compute/export actual correlation even then.
            corr = numeric_df.corr()
            self.table(corr.rename_axis('column').reset_index(), name + '_correlations')
            try:
                self.call(p, 'correlation_explorer', 'explore_correlations', numeric_df)
            except KeyError as exc:
                self.calls.append({'skill': p, 'script': 'correlation_explorer',
                    'status': 'HELPER_EMPTY_PAIRS_BUG', 'error': str(exc),
                    'resolution': 'matrix exported with pandas; no pairs promoted to findings'})
        p = 'data-quality-audit'
        nulls = self.call(p, 'null_counter', 'count_nulls', df)
        # Helper threshold=0 flags even 0% null as FAIL (>=). Use exact checks for keys.
        self.table(nulls, name + '_audit_nulls')
        dup = self.call(p, 'duplicate_finder', 'find_duplicates', df, keys)
        if rules:
            for c in rules:
                if c not in df:
                    raise ValueError('Rule column absent: ' + c)
                if 'allowed' not in rules[c] and not pd.api.types.is_numeric_dtype(df[c]):
                    raise TypeError('Range comparisons require verified numeric dtype: ' + c)
            self.table(self.call(p, 'value_range_validator', 'validate_ranges', df, rules), name + '_ranges')
        return {'grain_key': keys, 'rows': len(df), 'columns': len(df.columns),
                'required_key_null_cells': int(df[keys].isna().sum().sum()), 'duplicates': dup,
                'note': 'Default null/outlier screens are flags; no automatic deletion or imputation.'}

    def audit(self):
        a = self.load('data/processed/GT-01_aggregates.csv')
        s = self.load('data/processed/GT-07_segment_status.csv')
        seg = self.load('data/processed/GT-07_segments.csv')
        h = self.load('data/processed/GT-10_hazards.csv')
        land = self.load('data/processed/GT-11_hazards.csv')
        ideas, sources = read_ideas(PROJECT / 'data/traffic_contest_ideas_2022_2025.xlsx')
        # Author/team names are deliberately omitted from helper console outputs.
        ideas = ideas.drop(columns=['public_author_team'])
        audit = {}
        configs = [(a, 'GT01', ['region', 'year', 'metric'], {'value': {'min': 0}, 'year': {'allowed': [2022, 2023, 2024]}}, ['value']),
            (s, 'GT07', ['segment_id', 'updated_at'], {'velocity': {'min': 0}}, ['velocity']),
            (h, 'GT10', ['record_id'], None, []), (land, 'GT11', ['record_id'], None, []),
            (ideas, 'ideas', ['idea_id'], None, [])]
        for df, name, keys, rules, numeric in configs:
            audit[name] = self.profile(df, name, keys, rules, numeric)
        audit['GT07_segment_fk'] = self.call('data-quality-audit', 'referential_integrity',
            'check_referential_integrity', s, seg, 'segment_id', '_id')
        refs = pd.DataFrame([{'source_id': v, 'idea_id': r.idea_id} for r in ideas.itertuples()
            for v in re.findall(r'S\d+', str(r.source_ids))])
        audit['idea_source_fk'] = self.call('data-quality-audit', 'referential_integrity',
            'check_referential_integrity', refs, sources, 'source_id', 'source_id')
        gtrefs = pd.DataFrame([{'source_id': v} for text in ideas.linked_GT_ids_proposed.fillna('')
            for v in re.findall(r'GT-\d+', text)])
        registry = self.load('registry/source_audit.csv')
        assert set(registry.source_id) == {f'GT-{i:02}' for i in range(1, 23)}
        assert registry.source_id.is_unique
        coverage = registry[['source_id', 'access_status', 'content_status', 'license', 'coverage_start', 'coverage_end']].copy()
        reviewed = {'GT-01', 'GT-02', 'GT-04', 'GT-07', 'GT-08', 'GT-09', 'GT-10', 'GT-11', 'GT-12', 'GT-20'}
        coverage['checkpoint_scope'] = coverage.source_id.map(lambda v: 'LOCAL_RECHECK' if v in reviewed else 'PRIOR_AUDIT_RETAINED; NO_NEW_ACQUISITION')
        self.table(coverage, 'all_22_source_review_coverage')
        audit['idea_proposed_gt_fk'] = self.call('data-quality-audit', 'referential_integrity',
            'check_referential_integrity', gtrefs, registry, 'source_id', 'source_id')
        audit['idea_proposed_gt_fk']['interpretation'] = 'valid inventory IDs only; not evidence that projects actually used those datasets'
        # Explicit decision-use age screen, not an asserted publisher refresh SLA.
        freshness = self.call('data-quality-audit', 'freshness_check', 'check_freshness',
                              s, 'updated_at', max_lag_hours=24*365)
        freshness.update(threshold_basis='analyst sensitivity: within 365 days for a proposed current baseline; NOT publisher SLA',
                         historical_use='valid as historical artifact; not rejected for being historical')
        audit['GT07_freshness_screen'] = freshness
        audit['GT10_treatment_overlap'] = h.loc[h.treated.notna() & h.untreated.notna(), 'record_id'].tolist()
        audit['GT10_treatment_nonempty'] = int(h.treated.notna().sum())
        audit['GT10_untreated_nonempty'] = int(h.untreated.notna().sum())
        audit['GT10_treatment_meaning'] = 'free text, overlapping fields; not a binary completed/incomplete label'
        self.results['quality'] = audit
        return a, s, h, land, ideas

    def validate_contrast(self, s):
        status, pairs, days, coverage = paired_contrast(s)
        self.table(pairs.reset_index(), 'GT07_recomputed_pairs')
        self.table(days.reset_index(), 'GT07_recomputed_days')
        self.table(coverage, 'GT07_calendar_coverage')
        self.profile(pairs[['peak', 'midday', 'difference']].reset_index(drop=True),
                     'paired_numeric', ['peak', 'midday', 'difference'], numeric=['peak', 'midday', 'difference'])
        # Duplicate numeric tuples are expected here; not a key/entity failure.
        old = json.loads((RESEARCH / 'reports/measured_results.json').read_text(encoding='utf-8'))['GT-07']['exploratory_test']
        sd = days['mean'].std(ddof=1)
        t = stats.ttest_1samp(days['mean'], 0)
        shapiro = stats.shapiro(days['mean'])
        lodo = [days['mean'].drop(d).mean() for d in days.index]
        sensitivity = [
            {'estimator': 'equal_day_mean', 'estimate': days['mean'].mean(), 'unit_count': len(days)},
            {'estimator': 'equal_segment_day_mean', 'estimate': pairs.difference.mean(), 'unit_count': len(pairs)},
            {'estimator': 'median_day_mean', 'estimate': days['mean'].median(), 'unit_count': len(days)},
            {'estimator': 'mean_days_with_at_least_2_pairs', 'estimate': days.loc[days['size'].ge(2), 'mean'].mean(), 'unit_count': int(days['size'].ge(2).sum())},
            {'estimator': 'mean_days_with_at_least_5_pairs', 'estimate': days.loc[days['size'].ge(5), 'mean'].mean(), 'unit_count': int(days['size'].ge(5).sum())},
        ]
        self.table(pd.DataFrame(sensitivity), 'GT07_weighting_sensitivity')
        rng = np.random.default_rng(42)
        boot = np.array([rng.choice(days['mean'], len(days), replace=True).mean() for _ in range(5000)])
        reproduction = {'estimate_matches_old': bool(np.isclose(days['mean'].mean(), old['estimate'])),
            't_matches_old': bool(np.isclose(t.statistic, old['t'])),
            'p_matches_old': bool(np.isclose(t.pvalue, old['p'])),
            'iid_bootstrap_matches_old': bool(np.allclose(np.quantile(boot, [.025, .975]), old['ci95_bootstrap']))}
        result = {'n_status_rows': len(status), 'matched_segment_days': len(pairs),
            'unique_paired_segments': pairs.index.get_level_values('segment_id').nunique(), 'matched_days': len(days),
            'calendar_days': len(coverage), 'observed_days': int(coverage.observed.sum()),
            'unobserved_days_not_zero': int((~coverage.observed).sum()),
            'top_day_fraction': status.groupby('day').size().max()/len(status),
            'days_with_one_pair': int(days['size'].eq(1).sum()),
            'equal_day_mean': days['mean'].mean(), 'equal_segment_day_mean': pairs.difference.mean(),
            'day_sd': sd, 'standardized_day_mean_over_sd': days['mean'].mean()/sd,
            'shapiro_W': shapiro.statistic, 'shapiro_p': shapiro.pvalue,
            'old_t': t.statistic, 'old_df': len(days)-1, 'old_p': t.pvalue,
            'old_iid_bootstrap_interval': np.quantile(boot, [.025, .975]),
            'leave_one_day_out_estimate_range': [min(lodo), max(lodo)],
            'reproduction': reproduction, 'sensitivity': sensitivity,
            'updated_inference_status': 'DESCRIPTIVE_CONTRAST_ONLY; iid p/CI reproduced for audit, not calibrated population inference',
            'why': 'unknown sampling/velocity units, changing road mix, sparse irregular days, repeated roads, day independence not established',
            'sensitivity_status': 'post-hoc estimator comparison; estimands differ; no significance search; no new p-values',
            'time_series_gate': 'no ADF, decomposition, ARIMA, gap filling or forecast; sampling mechanism and regular comparable series unavailable',
        }
        assert all(reproduction.values()), reproduction
        self.results['GT07'] = result
        return days, coverage

    def other_sources(self, aggregates, ideas):
        boxes = {}
        for scene in ['VNTraffic', 'AICC22-Custom']:
            # Read original TXT representation independently of processed CSV.
            folder = RESEARCH / 'data/interim/GT-09' / scene
            txtp, jsonp = folder / (scene + '_GroundTruth.txt'), folder / (scene + '_GroundTruth.json')
            for p in [txtp, jsonp]:
                self.inputs[str(p.relative_to(PROJECT)).replace('\\', '/')] = sha(p)
            txt = pd.read_csv(txtp, header=None, names=['frame', 'track_id', 'x', 'y', 'width', 'height', 'confidence', 'u1', 'u2', 'u3'])
            boxes[scene] = reconcile_boxes(txt, json.loads(jsonp.read_text(encoding='utf-8')))
        self.results['GT09'] = boxes
        gtfs = {}
        for part in ['am', 'md', 'pm']:
            prefix = f'data/processed/GT-12_hanoi_gtfs_{part}_'
            trips, stops, times, cal = [self.load(prefix + name + '.csv') for name in ['trips', 'stops', 'stop_times', 'calendar']]
            gtfs[part] = {'times_to_trips': self.call('data-quality-audit', 'referential_integrity', 'check_referential_integrity', times, trips, 'trip_id', 'trip_id'),
                'times_to_stops': self.call('data-quality-audit', 'referential_integrity', 'check_referential_integrity', times, stops, 'stop_id', 'stop_id'),
                'calendar_start': int(cal.start_date.min()), 'calendar_end': int(cal.end_date.max()),
                'duplicate_trip_sequence_extra_rows': int(times.duplicated(['trip_id', 'stop_sequence']).sum()),
                'trip_ids': len(trips), 'stop_ids': len(stops),
                'headway_status': 'route-level historical schedule summary only; no direction/service-day comparability audit; not a current bus wait estimate'}
        self.results['GT12'] = gtfs
        masks = self.load('data/processed/GT-08_binary_masks_summary.csv')
        from ingest import events
        manifest = {e['label']: e for e in events() if e['source_id'] == 'GT-08' and e['status'] == 200 and e['label'].endswith('.npy')}
        for row in masks.itertuples():
            entry = manifest[row.file]
            path = RESEARCH / entry['path']
            assert sha(path) == row.sha256
            arr = np.load(path, allow_pickle=False)
            assert arr.ndim == 1 and set(np.unique(arr)).issubset({0, 1})
            assert len(arr) == row.frames and int(arr.sum()) == row.abnormal_frames
        self.results['GT08'] = {'files': len(masks), 'frames': int(masks.frames.sum()),
            'abnormal_frames': int(masks.abnormal_frames.sum()),
            'pooled_fraction': masks.abnormal_frames.sum()/masks.frames.sum(),
            'equal_file_mean_fraction': masks.abnormal_fraction.mean(),
            'claim_gate': 'curated binary annotation proportions only; not population prevalence or cargo-specific counts'}
        osm = self.load('data/processed/GT-04_osm_sample.csv')
        self.results['GT04'] = {'objects': len(osm), 'by_type': osm.osm_type.value_counts().to_dict(),
            'duplicate_type_id_extra_rows': int(osm.duplicated(['osm_type', 'osm_id']).sum()),
            'nodes_with_missing_coordinates': int(osm.loc[osm.osm_type.eq('node'), ['lat', 'lon']].isna().any(axis=1).sum()),
            'claim_gate': 'convenience bbox only; no spatial join, distance measurement, tag-absence inference or provincial extrapolation'}
        classes = self.load('data/processed/GT-20_classes.csv')
        self.results['GT20'] = {'classes': len(classes), 'reported_count_sum': int(classes.Count.sum()),
            'duplicate_ids': int(classes.ID.duplicated().sum()),
            'id31_labels': classes.loc[classes.ID.eq(31)].to_dict('records'),
            'claim_gate': 'publisher counts and bilingual label direction conflict; no image/annotation verification; no legal interpretation'}
        monthly = self.load('data/processed/GT-02_monthly_counts.csv')
        self.results['GT02'] = {'monthly_rows': len(monthly), 'months_as_extracted': monthly.month.tolist(),
            'time_series_gate': 'three preliminary monthly values; no seasonal adjustment/forecast; source revision unresolved',
            'lineage_gate': 'use source h1/content period, not URL slug; first stored row has differing URL month text'}
        a = aggregates.copy(); a.region = a.region.map(normalize)
        provinces = a[~a.region.isin(EXCLUDED_REGIONS)]
        assert provinces.region.nunique() == 63
        changes = province_changes(a)
        self.table(changes, 'all_63_province_changes_verified')
        # Use drill-down arithmetic only. Baseline for causal RCA is unavailable.
        contributions = []
        reconcile = []
        for metric in ['crashes', 'deaths', 'injuries']:
            rows_a = provinces[(provinces.year.eq(2023)) & provinces.metric.eq(metric)].to_dict('records')
            rows_b = provinces[(provinces.year.eq(2024)) & provinces.metric.eq(metric)].to_dict('records')
            rows = self.call('root-cause-investigation', 'drilldown_analyzer', 'drill_down', rows_a, rows_b, ['region'], 'value')
            # "mix effect" here is algebraic and adds no identified mechanism.
            contributions.extend({'metric': metric, **{k: v for k, v in r.items() if k != 'mix_effect'}} for r in rows)
            for year in [2022, 2023, 2024]:
                total = a[a.region.eq('TỔNG SỐ') & a.year.eq(year) & a.metric.eq(metric)].value.iloc[0]
                prov = provinces[provinces.year.eq(year) & provinces.metric.eq(metric)].value.sum(min_count=63)
                other = a[a.region.eq('Khác') & a.year.eq(year) & a.metric.eq(metric)].value.iloc[0]
                reconcile.append({'year': year, 'metric': metric, 'national': total,
                    'province_sum': prov, 'other': other, 'residual': total-prov-other if pd.notna(other) else None,
                    'status': 'RECONCILED' if pd.notna(other) and total == prov+other else 'OTHER_MISSING_NOT_TESTABLE' if pd.isna(other) else 'MISMATCH'})
        self.table(pd.DataFrame(contributions), 'province_signed_contributions')
        self.table(pd.DataFrame(reconcile), 'national_reconciliation')
        self.results['GT01'] = {'province_count': 63, 'reconciliation': reconcile,
            'root_cause_gate': 'arithmetic decomposition only; no 30-day pre-change baseline/event log; no causal attribution',
            'contribution_denominator': 'net change in SUM OF 63 PROVINCES, excluding Other; signed, can exceed 100%; not risk share',
            'time_series_gate': '3 annual points; no seasonal model, forecast or intervention time series',
            'selection': 'T01-T06 remain purposeful historical examples, not highest-risk provinces'}
        literature = self.load('reports/literature_search_log.csv')
        records = self.load('reports/literature_search_records.csv')
        self.results['literature'] = {'api_rows_logged': int(literature.retrieved.sum()),
            'api_records_table': len(records), 'all_searches_complete': bool(literature.complete.all()),
            'scope': 'existing bounded narrative review rechecked; no new exhaustive search or full-text eligibility process claimed',
            'prior_art': 'IDEA-032 is close to curve warning; IDEA-042/035/025 close to educational app; no novelty established'}
        self.results['ideas'] = {'records': len(ideas), 'unique_ids': ideas.idea_id.nunique(),
            'title_only_mechanisms': int(ideas.mechanism_evidence.eq('TỪ TIÊU ĐỀ').sum()),
            'recorded_awarded': int(ideas.status_verified.eq('AWARDED').sum()),
            'education_editorial_count': int(ideas.solution_cluster_inferred.eq('Giáo dục học đường').sum()),
            'education_title_screen_count': int(education_title_mask(ideas.title_public).sum()),
            'claim_gate': 'no winner prediction, significance tests or award causal inference; inferred clusters are editorial labels',
            'missing_awards': 'not recorded is not demonstrated loss; unknown award rank stays unknown'}
        discovery = json.loads((RESEARCH / 'reports/discovery/traffic_findings.json').read_text(encoding='utf-8'))
        # Independently compare all six selected historical examples to recomputation.
        verified = []
        for r in discovery:
            if r['id'] in [f'T{i:02}' for i in range(1, 7)]:
                region = r['filter_spec']['region']
                values = changes[changes.region_as_recorded_2023_2024.eq(region)].iloc[0]
                assert all(np.isclose(values[k], v) for k, v in r['metrics'].items())
            verified.append({**r, 'checkpoint_status': 'RETAINED_AS_BOUNDED_DESCRIPTIVE_EVIDENCE',
                'current_2026_local_mechanism_validated': False})
        write_json(self.out / 'ten_traffic_discoveries_rechecked.json', verified)
        self.table(pd.DataFrame([{'id': r['id'], 'title_vi': r['title_vi'],
            'evidence_vi': r['evidence_vi'], 'source_ids': r['source_ids'],
            'temporal_scope': r['temporal_scope'], 'checkpoint_status': r['checkpoint_status'],
            'limitation_vi': r['limitation_vi']} for r in verified]), 'ten_traffic_discoveries_rechecked')

    def assumptions(self):
        skill, script = 'analysis-assumptions-log', 'assumptions_tracker'
        log = self.call(skill, script, 'new_log', 'Rà soát bổ sung giao thông và ý tưởng dự thi', 'Codex; tự rà soát, không phải phản biện độc lập')
        items = [
            ('data', 'Các bản ghi tỉnh 2023–2024 so sánh được về định nghĩa và ghi nhận.', 'Nguồn cùng bảng nhưng chưa có xác nhận địa phương.', 'low', 'high', 'Đối chiếu định nghĩa, kỳ báo cáo và thay đổi ghi nhận tại sáu địa bàn.', 'chưa xác minh'),
            ('statistical', '26 ngày ghép GT-07 là độc lập/trao đổi được để suy luận dân số.', 'Ngày rời rạc, đoạn đường lặp, thiết kế mẫu không rõ.', 'low', 'high', 'Giữ mô tả; muốn suy luận cần thiết kế mẫu và chuỗi đại diện.', 'không được chấp nhận cho suy luận'),
            ('data', 'Hai biểu diễn VNTraffic có cùng hình học hộp.', 'Đối chiếu multiset theo frame và bốn tọa độ, giữ số lần lặp.', 'high', 'high', 'Đếm từ TXT/JSON gốc độc lập.', 'đã xác minh trong snapshot'),
            ('business_logic', 'Nội dung treated/untreated là nhãn xử lý nhị phân.', 'Bản ghi 79 có cả hai trường; kế hoạch khác hoàn thành.', 'low', 'high', 'Đọc tự do và xác minh hiện trạng với đơn vị quản lý.', 'đã bác bỏ cách mã hóa nhị phân'),
            ('data', 'Thông tin nguy cơ Sơn La năm 2025 còn đúng hiện nay.', 'Chưa khảo sát, nhiều kế hoạch 2026.', 'low', 'high', 'Kiểm tra hiện trường và hồ sơ hoàn công trước pilot.', 'chưa xác minh'),
            ('business_logic', 'Ý tưởng thắng giải có thể dự đoán tiêu chí chấm cho mùa sau.', 'Thiếu toàn bộ bài dự thi, điểm và đối chứng; 70 cơ chế chỉ từ tên.', 'low', 'high', 'Không xây mô hình dự đoán giải từ mẫu này.', 'không được chấp nhận'),
            ('data', 'Tọa độ/lý trình đủ chính xác để nối điểm nguy cơ với sạt lở.', 'Chỉ có cùng tên tuyến; không có hình học tuyến/CRS đáng tin.', 'low', 'high', 'Thu tuyến đã kiểm chứng, hệ quy chiếu và đối chiếu lý trình; không tự geocode.', 'chưa xác minh'),
            ('business_logic', 'Nhu cầu thị trường và tính mới của các ứng viên đã có.', 'Chưa có phỏng vấn, hồ sơ kỹ thuật đầy đủ hoặc tra cứu tính mới hoàn chỉnh.', 'low', 'high', 'Xác minh người dùng/giải pháp có trước và nhu cầu; không suy từ thiếu title.', 'chưa xác minh'),
        ]
        for cat, assumption, rationale, confidence, impact, plan, status in items:
            number = self.call(skill, script, 'add_assumption', log, cat, assumption, rationale, confidence, impact, plan)
            log['assumptions'][-1].update(review_status_vi=status, alternatives_considered_vi='Giữ phạm vi mô tả hoặc thu dữ liệu phù hợp; không tự bù missing, không suy nhân quả.')
            if status.startswith('đã '):
                self.call(skill, script, 'validate_assumption', log, number, 'confirmed' if 'xác minh' in status else 'rejected', status)
        write_json(self.out / 'assumptions.json', log)
        report = self.call(skill, script, 'report', log)
        (self.out / 'assumptions_log.md').write_text('# Nhật ký giả định và quyết định\n\n' + report +
            '\n\nCác giả định chưa xác minh là rào cản đối với triển khai/khẳng định nhân quả. Báo cáo mô tả vẫn cung cấp được khi giữ rõ phạm vi.\n', encoding='utf-8')

    def figures(self, days, coverage):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from PIL import Image
        with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 10, 'pdf.fonttype': 42}):
            fig, axes = plt.subplots(2, 1, figsize=(10, 7), layout='constrained')
            dates = pd.to_datetime(coverage.day)
            axes[0].scatter(dates[coverage.observed], coverage.loc[coverage.observed, 'recorded_rows'],
                            c='#0072B2', marker='o', s=13, label='Ngày có bản ghi')
            axes[0].scatter(dates[~coverage.observed], np.full((~coverage.observed).sum(), -2500),
                            c='#666666', marker='x', s=10, label='Không quan sát (không phải 0)')
            axes[0].axhline(0, color='black', lw=.5)
            axes[0].set(ylabel='Số bản ghi/ngày', title='GT-07: độ phủ mẫu lịch sử 2020–2021, múi giờ UTC+7')
            axes[0].legend(fontsize=9)
            axes[1].scatter(pd.to_datetime(days.index), days['mean'], c='#0072B2', marker='o', s=25)
            axes[1].axhline(0, color='black', lw=.6)
            axes[1].set(ylabel='Chênh lệch đơn vị thô', xlabel='Ngày quan sát',
                        title='26 trung bình ngày sau ghép đoạn: cao điểm trừ giữa ngày; không nối khoảng trống')
            path = self.out / 'GT07_coverage_and_contrast.png'
            fig.savefig(path, dpi=180, facecolor='white')
            fig.savefig(self.out / 'GT07_coverage_and_contrast.pdf', facecolor='white')
            plt.close(fig)
        with Image.open(path) as img:
            metadata = {'pixels': img.size, 'dpi': img.info.get('dpi'), 'mode': img.mode,
                'sha256': sha(path), 'matplotlib': matplotlib.__version__,
                'destination': 'báo cáo nội bộ; không khẳng định chuẩn tạp chí hoặc chứng nhận accessibility',
                'alt_vi': '120 ngày có bản ghi trong 294 ngày; một ngày chiếm gần 40% mẫu. 26 chênh lệch ngày rời rạc, nhiều giá trị gần 0 và hai ngày âm mạnh.',
                'underlying_tables': ['tables/GT07_calendar_coverage.csv', 'tables/GT07_recomputed_days.csv'],
                'uncertainty': 'raw day means; no calibrated confidence intervals shown'}
        write_json(self.out / 'figure_manifest.json', metadata)

    def finish(self):
        qa = {}
        for name in ['all_63_province_changes_verified', 'ten_traffic_discoveries_rechecked',
                     'GT07_weighting_sensitivity', 'national_reconciliation']:
            df = pd.read_csv(self.out / 'tables' / (name + '.csv'))
            qa[name] = self.call('analysis-qa-checklist', 'qa_runner', 'run_qa', df)
        write_json(self.out / 'automated_qa.json', qa)
        for r in self.skill_records:
            if r['skill'] in ['geopandas', 'statsmodels']:
                r['use'] = 'READ_NOT_APPLIED'
                r['reason'] = 'no validated spatial join input / no defensible new model; Python libraries not installed in research interpreter'
            else:
                r['use'] = 'APPLIED_PROCEDURAL_GUIDANCE'
        write_json(self.out / 'skills_used.json', self.skill_records)
        write_json(self.out / 'skill_execution_log.json', self.calls)
        write_json(self.out / 'input_checksums.json', self.inputs)
        write_json(self.out / 'measured_rechecks.json', self.results)
        write_json(self.out / 'environment.json', {'python': sys.version, 'platform': platform.platform(),
            'pandas': pd.__version__, 'numpy': np.__version__,
            'scipy': __import__('scipy').__version__,
            'note': 'existing Python 3.10 environment retained; methodological guidance used; not claimed to match newer pinned skill stacks'})


def protected_files():
    roots = [PROJECT / 'data', RESEARCH / 'input', RESEARCH / 'data', RESEARCH / 'reports/discovery']
    files = {p for root in roots for p in root.rglob('*') if p.is_file()}
    files.update(p for p in (RESEARCH / 'reports').glob('*') if p.is_file())
    return {str(p.relative_to(PROJECT)).replace('\\', '/'): sha(p) for p in sorted(files)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=RESEARCH / 'reports/revalidation_2026_11_19_v2')
    parser.add_argument('--skill-root', type=Path, default=Path.home() / '.agents/skills')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; choose a NEW --output path. Existing results are preserved.')
    before = protected_files()
    cp = Checkpoint(args.output, args.skill_root)
    a, s, h, land, ideas = cp.audit()
    days, coverage = cp.validate_contrast(s)
    cp.other_sources(a, ideas)
    cp.assumptions()
    cp.figures(days, coverage)
    cp.finish()
    after = {name: sha(PROJECT / name) for name in before}
    changed = [name for name in before if before[name] != after[name]]
    write_json(args.output / 'preservation_check.json', {'files_checked': len(before),
        'changed_files': changed, 'before_sha256': before, 'verified_utc': dt.datetime.now(dt.timezone.utc).isoformat()})
    if changed:
        raise RuntimeError('Protected inputs changed: ' + str(changed))
    from research_checkpoint_reports import render_reports
    render_reports(args.output)
    print(json.dumps(clean({'output': str(args.output), 'protected_files_unchanged': len(before),
                            'GT07': cp.results['GT07'], 'GT09': cp.results['GT09']}), ensure_ascii=True))


if __name__ == '__main__':
    main()
