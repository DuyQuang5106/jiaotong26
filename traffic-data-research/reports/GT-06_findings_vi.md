# Kết quả dữ liệu GT-06

[MEASURED RESULT] Hai hàng công bố kỳ 2025: Hà Nội congestion 49,2%, TP.HCM 46,9%; không tải probe hoặc mẫu số chuyến. Dùng mô tả cấp thành phố, không xác định điểm đen hay đánh giá tai nạn.

Nguồn: https://www.tomtom.com/traffic-index/country/vietnam/. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-06.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-06_published_city_summary.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Hai chỉ số công bố thuộc kỳ nào?
2. Chênh lệch thành phố có thể xác định một nút ùn tắc hay không?
3. Mẫu số probe và ranh giới đô thị có được cung cấp trong bảng không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Không có probe thô hoặc mẫu số chuyến; hai thành phố không xác định nút giao cụ thể.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Lấy định nghĩa vùng/phương pháp và đo lại hàng chờ tại nút chọn khảo sát.
