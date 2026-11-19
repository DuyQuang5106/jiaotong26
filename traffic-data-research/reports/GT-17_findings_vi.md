# Kết quả dữ liệu GT-17

[MEASURED RESULT] XLSX v1.1 có 18 sheet. Trích 10 giá trị dân số lịch sử 2015–2024 từ sheet Population, dòng Medium (cached values), giữ tách khỏi dự báo. Ghép năm cấp quốc gia với GT-01 cho số chết/100.000 dân: 2022=6,43; 2023=11,59; 2024=10,95. Dân số là mẫu số gánh nặng dân số, không là lưu lượng xe. GT-17 dùng lại NSO, không phải xác nhận độc lập; cached formula không chứng minh đã tái tính mô hình.

Nguồn: https://zenodo.org/records/17273112. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-17.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-17_historical_population.csv`. Mã thực thi: `src/extended_analysis.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Giá trị nào là lịch sử, giá trị nào là dự báo/tham số?
2. Dân số cùng năm có thể làm mẫu số mô tả quốc gia không?
3. Nguồn dân số có độc lập NSO để triangulation hay dùng lại nguồn?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Có historical, projection và tham số mô hình; công thức chỉ đọc cached value, không tái tính Excel/Solver; không độc lập NSO.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xác minh nguồn dân số gốc; không dùng dự báo 2026/2050 như quan sát thực.
