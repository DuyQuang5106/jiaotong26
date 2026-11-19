# Checkpoint tăng độ chắc bằng chứng — 19/11/2026

Tiếp tục nghiên cứu đã có, giữ nguyên raw, đầu vào và kết quả cũ. Đã tính lại bằng code, không chỉ đề xuất kế hoạch. Check bytes trước/sau: **253 tệp được bảo toàn**, không tệp nào trong tập kiểm thay đổi.

Kết quả quan trọng: VNTraffic TXT/JSON khớp **16.036/16.036 hộp hình học**; “8.771 bất đồng” cũ không là bằng chứng tọa độ nhãn sai. GT-07 tái lập số cũ nhưng nhạy mạnh với cân ngày/cặp, nên chỉ giữ tương phản mô tả và hạ phạm vi diễn giải p/CI iid. Sáu biến động tỉnh tính lại không đổi. Lịch sử giải thưởng tiếp tục chỉ phục vụ tìm ý tưởng có trước.

- [Những kết luận thay đổi và không thay đổi](01_nhung_ket_luan_da_thay_doi_vi.md)
- [10 phát hiện giao thông đã kiểm lại](04_muoi_phat_hien_da_kiem_lai_vi.md)
- [10 hồ sơ ý tưởng ứng viên, bằng chứng và điều kiện dừng](05_muoi_y_tuong_ung_vien_vi.md)
- [Kiểm toán chất lượng](03_kiem_toan_chat_luong_vi.md) / [bản HTML](audit_report.html)
- [Thống kê, chuỗi thời gian và phân rã](02_tham_dinh_thong_ke_va_thoi_gian_vi.md)
- [Giả định và quyết định](assumptions_log.md)
- [Thiết kế kiểm chứng tiếp theo](06_thiet_ke_kiem_chung_tiep_theo_vi.md)
- [Skill đã dùng, hash và tái lập](07_skill_va_tai_lap_vi.md)
- [Tài liệu/tính mới](08_ra_soat_tai_lieu_va_tinh_moi_vi.md)
- [QA và quyết định giao](09_qa_va_quyet_dinh_giao_vi.md)

Mười phát hiện là bằng chứng lịch sử/kiểm kê có phạm vi, không phải mười nguyên nhân đã xác minh. Mười ứng viên là giả thuyết: C01–C06 chưa biết cơ chế địa phương; C07–C10 có chi tiết hành lang nhưng chưa có hiệu quả/nhu cầu/tính mới. C07/C08 đáng xác minh trước **nếu** nhóm tiếp cận được địa bàn và vấn đề còn tồn tại. Không coi đủ số lượng là đủ điều kiện phát triển.

Giữ nguyên [10 mẫu hình lịch sử cuộc thi](../discovery/10_quy_luat_y_tuong_vi.md) và [6 hướng ban đầu](../discovery/ngach_dia_phuong_va_huong_du_thi_vi.md). Đọc kết quả cũ cùng log hiệu chỉnh. Chưa khảo sát hiện trường, thử can thiệp hoặc xác lập tính mới. Dữ liệu mới, công suất thử nghiệm và tra cứu hồ sơ kỹ thuật đầy đủ vẫn là các cổng cần vượt; không tự điền bằng ví dụ giả.

Tái lập riêng checkpoint bằng `python -X utf8 traffic-data-research/src/revalidate_research.py --output traffic-data-research/reports/revalidation_replay` từ gốc repo; output phải chưa tồn tại. `measured_rechecks.json`, JSON T/C, các CSV, checksum và log helper giữ dấu vết tính toán. Không cần chạy lại toàn bộ pipeline cũ.
