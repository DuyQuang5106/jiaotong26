"""Compare CHỞ VỪA app measurements with tape-measure values from the field-mode CSV.

Usage: python -X utf8 traffic-data-research/src/cho_vua_eval.py <chovua_checks.csv> --out <dir>

Writes eval.json and eval_vi.md. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean

HEADER = ['id', 'at', 'vehicle', 'item', 'ref_kind', 'overall',
          'side_left_min', 'side_left_max', 'side_right_min', 'side_right_max',
          'rear_min', 'rear_max', 'height_min', 'height_max',
          'tape_side_left', 'tape_side_right', 'tape_rear', 'tape_height', 'note']

DIMS = ['side_left', 'side_right', 'rear', 'height']
# Luật 36/2024 Điều 33 khoản 5 — motorbike limits in cm.
MOTORBIKE_LIMIT_CM = {'side_left': 30, 'side_right': 30, 'rear': 50, 'height': 200}


def _num(v: str | None) -> float | None:
    if v is None or str(v).strip() == '':
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _light(lo: float, hi: float, limit: float) -> str:
    if hi <= limit:
        return 'green'
    if lo > limit:
        return 'red'
    return 'yellow'


def evaluate(rows: list[dict]) -> dict[str, dict]:
    """Per reference kind: pairs, MAE of the interval midpoint, coverage, yellow rate, false greens.

    A pair is one dimension with both an app interval and a tape value. A dimension with only
    one of the two is counted in `skipped`. Light-based metrics use motorbike limits only.
    """
    acc: dict[str, dict] = {}
    for r in rows:
        g = acc.setdefault(r.get('ref_kind') or 'none', {'rows': 0, 'errors': [], 'covered': 0, 'lights': [], 'false_green': 0, 'skipped': 0})
        g['rows'] += 1
        for d in DIMS:
            lo, hi, tape = _num(r.get(f'{d}_min')), _num(r.get(f'{d}_max')), _num(r.get(f'tape_{d}'))
            has_app = lo is not None and hi is not None
            if has_app != (tape is not None):
                g['skipped'] += 1
            if not (has_app and tape is not None):
                continue
            g['errors'].append(abs((lo + hi) / 2 - tape))
            g['covered'] += lo <= tape <= hi
            if r.get('vehicle') == 'motorbike':
                limit = MOTORBIKE_LIMIT_CM[d]
                light = _light(lo, hi, limit)
                g['lights'].append(light)
                g['false_green'] += light == 'green' and tape > limit
    out = {}
    for kind, g in acc.items():
        n = len(g['errors'])
        out[kind] = {
            'rows': g['rows'],
            'pairs': n,
            'mae_cm': round(mean(g['errors']), 2) if n else None,
            'coverage': round(g['covered'] / n, 3) if n else None,
            'yellow_rate': round(g['lights'].count('yellow') / len(g['lights']), 3) if g['lights'] else None,
            'false_green': g['false_green'],
            'skipped': g['skipped'],
        }
    return out


def _report_vi(res: dict[str, dict], source: str) -> str:
    lines = [
        '# Đánh giá đo kích thước CHỞ VỪA',
        '',
        f'Nguồn: `{source}`. So số đo của app (khoảng sai số) với số đo thước. '
        'Đèn tính theo giới hạn xe máy (Luật 36/2024, Điều 33 khoản 5).',
        '',
        '| Nguồn tỷ lệ | Dòng | Cặp đo | Sai số TB (cm) | coverage | yellow_rate | false_green | skipped |',
        '|---|---|---|---|---|---|---|---|',
    ]
    for kind, r in sorted(res.items()):
        lines.append(f"| {kind} | {r['rows']} | {r['pairs']} | {r['mae_cm']} | {r['coverage']} | {r['yellow_rate']} | {r['false_green']} | {r['skipped']} |")
    lines += ['', '`false_green`: app báo xanh nhưng số đo thước vượt giới hạn — lỗi nguy hiểm nhất.',
              'Không chỉnh hằng số sai số trên chính mẫu dùng để báo kết quả này.', '']
    return '\n'.join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('csv')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    with open(a.csv, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    res = evaluate(rows)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'eval.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'eval_vi.md').write_text(_report_vi(res, a.csv), encoding='utf-8')
    print(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':
    main()
