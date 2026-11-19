# Jiaotong26 — Nghiên cứu dữ liệu an toàn giao thông Việt Nam

Workspace nghiên cứu dựa trên danh mục 22 nguồn, nhằm tìm vấn đề có bằng chứng cho ba hướng: ùn tắc/nút giao, hàng cồng kềnh và an toàn giao thông học sinh.

## Đọc kết quả

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

Kiểm thử được chạy trong workspace có snapshot: 10/10 đạt. Không coi đó là kết quả CI trên một bản clone thiếu dữ liệu. [Phương pháp tái lập](traffic-data-research/reports/08_methods_and_reproducibility.md) và [skill thực sự sử dụng](traffic-data-research/skills_used.md) ghi rõ môi trường, thao tác và giới hạn.
