# Kết quả dữ liệu GT-11

[MEASURED RESULT] 58 bản ghi trên 17 nhãn tuyến, đủ theo tổng web. QL.4G có 15/58 bản ghi. Đây là danh mục nguy cơ, không phải 58 lần sạt lở hoặc 58 tai nạn. Trùng nhãn tuyến giữa GT-10/11 chỉ là khả năng ghép thô.

Nguồn: https://data.soxaydung.sonla.gov.vn/detail_data/du-lieu-cac-diem-co-nguy-co-sat-lo-cao-tren-cac-tuyen-quoc-lo-duong-tinh. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-11.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-11_hazards.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Danh mục đủ 58 hàng qua phân trang chưa?
2. Phân bố bản ghi theo tuyến có tập trung ở đâu?
3. Có ngày sự kiện hoặc GPS đủ ghép mưa/tai nạn chưa?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Không có ngày xảy ra sạt lở, GPS hay outcome; cùng cơ quan GT-10, không độc lập.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Lấy nhật ký sạt lở, ngày đóng đường, GPS và mưa đo tại chỗ trước kiểm định dự báo.
