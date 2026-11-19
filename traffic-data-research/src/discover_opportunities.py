"""Evidence-bounded contest patterns and geographically specific discovery leads.

Read-only inputs. Writes a new synthesis under reports/discovery, preserving the
original research run and distinguishing reported mechanisms from field results.
Run from repository root: python traffic-data-research/src/discover_opportunities.py
"""
import datetime as dt
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

from parse_inventory import parse, read_workbook

PROJECT = Path(__file__).resolve().parents[2]
RESEARCH = PROJECT / 'traffic-data-research'
OUT = RESEARCH / 'reports/discovery'
TABLES = OUT / 'tables'
EXCLUDED_REGIONS = {
    'TỔNG SỐ', 'Khác', 'Đồng bằng sông Hồng', 'Trung du và miền núi phía Bắc',
    'Bắc Trung Bộ và Duyên hải miền Trung', 'Tây Nguyên', 'Đông Nam Bộ',
    'Đồng bằng sông Cửu Long',
}

def normalize(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', str(value))).strip()

def education_title_mask(series):
    return series.str.contains(r'học sinh|học đường|cổng trường|\bE[– -]?learning\b|SafeEduQR|Thư viện An toàn|Trò chơi|\bTHCS\b|\bTHPT\b',case=False,regex=True,na=False)

def workbook_table(sheet):
    headers = {re.sub(r'\d', '', key): value for key, value in sheet['rows'][0].items()}
    return pd.DataFrame([
        {headers.get(re.sub(r'\d', '', key), key): value for key, value in row.items()}
        for row in sheet['rows'][1:] if any(row.values())
    ])

def read_ideas(path):
    sheets = read_workbook(path)
    ideas = workbook_table(next(s for s in sheets if s['xml'] == 'xl/worksheets/sheet1.xml'))
    assert len(ideas) == 73 and ideas.idea_id.nunique() == 73
    assert len(ideas.columns) == 23
    return ideas, workbook_table(sheets[1])

def province_changes(aggregates):
    a = aggregates.copy()
    a['region'] = a.region.map(normalize)
    a = a[~a.region.isin(EXCLUDED_REGIONS)]
    assert a.region.nunique() == 63
    assert not a.duplicated(['region', 'year', 'metric']).any()
    wide = a.pivot(index='region', columns=['year', 'metric'], values='value')
    rows = []
    for region, values in wide.iterrows():
        row = {'region_as_recorded_2023_2024': region}
        for metric in ['crashes', 'deaths', 'injuries']:
            old, new = float(values[(2023, metric)]), float(values[(2024, metric)])
            row.update({f'{metric}_2023': old, f'{metric}_2024': new,
                        f'{metric}_delta': new-old,
                        f'{metric}_pct_change': (new-old)/old*100 if old > 0 else None})
        rows.append(row)
    return pd.DataFrame(rows)

def save_table(frame, name):
    frame.to_csv(TABLES/name, index=False, encoding='utf-8-sig')

def json_write(path, content):
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def record(identifier, title, evidence, interpretation, niche, next_test, limitation, **metadata):
    return dict(id=identifier, title_vi=title, evidence_vi=evidence,
                interpretation_vi=interpretation, opportunity_hypothesis_vi=niche,
                next_test_vi=next_test, limitation_vi=limitation, **metadata)

def idea_patterns(ideas):
    cluster = lambda value: ideas[ideas.solution_cluster_inferred.eq(value)]
    n = len(ideas)
    regulation = cluster('Điều tiết / đèn tín hiệu')
    education = cluster('Giáo dục học đường')
    blind = cluster('Điểm mù / va chạm')
    awards = lambda d: int(d.status_verified.eq('AWARDED').sum())
    ids = lambda d: ';'.join(d.idea_id)
    rows = []
    def add(i, title, subset, evidence, meaning, niche, test, limit, **kw):
        rows.append(record(f'I{i:02}', title, evidence, meaning, niche, test, limit,
                           source='data/traffic_contest_ideas_2022_2025.xlsx#IDEAS',
                           idea_ids=ids(subset), n_records=len(subset), denominator=n,
                           evidence_type='MEASURED WORKBOOK PATTERN; award claims verified only for the cited subset', **kw))
    add(1, 'Điều tiết và đèn tín hiệu là họ ý tưởng lặp qua nhiều mùa, không còn là điểm mới tự thân.', regulation,
        f'{len(regulation)}/{n} bản ghi mang nhãn điều tiết/đèn tín hiệu; xuất hiện đủ {regulation.year.nunique()} năm; {awards(regulation)} được workbook ghi có giải.',
        'Đổi thuật toán hoặc thêm AI chưa đủ cho thấy khác biệt với các hệ thống đã có.',
        'Một luồng rẽ/một nút/một khung giờ có trễ hoặc xung đột được đo và có người vận hành cụ thể.',
        'Đối chiếu IDEA-033/043/054/060/064; đo so với quy tắc hiện hành, không chỉ so với không có điều khiển.',
        'Nhãn nhóm do người tổng hợp gán, mẫu thiên về bài được công bố; không phải mật độ cạnh tranh toàn thị trường.')
    add(2, 'Giáo dục học đường đã có cả nội dung, trò chơi lẫn quy trình kiểm soát.', education,
        f'{len(education)} bản ghi được gán nhóm giáo dục, {awards(education)} ghi có giải. IDEA-042 E-learning: Nhì 2023; IDEA-035 thư viện: Ba 2024; IDEA-025 SafeEduQR: có giải 2025.',
        'Một app quiz/QR/game chung chung có ý tưởng có trước gần; cần chứng minh kỹ năng hoặc hành vi nào còn thiếu.',
        'Học sinh dùng xe điện tại một trường, một tình huống như rẽ trái/nhập dòng đã được quan sát khó khăn.',
        'Đo trước, sau và duy trì 1–2 tuần bằng tình huống tương đương; kiểm tra hành vi nếu có phép.',
        'Nhóm biên tập chứa cả bài không chuyên học sinh (ví dụ IDEA-067); phải rà title và hồ sơ, không coi cả 10 là đối thủ trực tiếp.')
    add(3, 'Điểm mù/va chạm có nhiều biến thể và nhiều mức giải; thêm cảnh báo không tự tạo khác biệt.', blind,
        f'{len(blind)} bản ghi trong nhóm, {awards(blind)} ghi có giải; IDEA-032 khúc cua Nhì 2024; IDEA-011 Vành đai ánh sáng Nhất 2025.',
        'Cần làm rõ cảnh báo cho ai, trước tình huống gì và người nhận phải làm gì sau đó.',
        'Một cặp xe đối đầu trên đường cong hẹp, thay vì cảnh báo mọi nguy cơ bằng cùng một âm báo.',
        'Đọc hồ sơ IDEA-032 và so vùng phủ, cảnh báo sai, hành động người lái và bảo trì trước đề xuất phần cứng.',
        'Giải thưởng không chứng minh giảm va chạm; cơ chế phần lớn mới suy từ tên.')
    actor_ids = ['IDEA-012', 'IDEA-014', 'IDEA-016', 'IDEA-028']
    add(4, 'Đổi đối tượng và điểm ra quyết định có thể tạo một phân khúc khác, nhưng chưa chứng minh mới.', ideas[ideas.idea_id.isin(actor_ids)],
        'Bốn ví dụ: mũ cho người đi xe máy (012), cảnh báo cho xe tải lớn (014), hỗ trợ phanh xe máy (016), xác thực quyền điều khiển (028); đều ghi có giải.',
        'Cùng chủ đề an toàn nhưng đầu vào, người sử dụng và hành động đầu ra khác nhau.',
        'Mô tả ngách bằng người dùng + địa điểm + thời điểm + quyết định, không chỉ bằng tên công nghệ.',
        'Phỏng vấn người thực hiện quyết định; kiểm xem họ có thể và muốn hành động khi nhận thông tin không.',
        'Chỉ đối chiếu tên gọi, không khẳng định kiến trúc kỹ thuật hay quyền sáng chế khác nhau.')
    physical_ids = ['IDEA-040', 'IDEA-041', 'IDEA-049']
    add(5, 'Giải pháp được gọi tên bằng thiết bị/quy trình đơn giản cũng được ghi nhận.', ideas[ideas.idea_id.isin(physical_ids)],
        '2023: móc khóa nhắc không lái khi uống rượu (040) và trụ đảo di động (041) ghi Nhì; cọc tiêu tái chế cổng trường (049) ghi Khuyến khích.',
        'Không có cơ sở buộc ý tưởng tốt phải là AI; nên bắt đầu bằng cách đơn giản nhất có thể kiểm nghiệm.',
        'Tổ chức luồng đón trả tại một cổng trường hoặc kiểm tra báo hiệu tại hai đoạn đường cụ thể.',
        'So baseline thủ công/vạch chỉ dẫn/quy trình sẵn có với phương án số, đo chi phí vận hành và outcome cùng mẫu.',
        'Tên không nêu AI không chứng minh hồ sơ không có công nghệ; không suy ưu thế chấm giải của đồ đơn giản.')
    local_ids = ['IDEA-050', 'IDEA-051', 'IDEA-055', 'IDEA-062', 'IDEA-065']
    local = ideas[ideas.idea_id.isin(local_ids)]
    add(6, 'Bài toán có địa danh cụ thể đã có chỗ trong các bài được công bố và đạt giải.', local,
        f'{awards(local)}/{len(local)} ví dụ tên nêu địa bàn có nhãn có giải. Đắk Nông/đường Hồ Chí Minh (062): Ba 2022; hai cổng trường Lâm Đồng (051): Khuyến khích 2023.',
        'Không cần bắt đầu bằng sản phẩm toàn quốc; một cơ chế địa phương đủ rõ có thể làm hồ sơ có căn cứ.',
        'Một cụm lý trình hoặc một trường có đơn vị đồng ý cho đo baseline và kiểm chứng.',
        'Xác nhận người dùng địa phương, quyền khảo sát, vấn đề lặp lại và khả năng mở rộng sau pilot.',
        'Đây là tập ví dụ chọn theo địa danh, không dùng 4/5 làm xác suất đạt giải; không chứng minh vấn đề ở đó còn tồn tại năm 2026.')
    y25 = ideas[ideas.year.eq('2025')]
    focus = y25[y25.theme_original.eq('Lướt mạng – Mất mạng')]
    add(7, 'Họ giải pháp đi theo chủ đề mùa thi; không được mang lý do đạt giải năm cũ áp sang năm mới.', y25,
        f'2025 có {len(y25)} bài, ba chủ đề × 10 bài; {len(focus[focus.solution_cluster_inferred.eq("Chống phân tâm")])}/10 bài trong Lướt mạng–Mất mạng được gán chống phân tâm.',
        'Một giải pháp từng hợp chủ đề có thể không đúng đối tượng/đầu ra của năm 2026.',
        'Với chủ đề 2, tập trung xe máy/thô sơ/tự chế chở hàng cồng kềnh; xe tải dài tại đường cong không tự khớp.',
        'Viết một câu nối đúng đối tượng, vấn đề, cơ chế và outcome với thể lệ 2026 đã kiểm tra.',
        'Không so thứ hạng giữa mùa/hạng mục; không dùng trọng số đề xuất của sheet RUBRIC làm tiêu chí chính thức.')
    top = y25[y25.top3_online_vote_2025.eq('YES')]
    other_awarded = y25[y25.status_verified.eq('AWARDED') & y25.top3_online_vote_2025.ne('YES')]
    add(8, 'Bình chọn, có giải và hạng giải là ba tín hiệu khác nhau.', y25,
        f'{len(top)} bài top bình chọn; workbook ghi 3 Nhất, 2 Nhì, 4 có giải chưa rõ hạng. Có {len(other_awarded)} bài ghi có giải mà không nằm top bình chọn.',
        'Không lấy lượt thích hay sự chú ý làm thước đo hiệu quả an toàn; cũng không bỏ qua chất lượng chứng minh.',
        'Demo người dùng hiểu được, kèm bảng kết quả so sánh độc lập, thay vì chỉ truyền thông.',
        'Tách số bình chọn, điểm ban giám khảo và kết quả can thiệp; hiện chưa có điểm giám khảo để mô hình hóa.',
        'Chỉ mô tả 30 bài shortlist 2025; không suy xác suất thắng hoặc nguyên nhân không được giải.')
    cargo = ideas[ideas.title_public.str.contains('cồng kềnh|quá khổ', case=False, regex=True, na=False)]
    add(9, 'Hàng cồng kềnh ít hiện diện trong tên bài của mẫu này: một hướng tìm kiếm, chưa phải khoảng trống thị trường.', cargo,
        f'{len(cargo)}/{n} tên bài khớp từ khóa cồng kềnh hoặc quá khổ. Sheet CHU_DE_2026 cũng ghi chưa nhận diện dự án chuyên biệt rõ.',
        'Đây là khoảng trống trong mẫu công bố, có thể còn dự án khác hoặc cơ chế không thể hiện qua tên.',
        'Một luồng giao hàng bằng xe máy ở một chợ/cửa hàng, với khó khăn và giải pháp thay thế được người dùng xác nhận.',
        'Đếm tổng chuyến và chuyến chở hàng theo định nghĩa độc lập, phỏng vấn người chở/chủ cửa hàng, tra thêm sản phẩm có trước.',
        'Chưa có địa bàn, nhu cầu trả tiền, tần suất nguy hiểm hoặc bằng chứng toàn quốc chưa có sản phẩm; không dùng nhãn abnormal thay cargo label.')
    weak = ideas[ideas.mechanism_evidence.eq('TỪ TIÊU ĐỀ')]
    add(10, 'Danh mục giải thưởng chỉ giúp tìm đối thủ/ý tưởng có trước, không tiết lộ công thức thắng.', ideas,
        f'{len(weak)}/{n} mô tả cơ chế suy từ tiêu đề; 3 từ báo mô tả. 55 bản ghi ghi có giải, 14 shortlist không có tên trong DS giải, 4 chưa xác minh kết quả.',
        'Thiếu hồ sơ kỹ thuật và điểm giám khảo nên chưa thể học quan hệ nhân quả giữa tính năng và đạt giải.',
        'Mỗi ý tưởng mới phải có đối chiếu cơ chế gần nhất và một phép thử có khả năng bác bỏ lợi ích.',
        'Đọc hồ sơ các IDEA gần nhất; phân biệt claim sản phẩm, đo kỹ thuật và tác động an toàn.',
        'Không huấn luyện mô hình winner trên mẫu này; không gán bài không thấy giải là thất bại kỹ thuật.')
    assert len(rows) == 10
    return rows

def traffic_findings(changes, hazards, landslides, manifest):
    rows = []
    selected = [
        ('Hà Nội', 'Thương tích tăng trong khi tử vong gần như đi ngang.',
         'Chọn một cụm đường/nút để xem loại va chạm gây thương tích; không chỉ tối ưu chỉ số tử vong.',
         'Cần hồ sơ vụ việc có tọa độ, loại phương tiện, tuổi và exposure; chưa có bằng chứng đây là tai nạn học sinh.'),
        ('Thái Nguyên', 'Số bị thương gần gấp đôi dù số chết giảm.',
         'Khảo sát cơ chế va chạm gây thương tích ở một địa điểm; nếu muốn chủ đề học sinh phải xác minh riêng xe điện và nhóm tuổi.',
         'Tăng ghi nhận hoặc thay định nghĩa có thể giải thích biến động; chưa có cơ cấu học sinh/xe máy.'),
        ('Đắk Lắk', 'Cả số vụ, số chết và số bị thương đều tăng trong bảng.',
         'Xin dữ liệu vụ việc để chọn một cơ chế và một hành lang cụ thể trước chọn cảnh báo hoặc giáo dục.',
         'Không đủ biết tuyến nào, giờ nào hoặc loại xe nào đóng góp; không tự gán nguyên nhân đường đèo/rượu bia.'),
        ('TP. Hồ Chí Minh', 'Các tổng năm giảm nhưng gánh nặng ghi nhận vẫn còn.',
         'Đánh giá phần tồn tại ở một nút có hàng chờ/xung đột được đo; đối chiếu với ITS và giải pháp đang vận hành.',
         'Không quy giảm cho camera/AI/đèn; GT-07 là dữ liệu 2020–2021, không nối thành baseline năm 2024/2026.'),
        ('Hải Dương', 'Vụ và thương tích tăng cùng với số chết.',
         'Một địa bàn theo ranh giới cũ cần truy vết về đường/nút hiện tại; đo trước khi chọn phân khúc người dùng.',
         'Tên Hải Dương là nhãn địa giới của bảng 2023–2024, không là khẳng định đơn vị hành chính hiện tại; chưa có crosswalk.'),
        ('Đồng Tháp', 'Cả ba tổng tăng mạnh, cần phân rã tại địa phương.',
         'Tìm cụm va chạm lặp lại và nhóm phương tiện cụ thể từ hồ sơ địa phương, rồi kiểm chứng hiện trường.',
         'Chưa biết tác động thay đổi ghi nhận; không suy từ địa danh ra nguy cơ bến phà, cầu, mưa hay xe nông nghiệp.'),
    ]
    for i, (region, title, niche, limit) in enumerate(selected, 1):
        values = changes[changes.region_as_recorded_2023_2024.eq(region)].iloc[0]
        evidence = '; '.join(f'{label}: {int(values[metric+"_2023"]):,} → {int(values[metric+"_2024"]):,} ({values[metric+"_pct_change"]:+.2f}%)'
                             for metric, label in [('crashes','vụ'),('deaths','chết'),('injuries','bị thương')])
        rows.append(record(f'T{i:02}', region+' — '+title, evidence,
            'Tín hiệu mô tả để quyết định xin dữ liệu chi tiết, chưa là nguy cơ trên mỗi chuyến và chưa chỉ ra cơ chế.', niche,
            'Đối chiếu số với công an/ban ATGT địa phương và định nghĩa kỳ báo cáo; lấy mẫu số lưu lượng cùng cửa sổ thời gian.',
            limit+' Có cờ tổng vùng NSO không khớp tỉnh thành phần; không dùng tổng vùng để xếp hạng. Không suy hiện trạng 2026.',
            geographic_scope=region+' theo địa giới trong nguồn 2023–2024', temporal_scope='2023 vs 2024', source_ids='GT-01',
            evidence_type='MEASURED RESULT FROM REPORTED COUNTS; comparability not independently validated',
            evidence_grade='E1 reported counts; derived arithmetic reproducible',
            analysis_table='tables/province_changes_2023_2024.csv', filter_spec={'region':region,'years':[2023,2024]},
            metrics={k:float(v) for k,v in values.items() if k!='region_as_recorded_2023_2024'},
            denominator='previous-year count for percent changes; no road-user exposure denominator',
            selection='purposeful examples after descriptive scan of all 63 historic provinces; not highest-risk ranking'))
    q = hazards[hazards.record_id.eq(9)].iloc[0]
    rows.append(record('T07','Quỳnh Nhai, Sơn La — đường cong hẹp với cơ chế xe dài phải mở lái sang làn đối diện.',
        'GT-10 bản ghi 9, QL.6B Km25+00–Km25+210: nguồn ghi mặt đường 5,50 m, che khuất tầm nhìn và xe dài/kích thước lớn cần mở lái sang làn đối diện.',
        'Có mô tả cơ chế cụ thể để xây thiết kế quan sát; chưa đo số lần lấn làn, xung đột hoặc tai nạn.',
        'Hỗ trợ nhận biết/nhường đường khi xe dài gặp xe ngược chiều tại một khúc cua, có cơ quan quản lý và người lái tham gia thiết kế.',
        'Xác minh lý trình rút gọn, mặt cắt, trạng thái xử lý; đếm lượt xe dài, lượt có xe đối diện và lượt lấn làn có chấm độc lập.',
        'Một mô tả cơ quan, không phải nghiên cứu hiệu quả. Xe tải dài không đồng nghĩa xe máy chở hàng cồng kềnh; chỉ phù hợp chủ đề 1 nếu giải trình được điểm nóng. IDEA-032 là ý tưởng có trước gần.',
        geographic_scope='QL.6B, địa danh Quỳnh Nhai theo nguồn', temporal_scope='snapshot 02/12/2025', source_ids='GT-10',
        evidence_type='VERIFIED SOURCE FACT + MEASURED ROW SELECTION; no field measurement', evidence_grade='E1 mechanism reported, not independently observed',
        analysis_table='tables/local_mechanism_evidence.csv', filter_spec={'record_ids':[9]}, metrics={'selected_records':1,'reported_road_surface_width_m':5.5},
        denominator='1 selected record out of 107; no vehicle/crash denominator', selection='mechanism specificity, not highest crash risk'))
    missing_ids = [13,14]
    m = hazards[hazards.record_id.isin(missing_ids)]
    assert len(m)==2 and m.condition.str.contains('chưa hoàn chỉnh',case=False).all()
    rows.append(record('T08','Mường La, Sơn La — hai đoạn có mô tả báo hiệu chưa hoàn chỉnh.',
        'GT-10 bản ghi 13–14: QL.279D Km87+200–Km87+400 và Km87+900–Km88+300; cả hai mô tả đường cong, tầm nhìn hạn chế, hệ thống báo hiệu chưa hoàn chỉnh.',
        'Khoảng thiếu hụt được ghi đích danh; cần kiểm lại sau kế hoạch bảo trì năm 2026 trước đề xuất thiết bị mới.',
        'Kiểm chứng khả năng nhìn/hiểu cảnh báo hiện hữu ban ngày và ban đêm; ưu tiên khắc phục đúng thành phần thiếu.',
        'Làm checklist hiện trường cùng đơn vị quản lý; so phương án báo hiệu chuẩn hiện hành với cải tiến bằng nhận biết nguy cơ trong bài thử an toàn.',
        'Trạng thái 2025 có thể đã thay đổi; không đồng nghĩa hai đoạn hiện vẫn thiếu biển hoặc đã gây tai nạn. Không tự lắp thiết bị công cộng.',
        geographic_scope='QL.279D, địa danh Mường La theo nguồn', temporal_scope='snapshot 02/12/2025', source_ids='GT-10',
        evidence_type='VERIFIED SOURCE FACT + MEASURED ROW SELECTION; no field measurement', evidence_grade='E1 maintenance gap reported, current status unknown',
        analysis_table='tables/local_mechanism_evidence.csv', filter_spec={'record_ids':missing_ids}, metrics={'selected_records':2,'corridor_records':5},
        denominator='2 selected records / 5 QL.279D records, not infrastructure prevalence', selection='explicit text gap; no crash outcome'))
    moc = hazards[hazards.road.eq('QL.43')]
    assert len(moc)==23 and moc.commune.eq('Mộc Châu').all()
    rows.append(record('T09','Mộc Châu, Sơn La — QL.43 có một cụm kiểm kê đủ lớn để chọn điểm khảo sát.',
        f'{len(moc)}/{len(hazards)} bản ghi GT-10 thuộc QL.43 và cùng ghi địa danh Mộc Châu ({len(moc)/len(hazards)*100:.2f}% danh mục). Bản ghi 30–31: Km46+700–Km46+780 và Km46+810–Km46+980.',
        'Có tập địa điểm để sàng lọc một pilot nhiều khúc cua; số bản ghi không chứng minh QL.43 rủi ro nhất.',
        'Hỗ trợ nhận biết chuỗi khúc cua cho nhóm người lái được xác minh cần trợ giúp; tránh cảnh báo dày đặc gây quá tải.',
        'Xác minh các lý trình, đo lưu lượng và khảo sát người lái quen/lạ đường; kiểm tra cảnh báo sai và khả năng hành động.',
        'Không có mẫu số chiều dài/xe, mật độ du khách hoặc tai nạn; không suy thị trường du lịch hay nhu cầu trả tiền. Không xác nhận nguy cơ vật lý mới.',
        geographic_scope='QL.43, Mộc Châu theo nguồn', temporal_scope='snapshot 02/12/2025', source_ids='GT-10',
        evidence_type='MEASURED INVENTORY CONCENTRATION; reported site characteristics', evidence_grade='E2 only for reproducible inventory share, not crash risk',
        analysis_table='tables/sonla_corridor_counts.csv', filter_spec={'road':'QL.43'}, metrics={'records':23,'all_hazard_records':107,'share_percent':23/107*100},
        denominator='107 selected inventory records, not road network length or trips', selection='inventory concentration'))
    curves = hazards[hazards.road.eq('QL.4G')]
    slides = landslides[landslides.road.eq('QL.4G')]
    rows.append(record('T10','QL.4G, Sơn La — một hành lang có hai nhóm nguy cơ được ghi nhận.',
        f'{len(curves)} bản ghi GT-10 đường cong/tầm nhìn và {len(slides)}/{len(landslides)} bản ghi GT-11 nguy cơ sạt lở cùng mang tên QL.4G. Phân bố: cong từ Km22+280 tới Km42+800; sạt lở từ Km16+050 tới Km117+800.',
        'Có khả năng khảo sát cùng hành lang cho hai loại thông tin; chưa chứng minh cùng điểm, cùng ngày hay tương tác với mưa.',
        'Quy trình cung cấp trạng thái tuyến và xác nhận cảnh báo bởi đơn vị duy tu, thay vì dự báo sạt lở chưa có sự kiện.',
        'Chuẩn hóa chainage/GPS có người kiểm tra; xin log đóng/mở đường, thời gian mưa và sự kiện trước đánh giá độ nhạy/cảnh báo sai.',
        'Hai danh mục cùng cơ quan, không là xác nhận độc lập; 6+15 không tự là 21 vị trí duy nhất hay 21 sự kiện. Độ phù hợp chủ đề 1 còn phải giải trình.',
        geographic_scope='QL.4G, Sơn La theo nguồn', temporal_scope='snapshot 02/12/2025', source_ids='GT-10;GT-11',
        evidence_type='MEASURED ROAD-LABEL OVERLAP ONLY', evidence_grade='E2 inventory counts only; no validated rain mechanism',
        analysis_table='tables/sonla_corridor_counts.csv', filter_spec={'road':'QL.4G'}, metrics={'hazard_records':len(curves),'landslide_records':len(slides),'all_landslide_records':len(landslides)},
        denominator='107 road-hazard records and 58 landslide-hazard records separately; no exposure', selection='same road label, not spatial/temporal event linkage'))
    for row in rows:
        row['source_snapshot_provenance'] = [
            {key:e.get(key) for key in ['source_id','url','download_utc','sha256','label','data_version']}
            for e in manifest if e['source_id'] in row['source_ids'].split(';')
            and (e['label']=='selected_table' or (e['source_id'] in ['GT-10','GT-11'] and e['label'] not in ['api_metadata']))
        ]
        row['method_script'] = 'traffic-data-research/src/discover_opportunities.py'
    assert len(rows)==10
    return rows

def md_table(frame):
    frame=frame.fillna('')
    escape=lambda x: str(x).replace('|','/').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(map(escape,frame.columns))+' |',
                      '| '+' | '.join(['---']*len(frame.columns))+' |']+
                     ['| '+' | '.join(map(escape,row))+' |' for row in frame.itertuples(index=False,name=None)])

def main():
    TABLES.mkdir(parents=True,exist_ok=True)
    input_files=[PROJECT/'data/traffic_contest_ideas_2022_2025.xlsx',PROJECT/'data/danh_muc_du_lieu_giao_thong_viet_nam_2026.xlsx',PROJECT/'data/TRAFFIC_DATA_RESEARCH_AGENT_PROMPT.md']
    ideas, idea_sources=read_ideas(input_files[0])
    _,inventory=parse(input_files[1]); assert len(inventory)==22
    hashes={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_files}
    p=RESEARCH/'data/processed'
    a=pd.read_csv(p/'GT-01_aggregates.csv')
    changes=province_changes(a)
    hazards=pd.read_csv(p/'GT-10_hazards.csv').fillna('')
    landslides=pd.read_csv(p/'GT-11_hazards.csv').fillna('')
    assert len(hazards)==107 and len(landslides)==58
    manifest=json.loads((RESEARCH/'registry/public_raw_manifest.json').read_text(encoding='utf-8'))
    # Exclude author names from derived idea tables: analysis concerns mechanisms.
    save_table(ideas.drop(columns=['public_author_team']), 'ideas_normalized.csv')
    save_table(idea_sources, 'idea_sources.csv')
    save_table(changes, 'province_changes_2023_2024.csv')
    save_table(ideas.groupby(['competition','year','status_verified']).size().rename('records').reset_index(),'idea_counts_by_year_status.csv')
    save_table(ideas.groupby(['solution_cluster_inferred','year','status_verified']).size().rename('records').reset_index(),'idea_clusters_by_year_status.csv')
    # Full selection rules and alternative values are retained, no p-value scan.
    descriptions=[]
    for region in ['Hà Nội','Thái Nguyên','Đắk Lắk','TP. Hồ Chí Minh','Hải Dương','Đồng Tháp']:
        values=changes[changes.region_as_recorded_2023_2024.eq(region)].iloc[0]
        descriptions.append(values)
    save_table(pd.DataFrame(descriptions), 'selected_province_changes.csv')
    common=hazards.groupby('road').size().rename('hazard_inventory_records').reset_index().merge(
        landslides.groupby('road').size().rename('landslide_inventory_records').reset_index(),on='road',how='outer').fillna(0)
    save_table(common,'sonla_corridor_counts.csv')
    # Analyst coding, no reproduction of long government prose.
    extracts=[]
    paraphrases={9:'Nguồn mô tả xe dài mở lái sang làn đối diện trên mặt đường 5,50 m.',
                 12:'Nguồn nêu đường cong R<=15 m và xe lớn mở lái sang phần đường đối diện.',
                 13:'Nguồn nêu báo hiệu chưa hoàn chỉnh cùng với hạn chế tầm nhìn.',
                 14:'Nguồn nêu báo hiệu chưa hoàn chỉnh cùng với hạn chế tầm nhìn.',
                 28:'Nguồn liệt kê một đoạn cong/dốc và tầm nhìn hạn chế.',
                 29:'Nguồn liệt kê một đoạn cong/dốc và tầm nhìn hạn chế.',
                 30:'Nguồn liệt kê đường cong bán kính nhỏ.',
                 31:'Nguồn liệt kê đường cong bán kính nhỏ.'}
    for rid in [9,12,13,14,28,29,30,31]:
        row=hazards[hazards.record_id.eq(rid)].iloc[0]
        extracts.append({k:row[k] for k in ['record_id','road','start_chainage','end_chainage','commune']}|
                        {'analyst_paraphrase':paraphrases[rid],
                         'visibility_mentioned':bool(re.search('tầm nhìn',row.condition,re.I)),
                         'signage_incomplete_reported':'chưa hoàn chỉnh' in row.condition,
                         'original_local_table':'data/processed/GT-10_hazards.csv',
                         'snapshot':'2025-12-02','source_id':'GT-10'})
    save_table(pd.DataFrame(extracts),'local_mechanism_evidence.csv')
    # Reconcile each year with all 63 provinces + explicitly reported Other.
    reconciliations=[]
    for year in [2022,2023,2024]:
        for metric in ['crashes','deaths','injuries']:
            b=a[(a.year==year)&(a.metric==metric)]
            national=b[b.region.eq('TỔNG SỐ')].value.iloc[0]
            provinces=b[~b.region.isin(EXCLUDED_REGIONS)].value.sum(min_count=1)
            other=b[b.region.eq('Khác')].value.iloc[0]
            # If Other is missing, do not silently turn that missing value into 0.
            total=provinces+other if pd.notna(other) else None
            reconciliations.append({'year':year,'metric':metric,'national':national,'province_sum':provinces,'other_reported':other,'difference_if_other_known':national-total if total is not None else None})
    save_table(pd.DataFrame(reconciliations),'national_vs_provinces_reconciliation.csv')
    # Independent lexical sensitivity to editorial clusters, no reclassification.
    strict_school=education_title_mask(ideas.title_public)
    save_table(ideas.loc[strict_school,['idea_id','title_public','solution_cluster_inferred','status_verified']], 'education_title_sensitivity.csv')
    patterns=idea_patterns(ideas)
    findings=traffic_findings(changes,hazards,landslides,manifest)
    json_write(OUT/'idea_patterns.json',patterns)
    json_write(OUT/'traffic_findings.json',findings)
    save_table(pd.DataFrame(patterns), '10_idea_patterns.csv')
    flat=[{k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v) for k,v in f.items()} for f in findings]
    save_table(pd.DataFrame(flat), '10_traffic_findings.csv')
    summary={'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'input_sha256':hashes,
             'derived_input_sha256':{str((p/name).relative_to(PROJECT)):hashlib.sha256((p/name).read_bytes()).hexdigest()
                                     for name in ['GT-01_aggregates.csv','GT-10_hazards.csv','GT-11_hazards.csv']},'ideas':len(ideas),
             'same_contest_ideas':int(ideas.competition.eq('Sáng kiến ATGT Việt Nam').sum()),'traffic_inventory_sources':len(inventory),
             'historic_provinces_scanned':len(changes),'patterns':len(patterns),'traffic_findings':len(findings),
             'selection_method':'Purposeful six province examples after full descriptive scan; four Son La corridor leads by mechanism specificity. No risk ranking or causal interpretation.',
             'boundaries':'2023-2024 as recorded; no relabeling to 2026 boundaries; Son La places from 2025 snapshot.',
             'new_inferential_tests':'none; post-hoc descriptive synthesis only',
             'idea_label_provenance':'Workbook claims unless a particular official article is separately checked; title clusters are editorial.',
             'limitations':['no current site validation','no travel exposure denominator','no customer demand or willingness-to-pay evidence','no winner prediction','novelty not established']}
    json_write(OUT/'inputs_and_methods.json',summary)
    render_reports(patterns,findings,ideas,changes,strict_school,summary)
    build_opportunity_bridge(patterns,findings)
    for path in input_files:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==hashes[str(path.relative_to(PROJECT))]
    print(json.dumps({k:summary[k] for k in ['ideas','same_contest_ideas','historic_provinces_scanned','patterns','traffic_findings']},ensure_ascii=False))

def render_reports(patterns,findings,ideas,changes,strict_school,summary):
    """Detailed prose is generated from the measured records and explicit judgments."""
    # Filled below; outputs are kept apart from the original reports.
    for name,rows,kind in [('10_quy_luat_y_tuong_vi.md',patterns,'ý tưởng'),('10_phat_hien_giao_thong_vi.md',findings,'giao thông')]:
        lines=[f'# 10 kết quả về {kind} phục vụ tìm ý tưởng dự thi','',
               'Ngày tổng hợp 19/11/2026. Bằng chứng mô tả được tách khỏi diễn giải và giả thuyết can thiệp. Không có công thức bảo đảm đạt giải hoặc xác nhận nhu cầu thị trường.','']
        if kind=='ý tưởng':
            lines += ['73 bản ghi, 67 cùng cuộc thi và 6 Data For Life; chưa là tổng thể mọi bài thi. 70/73 cơ chế suy từ tên. Không so xác suất đạt giải giữa cuộc thi hoặc năm. Nhãn AWARDED là thông tin workbook, không tự là xác minh mới toàn bộ website.',
                      f'Kiểm tra độ nhạy: {int(strict_school.sum())} tên khớp regex giáo dục so với 10 nhãn nhóm biên tập. Xem `tables/education_title_sensitivity.csv`; không tự sửa nhãn gốc.','']
        else:
            lines += ['Quét toàn bộ 63 nhãn tỉnh/thành theo bảng 2023–2024, chọn sáu ví dụ mô tả và bốn hành lang Sơn La. Tỉnh/thành theo địa giới nguồn, không phải khẳng định địa giới 2026. Mẫu số thay đổi % là số năm 2023; không có exposure nên không gọi là thay đổi nguy cơ.',
                      'GT-01 có ba sai lệch tổng vùng đã ghi ở báo cáo gốc. Tổng 63 tỉnh + Khác khớp toàn quốc ở các ô mà Khác có giá trị; không tự chứng minh tính so sánh từng tỉnh. Phải xác minh định nghĩa/cách ghi nhận trước kết luận xu hướng thật.',
                      'Các mô tả đường Sơn La là hồ sơ cơ quan ngày 02/12/2025, không phải kết quả đo xe/xung đột/tai nạn của nhóm. Hai tuyến/cùng cơ quan không là xác nhận độc lập.','']
        for row in rows:
            label='[VERIFIED SOURCE FACT]' if row['id'] in ['T07','T08'] else '[MEASURED RESULT]'
            lines += [f'## {row["id"]}. {row["title_vi"]}','',
                      label+' '+row['evidence_vi'],'',
                      '[INTERPRETATION] '+row['interpretation_vi'],'',
                      '[HYPOTHESIS] Ngách cần kiểm chứng: '+row['opportunity_hypothesis_vi'],'',
                      '[RECOMMENDATION] Phép thử tiếp theo: '+row['next_test_vi'],'',
                      '[NOT VERIFIED] '+row['limitation_vi'],'']
            if kind=='ý tưởng':
                lines += ['Bản ghi: '+(row['idea_ids'] or 'không tên nào khớp từ khóa; không suy không tồn tại')+'. Xem `tables/ideas_normalized.csv`; khóa nguồn và URL trong từng bản ghi.','']
            else:
                lines += [f'Nguồn {row["source_ids"]}; {row["temporal_scope"]}; {row["geographic_scope"]}. Mẫu số: {row["denominator"]}.',
                          f'Bảng: [{row["analysis_table"]}]({row["analysis_table"]}). Bộ lọc/giá trị chính xác, URL snapshot, UTC và SHA256: `traffic_findings.json` mục {row["id"]}.','']
        lines += ['## Tái lập và nguồn phương pháp','',
                  'Từ gốc repo: `python traffic-data-research/src/discover_opportunities.py`. Hash input, quy tắc chọn và giới hạn: `inputs_and_methods.json`. Không sửa input hoặc raw. Các dữ liệu đầu vào thô vẫn giữ cục bộ theo chính sách repo.',
                  'Áp dụng Spreadsheets (đọc OOXML), exploratory-data-analysis (độ phủ/mẫu số/độ nhạy), scientific-critical-thinking (phạm vi suy luận, thiên lệch chọn mẫu, tách bằng chứng và giả thuyết). Không thực hiện GRADE/RoB hoặc kiểm định nhân quả.',
                  'Nguồn quy trình Scientific Agent Skills đã dẫn ở [skills_used.md](../../skills_used.md): https://doi.org/10.48550/arXiv.2609.00065 . Đây không phải bằng chứng giao thông.','']
        if kind=='ý tưởng':
            lines += ['## Đối chiếu website có trước trong lượt tổng hợp này','',
                      'Đã đọc lại danh sách kết quả/tiêu chí 2025 và bài trao giải 2022, 2023, 2024. Đây là kiểm tra chọn lọc, không xác minh lại toàn bộ 73 bài và hồ sơ kỹ thuật.',
                      '- [Dân trí 2022](https://dantri.com.vn/thoi-su/cac-tac-pham-dat-giai-cao-nhat-cuoc-thi-sang-kien-an-toan-giao-thong-2022-20221227192604875.htm): xác nhận hai hạng mục và bài đường Hồ Chí Minh/Đắk Nông giải Ba.',
                      '- [BNEWS/TTXVN 2023](https://bnews.vn/trao-giai-thuong-sang-kien-an-toan-giao-thong-viet-nam-2023/311608.html): đối chiếu E-learning, trụ đảo/cọc tiêu và cổng trường Lâm Đồng.',
                      '- [Nhân Dân 2024](https://nhandan.vn/tam-tac-pham-xuat-sac-doat-giai-cuoc-thi-sang-kien-an-toan-giao-thong-post847717.html): đối chiếu thiết bị khúc cua, eTraffic và Thư viện ATGT; không tự sửa bất nhất số giải trong bài.',
                      '- [Trang cuộc thi 2025](https://sangkienatgt.dantri.com.vn/19-tac-pham-duoc-vinh-danh-tai-sang-kien-an-toan-giao-thong-2025): xác nhận 19 tên và tiêu chí công bố; danh sách này không cho hạng giải từng tên.',
                      '- [Thể lệ 2026](https://sangkienatgt.dantri.com.vn/the-le): kiểm tra đúng đối tượng ba chủ đề; không coi trọng số trong workbook là chính thức.',
                      'Lượt truy cập 19/11/2026; chi tiết thành công/thất bại trong `source_checks.json`.','']
        (OUT/name).write_text('\n'.join(lines),encoding='utf-8')

def build_opportunity_bridge(patterns,findings):
    """Analyst proposals, explicitly separate from observations and market proof."""
    candidates=[
        {'opportunity_id':'O01','title_vi':'Hỗ trợ nhận biết xe đối diện khi xe dài cần mở lái ở khúc cua hẹp',
         'place':'QL.6B Km25+00–Km25+210, Quỳnh Nhai theo nguồn Sơn La',
         'evidence_ids':'T07;I03;I04;I06','prior_art_idea_ids':'IDEA-032;IDEA-014;IDEA-047',
         'user_candidate':'lái xe dài và đơn vị quản lý tuyến; chưa phỏng vấn',
         'problem_hypothesis':'người lái không nhận biết đủ sớm xe ngược chiều khi phải mở lái; nguồn mô tả cơ chế hình học nhưng chưa đo hành vi',
         'intervention_hypothesis':'thử thông tin trạng thái xe đối diện có chỉ dẫn hành động trong mô phỏng trước khi bàn thiết bị ngoài đường',
         'baseline':'biển/gương/quy trình hiện tại sau kiểm kê; chưa đo',
         'primary_outcome':'tỷ lệ quyết định nhường/giảm tốc phù hợp trong tình huống mô phỏng; chỉ là outcome trung gian',
         'first_validation':'xác minh vị trí rút gọn, tình trạng xử lý; đọc hồ sơ IDEA-032; xin chấm độc lập video lượt xe dài/xe đối diện nếu được phép',
         'kill_criterion':'không tìm thấy cơ chế khi khảo sát, đã được xử lý đủ, không tiếp cận địa bàn hoặc không khác giải pháp cũ thì dừng',
         'competition_fit':'chủ đề 1 có điều kiện: phải chứng minh điểm nóng/xung đột; không tự phù hợp chủ đề 2',
         'priority':'ưu tiên xác minh cơ chế nếu tiếp cận được Sơn La; chưa sẵn sàng triển khai'},
        {'opportunity_id':'O02','title_vi':'Kiểm chứng và cải thiện khả năng nhận biết báo hiệu tại hai đoạn QL.279D',
         'place':'Km87+200–Km87+400 và Km87+900–Km88+300, Mường La theo nguồn',
         'evidence_ids':'T08;I03;I05','prior_art_idea_ids':'IDEA-032;IDEA-044',
         'user_candidate':'đơn vị duy tu và người lái trên tuyến; chưa xác nhận nhu cầu',
         'problem_hypothesis':'thiếu/thấy muộn thông tin báo hiệu làm quyết định tiếp cận đường cong khó hơn; chưa đo tác động',
         'intervention_hypothesis':'checklist kiểm tra + thiết kế cải thiện báo hiệu đúng thiếu hụt, đối chiếu tiêu chuẩn hiện hành cùng kỹ sư',
         'baseline':'hiện trạng sau kế hoạch bảo trì 2026 và phương án báo hiệu thông thường; chưa kiểm tra',
         'primary_outcome':'độ đầy đủ/khả năng nhận biết đúng cảnh báo trong bài thử an toàn; không gọi là tai nạn tránh được',
         'first_validation':'xác nhận hai bản ghi 13/14 còn đúng; kiểm ngày/đêm có phép; đọc IDEA-032 trước chốt thiết bị',
         'kill_criterion':'đã xử lý hoàn chỉnh hoặc không có thiếu hụt hữu ích vượt checklist thông thường thì không phát triển sản phẩm mới',
         'competition_fit':'chủ đề 1 có điều kiện; không mặc nhiên mọi đường cong là nút/điểm nóng',
         'priority':'ưu tiên kiểm hiện trạng; novelty có thể thấp nếu chỉ thêm biển/camera'},
        {'opportunity_id':'O03','title_vi':'Thông tin chuỗi khúc cua theo tuyến, kiểm soát quá tải cảnh báo',
         'place':'cụm QL.43 tại Mộc Châu theo nguồn; sàng lọc bản ghi 30/31 trước',
         'evidence_ids':'T09;I03;I06','prior_art_idea_ids':'IDEA-032;IDEA-062;IDEA-068',
         'user_candidate':'người lái chưa quen tuyến và đơn vị quản lý; chưa biết số lượng hay nhu cầu',
         'problem_hypothesis':'người chưa quen tuyến cần thông tin đúng đoạn và đúng lúc; chỉ là giả thuyết, không suy từ danh mục ra du khách',
         'intervention_hypothesis':'so thiết kế thông tin theo tuyến với cảnh báo liên tục, ưu tiên chuẩn bị trước hành trình/mô phỏng để tránh phân tâm khi lái',
         'baseline':'thông tin biển hiện hữu/ứng dụng đang dùng; cần khảo sát',
         'primary_outcome':'nhận biết đúng điểm cần chuẩn bị và số cảnh báo thừa trong bài thử an toàn',
         'first_validation':'kiểm lý trình và trạng thái các đoạn; phỏng vấn lái xe quen/lạ; khảo sát sản phẩm dẫn đường đã có',
         'kill_criterion':'nhu cầu đã được đáp ứng hoặc thông tin mới gây phân tâm/cảnh báo thừa thì dừng',
         'competition_fit':'chủ đề 1 có điều kiện; chưa có số xung đột tại cụm',
         'priority':'khảo sát thứ hai sau khi xác minh vị trí; không chọn chỉ vì có 23 bản ghi'},
        {'opportunity_id':'O04','title_vi':'Tình huống xe điện học sinh gắn với một cổng trường có bằng chứng mới',
         'place':'một trường tại Thái Nguyên hoặc Hà Nội nếu nhóm có đối tác; chưa chọn trường',
         'evidence_ids':'T01;T02;I02;I06;I07','prior_art_idea_ids':'IDEA-042;IDEA-035;IDEA-025;IDEA-051',
         'user_candidate':'học sinh dùng xe điện, giáo viên và phụ huynh; cần xác nhận đúng nhóm',
         'problem_hypothesis':'một tình huống rẽ/nhập dòng cụ thể bị xử lý chưa tốt; số thương tích toàn tỉnh không chứng minh điều này',
         'intervention_hypothesis':'bài tập tình huống theo đường tới trường, có kiểm tra duy trì, thay vì quiz luật chung',
         'baseline':'bài học hiện hành và khả năng xử lý tình huống trước can thiệp, chưa đo',
         'primary_outcome':'tỷ lệ xử lý phù hợp trên tình huống tương đương sau 1–2 tuần; không đồng nhất với giảm tai nạn',
         'first_validation':'xin dữ liệu/quan sát tổng hợp có phép về tuổi, loại xe, địa điểm; chọn trường dựa khó khăn thực, không dựa tổng tỉnh',
         'kill_criterion':'không có phép, không có thiếu hụt kỹ năng/nhóm xe điện, hoặc chỉ lặp game E-learning cũ thì dừng/đổi phạm vi',
         'competition_fit':'chủ đề 3 nếu đúng học sinh xe điện/xe gắn máy; đầy đủ hơn chủ đề cảnh báo đường cong',
         'priority':'ưu tiên có điều kiện theo đối tác trường; độ cụ thể cơ chế hiện thấp'},
        {'opportunity_id':'O05','title_vi':'Chọn một cơ chế va chạm ở địa phương có tín hiệu tăng đồng thời',
         'place':'Đắk Lắk, Đồng Tháp hoặc khu vực Hải Dương theo địa giới cũ; chưa xác định nút',
         'evidence_ids':'T03;T05;T06;I01;I06','prior_art_idea_ids':'IDEA-033;IDEA-043;IDEA-068',
         'user_candidate':'ban ATGT/cơ quan quản lý tại địa bàn có khả năng cấp dữ liệu tổng hợp',
         'problem_hypothesis':'một nhóm tình huống có thể đóng góp biến động tổng; chưa biết nhóm nào',
         'intervention_hypothesis':'chưa chọn; phải có loại va chạm/phương tiện/nút cụ thể trước đề xuất AI hay hạ tầng',
         'baseline':'hồ sơ vụ việc và lưu lượng cùng kỳ, chưa có',
         'primary_outcome':'chưa xác định cho can thiệp; bước đầu là mức độ lặp lại và tỷ lệ theo exposure của cơ chế chọn',
         'first_validation':'đối chiếu định nghĩa và thay đổi ghi nhận 2023–2024; xin phân rã vị trí/tuổi/xe và xác minh hiện tại',
         'kill_criterion':'biến động chủ yếu do ghi nhận hoặc không có dữ liệu chi tiết thì không chọn làm đề tài sản phẩm',
         'competition_fit':'chưa xác định, phụ thuộc cơ chế tìm được; không cố gán cho chủ đề 2026',
         'priority':'hàng đợi xin dữ liệu, chưa phải ý tưởng dự thi có cơ chế'},
        {'opportunity_id':'O06','title_vi':'Giảm chuyến chở hàng cồng kềnh bằng lựa chọn vận chuyển phù hợp',
         'place':'một cụm cửa hàng/chợ tại địa bàn nhóm tiếp cận được; chưa có địa điểm được xác minh',
         'evidence_ids':'I04;I09;I10','prior_art_idea_ids':'chưa thấy title khớp trong 73 bài; phải tìm thêm ngoài mẫu',
         'user_candidate':'chủ cửa hàng và người vận chuyển bằng xe máy/thô sơ; chưa phỏng vấn',
         'problem_hypothesis':'thiếu lựa chọn hợp lý về thời gian/chi phí có thể dẫn tới chuyến chở không an toàn; chưa có bằng chứng cơ chế',
         'intervention_hypothesis':'hỗ trợ quyết định chia chuyến/đổi phương tiện hoặc gom chuyến, so với cách cửa hàng đang làm',
         'baseline':'tổng chuyến, loại hàng, cách chọn xe hiện tại và phương án thay thế, chưa đo',
         'primary_outcome':'tỷ lệ chuyến có cấu hình chở hàng được chuyên gia xác định không an toàn / tổng chuyến; kèm thời gian và chi phí thực thu thập',
         'first_validation':'định nghĩa độc lập không dựa pixel chưa hiệu chỉnh; đếm mẫu thuận tiện có ghi giới hạn rồi thiết kế mẫu tốt hơn; phỏng vấn tự nguyện',
         'kill_criterion':'không có vấn đề lặp lại, nhu cầu chưa xác nhận hoặc phương án thay thế không khả thi thì dừng; không lấy abnormal video làm baseline',
         'competition_fit':'chủ đề 2 đúng đối tượng về mặt giả thuyết, chưa có bằng chứng địa phương',
         'priority':'nhánh khám phá E0; không xếp cao chỉ vì ít bài trong danh mục'},
    ]
    for c in candidates:
        c.update(evidence_status='HYPOTHESIS; not field validated',novelty_status='NOT ESTABLISHED',
                 market_status='NO VERIFIED DEMAND OR WILLINGNESS-TO-PAY',
                 evaluation_status='baseline and permissions not acquired',
                 decision_rule='access to site + confirmed mechanism + incremental benefit + measurable safe outcome; otherwise stop')
    save_table(pd.DataFrame(candidates),'opportunity_bridge.csv')
    json_write(OUT/'opportunity_bridge.json',candidates)
    lines=['# Ngách địa phương và điều kiện để trở thành ý tưởng dự thi','',
           'Đây là đề xuất nghiên cứu, chưa là thị trường đã được xác nhận. Một địa bàn chỉ trở thành ngách hữu ích khi có người dùng cụ thể, cơ chế vấn đề, quyền tiếp cận và outcome đo được. Không có số liệu nhu cầu trả tiền hoặc quy mô thị trường trong hai danh mục.','',
           'Ưu tiên khảo sát cơ chế O01/O02 nếu thực sự tiếp cận được Sơn La. Ưu tiên O04 nếu có đối tác trường và xác nhận được nhóm xe điện. O05 chỉ là hàng đợi xin dữ liệu; O06 vẫn E0. Không có thông tin địa bàn của nhóm nên không giả định việc đi Sơn La là khả thi nhất.','']
    for c in candidates:
        lines += [f'## {c["opportunity_id"]}. {c["title_vi"]}','']
        for key,label in [('place','Địa bàn'),('evidence_ids','Bằng chứng liên kết'),('prior_art_idea_ids','Ý tưởng có trước'),('user_candidate','Người dùng giả định'),
                          ('problem_hypothesis','Giả thuyết vấn đề'),('intervention_hypothesis','Giả thuyết can thiệp'),('baseline','Baseline'),('primary_outcome','Outcome'),
                          ('first_validation','Kiểm chứng đầu tiên'),('kill_criterion','Điều kiện dừng'),('competition_fit','Phù hợp cuộc thi'),('priority','Ưu tiên có điều kiện')]:
            lines += [f'**{label}:** {c[key]}','']
        lines += ['[NOT VERIFIED] Tính mới, nhu cầu khách hàng và hiệu quả can thiệp đều chưa xác lập.','']
    lines+=['## Cách chốt đề tài','',
            '1. Chọn địa bàn nhóm tiếp cận và xin phép được.','2. Xác minh vấn đề lặp lại, có mẫu số và đúng đối tượng.','3. Đọc hồ sơ ý tưởng cũ gần nhất, so cơ chế thay vì tiêu đề.',
            '4. Chọn cách can thiệp đơn giản nhất có outcome an toàn đo được.','5. Chỉ làm prototype sau khi qua bốn bước; báo cả kết quả không hiệu quả.','',
            'Mức phù hợp tham chiếu thể lệ 2026 đã xem ngày 19/11/2026: https://sangkienatgt.dantri.com.vn/the-le . Xe tải dài không tự thành đối tượng xe máy chở hàng cồng kềnh. Bài toán đường cong ngoài nút phải giải trình liên quan điểm nóng/chủ đề 1.','']
    (OUT/'ngach_dia_phuong_va_huong_du_thi_vi.md').write_text('\n'.join(lines),encoding='utf-8')
    # A concise entry point containing exactly 10 + 10 result rows.
    a=pd.DataFrame([{'Mã':r['id'],'Mẫu hình':r['title_vi'],'Căn cứ':r['evidence_vi']} for r in patterns])
    b=pd.DataFrame([{'Mã':r['id'],'Địa bàn/phát hiện':r['title_vi'],'Căn cứ':r['evidence_vi']} for r in findings])
    text='''# 10 quy luật ý tưởng và 10 phát hiện giao thông để tìm đề tài dự thi

Mục tiêu: tìm **vấn đề cụ thể tại địa phương, có người dùng, bằng chứng và cách kiểm chứng**, rồi mới chọn giải pháp. Không chọn công nghệ trước và tìm lý do sau.

“Quy luật” ở đây là mẫu hình quan sát và nguyên tắc lựa chọn có căn cứ, không là quy luật nhân quả bảo đảm đạt giải. 73 ý tưởng là mẫu công bố thiên về shortlist/đạt giải; 70 mô tả cơ chế suy từ tên. Số liệu tỉnh là 2023–2024 theo địa giới nguồn, không phải hiện trạng năm 2026. Các điểm Sơn La là danh mục nguy cơ cập nhật 02/12/2025, chưa đo tai nạn hoặc hiệu quả can thiệp.

## 10 quy luật/mẫu hình từ ý tưởng

'''+md_table(a)+'''

Định nghĩa, IDEA-ID, giới hạn và phép thử: [10 quy luật chi tiết](10_quy_luat_y_tuong_vi.md).

## 10 phát hiện giao thông

'''+md_table(b)+'''

T01–T06 chỉ cho biết biến động số ghi nhận, chưa xác định cơ chế hay nhóm học sinh. T07–T10 có chi tiết hành lang nhưng vẫn cần kiểm tra hiện trạng. Toàn bộ 63 tỉnh được giữ trong [bảng quét đầy đủ](tables/province_changes_2023_2024.csv); không xếp hạng nguy cơ khi thiếu exposure. Tổng vùng có sai lệch, cần đối chiếu nguồn địa phương.

Chi tiết bộ lọc, mẫu số, URL snapshot, UTC/SHA256 và bất định: [10 phát hiện chi tiết](10_phat_hien_giao_thong_vi.md), `traffic_findings.json`.

## Hướng nào nên đi tiếp?

- Có đối tác Sơn La: xác minh cơ chế xe dài mở lái tại QL.6B (O01), rồi khoảng thiếu báo hiệu QL.279D (O02). IDEA-032 đã rất gần, nên chưa coi cảnh báo khúc cua là mới.
- Có đối tác trường: xác minh một tình huống xe điện khó xử lý tại trường cụ thể (O04), không làm game/QR dạy luật chung. Dữ liệu tổng tỉnh chưa chứng minh thiếu kỹ năng học sinh.
- Có đối tác vận chuyển/cửa hàng: thử xác minh bài toán chọn phương tiện chở hàng (O06); chưa có bằng chứng địa phương nên không ưu tiên chỉ vì ít title trùng.

Xem [6 hồ sơ ngách và điều kiện dừng](ngach_dia_phuong_va_huong_du_thi_vi.md). Chưa có ngách nào được xác nhận nhu cầu thị trường, hiệu quả hoặc novelty. Thứ tự tiếp theo phụ thuộc khả năng tiếp cận địa bàn và baseline của nhóm.

## Tái lập

Từ gốc repo: `python traffic-data-research/src/discover_opportunities.py`. Đầu vào ba file trong `data/`, các snapshot dẫn xuất GT-01/10/11 của lần nghiên cứu trước; giữ nguyên bytes, không trộn thời kỳ. `inputs_and_methods.json` lưu hash và quy tắc chọn; các bảng nằm trong `tables/`. Chạy lại phần đầy đủ cần dữ liệu cục bộ không xuất bản; các CSV và báo cáo tổng hợp vẫn đọc được trong repo.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8')

if __name__=='__main__':
    main()
