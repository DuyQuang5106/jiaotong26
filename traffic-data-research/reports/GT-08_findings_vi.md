# Kết quả dữ liệu GT-08

[MEASURED RESULT] 50 mảng NPY nhị phân, 144,847 frame nhãn, 62,130 frame abnormal, tỷ phần 42.89% trong các file nhãn tải được. Đếm 606 chuỗi liên tiếp giá trị 1, không gọi là số xe/số vi phạm độc lập. Chỉ có nhãn 0/1; không xác định riêng hàng cồng kềnh. Không phải tỷ lệ ngoài thực địa.

Nguồn: https://uit-together.github.io/datasets/UIT-ADrone/. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-08.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-08_binary_masks_summary.csv`. Mã thực thi: `src/supplemental_analysis.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Tổng frame mask tải được là bao nhiêu, có nhãn khác 0/1 không?
2. Tỷ phần theo frame khác trung bình tỷ phần theo video thế nào?
3. Có nhãn riêng loại hàng cồng kềnh để ước lượng tần suất không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] Nhãn chỉ normal/abnormal, không phân biệt hàng cồng kềnh; video, COCO 379 MB/177,8 MB chưa tải; chưa thấy license rõ.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xin điều khoản nghiên cứu/redistribution; xác minh ánh xạ frame–video, lấy nhãn loại hành vi và mẫu không tuyển theo sự kiện.
