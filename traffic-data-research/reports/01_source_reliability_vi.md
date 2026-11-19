# Độ tin cậy và khả năng tiếp cận

[VERIFIED SOURCE FACT] Đã kiểm tra cả 22 mã qua HTTP thực, giữ phản hồi thô và checksum. A/B chỉ cấp khi tải và đọc được bảng/mảng. HTTP 200 của portal không được coi là dữ liệu mở.

- A_RAW_OPEN: 7 — GT-04, GT-07, GT-08, GT-09, GT-10, GT-11, GT-12
- B_AGGREGATE_OPEN: 5 — GT-01, GT-02, GT-06, GT-17, GT-20
- C_REPORT_ONLY: 4 — GT-03, GT-15, GT-16, GT-22
- D_CATALOG_ONLY: 5 — GT-05, GT-13, GT-14, GT-18, GT-21
- E_RESTRICTED: 1 — GT-19
- F_BROKEN_OR_MISSING: 0 mã ở phân lớp cuối; riêng landing Geofabrik thất bại hai lần được ghi trong GT-04.
- G_NOT_YET_CHECKED: 0.

Chi tiết từng lần truy cập: `../registry/source_audit.csv`, `http_events.jsonl`, `raw_manifest.json` và 22 dossier. GT-04 phân lớp A cho mẫu API OSM chính thức, không tuyên bố Geofabrik hoạt động. GT-02/06/20 phân lớp B cho bảng tổng hợp trích được, không phải raw cá thể. GT-17 là tổng hợp/tham số, không log giao thông.

[INTERPRETATION] Tin cậy cần tách: tính xác thực trang, tính đầy đủ bản tải, tính đúng định nghĩa và khả năng khái quát. Nguồn chính thức vẫn có sai lệch tổng và revision. Đối chiếu NSO/BCA và kiểm tra frame-track GT-09 phát hiện vấn đề cần xác minh. Các bảng mô hình hóa/tuyển chọn sự kiện/metadata nhập kho không đại diện điều kiện hiện tại.

[NOT VERIFIED] Không xác nhận license chỉ từ chữ public. GT-07 có CC0 ở metadata Kaggle gốc, TDC không nêu license; GT-09/17 ghi CC-BY-4.0; OSM cần ODbL/attribution. Các nguồn còn lại giữ trạng thái chưa xác minh quyền tái phân phối. Các snapshot chỉ lưu để kiểm toán cục bộ, không tự ý xuất bản lại dữ liệu.

[RECOMMENDATION] Xác minh định nghĩa velocity/LOS, ánh xạ track, kỳ lịch GTFS và tổng vùng trước dùng như nền mô hình. Xem `../registry/licenses_and_access.md`.
