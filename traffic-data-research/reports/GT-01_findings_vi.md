# Kết quả dữ liệu GT-01

[MEASURED RESULT] 639 ô thống kê (71 nhãn địa lý × 3 năm × 3 chỉ tiêu), hai giá trị thiếu. Toàn quốc 2024: 23.667 vụ, 11.101 người chết, 17.424 người bị thương. So 2023, số vụ +7,25%, số chết −4,53%. Ba ô tổng vùng miền Trung 2024 lệch tổng tỉnh thành phần: +2.914 vụ, +1.718 chết, +2.104 bị thương. Không sửa số gốc.

Nguồn: https://pxweb.nso.gov.vn/pxweb/vi/Y%20t%E1%BA%BF,%20v%C4%83n%20h%C3%B3a%20v%C3%A0%20MSDC/Y%20t%E1%BA%BF,%20v%C4%83n%20h%C3%B3a%20v%C3%A0%20MSDC/V14.88.px/. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-01.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-01_aggregates.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Tổng vùng có khớp các tỉnh thành phần không?
2. Số vụ và số chết 2023–2024 đổi thế nào khi giữ nguyên địa giới cũ?
3. Tỷ lệ theo dân số thay đổi kết luận mô tả tới đâu?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Tổng vùng miền Trung 2024 không khớp tỉnh thành phần; phạm vi/định nghĩa 2022–2023 chưa thống nhất.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xin NSO giải thích ba sai lệch, định nghĩa vụ và tử vong; giữ nguyên số gốc.
