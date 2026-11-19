# Nhật ký tổng hợp để tìm ý tưởng dự thi

Ngày 19/11/2026. Yêu cầu: 10 quy luật/mẫu hình ý tưởng, 10 phát hiện giao thông, ưu tiên ngách địa phương và khả năng hình thành ý tưởng dự thi có căn cứ.

1. Đọc ba file `data/`, giữ nguyên bytes; kiểm 73 ý tưởng/23 cột, 67 cùng cuộc thi và 6 Data For Life; danh mục giao thông đủ 22 mã.
2. Áp dụng Spreadsheets, exploratory-data-analysis và scientific-critical-thinking. Đọc lại chọn lọc nguồn 2022/2023/2024/2025 và thể lệ 2026; chưa xác minh toàn bộ 73 hồ sơ. Một số nguồn NSO/phân trang Sơn La không đọc được qua web tool, giữ kết quả từ snapshot lần nghiên cứu gốc. `source_checks.json` ghi rõ các lần thành công/thất bại.
3. Tính thống kê nhóm ý tưởng, trạng thái, năm và bình chọn; giữ riêng hạng chưa xác minh. 70/73 cơ chế suy từ tên. Kiểm tra regex E-learning tránh nhầm chuỗi Machine Learning; không đổi nhãn gốc để tăng số ví dụ.
4. Loại sáu tổng vùng, tổng quốc gia và Khác khi quét tỉnh; chuẩn hóa khoảng trắng, không gộp địa giới. Quét đủ 63 tỉnh/thành cho 2023–2024, lưu cả bảng đầy đủ; chọn sáu ví dụ khác chiều/thay đổi đồng thời để xin dữ liệu chi tiết. Không chọn theo p-value hoặc xếp hạng nguy cơ; không có kiểm định suy luận mới.
5. Đối chiếu bốn hành lang Sơn La bằng tên tuyến và record ID. Phân biệt mô tả nguy cơ với sự kiện và đo thực địa. Không geocode lý trình rút gọn, không cộng hai danh mục thành số vị trí duy nhất.
6. Sinh đúng 10 mẫu hình I01–I10 và 10 phát hiện T01–T10. Mỗi mục có bằng chứng, mẫu số/nguồn, diễn giải, giả thuyết ngách, bước kiểm chứng và giới hạn. Hash input cùng CSV dẫn xuất được ghi trong `inputs_and_methods.json`; URL snapshot/UTC/SHA256 theo từng phát hiện ở `traffic_findings.json`.
7. Nối kết thành sáu hồ sơ O01–O06, tất cả giữ novelty/market demand/hiệu quả chưa xác lập. Ưu tiên xác minh cơ chế không đồng nghĩa sẵn sàng triển khai hoặc chắc đạt giải. Hàng cồng kềnh vẫn E0 về bằng chứng địa phương. Không nhầm xe tải dài với đối tượng xe máy chở hàng cồng kềnh.
8. Cập nhật README và `RESEARCH_OBJECTIVE.md` theo mục tiêu chính: chọn vấn đề, người dùng và cách kiểm chứng trước công nghệ. Giữ các báo cáo nền nguyên trạng; bổ sung bước tổng hợp vào pipeline khi có workbook ý tưởng. Sửa bộ đếm kiểm thử tương lai để đọc số thực thay cho hằng 10.
9. Chạy `python -X utf8 traffic-data-research/src/discover_opportunities.py`: thành công. Chạy `python -X utf8 -m unittest discover -s traffic-data-research/tests -v`: **20/20 kiểm thử đạt**, gồm 7 kiểm thử mới cho phạm vi và phép biến đổi; log riêng `test_results.txt`. `git diff --check` không báo lỗi.

Chưa thực hiện khảo sát hiện trường, thu nhu cầu khách hàng, xác lập mức sẵn lòng trả tiền hoặc thử can thiệp. Không thay số liệu 2023–2024 bằng hiện trạng 2026. Không tự đẩy thay đổi của lượt này lên remote.
