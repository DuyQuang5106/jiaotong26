# Jiaotong26 — Tìm ý tưởng dự thi an toàn giao thông từ bằng chứng

Mục tiêu chính: tìm vấn đề cụ thể tại địa phương/nhóm người dùng, có dữ liệu và cách kiểm chứng, để phát triển thành ý tưởng dự thi tốt. Kết hợp danh mục 22 nguồn giao thông với 73 ý tưởng công bố giai đoạn 2022–2025; không mặc định làm AI, camera hoặc app trước khi xác nhận vấn đề. Xem [mục tiêu và tiêu chuẩn chọn đề tài](RESEARCH_OBJECTIVE.md).

## Kết quả phục vụ chọn ý tưởng

- **Mới nhất:** [Checkpoint kiểm chứng bổ sung — 10 phát hiện và 10 ý tưởng ứng viên](traffic-data-research/reports/revalidation_2026_11_19_v2/README.md)
- [Hiệu chỉnh kết luận GT-07/GT-09 và các kết quả giữ nguyên](traffic-data-research/reports/revalidation_2026_11_19_v2/01_nhung_ket_luan_da_thay_doi_vi.md)
- [10 quy luật/mẫu hình ý tưởng + 10 phát hiện giao thông](traffic-data-research/reports/discovery/README.md)
- [10 mẫu hình: số liệu, ý nghĩa, giới hạn và phép thử](traffic-data-research/reports/discovery/10_quy_luat_y_tuong_vi.md)
- [10 phát hiện: sáu tỉnh/thành và bốn hành lang Sơn La](traffic-data-research/reports/discovery/10_phat_hien_giao_thong_vi.md)
- [6 hồ sơ ngách, ý tưởng có trước và điều kiện dừng](traffic-data-research/reports/discovery/ngach_dia_phuong_va_huong_du_thi_vi.md)
- [Bảng quét toàn bộ 63 tỉnh/thành theo địa giới 2023–2024](traffic-data-research/reports/discovery/tables/province_changes_2023_2024.csv)

“Quy luật” là mẫu hình trong danh mục công bố, không là công thức thắng. “Ngách” là giả thuyết người dùng/địa bàn cần xác minh, chưa có bằng chứng nhu cầu thị trường. Không gọi số tai nạn là nguy cơ nếu thiếu exposure, không dùng số năm cũ làm hiện trạng 2026, và không gọi ý tưởng mới chỉ vì chưa thấy trong 73 tên.

Checkpoint bổ sung giữ nguyên dữ liệu và báo cáo cũ. VNTraffic khớp 16.036 hộp hình học giữa TXT/JSON khi đối chiếu đúng; GT-07 nhạy theo cách cân nên p/CI iid cũ chỉ giữ để kiểm toán, không dùng suy luận dân số. Mười ứng viên mới có điều kiện dừng và mức bằng chứng; chưa có ứng viên được xác nhận hiệu quả, nhu cầu thị trường hoặc tính mới. Sáu skill analytics mới đã được áp dụng; GeoPandas/statsmodels có hướng dẫn nhưng chưa dùng mô hình/GIS vì đầu vào chưa đủ.

Chạy riêng checkpoint vào thư mục mới, không cần chạy lại pipeline cũ: `python -X utf8 traffic-data-research/src/revalidate_research.py --output traffic-data-research/reports/revalidation_replay`. Cần các snapshot cục bộ và skill đúng hash theo log. Xem [skill, môi trường và cách tái lập checkpoint](traffic-data-research/reports/revalidation_2026_11_19_v2/07_skill_va_tai_lap_vi.md).

Từ gốc repo, chạy phần tổng hợp bằng `python traffic-data-research/src/discover_opportunities.py`. Cần ba file trong `data/` và các bảng GT-01/10/11 cục bộ đã thu hợp lệ; script chỉ viết kết quả dẫn xuất mới, giữ nguyên các file đầu vào. Thông tin nguồn/checksum và bộ lọc ở `reports/discovery/inputs_and_methods.json` và `traffic_findings.json`.

## Nghiên cứu nền và bằng chứng gốc

- [Tóm tắt điều hành](traffic-data-research/reports/00_executive_summary_vi.md)
- [Phân tích dữ liệu thực và giới hạn](traffic-data-research/reports/02_data_findings_vi.md)
- [Ma trận bằng chứng CSV](traffic-data-research/reports/03_problem_evidence_matrix.csv) / [Excel](traffic-data-research/reports/03_problem_evidence_matrix.xlsx)
- [Ba giả thuyết can thiệp](traffic-data-research/reports/05_top_3_interventions_vi.md)
- [Kiểm chứng 22 nguồn](traffic-data-research/registry/source_audit.md)
- [Tài liệu có trước và giới hạn tính mới](traffic-data-research/reports/06_prior_art_vi.md)

Lần nghiên cứu ngày 19/11/2026 đã audit 22/22 nguồn và phân tích dữ liệu bảng/mảng của 12 mã nguồn. Kết quả là bằng chứng mô tả và các giả thuyết cần kiểm chứng. Chưa có khảo sát hiện trường, thử nghiệm can thiệp hay tính mới được xác lập. Các mức điểm xếp hạng là đánh giá nghiên cứu, không phải xác suất rủi ro hoặc hiệu quả đã chứng minh.

## Nội dung repo public

Repo chứa giao thức, workbook danh mục đầu vào, code, báo cáo, 22 hồ sơ nguồn, kiểm toán chất lượng, bảng tóm tắt dẫn xuất và [manifest công khai](traffic-data-research/registry/public_raw_manifest.json).

Dữ liệu thô, video, ảnh, các bảng trích xuất nguyên bản chưa rõ quyền phân phối và log HTTP có cookie/session được giữ cục bộ, không đưa lên Git. Dữ liệu/mã nguồn của bên thứ ba giữ nguyên quyền của nhà cung cấp; repo không cấp lại giấy phép cho chúng. Chi tiết: [phạm vi xuất bản và tái lập](PUBLICATION.md).

## Chạy lại nghiên cứu

Sau khi có các snapshot gốc được phép sử dụng ở đúng vị trí theo manifest:

```powershell
cd traffic-data-research
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python src/run_all.py
```

**Chỉ clone repo chưa đủ để chạy lại toàn bộ offline**, vì raw được giữ cục bộ. Các adapter tải dữ liệu ở `src/acquire.py`, `deep_fetch.py`, `followup_fetch.py`, `final_fetch.py`, `uit_fetch.py`, `aggregate_fetch.py`; quyền truy cập, license và URL có thể thay đổi. Xem [backlog theo nguồn](traffic-data-research/registry/acquisition_backlog.csv) trước khi tải lại.

Lượt kiểm thử ban đầu: 10/10. Sau bổ sung tổng hợp và checkpoint: 28/28 đạt trong workspace có snapshot. Không coi đó là kết quả CI trên một bản clone thiếu dữ liệu hoặc chứng minh hiệu quả can thiệp. [Phương pháp tái lập](traffic-data-research/reports/08_methods_and_reproducibility.md) và [skill thực sự sử dụng](traffic-data-research/skills_used.md) ghi rõ môi trường, thao tác và giới hạn.
