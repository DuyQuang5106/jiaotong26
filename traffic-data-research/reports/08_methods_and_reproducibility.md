# Phương pháp và khả năng tái lập

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
