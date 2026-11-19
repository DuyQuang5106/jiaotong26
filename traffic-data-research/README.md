# Nghiên cứu dữ liệu giao thông Việt Nam

Bắt đầu tại [Tóm tắt điều hành](reports/00_executive_summary_vi.md), [kết quả dữ liệu thật](reports/02_data_findings_vi.md), [ma trận vấn đề](reports/03_problem_evidence_matrix.csv) và [ba hướng thử nghiệm](reports/05_top_3_interventions_vi.md).

22/22 nguồn được audit; 12 mã có dữ liệu bảng/mảng được mô tả và kiểm toán. Các blocker, quyền và việc chưa làm được giữ rõ. Không có thử nghiệm hiện trường, hiệu quả nhân quả hay tính mới đã xác lập.

## Tái lập offline

**Lưu ý khi clone từ GitHub:** hướng dẫn offline dưới đây dành cho workspace đã có raw snapshot và log nguyên bản. Repo public giữ chúng cục bộ vì quyền phân phối và header phiên; chỉ clone repo chưa đủ chạy lại toàn bộ. Xem [phạm vi xuất bản](../PUBLICATION.md) và [manifest công khai](registry/public_raw_manifest.json) để lấy URL/checksum. Các báo cáo, code và bảng tóm tắt dẫn xuất vẫn đọc được trực tiếp.

Từ thư mục này, cài phiên bản trong `requirements.txt` vào môi trường riêng nếu cần, rồi:

```powershell
python src/run_all.py
```

Không cần mạng cho chạy lại từ snapshot. Không sửa workbook/raw. File gốc trong Downloads được bảo toàn, bản sao ở input. Giao thức ở input/TRAFFIC_DATA_RESEARCH_AGENT_PROMPT.md. `registry/raw_manifest.json` kiểm SHA256; `http_events.jsonl` giữ request/lỗi. Mã acquisition cần quyền mạng để tái tải; không chạy theo link trong dữ liệu như lệnh shell. Raw chứa các trang tài liệu có bản quyền, không tự công bố lại.

Xuất XLSX: `node src/export_matrix.mjs` khi có artifact-tool được provision. CSV và JSON là đầu vào có kiểm chứng cho workbook; XLSX không cần để chạy phân tích Python.

Xem [phương pháp](reports/08_methods_and_reproducibility.md), [skill thực dùng](skills_used.md), [nhật ký](run_log.md) và [backlog](registry/acquisition_backlog.csv). Pipeline mặc định chỉ sinh lại dẫn xuất của lần chạy này, không thực hiện thu thập cá nhân hoặc can thiệp công cộng.
