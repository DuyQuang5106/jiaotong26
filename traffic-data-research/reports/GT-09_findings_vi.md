# Kết quả dữ liệu GT-09

[MEASURED RESULT] VNTraffic TXT: 16.036 hộp, 501 chỉ số frame (0–500), 85 track_id duy nhất, 2 khóa frame-track trùng. JSON: 205 track, cũng 16.036 hộp; ghép theo frame và ID nguyên bản không khớp 8.771 hộp. Đây là khác biệt biểu diễn/định danh chưa được giải thích, không tự quy thành lỗi toàn bộ ground truth. AICC22-Custom TXT 1.185 hộp/21 ID, JSON 2.439 hộp/25 ID; không dùng tập này suy luận Việt Nam. Chưa tính tốc độ thực, TTC hay PET.

Nguồn: https://zenodo.org/records/18195750. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-09.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-09_VNTraffic_boxes.csv`. Mã thực thi: `src/extended_analysis.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. TXT và JSON có cùng số hộp, track và khóa frame-track không?
2. Có track gián đoạn hoặc khóa trùng trước tính quỹ đạo không?
3. Đã có camera calibration và thời gian quay đủ tính TTC/PET chưa?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] TXT/JSON khác định danh track; có khóa frame-track trùng. Không có homography hoặc ngày quay xác minh.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xin giải thích ánh xạ track và sửa khóa trùng; hiệu chỉnh camera trước TTC/PET, không công bố ảnh người/biển số.
