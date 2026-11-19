# Kết quả dữ liệu GT-20

[MEASURED RESULT] classid.csv 82 lớp, tổng Count công bố 19.748; min 32, max 1.446, tỷ số max/min 45,19. ID31: tên Anh là No Moto Turn Left còn tiếng Việt ghi “Cấm xe máy rẻ phải”. Đây là cờ cần rà soát nhãn, chưa chứng minh mô hình kém hoặc học sinh thiếu kiến thức. ZIP ảnh 904,8 MB vượt trần nên không tải.

Nguồn: https://huggingface.co/datasets/star092304/Traffic-sign-detection-VietNam. Ngày truy cập từng file, URL chính xác, phiên bản và SHA256: `../registry/raw_manifest.json`; bản tải và lược đồ: `../sources/GT-20.md`. Kỳ/địa bàn gắn với từng chỉ tiêu ở trên, không thay bằng ngày xuất bản.

Bảng dẫn xuất: `../data/processed/GT-20_classes.csv`. Mã thực thi: `src/eda.py`. Hồ sơ thiếu/trùng/kiểu dữ liệu: `../quality/field_profiles.csv`. Mẫu số là số dòng/frame/đối tượng đã nêu, trừ tỷ lệ dân số có công thức riêng. Không ngoại suy sang tổng dân cư/xe.

## Câu hỏi EDA

1. Count công bố lệch giữa lớp tới mức nào?
2. Có mâu thuẫn tên Anh/Việt ảnh hưởng sử dụng giáo dục không?
3. Bảng lớp có cho phép kết luận mật độ biển hoặc lỗi người học không?

Kiểm tra độ bền/giải thích thay thế: GT-01 đối chiếu tổng vùng; GT-02 đối chiếu báo cáo tháng trước; GT-07 ghép đoạn-ngày, lọc ngưỡng và bỏ từng ngày; GT-08 so trọng số frame/video; GT-09 đối chiếu TXT/JSON; GT-10 đổi cụm từ; GT-11 so thứ tự/phân trang đầy đủ; GT-12 gộp theo tọa độ thay stop_id; GT-17 tách lịch sử/dự báo; GT-20 so hai ngôn ngữ. GT-04/06 chưa có kiểm chứng vật lý hoặc dữ liệu độc lập để thử kết luận an toàn; chỉ kiểm giới hạn phạm vi. Xem bảng chi tiết và giới hạn dưới đây, không gán sức mạnh xác nhận cho việc kiểm schema.

[NOT VERIFIED] ZIP vượt 500 MB/nguồn nên không tải. License chưa rõ; ID31 Anh/Viet trái/phải mâu thuẫn; Count là số công bố.

[INTERPRETATION] Đây là bằng chứng mô tả trong phạm vi nguồn. Không có thử nghiệm can thiệp mới. Không đủ dữ liệu xác định nguy cơ tai nạn cá nhân hoặc khẳng định hiệu quả nhân quả.

[RECOMMENDATION] Xác minh license, sửa từ điển lớp và lấy tập nhãn nhỏ có scene split; không gọi Count là số ảnh kiểm đếm.
