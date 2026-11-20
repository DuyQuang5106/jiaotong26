"""Read-only scan of supplied idea inventories for the track-2 decision memo.

Only the tabular scan is automated; candidate selection and verified web-claim
appraisal are analyst decisions in the accompanying Markdown/JSON files.
No award predictor, safety-effect estimate or new source acquisition is run.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from discover_opportunities import PROJECT, RESEARCH, workbook_table
from parse_inventory import read_workbook


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan(output):
    if output.exists():
        raise FileExistsError('Choose a new output directory; existing research is preserved.')
    paths = [PROJECT / 'data/traffic_contest_ideas_2022_2025.xlsx',
             PROJECT / 'data/global_traffic_contest_ideas_2023_2026.xlsx']
    hashes = {str(p.relative_to(PROJECT)).replace('\\', '/'): digest(p) for p in paths}
    domestic, global_ideas = [workbook_table(read_workbook(p)[0]).fillna('') for p in paths]
    assert len(domestic) == domestic.idea_id.nunique() == 73
    assert len(global_ideas) == global_ideas.idea_id.nunique() == 121
    # These are editorial mappings, NOT independently validated topic memberships.
    theme2 = global_ideas['2026_theme_similarity_proposed'].str.startswith('2')
    cargo_title = domestic.title_public.str.contains('cồng kềnh|quá khổ', case=False, regex=True)
    selected = ['WIDEA-008', 'WIDEA-010', 'WIDEA-014', 'WIDEA-018',
                'WIDEA-059', 'WIDEA-060', 'WIDEA-072', 'WIDEA-073',
                'WIDEA-076', 'WIDEA-087', 'WIDEA-111', 'WIDEA-116']
    reasons = {
        'WIDEA-008': 'Chính sách tài xế: liên quan khuyến khích, không trực tiếp đo tải.',
        'WIDEA-010': 'Quy trình và thời gian giao hàng; không là hiệu quả tải hàng tại Việt Nam.',
        'WIDEA-014': 'Ưu tiên đọc: quá khổ/quá tải; mô tả chi tiết kỹ thuật còn thiếu.',
        'WIDEA-018': 'Gắn phương tiện truyền thống với dịch vụ; đối tượng/điều kiện Việt Nam chưa rõ.',
        'WIDEA-059': 'Cho thuê phương tiện hàng: prior art phương án thay thế.',
        'WIDEA-060': 'Nano-hub: prior art trung chuyển; phân biệt nơi pilot và xuất xứ công ty.',
        'WIDEA-072': 'Thiết kế phương tiện khác; không tự đủ điều kiện lưu hành tại Việt Nam.',
        'WIDEA-073': 'Thu gom rác/định tuyến; không tự là chống chở quá khổ.',
        'WIDEA-076': 'Giám sát khu lên xuống hàng; không tự là kiểm tra tải xe máy.',
        'WIDEA-087': 'Kiểm soát xe tải; khác đối tượng track 2.',
        'WIDEA-111': 'Kiểm tra trước vận hành; xe tải/tanker khác xe máy/thô sơ.',
        'WIDEA-116': 'Định tuyến rủi ro; không xử lý trực tiếp hàng quá khổ.',
    }
    columns = ['idea_id', 'title_public', 'year', 'competition', 'mechanism_short',
               'mechanism_evidence', 'status_verified', 'entry_evidence_url',
               '2026_theme_similarity_proposed', 'country_or_team_origin', 'host_city']
    review = global_ideas[global_ideas.idea_id.isin(selected)][columns].copy()
    review['selection_reason_vi'] = review.idea_id.map(reasons)
    output.mkdir(parents=True)
    review.to_csv(output / 'international_prior_art_triage.csv', index=False, encoding='utf-8-sig')
    summary = {
        'as_of_local_date': '2026-11-19', 'timezone': 'Asia/Bangkok',
        'domestic_records': len(domestic), 'international_records': len(global_ideas),
        'international_unique_record_ids': global_ideas.idea_id.nunique(),
        'international_year_missing': int(global_ideas.year.eq('').sum()),
        'international_mechanism_evidence': dict(Counter(global_ideas.mechanism_evidence)),
        'international_editorial_track2_count': int(theme2.sum()),
        'international_editorial_track2_ids': global_ideas.loc[theme2, 'idea_id'].tolist(),
        'domestic_titles_matching_cargo_terms': int(cargo_title.sum()),
        'domestic_cargo_terms': ['cồng kềnh', 'quá khổ'],
        'records_triaged_for_related_prior_art': len(review),
        'selection_method': '11 editorial track-2 records plus WIDEA-111 as pre-trip inspection analogy; all retained with limitations',
        'interpretation_limits': [
            'Counts are records, not independent studies, unique products, market share or winner probabilities.',
            'Missing competition year remains missing; last_reviewed is not an event date.',
            'Editorial track mapping includes weak/indirect analogies; not all 11 address unsafe bulky loads.',
            'Zero title matches does not demonstrate novelty or absence of existing products.',
            'Web verification of selected claims is recorded separately; no full technical review of 121 projects claimed.',
        ],
        'input_sha256': hashes, 'script_sha256': digest(Path(__file__)),
    }
    assert {str(p.relative_to(PROJECT)).replace('\\', '/'): digest(p) for p in paths} == hashes
    (output / 'inventory_scan.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=RESEARCH / 'reports/track2_2026_11_19')
    scan(parser.parse_args().output)
