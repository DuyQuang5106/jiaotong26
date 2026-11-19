# Nhật ký thực thi và quyết định

Ngày nghiên cứu 19/11/2026 UTC+7. HTTP đầu: 2026-11-19T03:59:18.787231+00:00; HTTP cuối: 2026-11-19T04:10:53.415122+00:00. Mốc từng request trong `registry/http_events.jsonl`, không tái dựng timestamp không có bằng chứng.

1. Đọc master prompt và workbook; xác nhận 22 ID duy nhất, đủ 13 cột. Lưu bản sao byte-identical, cấu trúc sheet/hyperlink và SHA256 input. Không sửa input trong Downloads hoặc thư mục có trước.
2. Kết nối requests ban đầu thất bại WinError 10013 trong sandbox. Chạy HTTPS công khai với quyền mạng được auto-review cho phép, không có auto-review rejection. Kiểm tra đầy đủ 22 nguồn trước bắt đầu phân tích quan sát.
3. Geofabrik timeout hai lần; giữ lỗi, lấy mẫu API OSM chính thức bbox nhỏ thay vì giả định đã tải Vietnam PBF. OpenAQ GET /v3/countries trả 401, không chèn key. API NSO thử ban đầu 404, sau đó POST biểu mẫu công khai trả bảng dùng được. Các khác biệt được ghi ở dossier, không ghi đè thất bại.
4. Tải GT-07 ZIP và metadata gốc Kaggle, phân biệt năm dữ liệu 2020–2021 với metadata 2026. GT-09 ZIP và GT-17 XLSX tải hoàn chỉnh, checksum MD5 khớp metadata Zenodo; SHA256 cục bộ kiểm độc lập. Giữ tách VNTraffic/AICC22, không suy calibration.
5. Phân trang Sơn La công khai đủ 107/58 bản ghi; không gọi API Basic auth nội bộ. GTFS tải ba feed và phát hiện calendar 2018. GT-20 chỉ lấy classid.csv, dừng ZIP 904,8 MB vượt giới hạn 500 MB. UIT chỉ tải 50 mask nhỏ và README, không tải video/COCO lớn.
6. Chạy code profile/EDA/extended analysis/triangulation trên dữ liệu thật. Phát hiện sai tổng vùng NSO, revision không nhất quán BCA, track-ID TXT/JSON không tương thích, nhãn trái/phải GT-20 và lấy mẫu GT-07 lệch ngày. Các cờ còn nguyên, không tự sửa raw hoặc loại mẫu để tạo kết quả đẹp.
7. Chọn duy nhất một tương phản thăm dò GT-07 trước tính giá trị: peak–midday sau ghép segment-day, đơn vị ngày. p=0,2748, CI bootstrap chứa 0. Không đưa thành bằng chứng ùn tắc giờ cao điểm phổ quát hoặc nguyên nhân tai nạn. Mỗi frame không là quan sát độc lập.
8. Chạy `exploratory-data-analysis/scripts/tabular_profile.py` bằng Python bundled 3.12.14 trên CSV GT-07: exit 0. Pipeline chính Python 3.10.11 với phiên bản gói thực ghi trong environment.json; không cài/chứng nhận các phiên bản ví dụ trong skill.
9. Tra Crossref và Europe PMC có lưu raw/query/count; đọc nguồn mục tiêu, phân biệt abstract/fulltext/projected scenario. Novelty và prior-art search còn giới hạn. Trích dẫn Scientific Agent Skills sau kiểm tra arXiv v2, không dùng làm bằng chứng giao thông.
10. Chấm bốn vấn đề mô tả E1/E2 và một nhánh E0 tách riêng. Điểm là judgment theo trọng số giao thức. Thiếu quyền/baseline/outcome hiện tại vẫn chặn triển khai dù điểm cao; không ép đủ top 10. Ba hướng can thiệp có H0/H1, baseline, pilot assumptions và kill criteria.
11. Xuất CSV/XLSX ma trận bằng artifact-tool 2.8.148, 2 sheet, 5 record/37 field; render và xem cả hai sheet, điều chỉnh khoảng trắng và độ cao. Không có formula tính mô hình trong workbook; điểm static đối chiếu code Python. Không kiểm trong Excel desktop.
12. Chạy lại toàn pipeline offline từ raw. **10/10 unit tests đạt**, log `tests/test_results.txt`; kiểm checksum toàn raw, đối chiếu MD5 Zenodo, danh mục, ngày/múi giờ, rate, vùng, lý trình, CRS và scoring. Kiểm thử code đạt không làm biến mất cờ chất lượng dữ liệu. Không có test thất bại chưa xử lý. Không có thực nghiệm ngoài hiện trường hoặc causal effect mới.

## Tổng kiểm

136 HTTP event; 134 phản hồi raw lưu byte, tổng 65,528,358 byte, dưới 2 GB cộng dồn và 500 MB mỗi nguồn. 22 dossier, 22 dòng audit, 12 mã có phân tích bảng/mảng/mô tả; đủ các report có nội dung hỗ trợ. Rà soát tài liệu, GIS và acquisition có giới hạn ghi ở backlog. Không khẳng định toàn bộ mọi nguồn đã tải, không công bố dữ liệu license chưa rõ.

## Còn lại

Thực hiện các bước `registry/acquisition_backlog.csv`, đặc biệt giải thích sai lệch nguồn, xin phép khảo sát, baseline hiện tại, outcome hợp lệ và xác lập novelty. Các phần này cần dữ liệu/đối tác mới, chưa đạt trong phiên. Các chi phí, cỡ mẫu pilot và can thiệp trong báo cáo là đề xuất có nhãn, không phải hoạt động đã làm.
