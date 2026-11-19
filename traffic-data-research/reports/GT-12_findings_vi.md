# Kết quả dữ liệu GT-12

[MEASURED RESULT] Mỗi feed: 224 route_id, 7.670 stop_id nhưng chỉ 3.146 cặp tọa độ duy nhất. Chuyến AM/MD/PM lần lượt 3.024/6.713/3.301; stop_times 100.117/224.166/110.323. Cả ba calendar là 01/01–31/12/2018; headway lịch trình trung vị theo route trong từng khung là 12 phút. Không có trip/stop mồ côi hoặc khóa trip-sequence trùng. Không cộng ba khung thành lượt vận chuyển thực, không suy độ đúng giờ.

Nguồn: https://datacatalog.worldbank.org/search/dataset/0038236/hanoi-vietnam-general-transit-feed-specification-gtfs. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-12.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-12_hanoi_gtfs_am_stop_times.csv`. Mã thực thi: `src/extended_analysis.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Calendar khác ngày metadata cập nhật thế nào?
2. Stop_id có đại diện điểm dừng vật lý duy nhất không?
3. Khóa trip/stop, thứ tự trạm và headway lịch trình có nhất quán không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] 7.670 stop_id tương ứng 3.146 cặp tọa độ; không gọi stop_id là số trạm vật lý; không có GPS thực.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xin GTFS hiện hành, chuẩn hóa điểm dừng và mạng đi bộ, không cộng chuyến trùng giữa ba khung.
