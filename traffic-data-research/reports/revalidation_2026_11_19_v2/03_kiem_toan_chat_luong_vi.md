# Kiểm toán dữ liệu bổ sung

Phạm vi: snapshot cục bộ của các nguồn trọng tâm, ba file người dùng, danh mục 22 nguồn và kết quả đã có. Không tải lại nguồn. `all_22_source_review_coverage.csv` phân biệt kiểm lại cục bộ và giữ nguyên audit trước. 22 mã được kiểm đủ/duy nhất; không gọi lượt này là 22 lần kiểm tra trực tuyến mới.

GT-01 lấy từ trang NSO/PXWeb, nhưng metadata của bảng ghi **“Thống kê chính thức: Không”** theo [dossier đã kiểm](../../sources/GT-01.md). Tính xác thực trang không thay xác nhận định nghĩa/so sánh hoặc độ đúng của số đo.

| Dữ liệu | Số dòng | Grain / khóa | Ô khóa thiếu |
| --- | --- | --- | --- |
| GT01 | 639 | region, year, metric | 0 |
| GT07 | 90938 | segment_id, updated_at | 0 |
| GT10 | 107 | record_id | 0 |
| GT11 | 58 | record_id | 0 |
| ideas | 73 | idea_id | 0 |

Khóa ngoại GT-07 status→segments: 0 orphan; IDEA→NGUON: 0; GT-ID đề xuất→inventory: 0. Khớp mã GT chỉ xác minh mã tồn tại, không chứng minh dự án từng sử dụng dữ liệu đó. Khóa được kiểm thêm bằng biểu thức exact null/duplicate; mã định danh không đưa vào outlier/correlation như đại lượng khoa học.

Các bảng `*_eda_nulls`, `*_audit_nulls`, `*_outlier_screen`, `*_ranges` giữ toàn bộ cờ. Ngưỡng mặc định chỉ sàng lọc; thiếu award rank/treated/note có thể có ý nghĩa cấu trúc. Không tự bù, xóa ngoại lệ hay sửa raw. Pooled GT-01 trộn loại chỉ số/tỉnh/vùng nên outlier chỉ là cờ kỹ thuật, không đánh giá tỉnh bất thường. Ma trận tương quan của paired_numeric chứa difference=peak−midday, do đó quan hệ một phần do định nghĩa; không dùng làm phát hiện nhân quả. Các tuple số giống nhau ở bảng này là kết quả có thể lặp, không là khóa bản ghi gốc.

GT-08 đã đọc lại 50 NPY, kiểm hash/miền 0–1/tổng frame. GT-04 kiểm 1.125 đối tượng, khóa loại–ID và tọa độ node; không thực hiện GIS, đo khoảng cách hoặc suy thiếu hạ tầng từ thiếu tag. GT-20 giữ cờ nhãn và số do publisher công bố, chưa xác minh ảnh. GT-12 giữ riêng ba feed, không cộng chuyến có thể chồng lặp qua feed.

## Vấn đề và mức độ theo mục đích sử dụng

| Mức | Chiều chất lượng | Kết quả/cờ | Xử lý |
| --- | --- | --- | --- |
| HIGH | Accuracy / inference | GT-07: tương phản không ổn định theo cân; đơn vị, đại diện và độc lập chưa xác minh. | Giữ mô tả; thu baseline theo thiết kế nếu cần suy luận. |
| HIGH | Consistency | GT-01: tổng vùng có sai khác; hai ô Khác về thương tích bị thiếu. | Không dùng tổng vùng xếp hạng; không điền 0; đối chiếu nguồn địa phương. |
| MEDIUM | Consistency | GT-09: ID namespace khác; VNTraffic có 120 mục track rỗng và 2 khóa frame–track trùng. | Dùng phép đối chiếu hình học và ánh xạ ID; chưa tự xóa nhãn. |
| HIGH | Timeliness | GT-07/12 lịch sử và GT-10/11 snapshot không xác minh hiện trạng. | Không thay baseline triển khai 2026; chưa có SLA cập nhật của nhà cung cấp. |
| HIGH | Completeness / measurement | 70/73 cơ chế cuộc thi từ tên; không có toàn bộ bài/điểm giám khảo. | Dùng tìm prior art; không dự đoán giải; đọc hồ sơ kỹ thuật gần nhất. |
| MEDIUM | Validity | GT-10: treated và untreated cùng xuất hiện ở bản ghi 79. | Giữ văn bản, xác minh tiến độ theo hạng mục; không mã hóa nhị phân. |
| HIGH | Validity | GT-20 ID31 có hai nhãn ngôn ngữ khác hướng; chưa tải ảnh/annotation. | Không làm nội dung chỉ dẫn/huấn luyện trước đối chiếu nhãn và hình gốc. |
| MEDIUM | Lineage | GT-02: slug URL và kỳ trong nội dung có thể khác; số suy ngược tháng 9 không khớp bản tin tháng 9. | Dùng h1/nội dung, giữ từng phiên bản, chưa ghép chuỗi phân tích nguyên nhân. |

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
