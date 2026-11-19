"""Vietnamese checkpoint reports from measured rechecks, with proposed ideas separate."""
import html
import json
from pathlib import Path

import pandas as pd


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def md_table(headers, rows):
    def cell(v):
        return str(v).replace('|', '/').replace('\n', ' ')
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |'] +
                     ['| '+' | '.join(cell(v) for v in row)+' |' for row in rows])


def candidate_ideas(findings):
    """Explicitly conditional concepts; historic provincial totals do not identify mechanisms."""
    definitions = [
        ('C01', 'T01', 'Hồ sơ thương tích theo tình huống tại một cụm nút Hà Nội',
         'Hà Nội theo địa giới nguồn; chưa chọn nút hiện tại',
         'Ban ATGT/đơn vị quản lý nút; chưa có đối tác',
         'Một số tình huống lặp có thể bị che bởi tổng tỉnh; hiện chưa biết tình huống nào.',
         'Công cụ tổng hợp hồ sơ vụ việc đã ẩn danh theo sơ đồ chuyển động, hỗ trợ chọn một thay đổi tổ chức luồng nhỏ.',
         'Cách phân loại hồ sơ và tổ chức nút đang dùng; cần kiểm tra trước khi làm phần mềm.',
         'Tỷ lệ hồ sơ gán đúng tình huống so với hai người chấm; thời gian tìm cụm có thể hành động. Đây là outcome quy trình, chưa phải giảm thương tích.',
         'Xin hồ sơ chi tiết cùng kỳ, từ điển định nghĩa, lưu lượng và cập nhật địa giới; kiểm tra ba trường hợp đến hồ sơ gốc.',
         'Nếu không có dữ liệu vụ việc hoặc quy trình hiện tại đã đáp ứng thì dừng; tổng tỉnh không biện minh xây app.',
         'IDEA-033;IDEA-043;IDEA-068', 'Chủ đề điểm nóng/nút chỉ khi tìm được nút và cơ chế; bản thân dashboard chưa đủ.', 'E0 cơ chế địa phương; E1 biến động tổng'),
        ('C02', 'T02', 'Luyện một kỹ năng xe điện còn thiếu tại một trường Thái Nguyên',
         'Một trường ở khu vực Thái Nguyên; chưa xác minh trường/đối tượng',
         'Học sinh, giáo viên và phụ huynh tự nguyện; chưa tuyển',
         'Có thể tồn tại một lỗi xử lý rẽ/nhập dòng lặp lại; số bị thương toàn tỉnh không chứng minh lỗi này hay lỗi của học sinh.',
         'Bài tập tình huống lấy từ đường tới trường, phản hồi theo lỗi và kiểm tra duy trì bằng tình huống mới.',
         'Bài học hiện hành có cùng thời lượng; tránh so với nhóm không học gì.',
         'Tỷ lệ xử lý phù hợp trên tình huống mới ở đợt duy trì; không quy thành tỷ lệ giảm tai nạn.',
         'Xác nhận học sinh dùng xe điện/xe gắn máy, nhu cầu kỹ năng, quyền khảo sát và nội dung phù hợp; chỉ thu số tổng hợp cần thiết.',
         'Dừng nếu không đúng nhóm, không có khó khăn lặp lại, không có phép hoặc không tạo lợi ích vượt bài học hiện hành.',
         'IDEA-042;IDEA-035;IDEA-025;IDEA-010', 'Có thể phù hợp chủ đề học sinh sau xác minh đối tượng.', 'E0 cơ chế; E1 tổng thương tích'),
        ('C03', 'T03', 'Bộ chọn ca khảo sát và kiểm tra điều kiện nút tại Đắk Lắk',
         'Đắk Lắk trong bảng 2023–2024; chưa có hành lang/nút xác minh',
         'Tổ khảo sát/đơn vị quản lý đường địa phương; chưa tiếp cận',
         'Một cơ chế nút có thể góp vào biến động cùng chiều của ba tổng; chưa có bằng chứng về cơ chế cụ thể.',
         'Quy trình chọn ca từ hồ sơ, kiểm tra hiện trường bằng biểu mẫu thống nhất và so phương án tổ chức luồng hiện tại.',
         'Cách chọn điểm khảo sát hiện tại và giải pháp đã có; không chọn điểm chỉ vì tổng tỉnh tăng.',
         'Mức tái lập chọn điểm giữa hai người đánh giá và tỷ lệ điểm xác minh đúng vấn đề; sau đó mới chọn outcome can thiệp.',
         'Lấy phân rã tuyến/nút, loại va chạm, phương tiện và lưu lượng; kiểm tra thay đổi ghi nhận trước phân tích.',
         'Dừng nếu biến động do định nghĩa/ghi nhận hoặc không có điểm xác nhận; chưa chế tạo cảnh báo.',
         'IDEA-033;IDEA-062;IDEA-068', 'Chưa xác lập; phụ thuộc cơ chế điểm nóng được xác minh.', 'E0 cơ chế; E1 ba tổng'),
        ('C04', 'T04', 'Kiểm toán pha đèn và hàng chờ ở một nút TP.HCM',
         'Một nút TP.HCM được phép khảo sát; chưa chọn',
         'Người vận hành nút; chưa có quyền truy cập điều khiển',
         'Có thể còn một luồng chờ/xung đột cần xử lý; các tổng tai nạn giảm năm 2024 không chứng minh nút đó đang ùn.',
         'Công cụ hỗ trợ kiểm toán luồng/pha, đề xuất chỉnh quy tắc nhỏ và kiểm chứng offline trước khi xin thử.',
         'Pha đèn/ITS đang vận hành tại chính nút; không chỉ so với điều khiển cố định giả lập kém.',
         'Trễ/xe theo từng hướng và thời gian chờ người đi bộ; theo dõi xung đột riêng, không đổi trễ thành số tai nạn tránh được.',
         'Đo lưu lượng, pha và hàng chờ hiện tại; GT-07 lịch sử không thay baseline. Chỉ thử đường thật khi cơ quan cho phép.',
         'Dừng nếu không có vấn đề/đối tác, phương án hiện tại đã tốt hoặc đề xuất tăng bất lợi cho người đi bộ.',
         'IDEA-033;IDEA-043;IDEA-054;IDEA-060', 'Có thể thuộc chủ đề nút giao; điều khiển thích ứng đã có nhiều ý tưởng gần.', 'E0 nút/cơ chế; E1 số tổng'),
        ('C05', 'T05', 'Hồ sơ điểm nóng giữ được dấu vết địa giới Hải Dương lịch sử',
         'Khu vực mang nhãn Hải Dương trong nguồn 2023–2024; chưa có crosswalk hiện tại',
         'Người tổng hợp hồ sơ giao thông liên kỳ; chưa xác nhận nhu cầu',
         'Thay địa giới/mã địa điểm có thể làm khó theo dõi một cụm; chưa đo mức sai ghép.',
         'Công cụ nối hồ sơ theo tuyến/nút có phiên bản, giữ nhãn gốc và lý do ghép để ưu tiên xác minh hiện trường.',
         'Bảng chuyển mã và quy trình đang có; có thể đã đủ mà không cần sản phẩm mới.',
         'Tỷ lệ liên kết đúng trong mẫu có người chấm độc lập, số liên kết chưa xác minh và thời gian xử lý.',
         'Lấy crosswalk chính thức và hồ sơ đủ vị trí; không ghép chỉ từ tên tỉnh hoặc tự đoán ranh giới.',
         'Dừng nếu không có lỗi liên kết/nhu cầu hoặc không có vị trí đáng tin; không dùng làm bản đồ nguy cơ hiện tại.',
         'IDEA-033;IDEA-068', 'Hạ tầng bằng chứng; phù hợp cuộc thi trực tiếp còn yếu, không tự là can thiệp an toàn.', 'E0 khó khăn ghép; E1 số tổng lịch sử'),
        ('C06', 'T06', 'Quy trình quan sát xung đột có mẫu số tại một nút Đồng Tháp',
         'Một nút thuộc phạm vi Đồng Tháp của bảng nguồn; chưa xác minh địa điểm',
         'Tổ khảo sát và người quản lý địa bàn; chưa có phép',
         'Có thể có một xung đột lặp, cần ghi cả lượt qua và lượt có cơ hội xung đột; chưa biết loại xe hoặc dạng nút.',
         'Biểu mẫu quan sát dễ chấm, kiểm tra đồng thuận và báo cáo tỷ lệ để quyết định có cần đổi tổ chức luồng.',
         'Khảo sát thủ công/biểu mẫu hiện hành; chưa cần AI nếu cách đơn giản đã đủ.',
         'Đồng thuận giữa hai người chấm và số tình huống/đơn vị exposure; chưa lấy proxy làm bằng chứng giảm tai nạn.',
         'Xin hồ sơ vụ việc và lưu lượng, chọn điểm từ bằng chứng, khóa định nghĩa xung đột trước khi xem mẫu đánh giá.',
         'Dừng nếu không có xung đột lặp, không đủ mẫu/định nghĩa tin cậy hoặc không có người sử dụng kết quả.',
         'IDEA-033;IDEA-068', 'Chỉ phù hợp chủ đề điểm nóng sau xác nhận nút/cơ chế; chưa là ý tưởng sản phẩm hoàn chỉnh.', 'E0 cơ chế; E1 biến động tổng'),
        ('C07', 'T07', 'Hỗ trợ nhận biết xe dài ngược chiều trước cua QL.6B',
         'Quỳnh Nhai, Sơn La; bản ghi 9, Km25+00–Km25+210 cần xác minh lý trình',
         'Người lái xe dài và đơn vị quản lý tuyến',
         'Xe dài cần mở lái sang làn đối diện trong mô tả cơ quan; chưa đo tần suất gặp xe ngược chiều.',
         'Thông báo sự hiện diện/phương án nhường đường có hành động rõ; chỉ nghiên cứu sau khi kiểm tra báo hiệu hiện hữu.',
         'Biển, gương, thao tác quan sát/nhường đường hiện có; cảnh báo khúc cua đã có prior art.',
         'Nhận biết đúng và thời gian hành động trong mô phỏng/sân kín, cảnh báo sai/bỏ sót và phân tâm; chưa suy hiệu quả tai nạn.',
         'Xác minh hiện trạng và lý trình; đếm lượt xe dài, lượt đồng thời ngược chiều và lượt mở lái có chấm độc lập.',
         'Dừng nếu đường đã xử lý, không có tình huống lặp, thiết bị phân tâm hoặc không hơn baseline đơn giản.',
         'IDEA-032;IDEA-014;IDEA-062', 'Cần giải trình chủ đề điểm nóng; xe tải dài không tự phù hợp chủ đề xe máy chở hàng cồng kềnh.', 'E1 mô tả cơ chế từ cơ quan; chưa đo hiện trường'),
        ('C08', 'T08', 'Theo dõi khép kín việc khắc phục báo hiệu QL.279D',
         'Mường La, Sơn La; bản ghi 13/14, Km87+200–87+400 và Km87+900–88+300',
         'Đơn vị bảo trì và cán bộ kiểm tra tuyến',
         'Nguồn 2025 ghi báo hiệu chưa hoàn chỉnh; kế hoạch 2026 có thể đã xử lý.',
         'Hồ sơ việc cần làm, ảnh kiểm tra có ngày, người phụ trách và bước xác nhận hoàn thành tại đúng vị trí.',
         'Quy trình bảo trì/biên bản nghiệm thu hiện tại; không xây thêm dashboard nếu đã giải quyết được.',
         'Thời gian phát hiện đến xác minh, tỷ lệ xác nhận hoàn thành đúng qua kiểm tra độc lập, khối lượng công việc phát sinh.',
         'Kiểm tra hai đoạn và kế hoạch/hoàn công 2026; phỏng vấn quy trình xử lý, không suy trạng thái từ ô trống.',
         'Dừng nếu đã hoàn chỉnh và không có khoảng trống quy trình hoặc đơn vị không có thẩm quyền xử lý.',
         'IDEA-032;IDEA-062; FHWA curve delineation', 'Cần giải trình liên hệ chủ đề điểm nóng; giá trị có thể nằm ở thực thi/bảo trì, chưa chứng minh mới.', 'E1 mô tả thiếu báo hiệu năm 2025'),
        ('C09', 'T09', 'Ưu tiên cảnh báo để giảm quá tải thông tin trên QL.43',
         'Các đoạn QL.43 gắn Mộc Châu trong danh mục; 23 bản ghi, chưa là 23 tai nạn',
         'Người lái qua cụm cua và đơn vị vận hành; chưa khảo sát',
         'Cảnh báo nhiều vị trí liên tiếp có thể gây quá tải; đây là giả thuyết, không có đo quá tải trong dữ liệu.',
         'Gộp cảnh báo theo đoạn và ưu tiên thông tin dẫn đến hành động, thử trên mô phỏng trước thiết bị thật.',
         'Thông tin/báo hiệu hiện có và cảnh báo từng điểm; nội dung nguy cơ phải được kỹ sư tuyến xác nhận.',
         'Nhận biết nguy cơ, hành động phù hợp, bỏ sót và phân tâm ở tình huống mới; không chỉ hỏi thích giao diện nào.',
         'Xác minh vị trí, tình trạng đã xử lý và nhu cầu thông tin; ghi phiên bản nguồn và chỉ dẫn hiện có.',
         'Dừng nếu không quá tải, không thiếu thông tin hoặc cảnh báo gộp làm tăng bỏ sót.',
         'IDEA-032;IDEA-062; FHWA curve delineation', 'Chủ đề điểm nóng cần được xác nhận; không lấy số bản ghi cao làm xếp hạng nguy cơ.', 'E1 mật độ bản ghi kiểm kê; E0 quá tải cảnh báo'),
        ('C10', 'T10', 'Hàng đợi kiểm tra tuyến QL.4G từ hai danh mục nguy cơ',
         'QL.4G, Sơn La; 6 bản ghi đường cong và 15 bản ghi sạt lở',
         'Tổ quản lý/bảo trì tuyến',
         'Hai loại nguy cơ trên cùng hành lang có thể cần phối hợp kiểm tra; chưa có bằng chứng trùng điểm, sự kiện sau mưa hoặc bỏ sót nhiệm vụ.',
         'Hợp nhất danh sách công việc theo tuyến, giữ riêng loại nguy cơ và trạng thái chưa đối chiếu lý trình; không tạo điểm rủi ro dự báo.',
         'Danh sách/quy trình phối hợp hiện tại; không tự cộng 6+15 thành số sự cố độc lập.',
         'Tỷ lệ nhiệm vụ đúng vị trí/không trùng, thời gian lập tuyến kiểm tra và tỷ lệ nguy cơ xác minh; không dự báo sạt lở.',
         'Đối chiếu lý trình, bản đồ tuyến có CRS và nhật ký kiểm tra/sự kiện; dữ liệu mưa chỉ thêm khi có câu hỏi và nhãn sự kiện phù hợp.',
         'Dừng nếu không có nhu cầu phối hợp, không xác minh được vị trí hoặc danh mục không còn hiệu lực.',
         'GT-10/GT-11 cùng cơ quan, không là hai nghiên cứu độc lập; prior art quy trình chưa rà đầy đủ',
         'Phù hợp cuộc thi chưa rõ; không nên ưu tiên chỉ vì có hai bảng.', 'E1 cùng hành lang; E0 thiếu phối hợp/sự kiện'),
    ]
    keys = ['id', 'discovery_id', 'title_vi', 'place_vi', 'user_vi', 'problem_hypothesis_vi',
            'intervention_hypothesis_vi', 'baseline_vi', 'primary_outcome_vi', 'first_validation_vi',
            'stop_rule_vi', 'prior_art', 'competition_fit_vi', 'evidence_grade_vi']
    by_id = {r['id']: r for r in findings}
    candidates = []
    for definition in definitions:
        c = dict(zip(keys, definition))
        f = by_id[c['discovery_id']]
        c.update(verified_evidence_vi=f['evidence_vi'], source_ids=f['source_ids'],
                 source_snapshot_provenance=f['source_snapshot_provenance'],
                 status='CANDIDATE_HYPOTHESIS', novelty_status='NOT_ESTABLISHED',
                 demand_status='NOT_VALIDATED', intervention_effect_status='NOT_MEASURED',
                 current_site_access_status='NOT_ACQUIRED',
                 priority_vi='Xác minh cơ chế/hiện trạng nếu tiếp cận được địa bàn' if c['id'] in ['C07', 'C08'] else
                 'Chỉ khảo sát nhu cầu và khoảng trống sau đối chiếu hiện trạng' if c['id'] in ['C09', 'C10'] else
                 'Chờ dữ liệu chi tiết/đối tác; chưa ưu tiên chế tạo')
        candidates.append(c)
    return candidates


def render_reports(out):
    def write(name, text):
        (out / name).write_text(text.rstrip()+'\n', encoding='utf-8')
    r = json.loads((out / 'measured_rechecks.json').read_text(encoding='utf-8'))
    findings = json.loads((out / 'ten_traffic_discoveries_rechecked.json').read_text(encoding='utf-8'))
    candidates = candidate_ideas(findings)
    dump(out / 'ten_candidate_ideas.json', candidates)
    pd.DataFrame([{k: v for k, v in c.items() if k != 'source_snapshot_provenance'} for c in candidates]).to_csv(
        out / 'tables/ten_candidate_ideas.csv', index=False, encoding='utf-8-sig')
    g = r['GT07']; v = r['GT09']['VNTraffic']; a = r['GT09']['AICC22-Custom']
    changes = [
        ('GT-09 VNTraffic', '8.771 bất đồng theo khóa frame–track; đếm 205 đối tượng JSON.',
         f'{v["shared_box_instances"]:,}/{v["txt_rows"]:,} hộp khớp hình học. JSON có 205 mục, trong đó {v["json_empty_track_objects"]} mục rỗng; 85 track có hộp. Ánh xạ track trên hộp khớp là một-một; 49 mã khác tên.',
         'Hiệu chỉnh diễn giải: không có bằng chứng sai hình học từ phép đối chiếu này. Còn 2 khóa frame–track TXT trùng cần làm rõ, chưa kiểm với video.'),
        ('GT-09 AICC22', 'TXT/JSON khác tổng số hộp.',
         f'{a["shared_box_instances"]:,} hộp TXT đều có trong JSON; JSON thêm {a["json_only_box_instances"]:,} hộp.',
         'Giữ cờ không thay thế trực tiếp hai biểu diễn; không gọi cả 1.254 hộp thêm là nhãn sai; không suy luận Việt Nam từ AICC22.'),
        ('GT-07 suy luận', 'Tương phản thăm dò −3,459; t(25)=−1,117; p=0,275 và CI bootstrap ngày.',
         'Tái lập đúng số cũ. Cân đều cặp đoạn–ngày cho −0,020; trung vị ngày 0; lọc ngày có ≥2 cặp cho +1,448 (18 ngày).',
         'Hạ phạm vi diễn giải xuống tương phản mô tả trong mẫu; p/CI iid chỉ giữ để kiểm toán, không dùng như suy luận dân số được hiệu chỉnh.'),
        ('GT-10 trạng thái xử lý', '19 treated và 89 untreated không rỗng.',
         'Bản ghi 79 có cả hai trường: đã thực hiện một phần và còn đề nghị kế hoạch đầu tư.',
         'Giữ số đếm trường; bác bỏ cách xem chúng là nhãn hoàn thành/chưa hoàn thành loại trừ nhau.'),
        ('GT-01 sáu địa bàn', 'Các biến động 2023–2024 trong T01–T06.',
         'Tính lại cả 63 tỉnh và đối chiếu toàn bộ chỉ số sáu ví dụ: không đổi. Tổng quốc gia khớp tỉnh+Khác ở 7 ô có Khác; 2 ô Khác thiếu không kiểm được.',
         'Giữ phát hiện mô tả; không đổi thành xếp hạng nguy cơ, nguyên nhân hay hiện trạng năm 2026.'),
        ('GT-08', 'Tỷ lệ frame có nhãn bất thường trong 50 mask.',
         'Đọc lại 50 NPY với allow_pickle=False, kiểm hash, miền nhãn và tổng frame: khớp.',
         'Giữ kết quả benchmark tuyển chọn; không coi là tần suất vi phạm hoặc tỷ lệ chở hàng cồng kềnh trên đường.'),
        ('Cuộc thi', '10 nhóm giáo dục theo nhãn biên tập; 70/73 cơ chế từ tên.',
         f'Kiểm ID, nguồn liên kết và độ nhạy cách gán nhóm. Bộ lọc tiêu đề giáo dục cho {r["ideas"]["education_title_screen_count"]} bài; nhãn biên tập cho 10.',
         'Giữ 10 mẫu hình như mô tả danh mục; không xem nhãn nhóm là taxonomy đã thẩm định hoặc giải thưởng là nhãn dự đoán đáng tin.'),
        ('Tài liệu/tính mới', 'Rà soát tường thuật giới hạn, prior art cho cảnh báo cua và giáo dục.',
         'Kiểm log tìm kiếm; giữ rõ chưa phân trang hết/không đủ hồ sơ. Đối chiếu lại trang FHWA và nguồn trích dẫn skill.',
         'Không nâng novelty của bất kỳ ứng viên nào; không coi metadata/DOI/giải thưởng là chứng minh hiệu quả.'),
    ]
    dump(out / 'conclusion_change_log.json', [dict(zip(['subject', 'before_vi', 'recheck_vi', 'decision_vi'], row)) for row in changes])
    write('01_nhung_ket_luan_da_thay_doi_vi.md', '# Đối chiếu kết luận trước và sau checkpoint\n\n'+
        'Các báo cáo cũ được giữ nguyên. Khi có khác biệt, dùng hiệu chỉnh ở bảng này để đọc kết quả cũ. Lượt này kiểm lại snapshot, không thu một mẫu dân số mới.\n\n'+
        md_table(['Phạm vi', 'Trước', 'Kiểm lại', 'Quyết định'], changes))

    write('02_tham_dinh_thong_ke_va_thoi_gian_vi.md', f'''# Thẩm định thống kê và độ phủ thời gian

[KẾT QUẢ ĐO] GT-07 có {g['n_status_rows']:,} bản ghi, {g['observed_days']}/{g['calendar_days']} ngày lịch được quan sát; {g['unobserved_days_not_zero']} ngày không quan sát được giữ là missing. Một ngày chứa {100*g['top_day_fraction']:.2f}% bản ghi. Sau ghép cửa sổ cùng đoạn–ngày còn {g['matched_segment_days']} cặp trên {g['matched_days']} ngày, {g['unique_paired_segments']} đoạn; {g['days_with_one_pair']} ngày chỉ có một cặp.

Định nghĩa giữ nguyên: cao điểm 07:00–08:59 và 16:00–17:59; giữa ngày 10:00–14:59, UTC+7. Lấy trung vị từng cửa sổ trong đoạn–ngày, rồi trừ. Chưa xác minh đơn vị velocity, không viết km/h. Các bản ghi ngoài hai cửa sổ không thuộc tương phản; cặp thiếu một cửa sổ bị loại và không tự bù.

| Cách tổng hợp | Ước lượng, đơn vị thô | Đơn vị được cân đều |
| --- | ---: | --- |
| Trung bình các trung bình ngày | {g['equal_day_mean']:.3f} | 26 ngày |
| Trung bình tất cả cặp đoạn–ngày | {g['equal_segment_day_mean']:.3f} | 404 cặp |
| Trung vị các trung bình ngày | 0.000 | 26 ngày |
| Trung bình ngày có ít nhất 2 cặp | {g['sensitivity'][3]['estimate']:.3f} | 18 ngày |
| Trung bình ngày có ít nhất 5 cặp | {g['sensitivity'][4]['estimate']:.3f} | 13 ngày |

[DIỄN GIẢI] Đây là các đại lượng đích khác nhau. Khác số không chứng minh đại lượng nào là “đúng” cho thành phố; nó cho thấy kết luận phụ thuộc mạnh vào đối tượng được cân. Hai phân tích lọc ngày là độ nhạy hậu nghiệm, không là quy tắc loại dữ liệu đã đăng ký trước. Giữ mọi ngày và mọi kết quả; không chọn biến thể thuận dấu hoặc thuận p.

Tái lập được t({g['old_df']})={g['old_t']:.3f}, p={g['old_p']:.6f}; bootstrap iid 5.000 lần, seed 42, khoảng phân vị 95% [{g['old_iid_bootstrap_interval'][0]:.3f}, {g['old_iid_bootstrap_interval'][1]:.3f}]. Trung bình ngày/SD ngày={g['standardized_day_mean_over_sd']:.3f}; đây là chuẩn hóa nội bộ, không đánh giá ý nghĩa thực tế khi chưa có đơn vị. Loại lần lượt một ngày cho ước lượng [{g['leave_one_day_out_estimate_range'][0]:.3f}, {g['leave_one_day_out_estimate_range'][1]:.3f}], là khoảng độ nhạy, không phải CI.

Chẩn đoán Shapiro trên 26 chênh lệch ngày: W={g['shapiro_W']:.3f}, p={g['shapiro_p']:.3g}. Kết quả này không kiểm tra tính độc lập hoặc đại diện. Không tự chuyển sang Wilcoxon vì đổi câu hỏi và vẫn có giả định. Tính độc lập ngày chưa được thiết kế/kiểm chứng; đường lặp và ngày rời rạc còn tồn tại. Vì vậy **p/CI iid không được dùng để suy luận dân số hay khẳng định “không có chênh lệch”**. Không thêm kiểm định để tìm ý nghĩa thống kê, không áp dụng CI theo từng dòng trong 90.938 dòng.

## Điều kiện áp dụng chuỗi thời gian

- GT-01 chỉ có 3 điểm năm; GT-02 có 3 điểm tháng sơ bộ và sai khác số tháng trước suy ngược từ bản tin sau. Không đủ mùa vụ/baseline; không chạy ADF, STL hoặc ARIMA.
- GT-07 có 294 ngày lịch nhưng 174 ngày không quan sát, mức phủ đoạn và cơ chế lấy mẫu không ổn định. Số ngày trải dài không tự tạo chuỗi đều có thể so sánh. Không nội suy hoặc coi missing là không có xe/ùn.
- GT-10/11 là kiểm kê nguy cơ, không là chuỗi sự kiện; lịch kế hoạch không là ngày tai nạn.
- GT-12 calendar năm 2018: kiểm lại ba feed đều không có orphan trip/stop và không có trùng trip–sequence. Headway lịch trình theo route chưa được kiểm điều kiện direction/service-day; không dùng làm thời gian chờ xe buýt hiện tại.

Đã áp dụng bước kiểm tra điều kiện của skill time-series-analysis. Chưa thỏa đầu vào để chạy phân rã/dự báo; đây là quyết định phương pháp có ghi nhận, không là kết quả dự báo thất bại. Chưa có nhu cầu chọn chân trời dự báo hoặc số liệu đủ để đánh giá holdout.

## Phân rã biến động và giới hạn nguyên nhân

`tables/province_signed_contributions.csv` dùng drill_down trên 63 tỉnh, tách riêng từng chỉ số; tuyệt đối không cộng tổng vùng lồng nhau. Mẫu số contribution là thay đổi ròng tổng 63 tỉnh, không gồm Khác. Đóng góp âm hoặc trên 100% có thể xuất hiện do bù trừ; không là thị phần nguy cơ. Không quy tỉnh có contribution lớn thành nguyên nhân hay điểm can thiệp.

Skill root-cause-investigation cần baseline trước thay đổi và nhật ký sự kiện. Chưa có ít nhất 30 ngày trước biến động; không chạy z-score để gọi “bình thường”, không quy thay đổi cho camera, pháp luật, giáo dục hoặc hạ tầng. Các khả năng đổi ghi nhận, exposure, cơ cấu phương tiện và thay đổi thực tế đều còn mở.

![Độ phủ và tương phản lịch sử GT-07](GT07_coverage_and_contrast.png)

Mô tả hình: dấu tròn là ngày có bản ghi; dấu x dưới mốc 0 là ngày không quan sát, không phải giá trị âm của số bản ghi. Panel dưới hiện cả 26 trung bình ngày, không nối qua khoảng trống. Bảng dữ liệu kèm theo và `figure_manifest.json` ghi phiên bản, kích thước, DPI và phạm vi. Chưa chứng nhận tiêu chuẩn tạp chí/accessibility.
''')

    items = [
        ('HIGH', 'Accuracy / inference', 'GT-07: tương phản không ổn định theo cân; đơn vị, đại diện và độc lập chưa xác minh.', 'Giữ mô tả; thu baseline theo thiết kế nếu cần suy luận.'),
        ('HIGH', 'Consistency', 'GT-01: tổng vùng có sai khác; hai ô Khác về thương tích bị thiếu.', 'Không dùng tổng vùng xếp hạng; không điền 0; đối chiếu nguồn địa phương.'),
        ('MEDIUM', 'Consistency', 'GT-09: ID namespace khác; VNTraffic có 120 mục track rỗng và 2 khóa frame–track trùng.', 'Dùng phép đối chiếu hình học và ánh xạ ID; chưa tự xóa nhãn.'),
        ('HIGH', 'Timeliness', 'GT-07/12 lịch sử và GT-10/11 snapshot không xác minh hiện trạng.', 'Không thay baseline triển khai 2026; chưa có SLA cập nhật của nhà cung cấp.'),
        ('HIGH', 'Completeness / measurement', '70/73 cơ chế cuộc thi từ tên; không có toàn bộ bài/điểm giám khảo.', 'Dùng tìm prior art; không dự đoán giải; đọc hồ sơ kỹ thuật gần nhất.'),
        ('MEDIUM', 'Validity', 'GT-10: treated và untreated cùng xuất hiện ở bản ghi 79.', 'Giữ văn bản, xác minh tiến độ theo hạng mục; không mã hóa nhị phân.'),
        ('HIGH', 'Validity', 'GT-20 ID31 có hai nhãn ngôn ngữ khác hướng; chưa tải ảnh/annotation.', 'Không làm nội dung chỉ dẫn/huấn luyện trước đối chiếu nhãn và hình gốc.'),
        ('MEDIUM', 'Lineage', 'GT-02: slug URL và kỳ trong nội dung có thể khác; số suy ngược tháng 9 không khớp bản tin tháng 9.', 'Dùng h1/nội dung, giữ từng phiên bản, chưa ghép chuỗi phân tích nguyên nhân.'),
    ]
    nulls = r['quality']
    quality = '# Kiểm toán dữ liệu bổ sung\n\n'
    quality += 'Phạm vi: snapshot cục bộ của các nguồn trọng tâm, ba file người dùng, danh mục 22 nguồn và kết quả đã có. Không tải lại nguồn. `all_22_source_review_coverage.csv` phân biệt kiểm lại cục bộ và giữ nguyên audit trước. 22 mã được kiểm đủ/duy nhất; không gọi lượt này là 22 lần kiểm tra trực tuyến mới.\n\n'
    quality += 'GT-01 lấy từ trang NSO/PXWeb, nhưng metadata của bảng ghi **“Thống kê chính thức: Không”** theo [dossier đã kiểm](../../sources/GT-01.md). Tính xác thực trang không thay xác nhận định nghĩa/so sánh hoặc độ đúng của số đo.\n\n'
    quality += md_table(['Dữ liệu', 'Số dòng', 'Grain / khóa', 'Ô khóa thiếu'], [
        [name, nulls[name]['rows'], ', '.join(nulls[name]['grain_key']), nulls[name]['required_key_null_cells']]
        for name in ['GT01', 'GT07', 'GT10', 'GT11', 'ideas']])+'\n\n'
    quality += f'''Khóa ngoại GT-07 status→segments: {nulls['GT07_segment_fk']['orphan_count']} orphan; IDEA→NGUON: {nulls['idea_source_fk']['orphan_count']}; GT-ID đề xuất→inventory: {nulls['idea_proposed_gt_fk']['orphan_count']}. Khớp mã GT chỉ xác minh mã tồn tại, không chứng minh dự án từng sử dụng dữ liệu đó. Khóa được kiểm thêm bằng biểu thức exact null/duplicate; mã định danh không đưa vào outlier/correlation như đại lượng khoa học.

Các bảng `*_eda_nulls`, `*_audit_nulls`, `*_outlier_screen`, `*_ranges` giữ toàn bộ cờ. Ngưỡng mặc định chỉ sàng lọc; thiếu award rank/treated/note có thể có ý nghĩa cấu trúc. Không tự bù, xóa ngoại lệ hay sửa raw. Pooled GT-01 trộn loại chỉ số/tỉnh/vùng nên outlier chỉ là cờ kỹ thuật, không đánh giá tỉnh bất thường. Ma trận tương quan của paired_numeric chứa difference=peak−midday, do đó quan hệ một phần do định nghĩa; không dùng làm phát hiện nhân quả. Các tuple số giống nhau ở bảng này là kết quả có thể lặp, không là khóa bản ghi gốc.

GT-08 đã đọc lại 50 NPY, kiểm hash/miền 0–1/tổng frame. GT-04 kiểm 1.125 đối tượng, khóa loại–ID và tọa độ node; không thực hiện GIS, đo khoảng cách hoặc suy thiếu hạ tầng từ thiếu tag. GT-20 giữ cờ nhãn và số do publisher công bố, chưa xác minh ảnh. GT-12 giữ riêng ba feed, không cộng chuyến có thể chồng lặp qua feed.

## Vấn đề và mức độ theo mục đích sử dụng

'''
    quality += md_table(['Mức', 'Chiều chất lượng', 'Kết quả/cờ', 'Xử lý'], items)
    quality += '''

## Scorecard và quyết định sử dụng

| Chiều | Đánh giá | Giới hạn |
| --- | --- | --- |
| Completeness | Có kiểm trường và khóa; còn thiếu thông tin quan trọng | Không có hồ sơ cơ chế đầy đủ, exposure hoặc baseline hiện tại |
| Accuracy | Kiểm được số học/hình học giữa tệp | Chưa có ground truth hiện trường để chấm accuracy thực tế |
| Consistency | FK hợp lệ; tổng vùng/ID cần giải trình | Không xem khớp tổng là chứng minh đo đúng thực tế |
| Timeliness | Đã xác định kỳ dữ liệu | SLA nhà cung cấp chưa có; hiện trạng 2026 chưa xác minh |
| Uniqueness | Kiểm đúng grain | Track trùng/nhãn tự do cần giữ để xử lý có căn cứ |
| Validity | Có kiểm kiểu, range và miền nhãn | Đơn vị velocity và nhãn song ngữ chưa đủ xác minh |

Điểm tổng số học: **không tính**. Không có ground truth/SLA/chuẩn chấp nhận được đồng thuận; chuyển tỷ lệ check đạt thành “accuracy 9/10” sẽ tạo độ chắc giả. Điều chỉnh mẫu scorecard của skill để giữ sáu chiều và cờ cụ thể, phù hợp hướng dẫn scientific-critical-thinking không biến số checklist thành thước đo độ chắc khoa học. Được dùng cho báo cáo mô tả và thiết kế xác minh; chưa đủ cho mô hình vận hành/khuyến nghị thay hạ tầng.

## Kiểm tra chính script của skill

- `assumptions_tracker.py` và `drilldown_analyzer.py` có entry point chạy demo, không thực thi CLI như mô tả. Runner import hàm thật với dữ liệu nghiên cứu; không lấy demo làm kết quả.
- `null_counter` dùng >= với ngưỡng 0 nên có thể báo FAIL cả 0% missing. Không truyền ngưỡng 0; kiểm exact số ô khóa thiếu riêng.
- `correlation_explorer` có thể lỗi khi danh sách strong pairs rỗng. Runner giữ ma trận pandas và ghi lỗi helper nếu gặp; không sửa skill toàn cục.
- `value_range_validator` có nhánh bắt lỗi so sánh rồi coi như không vi phạm. Runner yêu cầu dtype số và đủ cột trước khi gọi range; không dùng helper để chứng nhận schema.
- `qa_runner` thử parse mọi cột như ngày; QA riêng kiểm dtype/thời kỳ để tránh lấy kiểm tra ngày tự động làm chứng nhận. Mọi lần gọi/hàm/hash/warning nằm ở `skill_execution_log.json`.
'''
    write('03_kiem_toan_chat_luong_vi.md', quality)
    rows_html = ''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in items)
    write('audit_report.html', '<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kiểm toán dữ liệu giao thông</title>'
        '<style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:20px}table{border-collapse:collapse}td,th{padding:10px;border:1px solid #aaa;text-align:left;vertical-align:top}</style>'
        '<h1>Kiểm toán dữ liệu bổ sung — 19/11/2026</h1><p>Tự rà soát bởi Codex. Dùng có giới hạn cho báo cáo mô tả; chưa đủ cho vận hành. Không chấm điểm accuracy/SLA chưa có chuẩn đối chiếu.</p>'
        '<table><tr><th>Mức</th><th>Chiều chất lượng</th><th>Phát hiện</th><th>Xử lý</th></tr>'+rows_html+'</table>'
        '<p>Điều chỉnh cấu trúc mẫu data-quality-audit theo sáu chiều; nội dung từ kết quả chạy thực. Xem <a href="03_kiem_toan_chat_luong_vi.md">báo cáo đầy đủ</a>, <a href="measured_rechecks.json">số đo</a> và <a href="skill_execution_log.json">log</a>.</p></html>')

    write('04_muoi_phat_hien_da_kiem_lai_vi.md', '# 10 phát hiện giữ được sau rà soát\n\n'
        '[ĐÃ KIỂM SNAPSHOT / ĐÃ TÍNH] Sáu phát hiện đầu là số ghi nhận 2023–2024, bốn phát hiện sau là mô tả kiểm kê cơ quan. Không phát hiện nào ở đây là bằng chứng hiệu quả can thiệp hoặc hiện trạng 2026 đã được đo. Tính lại toàn bộ số của T01–T06 và giữ provenance/bộ lọc của cả mười trong JSON kèm theo.\n\n'+
        md_table(['Mã', 'Phát hiện', 'Căn cứ', 'Giới hạn'], [[f['id'], f['title_vi'], f['evidence_vi'], f['limitation_vi']] for f in findings])+
        '\n\n[DIỄN GIẢI] T07/T08 có cơ chế/thiếu hụt tại lý trình cụ thể hơn sáu tổng tỉnh, nên có thể ưu tiên xác minh nếu tiếp cận được Sơn La. Điều đó chưa chứng minh mức rủi ro, nhu cầu khách hàng hoặc phù hợp thể lệ hơn mọi lựa chọn khác.\n\n[BẤT ĐỊNH] Chưa có exposure, phỏng vấn, kiểm chứng can thiệp, crosswalk địa giới hiện tại hoặc nhu cầu trả tiền. Không dùng sáu ví dụ chọn sau EDA làm xếp hạng tỉnh nguy hiểm nhất.')

    text = '# 10 ý tưởng ứng viên và điều kiện để được phát triển\n\n'
    text += '''[ĐỀ XUẤT] Mười hồ sơ sau là ứng viên có thể bị bác bỏ, không là mười giải pháp đã chứng minh. Từng hồ sơ nối với một phát hiện T01–T10 và giữ rõ khoảng cách bằng chứng. C01–C06 mới có tín hiệu tổng địa bàn, chưa có cơ chế được xác minh; C07–C10 có thông tin hành lang, nhưng nhu cầu và hiệu quả vẫn chưa đo. Không tăng mức ưu tiên chỉ để đủ số lượng.

Đối chiếu danh mục cũ: O01→C07, O02→C08, O03→C09, O04→C02; O05 tách các điều kiện địa bàn trong C03/C05/C06. O06 hàng cồng kềnh vẫn giữ nguyên ở discovery/ như nhánh E0, chưa bổ sung vào nhóm ưu tiên vì chưa có bằng chứng địa phương. Các hồ sơ O cũ không bị xóa hoặc viết lại.

Thứ tự xác minh có điều kiện: C07/C08 nếu có đối tác địa bàn và xác nhận vấn đề còn tồn tại; C09/C10 cần xác nhận thêm khoảng trống vận hành; C01–C06 chờ hồ sơ chi tiết/đối tác. Không có ứng viên nào được xác lập tính mới, nhu cầu thị trường, mức sẵn sàng trả tiền hoặc khả năng thắng giải. Một công cụ thu thập/chuẩn hóa dữ liệu có thể hữu ích nhưng chưa đủ để thành đề tài an toàn giao thông đáp ứng thể lệ.

'''
    for c in candidates:
        text += f'## {c["id"]}. {c["title_vi"]}\n\n'
        for key, label in [('discovery_id','Phát hiện nối'), ('place_vi','Địa bàn'), ('verified_evidence_vi','Căn cứ đã có'),
            ('evidence_grade_vi','Mức bằng chứng'), ('user_vi','Người dùng giả định'), ('problem_hypothesis_vi','Giả thuyết vấn đề'),
            ('intervention_hypothesis_vi','Ý tưởng thử'), ('baseline_vi','So với cách hiện tại'), ('primary_outcome_vi','Đại lượng đo chính'),
            ('first_validation_vi','Kiểm chứng tiếp theo'), ('stop_rule_vi','Điều kiện dừng'), ('prior_art','Ý tưởng/giải pháp có trước'),
            ('competition_fit_vi','Phù hợp cuộc thi'), ('priority_vi','Trạng thái ưu tiên')]:
            text += f'**{label}:** {c[key]}\n\n'
    write('05_muoi_y_tuong_ung_vien_vi.md', text)

    write('06_thiet_ke_kiem_chung_tiep_theo_vi.md', '''# Thiết kế kiểm chứng tiếp theo — chưa thu dữ liệu

[KẾ HOẠCH] Chưa có khảo sát hoặc thử nghiệm nào trong phần này đã diễn ra. Không dùng các bố trí sau làm kết quả thực nghiệm; chưa tuyển mẫu, phân nhóm hay tính công suất từ số giả định.

## Cổng chung trước prototype

1. Xác minh hiện trạng, đối tượng, vấn đề lặp và đối tác có quyền cho khảo sát. Giữ cả lượt không xảy ra tình huống để có mẫu số.
2. Lập định nghĩa outcome, đơn vị quan sát, quy tắc missing/exclusion, baseline, mức cải thiện tối thiểu có ý nghĩa và chi phí vận hành trước khi đánh giá hiệu quả.
3. Đọc hồ sơ gần nhất và cách làm hiện hành; sự khác biệt địa danh chưa chứng minh mới về cơ chế. Nếu không có lợi ích tăng thêm có thể kiểm nghiệm thì dừng.
4. Tách thiết kế thử thuật toán/giao diện, hành vi và tác động an toàn. Không nhân số frame, lượt chấm hoặc video thành số người/địa điểm độc lập.

## C07: cảnh báo gặp xe dài

Xác minh cơ chế bằng quan sát không can thiệp trước. Nếu còn khoảng trống, thử mô phỏng hoặc sân kín có kiểm soát và người có chuyên môn. Người lái là đơn vị thử; nhiều tình huống của cùng người là đo lặp. So cách hiện tại với hỗ trợ đề xuất; phân thứ tự ngẫu nhiên/cân bằng theo người, chặn theo kinh nghiệm và điều kiện nhìn. Dùng tình huống tương đương, kiểm carry-over/học bài; nếu không thể washout, chọn thiết kế nhóm song song thay crossover. Người chấm không biết điều kiện khi khả thi. Báo nhận biết đúng, cảnh báo sai/bỏ sót, thời gian hành động và phân tâm; không lấy cải thiện mô phỏng làm giảm tai nạn trên QL.6B.

## C02: kỹ năng học sinh

Đối tượng và kỹ năng phải được xác minh trước, có phép của đơn vị/phụ huynh khi cần. Nếu can thiệp theo lớp, lớp là đơn vị phân bổ; nhiều học sinh trong lớp không là các lần phân bổ độc lập. Chặn theo trường/khối và phân lớp ngẫu nhiên khi có đủ lớp ở cả hai điều kiện. Không dùng một lớp thử và một lớp đối chứng rồi coi hàng trăm học sinh là hàng trăm đơn vị độc lập. So bài hiện hành có cùng thời lượng, đánh giá tình huống mới ngay sau và sau khoảng duy trì đã khóa trước; ghi thiếu theo dõi và tránh rò nội dung giữa lớp.

## C08/C10: quy trình bảo trì

Baseline là thời gian/tỷ lệ xử lý hồ sơ thực tế, không phải số ô untreated. Mỗi nhiệm vụ có hạng mục, thời điểm mở/đóng và kiểm chứng hiện trường; nhiều ảnh cùng nhiệm vụ không là nhiều nhiệm vụ độc lập. Nếu chỉ một tổ áp dụng trước–sau, giữ là pilot khả thi có nhiễu theo mùa/nguồn lực; muốn suy nhân quả phải có nhiều tổ/địa bàn, đối chứng đồng thời và phân bổ phù hợp. Chưa có dữ liệu sự kiện/mưa để thử mô hình dự báo sạt lở.

## Công suất, phân tích và quyết định dừng

Chưa chốt cỡ mẫu vì chưa có mức cải thiện tối thiểu, biến thiên nền, ICC theo lớp/tổ, số đơn vị tiếp cận, tỷ lệ thiếu và thiết kế cuối. Thu pilot đo chất lượng/khả thi trước; sau đó dùng statistical-power với thiết kế đã khóa, không lấy effect quan sát thuận lợi làm “observed power” biện minh. Nêu rõ mọi lần xem dữ liệu trung gian và quy tắc dừng; không thử nhiều outcome/cửa sổ rồi chỉ báo kết quả thuận lợi. Không triển khai can thiệp trên đường công cộng từ prototype chưa thẩm định.
''')

    skills = json.loads((out / 'skills_used.json').read_text(encoding='utf-8'))
    calls = json.loads((out / 'skill_execution_log.json').read_text(encoding='utf-8'))
    use_map = {
        'programmatic-eda': 'Chạy overview/null/outlier/distribution/correlation trên bảng phù hợp; tách ID và cờ khỏi kết luận.',
        'data-quality-audit': 'Chạy null/duplicate/FK/range/freshness; xác minh dtype và khóa riêng; scorecard không tạo accuracy giả.',
        'analysis-assumptions-log': 'Khởi tạo log, ghi 8 giả định, xác nhận/bác bỏ phần kiểm được và xuất critical list.',
        'time-series-analysis': 'Kiểm khoảng thời gian, ngày thiếu, mùa vụ và đầu vào; không chạy mô hình khi không đủ điều kiện.',
        'root-cause-investigation': 'Chạy drill_down theo 63 tỉnh; chỉ phân rã số học, không quy nguyên nhân.',
        'analysis-qa-checklist': 'Chạy qa_runner trên bốn bảng; checklist từng mục và ghi quyết định giao có giới hạn.',
        'statistical-analysis': 'Kiểm đơn vị/độc lập, tái tính tương phản, độ nhạy cân, Shapiro và hạ phạm vi p/CI.',
        'scientific-critical-thinking': 'Tách nguồn, số đo, diễn giải, giả thuyết; kiểm bias, proxy, tính mới và phạm vi địa phương.',
        'experimental-design': 'Bố trí kế hoạch mô phỏng theo người/lớp/tổ, kiểm pseudoreplication, đối chứng và phân bổ; chưa chạy thử.',
        'scientific-visualization': 'Hình có ngày missing rõ, toàn bộ điểm ngày và bảng nguồn; kiểm metadata và xem ảnh.',
        'literature-review': 'Rà log/tính đầy đủ/prior art; kiểm lại nguồn FHWA và trích dẫn quy trình; không nhận systematic review.',
        'geopandas': 'Có SKILL.md, đã đọc; không dùng phép GIS. Python package chưa cài, thiếu tuyến/CRS/điểm đủ tin cậy.',
        'statsmodels': 'Có SKILL.md, đã đọc; không fit model. Python package chưa cài, chuỗi/thiết kế chưa đủ cho mô hình đề xuất.',
    }
    write('07_skill_va_tai_lap_vi.md', '# Skill thực sự dùng và tái lập\n\n'+
        'Đã kiểm thư mục global và đọc SKILL.md thật trước khi áp dụng. Không có skill được yêu cầu nào bị thiếu; có hướng dẫn không đồng nghĩa đã có Python package. Giữ Python 3.10 của nghiên cứu, không báo là chạy trên các stack pin mới của skill. Lượt này áp dụng hướng dẫn phương pháp và helper tương thích; không chạy Pingouin/PyMC, pydoe hay GeoPandas/statsmodels.\n\n'+
        md_table(['Skill', 'Tình trạng', 'Thao tác/giới hạn'], [[s['skill'], s['use'], use_map[s['skill']]] for s in skills])+
        f'\n\nCó {len(calls)} mục trong log gọi helper/cảnh báo. `skills_used.json` chứa SHA256 của từng SKILL.md; `skill_execution_log.json` chứa SHA256 script thật, hàm gọi và warning.\n\n'+
        '''Từ gốc repo, dùng thư mục output mới:

```powershell
python -X utf8 traffic-data-research/src/revalidate_research.py --output traffic-data-research/reports/revalidation_replay
python -X utf8 -m unittest discover -s traffic-data-research/tests -v
```

Runner từ chối output đã tồn tại. Có thể chỉ định `--skill-root` trỏ đến thư mục cài skill tương ứng. Để tái lập helper đúng phiên bản cần các hash trong log, không chỉ cùng tên skill. Cần các snapshot raw cục bộ theo manifest, ba file `data/`, bảng dẫn xuất và báo cáo discovery đã có; clone public chưa chứa tất cả raw. `input_checksums.json` ghi đầu vào dùng trực tiếp; `preservation_check.json` kiểm bytes trước/sau các tệp gốc/kết quả cũ. Lượt đầu tự động nằm ở `../revalidation_2026_11_19/`; lượt v2 mở rộng kiểm và sinh các báo cáo này, giữ lượt đầu.

Không tải lại raw, thay input, huấn luyện mô hình giải thưởng, tự điền ngày thiếu hoặc sửa nhãn gốc. Code được bổ sung độc lập với pipeline cũ. `test_results.txt` là log thực tế trong workspace đủ snapshot, không là CI cho clone thiếu dữ liệu. Các báo cáo cũ phải đọc cùng `01_nhung_ket_luan_da_thay_doi_vi.md`.

Nguồn quy trình: Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. [arXiv](https://doi.org/10.48550/arXiv.2609.00065). Đã đối chiếu lại trang arXiv ngày 19/11/2026, bản mới nhất hiển thị v2; đây là nguồn phần mềm/phương pháp, không là bằng chứng giao thông.
''')

    write('08_ra_soat_tai_lieu_va_tinh_moi_vi.md', f'''# Rà lại tài liệu và tính mới

Lượt này tiếp tục rà soát tường thuật một người đã có, không khởi động một systematic review mới. Log cũ có {r['literature']['api_rows_logged']} kết quả API trong {r['literature']['api_records_table']} dòng bảng bản ghi; không đồng nghĩa từng đó nghiên cứu độc lập hay toàn văn đã đánh giá. Các truy vấn chưa phân trang đủ, không được dùng làm bằng chứng tìm kiếm exhaustive. Giữ log, prior_art_matrix và mức đọc abstract/full text của báo cáo trước.

| Họ ý tưởng | Bằng chứng có trước | Hệ quả |
| --- | --- | --- |
| Cảnh báo cua/đối đầu | IDEA-032 được công bố trong danh mục; FHWA mô tả báo hiệu, vạch và cảnh báo động ở đường cong | C07/C09 không thể lấy “cảnh báo khúc cua” làm tuyên bố mới; C08 còn phải đối chiếu quy trình bảo trì hiện tại |
| Học sinh | IDEA-042/035/025 và các chương trình vùng trường trong review trước | C02 cần đối tượng/kỹ năng và lợi ích tăng thêm; giải cũ không chứng minh hiệu quả giáo dục |
| Điều tiết | IDEA-033/043/054/060, ITS đã mô tả trong GT-16 | C04 phải so với hệ thống hiện hành tại nút, chưa đủ lý do chọn thuật toán mới |
| Kiểm kê sạt lở/phối hợp tuyến | GT-10/11 có nguồn chung; thiếu nghiên cứu kiểm chứng đúng địa bàn | C10 chưa là mô hình cảnh báo sạt lở và chưa xác lập novelty |

Đối chiếu bổ sung ngày 19/11/2026: [FHWA — Enhanced Delineation for Horizontal Curves](https://highways.dot.gov/safety/proven-safety-countermeasures/enhanced-delineation-horizontal-curves) mô tả nhiều biện pháp cho đoạn cong, gồm báo hiệu động. Nội dung này xác minh có phương án tương tự, không cung cấp effect size chuyển giao sang Sơn La. [Bản ghi arXiv về skill](https://arxiv.org/abs/2609.00065) được kiểm lại để trích nguồn phương pháp; không dùng như nghiên cứu giao thông.

Chưa tra cứu đầy đủ sản phẩm, hồ sơ kỹ thuật các bài thi, bằng sáng chế hoặc mọi nghiên cứu mới; chưa có người đánh giá độc lập. Không coi địa danh mới, không thấy từ khóa, đăng ký DOI hay giải thưởng là bằng chứng hiệu quả hoặc tính mới. Không gộp nhiều báo cáo cùng chương trình/dữ liệu thành tái lập độc lập. Mỗi ứng viên giữ novelty_status=NOT_ESTABLISHED.
''')

    qa = json.loads((out / 'automated_qa.json').read_text(encoding='utf-8'))
    fails = [(name, c['check'], c['detail']) for name, checks in qa.items() for c in checks if c['status'] == 'FAIL']
    warns = [(name, c['check'], c['detail']) for name, checks in qa.items() for c in checks if c['status'] == 'WARN']
    # Item-by-item master checklist, rather than one unsubstantiated "PASS" per section.
    checklist = [
        ('1.1', 'Câu hỏi thực của người dùng', 'PASS', '10 phát hiện + 10 ứng viên, ưu tiên chứng cứ; giữ 10 mẫu hình cũ.'),
        ('1.2', 'Ranh giới phạm vi', 'PASS', 'Không suy AICC22/benchmark thành hiện trạng Việt Nam.'),
        ('1.3', 'Thời kỳ đúng đề bài', 'CAVEAT', 'Dữ liệu lịch sử được ghi đúng kỳ; chưa có baseline 2026.'),
        ('1.4', 'Định nghĩa thuật ngữ', 'PASS', 'Ứng viên, ngách, bản ghi nguy cơ, số vụ khác nguy cơ/exposure.'),
        ('2.1', 'Nguồn được xác định', 'PASS', '22 mã đối chiếu; URL/hash/provenance được giữ.'),
        ('2.2', 'Freshness', 'CAVEAT', 'Kỳ cũ/không có SLA; dùng mô tả, không triển khai.'),
        ('2.3', 'Lineage', 'PASS', 'Raw→processed→recheck; hash trực tiếp và manifest bảo toàn.'),
        ('2.4', 'Quyền truy cập', 'PASS', 'Chỉ đọc snapshot đã có; không thu nguồn/đăng dữ liệu mới.'),
        ('2.5', 'Vấn đề nguồn và tác động', 'PASS', 'Báo tổng vùng, mã track, revision tháng, nhãn song ngữ.'),
        ('3.1', 'Kiểu join và số dòng', 'PASS', 'FK riêng; đối chiếu multiset; không spatial join mù.'),
        ('3.2', 'Grain/cộng trùng', 'PASS', '63 tỉnh tách tổng vùng; frame/track/ngày không là mẫu độc lập.'),
        ('3.3', 'Null', 'PASS', 'Hai ô Khác giữ missing; không điền 0 ngày không quan sát.'),
        ('3.4', 'Múi giờ', 'PASS', 'GT-07 UTC→UTC+7 trước ghép.'),
        ('3.5', 'Chia 0', 'PASS', 'province_changes giữ NA nếu base 0; có test.'),
        ('3.6', 'Mẫu số', 'PASS', 'Previous-year count/contribution/annotation fraction ghi riêng.'),
        ('3.7', 'Spot-check ít nhất 3 dòng', 'PASS', 'Đối chiếu toàn bộ chỉ số 6 ví dụ tỉnh với tính lại.'),
        ('4.1', 'Cỡ mẫu cho claim', 'CAVEAT', 'Không đủ cho nhân quả/dự báo; đã giới hạn claim.'),
        ('4.2', 'Phép kiểm', 'CAVEAT', 't/CI iid chỉ tái lập kiểm toán; không quảng bá p mới.'),
        ('4.3', 'Uncertainty', 'PASS', 'CI cũ giữ cùng giả định; sensitivity không gọi là CI.'),
        ('4.4', 'Multiplicity', 'N/A', 'Không thêm family kiểm định hoặc dự đoán giải; EDA không p.'),
        ('4.5', 'Nhân quả', 'PASS', 'Đóng góp tỉnh/giải thưởng không được gọi là nguyên nhân.'),
        ('4.6', 'Outlier/độ nhạy', 'PASS', 'Giữ toàn bộ, cân khác/LODO được báo không chọn dấu.'),
        ('5.1', 'Mỗi kết luận có căn cứ', 'PASS', 'JSON T/C có mã nguồn; ý tưởng giả thuyết tách riêng.'),
        ('5.2', 'Không vượt dữ liệu', 'PASS', 'E0 cơ chế của 6 tỉnh; không gán nhóm học sinh/loại xe.'),
        ('5.3', 'Bất ngờ được báo', 'PASS', 'GT-09 khớp geometry, GT-07 đổi dấu sensitivity được giữ.'),
        ('5.4', 'Giới hạn rõ', 'PASS', 'Novelty/demand/current status đều chưa xác lập.'),
        ('5.5', 'Hành động theo kết quả', 'PASS', 'Từng ứng viên có baseline, phép thử và điều kiện dừng.'),
        ('6.1', 'Trục/hình', 'REVIEW_REQUIRED', 'Đã sinh metadata; cần xem ảnh bằng công cụ trước giao.'),
        ('6.2', 'Loại biểu đồ', 'PASS', 'Scatter không nối missing, có bảng nguồn.'),
        ('6.3', 'Định dạng số', 'PASS', 'Báo cáo làm tròn; JSON giữ precision tính toán.'),
        ('6.4', 'Ngôn ngữ', 'PASS', 'Báo cáo tiếng Việt; giải thích thuật ngữ và phạm vi.'),
        ('6.5', 'Link/placeholder', 'REVIEW_REQUIRED', 'Kiểm bằng script kiểm thử và xem file trước giao.'),
    ]
    dump(out / 'qa_checklist.json', [dict(zip(['item', 'question_vi', 'status', 'evidence_vi'], row)) for row in checklist])
    write('09_qa_va_quyet_dinh_giao_vi.md', '# QA và quyết định giao\n\n'
        'Tác giả/người tự rà soát: Codex, ngày 19/11/2026; chưa có reviewer độc lập hoặc chữ ký phê duyệt của người dùng. Đối tượng: nhóm tìm đề tài dự thi.\n\n'+
        f'qa_runner trên bốn bảng: {len(fails)} FAIL, {len(warns)} WARN. Log đầy đủ ở `automated_qa.json`. Kiểm tự động không chứng nhận đúng thực tế hoặc phương pháp.\n\n'+
        md_table(['Mục', 'Câu hỏi', 'Trạng thái', 'Căn cứ'], checklist)+
        '\n\nQuyết định: **giao báo cáo mô tả có điều kiện**, sau khi hoàn tất kiểm ảnh/link và kiểm thử ghi ở `delivery_verification.json`. Không phê duyệt triển khai, kết luận nhân quả, tính mới hoặc dự đoán giải. Các cờ thiếu dữ liệu được giữ là giới hạn, không tự “risk accept” thay cơ quan/khách hàng. Không tuyên bố toàn bộ checklist đã PASS.\n\n'+
        'Những việc phải xong trước claim mạnh hơn: xác minh hiện trạng/địa giới, cơ chế và exposure; hồ sơ kỹ thuật prior art; mẫu số/cỡ mẫu phù hợp; đối chứng và thẩm quyền pilot. Chưa có ngày cam kết hoặc người chịu trách nhiệm bên ngoài được tự gán.')

    preservation = json.loads((out / 'preservation_check.json').read_text(encoding='utf-8'))
    write('README.md', f'''# Checkpoint tăng độ chắc bằng chứng — 19/11/2026

Tiếp tục nghiên cứu đã có, giữ nguyên raw, đầu vào và kết quả cũ. Đã tính lại bằng code, không chỉ đề xuất kế hoạch. Check bytes trước/sau: **{preservation['files_checked']} tệp được bảo toàn**, không tệp nào trong tập kiểm thay đổi.

Kết quả quan trọng: VNTraffic TXT/JSON khớp **16.036/16.036 hộp hình học**; “8.771 bất đồng” cũ không là bằng chứng tọa độ nhãn sai. GT-07 tái lập số cũ nhưng nhạy mạnh với cân ngày/cặp, nên chỉ giữ tương phản mô tả và hạ phạm vi diễn giải p/CI iid. Sáu biến động tỉnh tính lại không đổi. Lịch sử giải thưởng tiếp tục chỉ phục vụ tìm ý tưởng có trước.

- [Những kết luận thay đổi và không thay đổi](01_nhung_ket_luan_da_thay_doi_vi.md)
- [10 phát hiện giao thông đã kiểm lại](04_muoi_phat_hien_da_kiem_lai_vi.md)
- [10 hồ sơ ý tưởng ứng viên, bằng chứng và điều kiện dừng](05_muoi_y_tuong_ung_vien_vi.md)
- [Kiểm toán chất lượng](03_kiem_toan_chat_luong_vi.md) / [bản HTML](audit_report.html)
- [Thống kê, chuỗi thời gian và phân rã](02_tham_dinh_thong_ke_va_thoi_gian_vi.md)
- [Giả định và quyết định](assumptions_log.md)
- [Thiết kế kiểm chứng tiếp theo](06_thiet_ke_kiem_chung_tiep_theo_vi.md)
- [Skill đã dùng, hash và tái lập](07_skill_va_tai_lap_vi.md)
- [Tài liệu/tính mới](08_ra_soat_tai_lieu_va_tinh_moi_vi.md)
- [QA và quyết định giao](09_qa_va_quyet_dinh_giao_vi.md)

Mười phát hiện là bằng chứng lịch sử/kiểm kê có phạm vi, không phải mười nguyên nhân đã xác minh. Mười ứng viên là giả thuyết: C01–C06 chưa biết cơ chế địa phương; C07–C10 có chi tiết hành lang nhưng chưa có hiệu quả/nhu cầu/tính mới. C07/C08 đáng xác minh trước **nếu** nhóm tiếp cận được địa bàn và vấn đề còn tồn tại. Không coi đủ số lượng là đủ điều kiện phát triển.

Giữ nguyên [10 mẫu hình lịch sử cuộc thi](../discovery/10_quy_luat_y_tuong_vi.md) và [6 hướng ban đầu](../discovery/ngach_dia_phuong_va_huong_du_thi_vi.md). Đọc kết quả cũ cùng log hiệu chỉnh. Chưa khảo sát hiện trường, thử can thiệp hoặc xác lập tính mới. Dữ liệu mới, công suất thử nghiệm và tra cứu hồ sơ kỹ thuật đầy đủ vẫn là các cổng cần vượt; không tự điền bằng ví dụ giả.

Tái lập riêng checkpoint bằng `python -X utf8 traffic-data-research/src/revalidate_research.py --output traffic-data-research/reports/revalidation_replay` từ gốc repo; output phải chưa tồn tại. `measured_rechecks.json`, JSON T/C, các CSV, checksum và log helper giữ dấu vết tính toán. Không cần chạy lại toàn bộ pipeline cũ.
''')


if __name__ == '__main__':
    raise SystemExit('Called by revalidate_research.py; requires its measured checkpoint outputs.')
