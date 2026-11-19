# Kết quả dữ liệu GT-02

[MEASURED RESULT] Ba báo cáo sơ bộ tháng 8–10/2026. Tháng 10: 1.266 vụ, 720 chết, 765 bị thương. Tháng 9 riêng: 1.327/782/793; tháng 10 cộng mức giảm đã công bố suy ra tháng 9 là 1.330/787/791. Sai lệch lần lượt +3/+5/−2, có thể do cập nhật hoặc lỗi báo cáo; chưa có giải thích từ cơ quan.

Nguồn: https://bocongan.gov.vn/chuyen-muc/thong-tin-thong-ke. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-02.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-02_monthly_counts.csv`. Mã thực thi: `src/supplemental_analysis.py; src/triangulation.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Ba báo cáo tháng có nhất quán với mức tăng giảm tháng liền trước không?
2. Số sơ bộ có dấu hiệu revision nào?
3. Có đủ tháng và exposure để kiểm định mùa vụ hay không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Chênh lệch tháng 9 suy ngược từ báo cáo tháng 10 so với báo cáo tháng 9 riêng; không có mẫu số lưu lượng.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xác minh revision và kỳ chốt thống kê; không cộng nối với NSO năm khác.
