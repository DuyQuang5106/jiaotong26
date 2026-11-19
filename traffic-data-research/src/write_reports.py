"""Render Vietnamese research reports from measured artifacts and explicit judgments."""
import importlib.metadata as meta,json,platform,subprocess,sys
from pathlib import Path
import pandas as pd
from acquire import ROOT
from build_registry import NOTES
from ingest import events
def write(path,text): (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
def table(df):
    cols=df.columns.tolist(); rows=['| '+' | '.join(cols)+' |','|'+'|'.join(['---']*len(cols))+'|']
    for row in df.fillna('NOT_AVAILABLE').itertuples(index=False,name=None): rows.append('| '+' | '.join(str(x).replace('|','/').replace('\n',' ') for x in row)+' |')
    return '\n'.join(rows)
def main():
    r=json.loads((ROOT/'reports/measured_results.json').read_text(encoding='utf-8')); track=json.loads((ROOT/'reports/GT-09_results.json').read_text(encoding='utf-8')); gtfs=json.loads((ROOT/'reports/GT-12_results.json').read_text(encoding='utf-8'))
    audit=pd.read_csv(ROOT/'registry/source_audit.csv'); matrix=pd.read_csv(ROOT/'reports/03_problem_evidence_matrix.csv'); masks=pd.read_csv(ROOT/'data/processed/GT-08_binary_masks_summary.csv'); rates=pd.read_csv(ROOT/'data/processed/GT-01_GT-17_population_rates.csv'); inv={x['Mã nguồn']:x for x in json.loads((ROOT/'registry/inventory.json').read_text(encoding='utf-8'))}
    measured={
    'GT-01':f"639 ô thống kê (71 nhãn địa lý × 3 năm × 3 chỉ tiêu), hai giá trị thiếu. Toàn quốc 2024: 23.667 vụ, 11.101 người chết, 17.424 người bị thương. So 2023, số vụ +7,25%, số chết −4,53%. Ba ô tổng vùng miền Trung 2024 lệch tổng tỉnh thành phần: +2.914 vụ, +1.718 chết, +2.104 bị thương. Không sửa số gốc.",
    'GT-02':'Ba báo cáo sơ bộ tháng 8–10/2026. Tháng 10: 1.266 vụ, 720 chết, 765 bị thương. Tháng 9 riêng: 1.327/782/793; tháng 10 cộng mức giảm đã công bố suy ra tháng 9 là 1.330/787/791. Sai lệch lần lượt +3/+5/−2, có thể do cập nhật hoặc lỗi báo cáo; chưa có giải thích từ cơ quan.',
    'GT-04':'Mẫu bbox 106.797–106.801E, 10.868–10.872N: 1.125 đối tượng (1.026 node, 88 way, 11 relation), 53 đối tượng có highway, 5 có crossing và 1 có amenity=school. Đối tượng trả về có thể mở rộng ra ngoài bbox. Đây là mức ghi tag trong mẫu thuận tiện, không chứng minh thiếu công trình.',
    'GT-06':'Hai hàng công bố kỳ 2025: Hà Nội congestion 49,2%, TP.HCM 46,9%; không tải probe hoặc mẫu số chuyến. Dùng mô tả cấp thành phố, không xác định điểm đen hay đánh giá tai nạn.',
    'GT-07':f"5 bảng: nodes 577.967; segments 84.633; streets 5.553; segment_status 90.938; train 33.441 dòng. Trạng thái trải 03/07/2020–22/04/2021 UTC, 10.027 segment, 120 ngày địa phương có quan sát. Một ngày chiếm 39,69% dòng. 107 giá trị velocity >120 trên thang gốc, 448 bằng 0; đơn vị chưa xác minh. 154 đoạn có length=0; train thiếu max_velocity ở 28.495/33.441 dòng. Không coi velocity cao là vi phạm khi thiếu định nghĩa.",
    'GT-08':f"{len(masks)} mảng NPY nhị phân, {int(masks.frames.sum()):,} frame nhãn, {int(masks.abnormal_frames.sum()):,} frame abnormal, tỷ phần {masks.abnormal_frames.sum()/masks.frames.sum():.2%} trong các file nhãn tải được. Đếm {int(masks.event_runs.sum())} chuỗi liên tiếp giá trị 1, không gọi là số xe/số vi phạm độc lập. Chỉ có nhãn 0/1; không xác định riêng hàng cồng kềnh. Không phải tỷ lệ ngoài thực địa.",
    'GT-09':'VNTraffic TXT: 16.036 hộp, 501 chỉ số frame (0–500), 85 track_id duy nhất, 2 khóa frame-track trùng. JSON: 205 track, cũng 16.036 hộp; ghép theo frame và ID nguyên bản không khớp 8.771 hộp. Đây là khác biệt biểu diễn/định danh chưa được giải thích, không tự quy thành lỗi toàn bộ ground truth. AICC22-Custom TXT 1.185 hộp/21 ID, JSON 2.439 hộp/25 ID; không dùng tập này suy luận Việt Nam. Chưa tính tốc độ thực, TTC hay PET.',
    'GT-10':'107 bản ghi trên 19 nhãn tuyến, đầy đủ theo tổng web. 48/107 mô tả có cụm “tầm nhìn”, 105/107 có “cong” hoặc “cua”; 19 ô đã xử lý không rỗng và 89 ô chưa xử lý không rỗng. Hai trường không được giả định loại trừ nhau hoặc nhị phân hoàn tất. Quy tắc chặt “hạn chế tầm nhìn” chỉ cho 16/107, cho thấy độ nhạy của mã hóa văn bản.',
    'GT-11':'58 bản ghi trên 17 nhãn tuyến, đủ theo tổng web. QL.4G có 15/58 bản ghi. Đây là danh mục nguy cơ, không phải 58 lần sạt lở hoặc 58 tai nạn. Trùng nhãn tuyến giữa GT-10/11 chỉ là khả năng ghép thô.',
    'GT-12':'Mỗi feed: 224 route_id, 7.670 stop_id nhưng chỉ 3.146 cặp tọa độ duy nhất. Chuyến AM/MD/PM lần lượt 3.024/6.713/3.301; stop_times 100.117/224.166/110.323. Cả ba calendar là 01/01–31/12/2018; headway lịch trình trung vị theo route trong từng khung là 12 phút. Không có trip/stop mồ côi hoặc khóa trip-sequence trùng. Không cộng ba khung thành lượt vận chuyển thực, không suy độ đúng giờ.',
    'GT-17':'XLSX v1.1 có 18 sheet. Trích 10 giá trị dân số lịch sử 2015–2024 từ sheet Population, dòng Medium (cached values), giữ tách khỏi dự báo. Ghép năm cấp quốc gia với GT-01 cho số chết/100.000 dân: 2022=6,43; 2023=11,59; 2024=10,95. Dân số là mẫu số gánh nặng dân số, không là lưu lượng xe. GT-17 dùng lại NSO, không phải xác nhận độc lập; cached formula không chứng minh đã tái tính mô hình.',
    'GT-20':'classid.csv 82 lớp, tổng Count công bố 19.748; min 32, max 1.446, tỷ số max/min 45,19. ID31: tên Anh là No Moto Turn Left còn tiếng Việt ghi “Cấm xe máy rẻ phải”. Đây là cờ cần rà soát nhãn, chưa chứng minh mô hình kém hoặc học sinh thiếu kiến thức. ZIP ảnh 904,8 MB vượt trần nên không tải.'}
    limits={sid:NOTES[int(sid[-2:])][1] for sid in measured}
    files={sid:'src/eda.py' for sid in measured}; files.update({'GT-02':'src/supplemental_analysis.py; src/triangulation.py','GT-08':'src/supplemental_analysis.py','GT-09':'src/extended_analysis.py','GT-12':'src/extended_analysis.py','GT-17':'src/extended_analysis.py'})
    artifacts={'GT-01':'GT-01_aggregates.csv','GT-02':'GT-02_monthly_counts.csv','GT-04':'GT-04_osm_sample.csv','GT-06':'GT-06_published_city_summary.csv','GT-07':'GT-07_segment_status.csv','GT-08':'GT-08_binary_masks_summary.csv','GT-09':'GT-09_VNTraffic_boxes.csv','GT-10':'GT-10_hazards.csv','GT-11':'GT-11_hazards.csv','GT-12':'GT-12_hanoi_gtfs_am_stop_times.csv','GT-17':'GT-17_historical_population.csv','GT-20':'GT-20_classes.csv'}
    questions={
        'GT-01':['Tổng vùng có khớp các tỉnh thành phần không?','Số vụ và số chết 2023–2024 đổi thế nào khi giữ nguyên địa giới cũ?','Tỷ lệ theo dân số thay đổi kết luận mô tả tới đâu?'],
        'GT-02':['Ba báo cáo tháng có nhất quán với mức tăng giảm tháng liền trước không?','Số sơ bộ có dấu hiệu revision nào?','Có đủ tháng và exposure để kiểm định mùa vụ hay không?'],
        'GT-04':['Mẫu nhỏ có bao nhiêu đối tượng mang tag trường/vạch qua đường?','Way/relation có mở rộng ra ngoài bbox khiến số đếm sai phạm vi không?','Có thể khẳng định thiếu hạ tầng từ tag trống hay không?'],
        'GT-06':['Hai chỉ số công bố thuộc kỳ nào?','Chênh lệch thành phố có thể xác định một nút ùn tắc hay không?','Mẫu số probe và ranh giới đô thị có được cung cấp trong bảng không?'],
        'GT-07':['Quan sát có tập trung ở một ngày hoặc giờ không?','Ghép cùng đoạn-cùng ngày có còn chênh lệch peak–midday không?','Sàng lọc ngoại lệ và bỏ từng ngày ảnh hưởng ước lượng thế nào?'],
        'GT-08':['Tổng frame mask tải được là bao nhiêu, có nhãn khác 0/1 không?','Tỷ phần theo frame khác trung bình tỷ phần theo video thế nào?','Có nhãn riêng loại hàng cồng kềnh để ước lượng tần suất không?'],
        'GT-09':['TXT và JSON có cùng số hộp, track và khóa frame-track không?','Có track gián đoạn hoặc khóa trùng trước tính quỹ đạo không?','Đã có camera calibration và thời gian quay đủ tính TTC/PET chưa?'],
        'GT-10':['Bao nhiêu mô tả nhắc tầm nhìn và độ cong?','Thay cụm từ mã hóa có làm số đếm thay đổi không?','Ô đã/chưa xử lý có thể diễn giải thành nhị phân hoàn tất không?'],
        'GT-11':['Danh mục đủ 58 hàng qua phân trang chưa?','Phân bố bản ghi theo tuyến có tập trung ở đâu?','Có ngày sự kiện hoặc GPS đủ ghép mưa/tai nạn chưa?'],
        'GT-12':['Calendar khác ngày metadata cập nhật thế nào?','Stop_id có đại diện điểm dừng vật lý duy nhất không?','Khóa trip/stop, thứ tự trạm và headway lịch trình có nhất quán không?'],
        'GT-17':['Giá trị nào là lịch sử, giá trị nào là dự báo/tham số?','Dân số cùng năm có thể làm mẫu số mô tả quốc gia không?','Nguồn dân số có độc lập NSO để triangulation hay dùng lại nguồn?'],
        'GT-20':['Count công bố lệch giữa lớp tới mức nào?','Có mâu thuẫn tên Anh/Việt ảnh hưởng sử dụng giáo dục không?','Bảng lớp có cho phép kết luận mật độ biển hoặc lỗi người học không?']}
    for sid,finding in measured.items():
        page=f'''# Kết quả dữ liệu {sid}

[MEASURED RESULT] {finding}

Nguồn: {inv[sid]['Link nguồn gốc']}. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/{sid}.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/{artifacts[sid]}`. Mã thực thi: `{files[sid]}`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

{chr(10).join(str(i+1)+'. '+q for i,q in enumerate(questions[sid]))}

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] {limits[sid]}

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] {NOTES[int(sid[-2:])][2]}
'''
        write(f'reports/{sid}_findings_vi.md',page)
    test=r['GT-07']['exploratory_test']
    write('reports/02_data_findings_vi.md',f'''# Kết quả từ dữ liệu thực

Ngày nghiên cứu: 19/11/2026. Phân tích mô tả/kiểm toán 12 mã nguồn: {', '.join(measured)}. Chỉ GT-07 có một kiểm định thăm dò định lượng mới; các nguồn khác có kiểm tra tính nhất quán/độ nhạy, không ép tạo p-value từ metadata hoặc tổng hợp không độc lập.

'''+ '\n\n'.join(f'## {sid}\n\n[MEASURED RESULT] {text}\n\n[NOT VERIFIED] {limits[sid]}\n\nChi tiết: [{sid}_findings_vi.md]({sid}_findings_vi.md).' for sid,text in measured.items())+f'''

## Kiểm định thăm dò GT-07

[MEASURED RESULT] Sau đổi timestamp Z sang UTC+7, so sánh khung 07:00–08:59 và 16:00–17:59 với 10:00–14:59. Lấy trung vị trong segment × ngày × khung, giữ cặp có cả hai khung, rồi trung bình chênh lệch theo ngày: 404 segment-ngày, 26 ngày. H0: trung bình chênh lệch ngày bằng 0, H1 hai phía. Ước lượng −3,46 đơn vị velocity gốc; bootstrap 5.000 mẫu theo ngày, seed 42, khoảng percentile 95% [−10,07; 1,79]. t(25)=−1,117, p=0,2748. Một tương phản thăm dò, không quét nhiều giả thuyết để chọn p nhỏ.

[INTERPRETATION] Chưa đủ bằng chứng bác bỏ H0 dưới giả định kiểm định; đây là **NO EVIDENCE**, không phải **EVIDENCE OF NO EFFECT**. Phụ thuộc giữa ngày, phủ quan sát chọn lọc và đơn vị chưa xác minh hạn chế suy luận. Không gọi các số này là km/h. Sau sàng lọc độ nhạy 0–120 trên thang gốc, ước lượng −3,43; bỏ lần lượt một ngày cho ước lượng khoảng −4,11 tới −1,20. Không coi 90.938 dòng là các mẫu độc lập.

Bảng: `../data/processed/GT-07_paired_segment_day.csv`, `GT-07_paired_day_effects.csv`, `GT-07_daily_coverage.csv`. Biểu đồ quan sát: `../figures/GT-07_hourly_coverage.png`. Mã: `src/eda.py`.

## Tỷ lệ theo dân số và kiểm tra đối chiếu

[MEASURED RESULT] Công thức = số ghi nhận / (dân số triệu × 10), đơn vị /100.000 dân. Bảng tái lập: `../data/processed/GT-01_GT-17_population_rates.csv`. Dân số lịch sử, không dùng dự báo. Chưa có khoảng tin cậy cho các tổng hành chính do chưa mô hình hóa sai số thu thập; khoảng Poisson không xử lý sai lệch ghi nhận nên không thêm cho có.

[NOT VERIFIED] Sai lệch tổng vùng NSO và revision báo cáo BCA còn nguyên. Không kết luận tăng vụ năm 2023 là tăng nguy cơ thực do chưa xác minh định nghĩa, cách ghi nhận và độ phủ. Không hài hòa tỉnh 2025–2026 vì chưa có crosswalk; giữ địa giới gắn với thời kỳ 2022–2024.

## Triangulation

Tương thích khóa và kết quả ghép thô: `cross_source_compatibility.csv`. GT-01/17 ghép được năm cấp quốc gia nhưng cùng gốc NSO; GT-10/11 cùng cơ quan, chỉ đối chiếu nhãn tuyến, không xác nhận độc lập tai nạn. GT-06/07 khác thời kỳ; GT-08/09 khác camera/đơn vị. Không tạo điểm rủi ro bằng cách ghép giả những nguồn này. Chưa có vấn đề đạt E3/E4.
''')
    counts=audit.access_status.value_counts()
    classes='\n'.join(f'- {c}: {len(g)} — '+', '.join(g.source_id) for c,g in audit.groupby('access_status'))+'\n- F_BROKEN_OR_MISSING: 0 mã ở phân lớp cuối; riêng landing Geofabrik thất bại hai lần được ghi trong GT-04.\n- G_NOT_YET_CHECKED: 0.'
    write('reports/01_source_reliability_vi.md',f'''# Độ tin cậy và khả năng tiếp cận

[VERIFIED SOURCE FACT] Đã kiểm tra cả 22 mã qua HTTP thực, giữ phản hồi thô và checksum. A/B chỉ cấp khi tải và đọc được bảng/mảng. HTTP 200 của portal không được coi là dữ liệu mở.

{classes}

Chi tiết từng lần truy cập: `../registry/source_audit.csv`, `http_events.jsonl`, `raw_manifest.json` và 22 dossier. GT-04 phân lớp A cho mẫu API OSM chính thức, không tuyên bố Geofabrik hoạt động. GT-02/06/20 phân lớp B cho bảng tổng hợp trích được, không phải raw cá thể. GT-17 là tổng hợp/tham số, không log giao thông.

[INTERPRETATION] Tin cậy cần tách: tính xác thực trang, tính đầy đủ bản tải, tính đúng định nghĩa và khả năng khái quát. Nguồn chính thức vẫn có sai lệch tổng và revision. Đối chiếu NSO/BCA và kiểm tra frame-track GT-09 phát hiện vấn đề cần xác minh. Các bảng mô hình hóa/tuyển chọn sự kiện/metadata nhập kho không đại diện điều kiện hiện tại.

[NOT VERIFIED] Không xác nhận license chỉ từ chữ public. GT-07 có CC0 ở metadata Kaggle gốc, TDC không nêu license; GT-09/17 ghi CC-BY-4.0; OSM cần ODbL/attribution. Các nguồn còn lại giữ trạng thái chưa xác minh quyền tái phân phối. Các snapshot chỉ lưu để kiểm toán cục bộ, không tự ý xuất bản lại dữ liệu.

[RECOMMENDATION] Xác minh định nghĩa velocity/LOS, ánh xạ track, kỳ lịch GTFS và tổng vùng trước dùng như nền mô hình. Xem `../registry/licenses_and_access.md`.
''')
    supported=matrix[matrix.evidence_strength!='E0']
    write('reports/04_top_10_problems_vi.md','''# Danh sách vấn đề có thể điều tra

Chỉ chọn **4** vấn đề có bằng chứng mô tả phù hợp ở mức E1/E2. Không đủ 10 vấn đề độc lập có căn cứ. Xếp hạng là quyết định nghiên cứu chủ quan, không phải xác suất tai nạn hay bằng chứng hiệu quả giải pháp.

Trọng số: bằng chứng 25%, ý nghĩa an toàn 15%, khả năng can thiệp/đo hiệu quả 20%, dữ liệu/khả thi trước hạn 15%, khoảng trống/tính mới 15%, phù hợp cuộc thi 10%. Mỗi thành phần 0–5. E1 được cho bằng chứng 1/5, E2 mô tả 2/5; tính mới 1/5 do NOT ESTABLISHED. Khoảng điểm là kịch bản mỗi thành phần ±1 có chặn 0–5, không phải CI.

'''+table(supported[['problem_id','problem_statement_vi','evidence_strength','weighted_score','score_low','score_high']])+'''

Tất cả có cổng kiểm chứng chưa đạt: quyền khảo sát/can thiệp, baseline mới, outcome hợp lệ tại địa bàn. **Không vấn đề nào được thông qua để triển khai công cộng chỉ nhờ điểm tổng.** P02 có bằng chứng lịch sử về học sinh hành khách, chưa chứng minh nhóm tự lái xe điện hiện tại; P03 chỉ số cấp thành phố; P01/P04 danh mục nguy cơ chưa có tai nạn/mẫu số. Độ tin cậy hiệu quả can thiệp: thấp.

P04 có dữ liệu kiểm kê rõ nhưng thiếu cơ chế đánh giá dự báo mưa và ít phù hợp chủ đề nút giao. H01 (hàng cồng kềnh) giữ E0, tách khỏi xếp hạng có bằng chứng: benchmark chỉ có nhãn abnormal tổng quát, không có denominator hành vi và outcome. Không dùng tỷ phần nhãn bất thường để suy tỷ lệ hàng cồng kềnh ngoài đường.

Phép thử bác bỏ: P01 nếu khảo sát cho thấy tầm nhìn/biển đã đáp ứng và không có hành vi nguy hiểm thì dừng giả thuyết bổ sung cảnh báo; P02 nếu kỹ năng/duy trì đã cao và không cải thiện so đối chứng thì bỏ can thiệp giáo dục thêm; P03 nếu không có hàng chờ kéo dài hoặc thiếu quyền thay đổi điều tiết thì không làm tối ưu tín hiệu; P04 nếu không ghép được ngày mưa–sự kiện độc lập thì không tuyên bố mô hình cảnh báo có ích.
''')
    write('reports/05_top_3_interventions_vi.md','''# Ba hướng đề xuất có điều kiện

[RECOMMENDATION] Đây là ba giả thuyết can thiệp để khảo sát và làm hồ sơ, không phải ba giải pháp đã chứng minh hiệu quả. Từ ngày 19/11/2026 tới mốc 15/12 là 26 ngày; thể lệ dùng cách diễn đạt “trước ngày 15/12”, nên dự kiến hoàn thiện hồ sơ trước 14/12. Chưa có báo giá hay cam kết của đối tác. Không thể chứng minh giảm tai nạn trong vài tuần.

## 1. P02 — Duy trì quyết định an toàn khi học sinh gặp tình huống trên đường

[VERIFIED SOURCE FACT] Nghiên cứu lịch sử cho thấy hành vi đội mũ thay đổi sau chiến dịch; không xác nhận hiện trạng học sinh tự lái xe điện. Chủ đề 3 của cuộc thi tập trung giáo dục nhóm này. Bước đầu phải xác nhận vấn đề với giáo viên/học sinh phù hợp, không dùng ảnh đường để suy học sinh kém kỹ năng.

[HYPOTHESIS] H0: bài tập tương tác có nhắc lại không thay đổi tỷ lệ chọn hành động an toàn so với bài học hiện hành ở lần đo sau 7–14 ngày. H1: tỷ lệ đó cao hơn. Outcome chính: chênh lệch điểm tỷ lệ lựa chọn đúng trên bộ tình huống tương đương có chấm độc lập. Outcome phụ: hành vi đội mũ quan sát tổng hợp nếu được phép. Không đánh đồng điểm bài học với giảm tai nạn.

[RECOMMENDATION] Baseline là bài học hiện hành và pretest, chưa đo. Bộ tối thiểu đề xuất: ít nhất 4 lớp tại 2 trường, mã lớp ẩn danh, thời điểm pre/post/follow-up, tình huống tương đương, exposure bài học, thiếu/thoát mẫu. Đây là mức tổ chức pilot dự kiến, không phải cỡ mẫu đủ power. Ngẫu nhiên theo lớp, delayed control, phân tích ITT theo cụm; quá ít cụm chỉ báo cáo mô tả/CI và hạn chế. Chi phí giả định 2–5 triệu VND cho nội dung/in ấn/đi lại, 10–18 ngày nếu có phép và không thu thông tin cá nhân. Không thực hiện tuyển học sinh trong phiên này. Kill: không có phép trước 24/11, baseline gần trần, chấm không tin cậy hoặc không giữ được nhóm so sánh thì chuyển sang demo nội dung có nhãn chưa đánh giá.

[NOT VERIFIED] Tính mới NOT ESTABLISHED: chương trình giáo dục mũ bảo hiểm và Safe School Zones đã có. Đóng góp khả dĩ là đánh giá duy trì kỹ năng đúng nhóm xe điện tại địa bàn cụ thể, chưa được xác lập là mới. Không lặp lại khẳng định giải pháp đầu tiên.

## 2. P03 — Hàng chờ tại nút giao cần được đo trước hỗ trợ điều tiết

[MEASURED RESULT] TomTom công bố Hà Nội 49,2% và TP.HCM 46,9% kỳ 2025; GT-07 không đủ bằng chứng xác nhận chênh lệch peak–midday trong mẫu cũ. Hai thông tin không xác định một nút cụ thể.

[HYPOTHESIS] H0: quy trình hỗ trợ điều tiết không làm thay đổi trễ mỗi xe so quy tắc hiện hành; H1: giảm trễ mà không tăng xung đột/giảm phục vụ người đi bộ. Outcome chính: trễ/xe theo phút quan sát có tổng xe mẫu số; phụ: P95 hàng chờ và thời gian chờ người đi bộ.

[RECOMMENDATION] Baseline: quy tắc hiện hành, chưa đo. Tối thiểu pilot dự kiến 2 nút tương đồng, 5 ngày baseline và 5 ngày follow-up, cùng 2 khung giờ, log pha đèn/lưu lượng rẽ/hàng chờ/mưa/công trình. Thiết kế trước–sau có đối chứng, không lấy từng frame làm mẫu độc lập. Chưa có power đủ cho tác động nhỏ; cần dữ liệu pilot để thiết kế chính thức. 3–8 triệu VND giả định quan sát thủ công 10–20 ngày. Prototype là bảng khuyến nghị cho người vận hành, không kết nối sửa đèn thật. Kill: không có quyền/log hoặc không có hàng chờ lặp lại, mất đối chứng, tăng chờ đi bộ thì dừng thử nghiệm hiện trường.

[NOT VERIFIED] ITS/VDS và điều khiển thích ứng đã có tại TP.HCM. Bài SURTRAC tìm được chỉ dự phóng, không chứng minh mức giảm tai nạn thực ở Việt Nam. Tính mới cần nằm ở ràng buộc vận hành/đánh giá tại nút, chưa xác lập.

## 3. P01 — Kiểm chứng đoạn cong có tầm nhìn bị mô tả hạn chế

[MEASURED RESULT] 48/107 bản ghi GT-10 nhắc tầm nhìn; nhiều đoạn đã có biển/gương. Không xác nhận 48 điểm thiếu biển hoặc 48 điểm đen tai nạn. Mức phù hợp chủ đề nút/điểm nóng phải giải trình, không mặc nhiên đạt.

[HYPOTHESIS] H0: bổ sung cảnh báo được kỹ sư lựa chọn không thay đổi tỷ lệ xe tiếp cận vượt tốc độ tư vấn được phê duyệt; H1: giảm tỷ lệ đó. Outcome chính có mẫu số số xe quan sát; phụ là khả năng đọc biển/tầm nhìn, không phải tai nạn dự đoán.

[RECOMMENDATION] Baseline: kiểm tra lý trình và hạ tầng hiện hữu, đo tốc độ bằng thiết bị được phép/hiệu chuẩn; chưa đo. Tối thiểu pilot dự kiến 2 đoạn can thiệp và 2 đối chứng, đo ngày/đêm cùng lịch; xác định độc lập ngưỡng kỹ thuật. So sánh trước–sau có đối chứng, báo phụ thuộc theo đoạn/ngày. 5–15 triệu VND giả định khảo sát/thuê thiết bị, chưa gồm xây dựng, 2–3 tuần chỉ nếu cơ quan hỗ trợ. Trước hạn ưu tiên bản thiết kế và bằng chứng khảo sát, không tự lắp thiết bị đường công cộng. Kill: không geocode chắc, hạ tầng đã đạt, không phép hoặc không đo được outcome thì dừng đề xuất lắp đặt.

[NOT VERIFIED] Cảnh báo đường cong/chevron đã có trong hướng dẫn FHWA và trong GT-10; ý tưởng cảnh báo tự thân không mới. Chưa có bằng chứng hiệu quả nhân quả địa phương.

## Nhánh dự phòng chủ đề 2

[HYPOTHESIS] H01: hỗ trợ chọn phương tiện phù hợp có thể giảm chuyến chở hàng không an toàn. Chưa có bằng chứng cargo-specific trong bản tải, nên không thay một hướng có bằng chứng bằng nhánh này. Cần đếm thực địa có định nghĩa độc lập, tổng chuyến, loại hàng, điều kiện đường và cơ chế tác hại, cùng phỏng vấn tự nguyện trước đề xuất AI hay nền tảng vận tải.
''')
    write('reports/07_blockers_next_actions_vi.md','# Trở ngại và việc tiếp theo\n\n[NOT VERIFIED] Mỗi mã đều có bước theo dõi, dù đã có dữ liệu để phân tích. Không coi trạng thái FOLLOWUP_REQUIRED là chưa làm audit.\n\n'+'\n\n'.join(f'## {sid}\n\n{NOTES[int(sid[-2:])][1]}\n\n[RECOMMENDATION] {NOTES[int(sid[-2:])][2]}' for sid in inv)+'''\n\n## Công việc chưa thực hiện\n\nChưa có khảo sát hiện trường, quyền tiếp cận dữ liệu hệ thống nội bộ, thử can thiệp hoặc xác lập novelty. Chưa phân tích PDF GT-03, chưa lấy raster mưa GT-18, chưa lấy ảnh Mapillary, chưa lấy bảng vận tải GT-21 riêng hay API lịch sử GT-22. Không có sai số nhân quả/near-miss vật lý từ GT-08/09. Có backlog máy đọc được ở `../registry/acquisition_backlog.csv`. Các phần chưa làm có blocker cụ thể, không được trình bày như kết quả.\n''')
    write('reports/00_executive_summary_vi.md',f'''# Tóm tắt nghiên cứu giao thông Việt Nam

Ngày 19/11/2026. Kết quả của lần chạy có dữ liệu thật, nhưng chưa hoàn tất thực nghiệm hiện trường hoặc chứng minh hiệu quả giải pháp.

## Đã xác minh

Danh mục hợp lệ: 22 ID duy nhất, giữ nguyên 13 cột, workbook gốc không sửa. Audit 22/22 nguồn; A=7, B=5, C=4, D=5, E=1, F=0, G=0. Phân lớp nguồn và URL/checksum: `../registry/source_audit.csv`, `raw_manifest.json` và 22 dossier. Geofabrik timeout nhưng mẫu OSM chính thức tải được; OpenAQ trả 401. Không gọi HTTP 200 của portal là raw data.

## Kết quả thực

- GT-01: toàn quốc 2024 ghi 23.667 vụ, 11.101 chết; phát hiện tổng vùng không khớp thành phần, chưa suy biến động nguy cơ.
- GT-07: 90.938 trạng thái của 10.027 segment; 39,69% dòng thuộc một ngày. Kiểm định thăm dò 26 ngày: chênh lệch −3,46 đơn vị gốc, CI bootstrap [−10,07;1,79], p=0,275. Chưa có bằng chứng khác biệt theo khung giờ với thiết kế này.
- GT-08: 50 mảng nhãn / 144.847 frame, 62.130 frame abnormal; 42,89% chỉ là tỷ phần benchmark tuyển chọn, không là prevalence vi phạm.
- GT-09: 16.036 hộp VNTraffic, 501 frame; TXT có 85 ID và JSON 205 ID, cần giải thích trước đo quỹ đạo.
- GT-10/11: đủ 107/58 bản ghi nguy cơ; 48/107 mô tả GT-10 nhắc tầm nhìn. Không phải số tai nạn.
- GTFS: calendar thực là 2018, không phải lịch hiện tại. GT-20 có 82 lớp thống kê và cờ bản dịch trái/phải.

Chi tiết 12 nguồn đã phân tích, mẫu số và giới hạn: `02_data_findings_vi.md`; 12 trang theo nguồn. Kết quả rate theo dân số là gánh nặng trên dân số, không thay exposure giao thông. Chưa có E3/E4 từ các nguồn ghép.

## Vấn đề và lựa chọn

Chỉ có 4 ứng viên có bằng chứng mô tả E1/E2, không đủ 10. Điểm chủ quan có trọng số: P02 duy trì hành vi an toàn học sinh 2,65/5; P03 định vị hàng chờ 2,55; P01 đoạn cong/tầm nhìn 2,45; P04 danh mục sạt lở 2,00. Các điểm không vượt cổng thiếu baseline/quyền/outcome. Hàng cồng kềnh giữ E0 do chưa có nhãn riêng và mẫu số tác hại.

[RECOMMENDATION] Ba hướng điều tra: học tương tác có đo duy trì; hỗ trợ điều tiết dựa trên đo hàng chờ; xác minh cảnh báo đoạn cong. H0/H1, baseline, minimum pilot, ngân sách giả định và kill criterion trong `05_top_3_interventions_vi.md`. Chưa có giải pháp sẵn sàng triển khai. Novelty tất cả NOT ESTABLISHED.

## Cuộc thi và tái lập

[VERIFIED SOURCE FACT] [Thể lệ 2026](https://sangkienatgt.dantri.com.vn/the-le) xác nhận ba chủ đề và yêu cầu hồ sơ trước 15/12/2026. Trang nêu tính độc đáo, khả thi và phù hợp; chưa thấy rubric trọng số định lượng của ban giám khảo. Trọng số xếp hạng nghiên cứu là do master prompt quy định, không gán cho cuộc thi.

Lệnh offline từ thư mục này: `python src/run_all.py`. Raw giữ nguyên, mọi kết quả sinh từ snapshot trong manifest. Dữ liệu web tương lai có thể đổi, không bảo đảm tải lại giống snapshot. Kiểm thử: `python -m unittest discover -s tests -v`; log thực nằm ở `../run_log.md` và `../tests/test_results.txt`.
''')
    write('reports/08_methods_and_reproducibility.md','''# Phương pháp và khả năng tái lập

Phạm vi: audit đầy đủ danh mục và phân tích phần dữ liệu công khai khả thi trong phiên; không là nghiên cứu hiện trường hoàn chỉnh. Giao thức đầu vào được lưu nguyên bản. Seed 42; ngày tham chiếu 19/11/2026 Asia/Bangkok (UTC+7). Timestamp HTTP ghi UTC thực; dòng trạng thái GT-07 chuyển sang Asia/Ho_Chi_Minh để phân nhóm giờ.

## Chạy lại

Từ `traffic-data-research`: `python src/run_all.py`. Offline, không cần token. Môi trường phân tích thực Python 3.10.11, phiên bản gói ở `environment.json`/`requirements.txt`. Bundled EDA CLI thực thi riêng bằng runtime Python 3.12.14 do skill yêu cầu 3.11+. Không khẳng định toàn bộ stack mẫu của skill đã được cài. XLSX tùy chọn tạo bằng Node artifact-tool, xem `src/export_matrix.mjs` và `environment.json`; CSV là bản đối chiếu chuẩn.

Các bước: ingest → quality → eda → extended_analysis → supplemental_analysis → triangulation → registry → evidence matrix → reports → tests. `src/parse_inventory.py` đọc OOXML theo tọa độ ô, shared strings, inline strings, relationships/hyperlinks và assert đủ ID/13 cột; không thực thi macro/formula. Workbook 17 dùng cached values, giữ riêng lịch sử/dự báo. Zip kiểm tra đường dẫn và kích thước mở rộng, chỉ parse tài liệu/bảng, không thực thi nội dung tải.

## Thu thập

`acquire.py` audit URL danh mục. `deep_fetch.py`, `followup_fetch.py`, `final_fetch.py`, `uit_fetch.py`, `aggregate_fetch.py` ghi rõ request bổ sung. Phiên này cần chạy shell có mạng được cấp quyền vì sandbox mặc định WinError 10013. GET công khai, một POST biểu mẫu PX-Web, không bypass auth. Retry hữu hạn cho lỗi tạm thời, timeout kết nối/đọc, cap 500 MB/nguồn và 2 GB cộng dồn. Các lần tải trước khi thêm retry/cap cộng dồn vẫn dưới trần; không giả nhận có retry ở từng lần cũ. HTTP events là bằng chứng thực thi, lỗi/404/401/timeout được giữ.

Raw gồm cả trang lỗi: phân loại dựa nội dung đọc được. Mỗi entry có source_id, URL gốc/cuối, UTC, content type, byte, SHA256, period/region/version/terms đã biết hoặc NOT_VERIFIED, script biến đổi. Region ban đầu từ Excel được coi là mô tả inventory, không xác nhận phủ quan sát; dossier/analysis ghi phạm vi thực. Tái tải có tên timestamp mới, không sửa bytes cũ. Không đăng dữ liệu license chưa rõ lên Git; `.gitignore` loại raw/video và credentials.

## Suy luận

Thống kê mô tả theo mẫu số thực. Profile toàn file CSV có số dòng/thiếu/trùng; bản EDA skill CLI quét 90.938 dòng GT-07 trong giới hạn 100.000. Không impute, không bỏ ngoại lệ khỏi bản chính. GT-07 sensitivity 0–120 là thay ngưỡng thử trên thang chưa xác minh, không xác định speed violation. Không có mô hình AI được huấn luyện, không validation intervention.

Một kiểm định thăm dò trước khi tính tương phản peak–midday; bảng lưu 26 đơn vị ngày sau ghép segment-day. t-test một mẫu và bootstrap ngày 5.000 lần cho CI percentile. Giả định trao đổi/độc lập giữa ngày chưa xác nhận, nên p không được dùng kết luận nhân quả hoặc chọn ý tưởng. Không quét đa giả thuyết nên không cần hiệu chỉnh một family mới; nếu mở rộng phải định nghĩa family/FDR trước. Không kiểm định trên frame độc lập. Quốc gia có ba năm không đủ seasonality/breakpoint đáng tin.

OSM lưu WGS84; không thực hiện buffer/khoảng cách trên độ. `spatial.py` kiểm tra metric CRS cho công việc sau, không tuyên bố đã chạy spatial join trường–đường. GT-10/11 chỉ so nhãn tuyến, không geocode tự động lý trình rút gọn. GT-09 không quy pixel ra mét hoặc giây, không TTC/PET; JSON/TXT khác ID được giữ như cờ biểu diễn, chưa quy lỗi nhãn.

## Trạng thái bằng chứng

VERIFIED SOURCE FACT = nội dung nguồn đã xem. MEASURED RESULT = tính từ file tải có provenance. INTERPRETATION = diễn giải có giới hạn. HYPOTHESIS = giả thuyết chưa xác nhận. NOT VERIFIED = chưa biết. RECOMMENDATION = lựa chọn/đề xuất. E2 chỉ cấp cho mô tả tái lập có mẫu số, không bao hàm tính đại diện. E3 cần xác nhận độc lập đúng cơ chế/địa bàn; E4 cần thử can thiệp hợp lệ. Không nguồn ghép nào trong lần chạy đủ điều kiện nâng E3.

Danh sách 4 vấn đề và H01 được chấm theo trọng số master prompt, kèm component/uncertainty/fatal gates. Đây là phán đoán của người phân tích, không phép đo thực nghiệm. Literature là rà soát tường thuật có giới hạn; không tuyên bố PRISMA/systematic review, không có reviewer thứ hai. Chưa kiểm tra đầy đủ sản phẩm startup, prior contest entries hoặc bằng sáng chế nên novelty chưa xác lập.

## Skill thực sự áp dụng

Xem `../skills_used.md`: Spreadsheets (OOXML và xuất ma trận), Exploratory Data Analysis (nguyên tắc và CLI profile thực chạy), Statistical Analysis (thiết kế tương phản, đơn vị cụm, báo cáo effect/CI/p; không chạy stack Pingouin mẫu), Paper Lookup (API Crossref/Europe PMC, metadata/provenance; không dùng metadata như full text), Literature Review (scope, truy vấn, giới hạn và synthesis). Không sử dụng skill GIS hay mô hình AI khi chưa có tác vụ phù hợp.
''')
    env={'python':sys.version,'platform':platform.platform(),'seed':42,'dependencies':{name:meta.version(name) for name in ['pandas','numpy','scipy','matplotlib','requests','beautifulsoup4','PyYAML']},'bundled_eda_python':'3.12.14','artifact_tool':'2.8.148','run_date_local':'2026-11-19'}
    write('environment.json',json.dumps(env,indent=2)); write('requirements.txt','\n'.join(k+'=='+v for k,v in env['dependencies'].items()))
    write('config.yaml','''seed: 42
research_date_local: '2026-11-19'
timezone: Asia/Ho_Chi_Minh
max_source_bytes: 500000000
max_total_bytes: 2000000000
priority_sources: [GT-01, GT-04, GT-07, GT-08, GT-09, GT-10]
bootstrap_replicates: 5000
osm_bbox: [106.797, 10.868, 106.801, 10.872]
evidence_weights: [0.25, 0.15, 0.20, 0.15, 0.15, 0.10]
''')
    write('skills_used.md','''# Skill đã áp dụng

| Skill | Thao tác thực tế | Giới hạn |
|---|---|---|
| Spreadsheets | Đọc OOXML 13 cột, kiểm sheet/hyperlink, bảo toàn input, tạo ma trận CSV/XLSX | Không tái tính formula input/Solver |
| exploratory-data-analysis | Quy tắc missing/outlier/sampling, profile CSV, chạy `tabular_profile.py` trên GT-07 bằng Python 3.12.14, exit 0 | Không dùng phiên bản package gợi ý như bằng chứng môi trường |
| statistical-analysis | Thiết kế tương phản theo ngày sau ghép segment, effect + bootstrap CI + t-test thăm dò, giới hạn độc lập | Không chạy Pingouin/PyMC và không chứng nhận giả định |
| paper-lookup | Thực gọi Crossref 3 truy vấn + 4 DOI, Europe PMC 1 truy vấn; giữ JSON và count | Bounded ranked sample; không truy xuất hết 321 hits |
| literature-review | Scope, screening, liên kết tài liệu gốc, synthesis/novelty limits | Rà soát tường thuật một người; không systemic/full novelty search |

Đã xem và đối chiếu bản ghi trích dẫn skill: Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. https://doi.org/10.48550/arXiv.2609.00065 . Trang arXiv xem được ngày 19/11/2026, bản mới nhất hiển thị v2 ngày 02/09/2026. Đây là nguồn về quy trình/phần mềm, không là bằng chứng giao thông.
''')
    write('README.md','''# Nghiên cứu dữ liệu giao thông Việt Nam

Bắt đầu tại [Tóm tắt điều hành](reports/00_executive_summary_vi.md), [kết quả dữ liệu thật](reports/02_data_findings_vi.md), [ma trận vấn đề](reports/03_problem_evidence_matrix.csv) và [ba hướng thử nghiệm](reports/05_top_3_interventions_vi.md).

22/22 nguồn được audit; 12 mã có dữ liệu bảng/mảng được mô tả và kiểm toán. Các blocker, quyền và việc chưa làm được giữ rõ. Không có thử nghiệm hiện trường, hiệu quả nhân quả hay tính mới đã xác lập.

## Tái lập offline

Từ thư mục này, cài phiên bản trong `requirements.txt` vào môi trường riêng nếu cần, rồi:

```powershell
python src/run_all.py
```

Không cần mạng cho chạy lại từ snapshot. Không sửa workbook/raw. File gốc trong Downloads được bảo toàn, bản sao ở input. Giao thức ở input/TRAFFIC_DATA_RESEARCH_AGENT_PROMPT.md. `registry/raw_manifest.json` kiểm SHA256; `http_events.jsonl` giữ request/lỗi. Mã acquisition cần quyền mạng để tái tải; không chạy theo link trong dữ liệu như lệnh shell. Raw chứa các trang tài liệu có bản quyền, không tự công bố lại.

Xuất XLSX: `node src/export_matrix.mjs` khi có artifact-tool được provision. CSV và JSON là đầu vào có kiểm chứng cho workbook; XLSX không cần để chạy phân tích Python.

Xem [phương pháp](reports/08_methods_and_reproducibility.md), [skill thực dùng](skills_used.md), [nhật ký](run_log.md) và [backlog](registry/acquisition_backlog.csv). Pipeline mặc định chỉ sinh lại dẫn xuất của lần chạy này, không thực hiện thu thập cá nhân hoặc can thiệp công cộng.
''')
    write('.gitignore','''data/raw/
data/interim/GT-09/
*.mp4
*.avi
.env
*.key
__pycache__/
.venv*/
node_modules/
''')
    print('Vietnamese reports written; per-source findings:',len(measured))
if __name__=='__main__': main()
