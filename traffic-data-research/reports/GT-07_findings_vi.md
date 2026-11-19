# Kết quả dữ liệu GT-07

[MEASURED RESULT] 5 bảng: nodes 577.967; segments 84.633; streets 5.553; segment_status 90.938; train 33.441 dòng. Trạng thái trải 03/07/2020–22/04/2021 UTC, 10.027 segment, 120 ngày địa phương có quan sát. Một ngày chiếm 39,69% dòng. 107 giá trị velocity >120 trên thang gốc, 448 bằng 0; đơn vị chưa xác minh. 154 đoạn có length=0; train thiếu max_velocity ở 28.495/33.441 dòng. Không coi velocity cao là vi phạm khi thiếu định nghĩa.

Nguồn: https://ckan.transport-data.org/dataset/traffic-flow-data-in-ho-chi-minh-city-viet-nam-hochiminhcity/resource/9e5ba67b-cfb3-44f8-ac34-fdef7343e1a6. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-07.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-07_segment_status.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Quan sát có tập trung ở một ngày hoặc giờ không?
2. Ghép cùng đoạn-cùng ngày có còn chênh lệch peak–midday không?
3. Sàng lọc ngoại lệ và bỏ từng ngày ảnh hưởng ước lượng thế nào?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Đơn vị velocity và cách thu mẫu chưa xác minh; lịch lấy mẫu lệch; metadata 2026 không phải kỳ quan sát.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xác nhận đơn vị/LOS với tác giả; đo mẫu hiện hành để kiểm chứng.
