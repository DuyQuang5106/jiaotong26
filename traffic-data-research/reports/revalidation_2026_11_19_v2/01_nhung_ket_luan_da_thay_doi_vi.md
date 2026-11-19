# Đối chiếu kết luận trước và sau checkpoint

Các báo cáo cũ được giữ nguyên. Khi có khác biệt, dùng hiệu chỉnh ở bảng này để đọc kết quả cũ. Lượt này kiểm lại snapshot, không thu một mẫu dân số mới.

| Phạm vi | Trước | Kiểm lại | Quyết định |
| --- | --- | --- | --- |
| GT-09 VNTraffic | 8.771 bất đồng theo khóa frame–track; đếm 205 đối tượng JSON. | 16,036/16,036 hộp khớp hình học. JSON có 205 mục, trong đó 120 mục rỗng; 85 track có hộp. Ánh xạ track trên hộp khớp là một-một; 49 mã khác tên. | Hiệu chỉnh diễn giải: không có bằng chứng sai hình học từ phép đối chiếu này. Còn 2 khóa frame–track TXT trùng cần làm rõ, chưa kiểm với video. |
| GT-09 AICC22 | TXT/JSON khác tổng số hộp. | 1,185 hộp TXT đều có trong JSON; JSON thêm 1,254 hộp. | Giữ cờ không thay thế trực tiếp hai biểu diễn; không gọi cả 1.254 hộp thêm là nhãn sai; không suy luận Việt Nam từ AICC22. |
| GT-07 suy luận | Tương phản thăm dò −3,459; t(25)=−1,117; p=0,275 và CI bootstrap ngày. | Tái lập đúng số cũ. Cân đều cặp đoạn–ngày cho −0,020; trung vị ngày 0; lọc ngày có ≥2 cặp cho +1,448 (18 ngày). | Hạ phạm vi diễn giải xuống tương phản mô tả trong mẫu; p/CI iid chỉ giữ để kiểm toán, không dùng như suy luận dân số được hiệu chỉnh. |
| GT-10 trạng thái xử lý | 19 treated và 89 untreated không rỗng. | Bản ghi 79 có cả hai trường: đã thực hiện một phần và còn đề nghị kế hoạch đầu tư. | Giữ số đếm trường; bác bỏ cách xem chúng là nhãn hoàn thành/chưa hoàn thành loại trừ nhau. |
| GT-01 sáu địa bàn | Các biến động 2023–2024 trong T01–T06. | Tính lại cả 63 tỉnh và đối chiếu toàn bộ chỉ số sáu ví dụ: không đổi. Tổng quốc gia khớp tỉnh+Khác ở 7 ô có Khác; 2 ô Khác thiếu không kiểm được. | Giữ phát hiện mô tả; không đổi thành xếp hạng nguy cơ, nguyên nhân hay hiện trạng năm 2026. |
| GT-08 | Tỷ lệ frame có nhãn bất thường trong 50 mask. | Đọc lại 50 NPY với allow_pickle=False, kiểm hash, miền nhãn và tổng frame: khớp. | Giữ kết quả benchmark tuyển chọn; không coi là tần suất vi phạm hoặc tỷ lệ chở hàng cồng kềnh trên đường. |
| Cuộc thi | 10 nhóm giáo dục theo nhãn biên tập; 70/73 cơ chế từ tên. | Kiểm ID, nguồn liên kết và độ nhạy cách gán nhóm. Bộ lọc tiêu đề giáo dục cho 8 bài; nhãn biên tập cho 10. | Giữ 10 mẫu hình như mô tả danh mục; không xem nhãn nhóm là taxonomy đã thẩm định hoặc giải thưởng là nhãn dự đoán đáng tin. |
| Tài liệu/tính mới | Rà soát tường thuật giới hạn, prior art cho cảnh báo cua và giáo dục. | Kiểm log tìm kiếm; giữ rõ chưa phân trang hết/không đủ hồ sơ. Đối chiếu lại trang FHWA và nguồn trích dẫn skill. | Không nâng novelty của bất kỳ ứng viên nào; không coi metadata/DOI/giải thưởng là chứng minh hiệu quả. |
