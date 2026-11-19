# Kết quả dữ liệu GT-10

[MEASURED RESULT] 107 bản ghi trên 19 nhãn tuyến, đầy đủ theo tổng web. 48/107 mô tả có cụm “tầm nhìn”, 105/107 có “cong” hoặc “cua”; 19 ô đã xử lý không rỗng và 89 ô chưa xử lý không rỗng. Hai trường không được giả định loại trừ nhau hoặc nhị phân hoàn tất. Quy tắc chặt “hạn chế tầm nhìn” chỉ cho 16/107, cho thấy độ nhạy của mã hóa văn bản.

Nguồn: https://data.soxaydung.sonla.gov.vn/detail_data/du-lieu-cac-diem-tiem-an-tai-nan-giao-thong-tren-cac-tuyen-quoc-lo-duong-tinh. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-10.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-10_hazards.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Bao nhiêu mô tả nhắc tầm nhìn và độ cong?
2. Thay cụm từ mã hóa có làm số đếm thay đổi không?
3. Ô đã/chưa xử lý có thể diễn giải thành nhị phân hoàn tất không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Không phải tai nạn thực tế; lý trình có dạng rút gọn; chưa geocode/đo hiện trường; không có giấy phép tái phân phối rõ.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xác nhận trạng thái xử lý 2026, chuẩn hóa lý trình có người kiểm tra, đo lưu lượng và tầm nhìn.
