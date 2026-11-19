# Skill đã áp dụng

| Skill | Thao tác thực tế | Giới hạn |
|---|---|---|
| Spreadsheets | Đọc OOXML 13 cột, kiểm sheet/hyperlink, bảo toàn input, tạo ma trận CSV/XLSX | Không tái tính formula input/Solver |
| exploratory-data-analysis | Quy tắc missing/outlier/sampling, profile CSV, chạy `tabular_profile.py` trên GT-07 bằng Python 3.12.14, exit 0 | Không dùng phiên bản package gợi ý như bằng chứng môi trường |
| statistical-analysis | Thiết kế tương phản theo ngày sau ghép segment, effect + bootstrap CI + t-test thăm dò, giới hạn độc lập | Không chạy Pingouin/PyMC và không chứng nhận giả định |
| paper-lookup | Thực gọi Crossref 3 truy vấn + 4 DOI, Europe PMC 1 truy vấn; giữ JSON và count | Bounded ranked sample; không truy xuất hết 321 hits |
| literature-review | Scope, screening, liên kết tài liệu gốc, synthesis/novelty limits | Rà soát tường thuật một người; không systemic/full novelty search |

Đã xem và đối chiếu bản ghi trích dẫn skill: Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. https://doi.org/10.48550/arXiv.2609.00065 . Trang arXiv xem được ngày 19/11/2026, bản mới nhất hiển thị v2 ngày 02/09/2026. Đây là nguồn về quy trình/phần mềm, không là bằng chứng giao thông.

## Bổ sung trong lượt tổng hợp để tìm ý tưởng dự thi

- **scientific-critical-thinking:** đã đọc SKILL.md và áp dụng kiểm tra đơn vị quan sát, thiên lệch công bố/shortlist, nhãn cơ chế suy từ tên, thiếu exposure và khả năng khái quát địa giới/thời kỳ. Tách các số đếm trong workbook, mô tả cơ quan, diễn giải và giả thuyết thị trường. Không thực hiện đánh giá GRADE/RoB hoặc suy nhân quả.
- **Spreadsheets:** đọc OOXML hai workbook trong `data/` bằng parser có sẵn, giữ file gốc; đối chiếu 73 ID ý tưởng/23 cột và 22 ID nguồn.
- **exploratory-data-analysis:** quét toàn bộ 63 nhãn tỉnh/thành lịch sử, lưu bảng đủ để thấy cách chọn sáu ví dụ, thử regex giáo dục thay cho nhãn biên tập và giữ missing denominator khác 0. Không dùng EDA làm chứng minh hiệu quả can thiệp.

Mã, đầu ra và log: `src/discover_opportunities.py`, `reports/discovery/`. Đã đọc lại trang arXiv ở lượt này; thông tin tác giả và bản mới nhất không thay đổi so với trích dẫn trên.

## Checkpoint sau khi cài thêm skill — 19/11/2026

Đã kiểm thư mục global và đọc SKILL.md thực tế. Cả sáu skill mới đều có và được áp dụng:

- **programmatic-eda:** gọi các hàm overview/null/outlier/distribution; thử correlation, giữ ma trận và ghi lỗi helper khi không có strong pair. Bỏ ID khỏi biến số phân tích.
- **data-quality-audit:** chạy kiểm null/duplicate/FK/range/freshness, kiểm exact khóa và dtype riêng; giữ missing, ghi sáu chiều chất lượng mà không tạo điểm accuracy/SLA chưa được xác nhận.
- **analysis-assumptions-log:** khởi tạo log, ghi 8 giả định và kế hoạch xác minh; xác nhận khớp hình học, bác bỏ trạng thái xử lý nhị phân; giữ giả định chưa xác minh mở.
- **time-series-analysis:** kiểm kỳ, lịch quan sát, ngày thiếu và tính thích hợp của chuỗi; từ chối ADF/phân rã/ARIMA khi dữ liệu chưa đủ. Không chạy script dự báo minh họa.
- **root-cause-investigation:** gọi `drill_down` trên 63 tỉnh, giữ đóng góp có dấu; chỉ phân rã số học, không quy nguyên nhân khi thiếu baseline/nhật ký.
- **analysis-qa-checklist:** chạy `qa_runner` trên bốn bảng; checklist từng mục, kiểm ảnh/link và ghi quyết định giao mô tả có giới hạn; chưa có reviewer độc lập.

Các skill có sẵn áp dụng tiếp: **statistical-analysis**, **scientific-critical-thinking**, **experimental-design** (kế hoạch kiểm chứng, chưa chạy thí nghiệm), **scientific-visualization** (hình độ phủ/chênh lệch, bảng nguồn và metadata), **literature-review** (rà lại log/prior art, giới hạn tính mới).

**geopandas** và **statsmodels**: có SKILL.md, đã đọc nhưng không áp dụng GIS/fit model. Package Python chưa có trong interpreter nghiên cứu; dữ liệu không có tọa độ/CRS đủ để ghép điểm và chuỗi chưa thích hợp để dự báo. Không coi có skill là đã cài thư viện hoặc đã thực hiện phân tích.

Chi tiết: [skill và tái lập](reports/revalidation_2026_11_19_v2/07_skill_va_tai_lap_vi.md), [hash và trạng thái](reports/revalidation_2026_11_19_v2/skills_used.json), [log hàm/helper](reports/revalidation_2026_11_19_v2/skill_execution_log.json), [thay đổi kết luận](reports/revalidation_2026_11_19_v2/01_nhung_ket_luan_da_thay_doi_vi.md). Giữ Python 3.10 của nghiên cứu; không tuyên bố tương thích đầy đủ các stack pin mới trong skill. Các helper có lỗi/giới hạn được ghi, không sửa skill global.

Đã thêm lại trích dẫn Kassis et al. (2026), DOI 10.48550/arXiv.2609.00065, trong báo cáo checkpoint; đối chiếu trang arXiv ngày 19/11/2026, bản mới nhất hiển thị v2. Trích dẫn này dành cho quy trình, không hỗ trợ kết luận giao thông.
