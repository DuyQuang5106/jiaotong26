# Kết quả từ dữ liệu thực

Ngày nghiên cứu: 19/11/2026. Phân tích mô tả/kiểm toán 12 mã nguồn: GT-01, GT-02, GT-04, GT-06, GT-07, GT-08, GT-09, GT-10, GT-11, GT-12, GT-17, GT-20. Chỉ GT-07 có một kiểm định thăm dò định lượng mới; các nguồn khác có kiểm tra tính nhất quán/độ nhạy, không ép tạo p-value từ metadata hoặc tổng hợp không độc lập.

## GT-01

[MEASURED RESULT] 639 ô thống kê (71 nhãn địa lý × 3 năm × 3 chỉ tiêu), hai giá trị thiếu. Toàn quốc 2024: 23.667 vụ, 11.101 người chết, 17.424 người bị thương. So 2023, số vụ +7,25%, số chết −4,53%. Ba ô tổng vùng miền Trung 2024 lệch tổng tỉnh thành phần: +2.914 vụ, +1.718 chết, +2.104 bị thương. Không sửa số gốc.

[NOT VERIFIED] Tổng vùng miền Trung 2024 không khớp tỉnh thành phần; phạm vi/định nghĩa 2022–2023 chưa thống nhất.

Chi tiết: [GT-01_findings_vi.md](GT-01_findings_vi.md).

## GT-02

[MEASURED RESULT] Ba báo cáo sơ bộ tháng 8–10/2026. Tháng 10: 1.266 vụ, 720 chết, 765 bị thương. Tháng 9 riêng: 1.327/782/793; tháng 10 cộng mức giảm đã công bố suy ra tháng 9 là 1.330/787/791. Sai lệch lần lượt +3/+5/−2, có thể do cập nhật hoặc lỗi báo cáo; chưa có giải thích từ cơ quan.

[NOT VERIFIED] Chênh lệch tháng 9 suy ngược từ báo cáo tháng 10 so với báo cáo tháng 9 riêng; không có mẫu số lưu lượng.

Chi tiết: [GT-02_findings_vi.md](GT-02_findings_vi.md).

## GT-04

[MEASURED RESULT] Mẫu bbox 106.797–106.801E, 10.868–10.872N: 1.125 đối tượng (1.026 node, 88 way, 11 relation), 53 đối tượng có highway, 5 có crossing và 1 có amenity=school. Đối tượng trả về có thể mở rộng ra ngoài bbox. Đây là mức ghi tag trong mẫu thuận tiện, không chứng minh thiếu công trình.

[NOT VERIFIED] Mẫu thuận tiện nhỏ, không đại diện Việt Nam; không có kiểm tra thực địa; Geofabrik chưa xác minh được.

Chi tiết: [GT-04_findings_vi.md](GT-04_findings_vi.md).

## GT-06

[MEASURED RESULT] Hai hàng công bố kỳ 2025: Hà Nội congestion 49,2%, TP.HCM 46,9%; không tải probe hoặc mẫu số chuyến. Dùng mô tả cấp thành phố, không xác định điểm đen hay đánh giá tai nạn.

[NOT VERIFIED] Không có probe thô hoặc mẫu số chuyến; hai thành phố không xác định nút giao cụ thể.

Chi tiết: [GT-06_findings_vi.md](GT-06_findings_vi.md).

## GT-07

[MEASURED RESULT] 5 bảng: nodes 577.967; segments 84.633; streets 5.553; segment_status 90.938; train 33.441 dòng. Trạng thái trải 03/07/2020–22/04/2021 UTC, 10.027 segment, 120 ngày địa phương có quan sát. Một ngày chiếm 39,69% dòng. 107 giá trị velocity >120 trên thang gốc, 448 bằng 0; đơn vị chưa xác minh. 154 đoạn có length=0; train thiếu max_velocity ở 28.495/33.441 dòng. Không coi velocity cao là vi phạm khi thiếu định nghĩa.

[NOT VERIFIED] Đơn vị velocity và cách thu mẫu chưa xác minh; lịch lấy mẫu lệch; metadata 2026 không phải kỳ quan sát.

Chi tiết: [GT-07_findings_vi.md](GT-07_findings_vi.md).

## GT-08

[MEASURED RESULT] 50 mảng NPY nhị phân, 144,847 frame nhãn, 62,130 frame abnormal, tỷ phần 42.89% trong các file nhãn tải được. Đếm 606 chuỗi liên tiếp giá trị 1, không gọi là số xe/số vi phạm độc lập. Chỉ có nhãn 0/1; không xác định riêng hàng cồng kềnh. Không phải tỷ lệ ngoài thực địa.

[NOT VERIFIED] Nhãn chỉ normal/abnormal, không phân biệt hàng cồng kềnh; video, COCO 379 MB/177,8 MB chưa tải; chưa thấy license rõ.

Chi tiết: [GT-08_findings_vi.md](GT-08_findings_vi.md).

## GT-09

[MEASURED RESULT] VNTraffic TXT: 16.036 hộp, 501 chỉ số frame (0–500), 85 track_id duy nhất, 2 khóa frame-track trùng. JSON: 205 track, cũng 16.036 hộp; ghép theo frame và ID nguyên bản không khớp 8.771 hộp. Đây là khác biệt biểu diễn/định danh chưa được giải thích, không tự quy thành lỗi toàn bộ ground truth. AICC22-Custom TXT 1.185 hộp/21 ID, JSON 2.439 hộp/25 ID; không dùng tập này suy luận Việt Nam. Chưa tính tốc độ thực, TTC hay PET.

[NOT VERIFIED] TXT/JSON khác định danh track; có khóa frame-track trùng. Không có homography hoặc ngày quay xác minh.

Chi tiết: [GT-09_findings_vi.md](GT-09_findings_vi.md).

## GT-10

[MEASURED RESULT] 107 bản ghi trên 19 nhãn tuyến, đầy đủ theo tổng web. 48/107 mô tả có cụm “tầm nhìn”, 105/107 có “cong” hoặc “cua”; 19 ô đã xử lý không rỗng và 89 ô chưa xử lý không rỗng. Hai trường không được giả định loại trừ nhau hoặc nhị phân hoàn tất. Quy tắc chặt “hạn chế tầm nhìn” chỉ cho 16/107, cho thấy độ nhạy của mã hóa văn bản.

[NOT VERIFIED] Không phải tai nạn thực tế; lý trình có dạng rút gọn; chưa geocode/đo hiện trường; không có giấy phép tái phân phối rõ.

Chi tiết: [GT-10_findings_vi.md](GT-10_findings_vi.md).

## GT-11

[MEASURED RESULT] 58 bản ghi trên 17 nhãn tuyến, đủ theo tổng web. QL.4G có 15/58 bản ghi. Đây là danh mục nguy cơ, không phải 58 lần sạt lở hoặc 58 tai nạn. Trùng nhãn tuyến giữa GT-10/11 chỉ là khả năng ghép thô.

[NOT VERIFIED] Không có ngày xảy ra sạt lở, GPS hay outcome; cùng cơ quan GT-10, không độc lập.

Chi tiết: [GT-11_findings_vi.md](GT-11_findings_vi.md).

## GT-12

[MEASURED RESULT] Mỗi feed: 224 route_id, 7.670 stop_id nhưng chỉ 3.146 cặp tọa độ duy nhất. Chuyến AM/MD/PM lần lượt 3.024/6.713/3.301; stop_times 100.117/224.166/110.323. Cả ba calendar là 01/01–31/12/2018; headway lịch trình trung vị theo route trong từng khung là 12 phút. Không có trip/stop mồ côi hoặc khóa trip-sequence trùng. Không cộng ba khung thành lượt vận chuyển thực, không suy độ đúng giờ.

[NOT VERIFIED] 7.670 stop_id tương ứng 3.146 cặp tọa độ; không gọi stop_id là số trạm vật lý; không có GPS thực.

Chi tiết: [GT-12_findings_vi.md](GT-12_findings_vi.md).

## GT-17

[MEASURED RESULT] XLSX v1.1 có 18 sheet. Trích 10 giá trị dân số lịch sử 2015–2024 từ sheet Population, dòng Medium (cached values), giữ tách khỏi dự báo. Ghép năm cấp quốc gia với GT-01 cho số chết/100.000 dân: 2022=6,43; 2023=11,59; 2024=10,95. Dân số là mẫu số gánh nặng dân số, không là lưu lượng xe. GT-17 dùng lại NSO, không phải xác nhận độc lập; cached formula không chứng minh đã tái tính mô hình.

[NOT VERIFIED] Có historical, projection và tham số mô hình; công thức chỉ đọc cached value, không tái tính Excel/Solver; không độc lập NSO.

Chi tiết: [GT-17_findings_vi.md](GT-17_findings_vi.md).

## GT-20

[MEASURED RESULT] classid.csv 82 lớp, tổng Count công bố 19.748; min 32, max 1.446, tỷ số max/min 45,19. ID31: tên Anh là No Moto Turn Left còn tiếng Việt ghi “Cấm xe máy rẻ phải”. Đây là cờ cần rà soát nhãn, chưa chứng minh mô hình kém hoặc học sinh thiếu kiến thức. ZIP ảnh 904,8 MB vượt trần nên không tải.

[NOT VERIFIED] ZIP vượt 500 MB/nguồn nên không tải. License chưa rõ; ID31 Anh/Viet trái/phải mâu thuẫn; Count là số công bố.

Chi tiết: [GT-20_findings_vi.md](GT-20_findings_vi.md).

## Kiểm định thăm dò GT-07

[MEASURED RESULT] Sau đổi timestamp Z sang UTC+7, so sánh khung 07:00–08:59 và 16:00–17:59 với 10:00–14:59. Lấy trung vị trong segment × ngày × khung, giữ cặp có cả hai khung, rồi trung bình chênh lệch theo ngày: 404 segment-ngày, 26 ngày. H0: trung bình chênh lệch ngày bằng 0, H1 hai phía. Ước lượng −3,46 đơn vị velocity gốc; bootstrap 5.000 mẫu theo ngày, seed 42, khoảng percentile 95% [−10,07; 1,79]. t(25)=−1,117, p=0,2748. Một tương phản thăm dò, không quét nhiều giả thuyết để chọn p nhỏ.

[INTERPRETATION] Chưa đủ bằng chứng bác bỏ H0 dưới giả định kiểm định; đây là **NO EVIDENCE**, không phải **EVIDENCE OF NO EFFECT**. Phụ thuộc giữa ngày, phủ quan sát chọn lọc và đơn vị chưa xác minh hạn chế suy luận. Không gọi các số này là km/h. Sau sàng lọc độ nhạy 0–120 trên thang gốc, ước lượng −3,43; bỏ lần lượt một ngày cho ước lượng khoảng −4,11 tới −1,20. Không coi 90.938 dòng là các mẫu độc lập.

Bảng: `../data/processed/GT-07_paired_segment_day.csv`, `GT-07_paired_day_effects.csv`, `GT-07_daily_coverage.csv`. Biểu đồ quan sát: `../figures/GT-07_hourly_coverage.png`. Mã: `src/eda.py`.

## Tỷ lệ theo dân số và kiểm tra đối chiếu

[MEASURED RESULT] Công thức = số ghi nhận / (dân số triệu × 10), đơn vị /100.000 dân. Bảng tái lập: `../data/processed/GT-01_GT-17_population_rates.csv`. Dân số lịch sử, không dùng dự báo. Chưa có khoảng tin cậy cho các tổng hành chính do chưa mô hình hóa sai số thu thập; khoảng Poisson không xử lý sai lệch ghi nhận nên không thêm cho có.

[NOT VERIFIED] Sai lệch tổng vùng NSO và revision báo cáo BCA còn nguyên. Không kết luận tăng vụ năm 2023 là tăng nguy cơ thực do chưa xác minh định nghĩa, cách ghi nhận và độ phủ. Không hài hòa tỉnh 2025–2026 vì chưa có crosswalk; giữ địa giới gắn với thời kỳ 2022–2024.

## Triangulation

Tương thích khóa và kết quả ghép thô: `cross_source_compatibility.csv`. GT-01/17 ghép được năm cấp quốc gia nhưng cùng gốc NSO; GT-10/11 cùng cơ quan, chỉ đối chiếu nhãn tuyến, không xác nhận độc lập tai nạn. GT-06/07 khác thời kỳ; GT-08/09 khác camera/đơn vị. Không tạo điểm rủi ro bằng cách ghép giả những nguồn này. Chưa có vấn đề đạt E3/E4.
