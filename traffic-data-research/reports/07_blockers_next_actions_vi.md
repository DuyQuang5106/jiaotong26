# Trở ngại và việc tiếp theo

[NOT VERIFIED] Mỗi mã đều có bước theo dõi, dù đã có dữ liệu để phân tích. Không coi trạng thái FOLLOWUP_REQUIRED là chưa làm audit.

## GT-01

Tổng vùng miền Trung 2024 không khớp tỉnh thành phần; phạm vi/định nghĩa 2022–2023 chưa thống nhất.

[RECOMMENDATION] Xin NSO giải thích ba sai lệch, định nghĩa vụ và tử vong; giữ nguyên số gốc.

## GT-02

Chênh lệch tháng 9 suy ngược từ báo cáo tháng 10 so với báo cáo tháng 9 riêng; không có mẫu số lưu lượng.

[RECOMMENDATION] Xác minh revision và kỳ chốt thống kê; không cộng nối với NSO năm khác.

## GT-03

Chỉ metadata/nội dung báo cáo; chưa tải hay phân tích PDF.

[RECOMMENDATION] Tải PDF gốc, ghi năm của từng chỉ tiêu và nguồn WHO/nhà nước; tránh đếm độc lập dữ liệu tái sử dụng.

## GT-04

Mẫu thuận tiện nhỏ, không đại diện Việt Nam; không có kiểm tra thực địa; Geofabrik chưa xác minh được.

[RECOMMENDATION] Mở rộng mẫu có thiết kế và kiểm chứng độc lập; OSM thiếu tag không có nghĩa thiếu hạ tầng.

## GT-05

Chưa thử tải ảnh/map features; quyền token và coverage chưa xác minh.

[RECOMMENDATION] Kiểm tra chính sách và token của tài khoản được phép, chọn mẫu có quyền sử dụng.

## GT-06

Không có probe thô hoặc mẫu số chuyến; hai thành phố không xác định nút giao cụ thể.

[RECOMMENDATION] Lấy định nghĩa vùng/phương pháp và đo lại hàng chờ tại nút chọn khảo sát.

## GT-07

Đơn vị velocity và cách thu mẫu chưa xác minh; lịch lấy mẫu lệch; metadata 2026 không phải kỳ quan sát.

[RECOMMENDATION] Xác nhận đơn vị/LOS với tác giả; đo mẫu hiện hành để kiểm chứng.

## GT-08

Nhãn chỉ normal/abnormal, không phân biệt hàng cồng kềnh; video, COCO 379 MB/177,8 MB chưa tải; chưa thấy license rõ.

[RECOMMENDATION] Xin điều khoản nghiên cứu/redistribution; xác minh ánh xạ frame–video, lấy nhãn loại hành vi và mẫu không tuyển theo sự kiện.

## GT-09

TXT/JSON khác định danh track; có khóa frame-track trùng. Không có homography hoặc ngày quay xác minh.

[RECOMMENDATION] Xin giải thích ánh xạ track và sửa khóa trùng; hiệu chỉnh camera trước TTC/PET, không công bố ảnh người/biển số.

## GT-10

Không phải tai nạn thực tế; lý trình có dạng rút gọn; chưa geocode/đo hiện trường; không có giấy phép tái phân phối rõ.

[RECOMMENDATION] Xác nhận trạng thái xử lý 2026, chuẩn hóa lý trình có người kiểm tra, đo lưu lượng và tầm nhìn.

## GT-11

Không có ngày xảy ra sạt lở, GPS hay outcome; cùng cơ quan GT-10, không độc lập.

[RECOMMENDATION] Lấy nhật ký sạt lở, ngày đóng đường, GPS và mưa đo tại chỗ trước kiểm định dự báo.

## GT-12

7.670 stop_id tương ứng 3.146 cặp tọa độ; không gọi stop_id là số trạm vật lý; không có GPS thực.

[RECOMMENDATION] Xin GTFS hiện hành, chuẩn hóa điểm dừng và mạng đi bộ, không cộng chuyến trùng giữa ba khung.

## GT-13

Danh mục không chứng minh đã có từng file quan sát giao thông.

[RECOMMENDATION] Theo cổng Hà Nội tìm từng tài nguyên có schema/license; không coi mọi dữ liệu dùng chung là mở.

## GT-14

Chưa kiểm chứng từng resource, giấy phép hay dữ liệu đường/nút cụ thể.

[RECOMMENDATION] Chọn tài nguyên giao thông tại data.hochiminhcity.gov.vn, kiểm tra link và kỳ cập nhật.

## GT-15

Thông số camera là công bố năng lực, không phải log quan sát công khai; không thử quyền hệ thống nội bộ.

[RECOMMENDATION] Đề nghị cơ quan cấp bảng đếm tổng hợp theo nút × 15 phút, loại dữ liệu cá nhân.

## GT-16

Không có raw VDS/phasing; công bố không chứng minh hiệu quả nhân quả.

[RECOMMENDATION] Xin log lưu lượng và pha đèn cùng thời kỳ; chọn thiết kế đánh giá với đối chứng.

## GT-17

Có historical, projection và tham số mô hình; công thức chỉ đọc cached value, không tái tính Excel/Solver; không độc lập NSO.

[RECOMMENDATION] Xác minh nguồn dân số gốc; không dùng dự báo 2026/2050 như quan sát thực.

## GT-18

Chưa lấy raster hoặc kiểm thử Earthdata; không kết luận đã bị hạn chế tài khoản.

[RECOMMENDATION] Chọn sản phẩm/phiên bản, bbox và cửa sổ sự kiện có outcome; thử endpoint chính thức và ghi quyền.

## GT-19

NO ACCESS TO DATA trong lần chạy; chưa xác minh phủ trạm Việt Nam.

[RECOMMENDATION] Dùng API key do người dùng tự quản lý sau khi được phép; không suy nguồn ô nhiễm từ tương quan.

## GT-20

ZIP vượt 500 MB/nguồn nên không tải. License chưa rõ; ID31 Anh/Viet trái/phải mâu thuẫn; Count là số công bố.

[RECOMMENDATION] Xác minh license, sửa từ điển lớp và lấy tập nhãn nhỏ có scene split; không gọi Count là số ảnh kiểm đếm.

## GT-21

Không có dữ liệu quan sát mới ngoài GT-01; đây là portal.

[RECOMMENDATION] Chọn bảng theo chỉ tiêu, kiểm tra đơn vị, metadata và lấy toàn bộ giá trị liên quan.

## GT-22

Không có log lịch sử hoặc API thô đã xác minh; không lưu camera stream.

[RECOMMENDATION] Xin tài liệu API lịch sử và quyền sử dụng; chỉ thu bảng tổng hợp được cho phép.

## Công việc chưa thực hiện

Chưa có khảo sát hiện trường, quyền tiếp cận dữ liệu hệ thống nội bộ, thử can thiệp hoặc xác lập novelty. Chưa phân tích PDF GT-03, chưa lấy raster mưa GT-18, chưa lấy ảnh Mapillary, chưa lấy bảng vận tải GT-21 riêng hay API lịch sử GT-22. Không có sai số nhân quả/near-miss vật lý từ GT-08/09. Có backlog máy đọc được ở `../registry/acquisition_backlog.csv`. Các phần chưa làm có blocker cụ thể, không được trình bày như kết quả.
