# Phạm vi xuất bản và tái lập

## Được đưa lên repo

- Code và cấu hình của nghiên cứu, giao thức và bản sao danh mục 22 nguồn do người dùng cung cấp.
- Báo cáo tiếng Việt, ma trận vấn đề, hồ sơ nguồn, kết quả kiểm toán và bảng thống kê dẫn xuất phục vụ kết luận.
- `registry/public_raw_manifest.json`: 134 phản hồi tải trong lần nghiên cứu, giữ URL công khai, UTC, loại nội dung, byte, SHA256, phiên bản/quyền đã biết và vị trí tương đối trong workspace.
- Bảng tổng hợp GT-07 được tạo từ nguồn có metadata Kaggle ghi CC0; thống kê track GT-09 và dân số lịch sử GT-17 từ bản Zenodo ghi CC-BY-4.0. Trích dẫn và giới hạn nguồn được giữ trong báo cáo/dossier.

## Giữ cục bộ, không đưa lên repo

- Toàn bộ `data/raw/`, `data/interim/`, video, ảnh và các bảng nguồn đầy đủ chưa rõ quyền tái phân phối.
- `registry/http_events.jsonl` và `registry/raw_manifest.json` nguyên bản: có thể chứa header cookie, session và trạng thái biểu mẫu.
- Cache kỹ năng, node_modules dạng junction, môi trường Python, danh mục package của máy, preview/inspection tạm.

Các file này không bị xóa. Bản manifest public chỉ chọn trường cần để kiểm toán và bỏ tham số URL có thể chứa thông tin xác thực. Không thay manifest public cho bằng chứng bytes/HTTP đầy đủ đang lưu cục bộ.

## Tái lập

`python src/run_all.py` chạy offline khi workspace đã có raw và log nguyên bản. Bản clone public thiếu các snapshot đó theo chủ ý; muốn chạy lại cần tự thu thập hợp lệ hoặc khôi phục bản sao được phép sử dụng. Không có token trong repo, không bảo đảm URL tương lai còn trả dữ liệu giống ngày nghiên cứu.

Các file input và raw cục bộ được bảo toàn. Bộ 10 kiểm thử và kết quả của lần chạy gốc được giữ để tham chiếu; một số kiểm thử cần raw và không chạy được chỉ từ repo public. Không có kết quả can thiệp ngoài thực địa trong repo.

## Quyền của bên thứ ba

Repo không áp dụng giấy phép blanket cho dữ liệu bên thứ ba. Xem `traffic-data-research/registry/licenses_and_access.md` và từng dossier. Các bảng thống kê và trích dẫn không có nghĩa là mọi ảnh/video/bản dữ liệu gốc đều được phép tái phân phối. Raw không được xuất bản ở đây.
