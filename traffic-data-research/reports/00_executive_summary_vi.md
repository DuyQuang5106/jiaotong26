# Tóm tắt nghiên cứu giao thông Việt Nam

Ngày 19/11/2026. Kết quả của lần chạy có dữ liệu thật, nhưng chưa hoàn tất thực nghiệm hiện trường hoặc chứng minh hiệu quả giải pháp.

## Đã xác minh

Danh mục hợp lệ: 22 ID duy nhất, giữ nguyên 13 cột, workbook gốc không sửa. Audit 22/22 nguồn; A=7, B=5, C=4, D=5, E=1, F=0, G=0. Phân lớp nguồn và URL/checksum: `../registry/source_audit.csv`, `raw_manifest.json` và 22 dossier. Geofabrik timeout nhưng mẫu OSM chính thức tải được; OpenAQ trả 401. Không gọi HTTP 200 của portal là raw data.

## Kết quả thực

- GT-01: toàn quốc 2024 ghi 23.667 vụ, 11.101 chết; phát hiện tổng vùng không khớp thành phần, chưa suy biến động nguy cơ.
- GT-07: 90.938 trạng thái của 10.027 segment; 39,69% dòng thuộc một ngày. Kiểm định thăm dò 26 ngày: chênh lệch −3,46 đơn vị gốc, CI bootstrap [−10,07;1,79], p=0,275. Chưa có bằng chứng khác biệt theo khung giờ với thiết kế này.
- GT-08: 50 mảng nhãn / 144.847 frame, 62.130 frame abnormal; 42,89% chỉ là tỷ phần benchmark tuyển chọn, không là prevalence vi phạm.
- GT-09: 16.036 hộp VNTraffic, 501 frame; TXT có 85 ID và JSON 205 ID, cần giải thích trước đo quỹ đạo.
- GT-10/11: đủ 107/58 bản ghi nguy cơ; 48/107 mô tả GT-10 nhắc tầm nhìn. Không phải số tai nạn.
- GTFS: calendar thực là 2018, không phải lịch hiện tại. GT-20 có 82 lớp thống kê và cờ bản dịch trái/phải.

Chi tiết 12 nguồn đã phân tích, mẫu số và giới hạn: `02_data_findings_vi.md`; 12 trang theo nguồn. Kết quả rate theo dân số là gánh nặng trên dân số, không thay exposure giao thông. Chưa có E3/E4 từ các nguồn ghép.

## Vấn đề và lựa chọn

Chỉ có 4 ứng viên có bằng chứng mô tả E1/E2, không đủ 10. Điểm chủ quan có trọng số: P02 duy trì hành vi an toàn học sinh 2,65/5; P03 định vị hàng chờ 2,55; P01 đoạn cong/tầm nhìn 2,45; P04 danh mục sạt lở 2,00. Các điểm không vượt cổng thiếu baseline/quyền/outcome. Hàng cồng kềnh giữ E0 do chưa có nhãn riêng và mẫu số tác hại.

[RECOMMENDATION] Ba hướng điều tra: học tương tác có đo duy trì; hỗ trợ điều tiết dựa trên đo hàng chờ; xác minh cảnh báo đoạn cong. H0/H1, baseline, minimum pilot, ngân sách giả định và kill criterion trong `05_top_3_interventions_vi.md`. Chưa có giải pháp sẵn sàng triển khai. Novelty tất cả NOT ESTABLISHED.

## Cuộc thi và tái lập

[VERIFIED SOURCE FACT] [Thể lệ 2026](https://sangkienatgt.dantri.com.vn/the-le) xác nhận ba chủ đề và yêu cầu hồ sơ trước 15/12/2026. Trang nêu tính độc đáo, khả thi và phù hợp; chưa thấy rubric trọng số định lượng của ban giám khảo. Trọng số xếp hạng nghiên cứu là do master prompt quy định, không gán cho cuộc thi.

Lệnh offline từ thư mục này: `python src/run_all.py`. Raw giữ nguyên, mọi kết quả sinh từ snapshot trong manifest. Dữ liệu web tương lai có thể đổi, không bảo đảm tải lại giống snapshot. Kiểm thử: `python -m unittest discover -s tests -v`; log thực nằm ở `../run_log.md` và `../tests/test_results.txt`.
