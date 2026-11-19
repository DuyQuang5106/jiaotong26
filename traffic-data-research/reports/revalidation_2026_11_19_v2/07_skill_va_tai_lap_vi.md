# Skill thực sự dùng và tái lập

Đã kiểm thư mục global và đọc SKILL.md thật trước khi áp dụng. Không có skill được yêu cầu nào bị thiếu; có hướng dẫn không đồng nghĩa đã có Python package. Giữ Python 3.10 của nghiên cứu, không báo là chạy trên các stack pin mới của skill. Lượt này áp dụng hướng dẫn phương pháp và helper tương thích; không chạy Pingouin/PyMC, pydoe hay GeoPandas/statsmodels.

| Skill | Tình trạng | Thao tác/giới hạn |
| --- | --- | --- |
| programmatic-eda | APPLIED_PROCEDURAL_GUIDANCE | Chạy overview/null/outlier/distribution/correlation trên bảng phù hợp; tách ID và cờ khỏi kết luận. |
| data-quality-audit | APPLIED_PROCEDURAL_GUIDANCE | Chạy null/duplicate/FK/range/freshness; xác minh dtype và khóa riêng; scorecard không tạo accuracy giả. |
| analysis-assumptions-log | APPLIED_PROCEDURAL_GUIDANCE | Khởi tạo log, ghi 8 giả định, xác nhận/bác bỏ phần kiểm được và xuất critical list. |
| time-series-analysis | APPLIED_PROCEDURAL_GUIDANCE | Kiểm khoảng thời gian, ngày thiếu, mùa vụ và đầu vào; không chạy mô hình khi không đủ điều kiện. |
| root-cause-investigation | APPLIED_PROCEDURAL_GUIDANCE | Chạy drill_down theo 63 tỉnh; chỉ phân rã số học, không quy nguyên nhân. |
| analysis-qa-checklist | APPLIED_PROCEDURAL_GUIDANCE | Chạy qa_runner trên bốn bảng; checklist từng mục và ghi quyết định giao có giới hạn. |
| statistical-analysis | APPLIED_PROCEDURAL_GUIDANCE | Kiểm đơn vị/độc lập, tái tính tương phản, độ nhạy cân, Shapiro và hạ phạm vi p/CI. |
| scientific-critical-thinking | APPLIED_PROCEDURAL_GUIDANCE | Tách nguồn, số đo, diễn giải, giả thuyết; kiểm bias, proxy, tính mới và phạm vi địa phương. |
| experimental-design | APPLIED_PROCEDURAL_GUIDANCE | Bố trí kế hoạch mô phỏng theo người/lớp/tổ, kiểm pseudoreplication, đối chứng và phân bổ; chưa chạy thử. |
| scientific-visualization | APPLIED_PROCEDURAL_GUIDANCE | Hình có ngày missing rõ, toàn bộ điểm ngày và bảng nguồn; kiểm metadata và xem ảnh. |
| literature-review | APPLIED_PROCEDURAL_GUIDANCE | Rà log/tính đầy đủ/prior art; kiểm lại nguồn FHWA và trích dẫn quy trình; không nhận systematic review. |
| geopandas | READ_NOT_APPLIED | Có SKILL.md, đã đọc; không dùng phép GIS. Python package chưa cài, thiếu tuyến/CRS/điểm đủ tin cậy. |
| statsmodels | READ_NOT_APPLIED | Có SKILL.md, đã đọc; không fit model. Python package chưa cài, chuỗi/thiết kế chưa đủ cho mô hình đề xuất. |

Có 62 mục trong log gọi helper/cảnh báo. `skills_used.json` chứa SHA256 của từng SKILL.md; `skill_execution_log.json` chứa SHA256 script thật, hàm gọi và warning.

Từ gốc repo, dùng thư mục output mới:

```powershell
python -X utf8 traffic-data-research/src/revalidate_research.py --output traffic-data-research/reports/revalidation_replay
python -X utf8 -m unittest discover -s traffic-data-research/tests -v
```

Runner từ chối output đã tồn tại. Có thể chỉ định `--skill-root` trỏ đến thư mục cài skill tương ứng. Để tái lập helper đúng phiên bản cần các hash trong log, không chỉ cùng tên skill. Cần các snapshot raw cục bộ theo manifest, ba file `data/`, bảng dẫn xuất và báo cáo discovery đã có; clone public chưa chứa tất cả raw. `input_checksums.json` ghi đầu vào dùng trực tiếp; `preservation_check.json` kiểm bytes trước/sau các tệp gốc/kết quả cũ. Lượt đầu tự động nằm ở `../revalidation_2026_11_19/`; lượt v2 mở rộng kiểm và sinh các báo cáo này, giữ lượt đầu.

Không tải lại raw, thay input, huấn luyện mô hình giải thưởng, tự điền ngày thiếu hoặc sửa nhãn gốc. Code được bổ sung độc lập với pipeline cũ. `test_results.txt` là log thực tế trong workspace đủ snapshot, không là CI cho clone thiếu dữ liệu. Các báo cáo cũ phải đọc cùng `01_nhung_ket_luan_da_thay_doi_vi.md`.

Nguồn quy trình: Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. [arXiv](https://doi.org/10.48550/arXiv.2609.00065). Đã đối chiếu lại trang arXiv ngày 19/11/2026, bản mới nhất hiển thị v2; đây là nguồn phần mềm/phương pháp, không là bằng chứng giao thông.
