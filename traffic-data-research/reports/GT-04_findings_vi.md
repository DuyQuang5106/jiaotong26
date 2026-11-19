# Kết quả dữ liệu GT-04

[MEASURED RESULT] Mẫu bbox 106.797–106.801E, 10.868–10.872N: 1.125 đối tượng (1.026 node, 88 way, 11 relation), 53 đối tượng có highway, 5 có crossing và 1 có amenity=school. Đối tượng trả về có thể mở rộng ra ngoài bbox. Đây là mức ghi tag trong mẫu thuận tiện, không chứng minh thiếu công trình.

Nguồn: https://download.geofabrik.de/asia/vietnam.html. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-04.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-04_osm_sample.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Mẫu nhỏ có bao nhiêu đối tượng mang tag trường/vạch qua đường?
2. Way/relation có mở rộng ra ngoài bbox khiến số đếm sai phạm vi không?
3. Có thể khẳng định thiếu hạ tầng từ tag trống hay không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Mẫu thuận tiện nhỏ, không đại diện Việt Nam; không có kiểm tra thực địa; Geofabrik chưa xác minh được.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Mở rộng mẫu có thiết kế và kiểm chứng độc lập; OSM thiếu tag không có nghĩa thiếu hạ tầng.
