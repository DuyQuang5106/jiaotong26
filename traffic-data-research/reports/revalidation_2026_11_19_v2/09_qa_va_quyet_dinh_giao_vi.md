# QA và quyết định giao

Tác giả/người tự rà soát: Codex, ngày 19/11/2026; chưa có reviewer độc lập hoặc chữ ký phê duyệt của người dùng. Đối tượng: nhóm tìm đề tài dự thi.

qa_runner trên bốn bảng: 0 FAIL, 0 WARN. Log đầy đủ ở `automated_qa.json`. Kiểm tự động không chứng nhận đúng thực tế hoặc phương pháp.

| Mục | Câu hỏi | Trạng thái | Căn cứ |
| --- | --- | --- | --- |
| 1.1 | Câu hỏi thực của người dùng | PASS | 10 phát hiện + 10 ứng viên, ưu tiên chứng cứ; giữ 10 mẫu hình cũ. |
| 1.2 | Ranh giới phạm vi | PASS | Không suy AICC22/benchmark thành hiện trạng Việt Nam. |
| 1.3 | Thời kỳ đúng đề bài | CAVEAT | Dữ liệu lịch sử được ghi đúng kỳ; chưa có baseline 2026. |
| 1.4 | Định nghĩa thuật ngữ | PASS | Ứng viên, ngách, bản ghi nguy cơ, số vụ khác nguy cơ/exposure. |
| 2.1 | Nguồn được xác định | PASS | 22 mã đối chiếu; URL/hash/provenance được giữ. |
| 2.2 | Freshness | CAVEAT | Kỳ cũ/không có SLA; dùng mô tả, không triển khai. |
| 2.3 | Lineage | PASS | Raw→processed→recheck; hash trực tiếp và manifest bảo toàn. |
| 2.4 | Quyền truy cập | PASS | Chỉ đọc snapshot đã có; không thu nguồn/đăng dữ liệu mới. |
| 2.5 | Vấn đề nguồn và tác động | PASS | Báo tổng vùng, mã track, revision tháng, nhãn song ngữ. |
| 3.1 | Kiểu join và số dòng | PASS | FK riêng; đối chiếu multiset; không spatial join mù. |
| 3.2 | Grain/cộng trùng | PASS | 63 tỉnh tách tổng vùng; frame/track/ngày không là mẫu độc lập. |
| 3.3 | Null | PASS | Hai ô Khác giữ missing; không điền 0 ngày không quan sát. |
| 3.4 | Múi giờ | PASS | GT-07 UTC→UTC+7 trước ghép. |
| 3.5 | Chia 0 | PASS | province_changes giữ NA nếu base 0; có test. |
| 3.6 | Mẫu số | PASS | Previous-year count/contribution/annotation fraction ghi riêng. |
| 3.7 | Spot-check ít nhất 3 dòng | PASS | Đối chiếu toàn bộ chỉ số 6 ví dụ tỉnh với tính lại. |
| 4.1 | Cỡ mẫu cho claim | CAVEAT | Không đủ cho nhân quả/dự báo; đã giới hạn claim. |
| 4.2 | Phép kiểm | CAVEAT | t/CI iid chỉ tái lập kiểm toán; không quảng bá p mới. |
| 4.3 | Uncertainty | PASS | CI cũ giữ cùng giả định; sensitivity không gọi là CI. |
| 4.4 | Multiplicity | N/A | Không thêm family kiểm định hoặc dự đoán giải; EDA không p. |
| 4.5 | Nhân quả | PASS | Đóng góp tỉnh/giải thưởng không được gọi là nguyên nhân. |
| 4.6 | Outlier/độ nhạy | PASS | Giữ toàn bộ, cân khác/LODO được báo không chọn dấu. |
| 5.1 | Mỗi kết luận có căn cứ | PASS | JSON T/C có mã nguồn; ý tưởng giả thuyết tách riêng. |
| 5.2 | Không vượt dữ liệu | PASS | E0 cơ chế của 6 tỉnh; không gán nhóm học sinh/loại xe. |
| 5.3 | Bất ngờ được báo | PASS | GT-09 khớp geometry, GT-07 đổi dấu sensitivity được giữ. |
| 5.4 | Giới hạn rõ | PASS | Novelty/demand/current status đều chưa xác lập. |
| 5.5 | Hành động theo kết quả | PASS | Từng ứng viên có baseline, phép thử và điều kiện dừng. |
| 6.1 | Trục/hình | PASS | Đã xem PNG: nhãn rõ, trục đầy đủ, ngày thiếu không bị nội suy; có metadata và bảng nguồn. |
| 6.2 | Loại biểu đồ | PASS | Scatter không nối missing, có bảng nguồn. |
| 6.3 | Định dạng số | PASS | Báo cáo làm tròn; JSON giữ precision tính toán. |
| 6.4 | Ngôn ngữ | PASS | Báo cáo tiếng Việt; giải thích thuật ngữ và phạm vi. |
| 6.5 | Link/placeholder | PASS | Không có link Markdown hỏng; 28 kiểm thử đạt; đã xem nội dung. |

Quyết định: **giao báo cáo mô tả có điều kiện**. Đã hoàn tất kiểm ảnh/link và 28 kiểm thử, ghi ở `delivery_verification.json`; lần chạy độc lập khớp 28/28 bảng CSV và kết quả đo khi bỏ trường freshness phụ thuộc đồng hồ. Không phê duyệt triển khai, kết luận nhân quả, tính mới hoặc dự đoán giải. Các cờ thiếu dữ liệu được giữ là giới hạn, không tự “risk accept” thay cơ quan/khách hàng. Không tuyên bố toàn bộ checklist đã PASS.

Hai mục trình bày được cập nhật sau bước sinh báo cáo bằng kiểm tra ảnh/link thực tế; đó là bước tự rà soát sau chạy, không được runner tự chứng nhận khi tái lập ở output mới.

Những việc phải xong trước claim mạnh hơn: xác minh hiện trạng/địa giới, cơ chế và exposure; hồ sơ kỹ thuật prior art; mẫu số/cỡ mẫu phù hợp; đối chứng và thẩm quyền pilot. Chưa có ngày cam kết hoặc người chịu trách nhiệm bên ngoài được tự gán.
