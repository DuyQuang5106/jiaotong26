# Kế hoạch build app CHỞ VỪA (bản demo dự thi)

Ngày 20/11/2026. Hạn nộp: trước 15/12/2026, còn khoảng 25 ngày. Căn cứ luật: [luat_cho_hang_vi.md](../traffic-data-research/reports/track2_2026_11_20/luat_cho_hang_vi.md). Thiết kế đo: [cv_do_kich_thuoc_vi.md](../traffic-data-research/reports/track2_2026_11_20/cv_do_kich_thuoc_vi.md).

## 1. Hai nhóm người dùng

| Chế độ | Ai dùng | Họ cần gì | Màn hình chính |
|---|---|---|---|
| **Người chở** | Xe ôm, người giao hàng, khách tự chở | "Chở thế này có bị phạt không?" | Chụp xe đã chất hàng → đèn xanh/vàng/đỏ cho từng luật, mức phạt có thể gặp, cách sửa |
| **Chủ hàng** | Cửa hàng, người gửi hàng | "Món này chở bằng xe gì, giá bao nhiêu?" | Chụp hoặc chọn món hàng → ước tính kích cỡ → loại xe phù hợp + giá công bố + nút mở Lalamove/Ahamove/Grab |

Hai chế độ dùng chung một lõi: nhận diện, ước tính kích cỡ, bộ luật, bảng xe.

## 2. Các loại xe app phải nhận

| Loại xe | Trạng thái pháp lý | Luật áp dụng chính |
|---|---|---|
| Xe máy thường (không giá đèo hàng) | Hợp lệ | Đ33.5 Luật 36: mốc là giá đèo hàng theo thiết kế; xe không có giá thì cần xử lý riêng |
| Xe máy có giá đèo hàng / baga | Hợp lệ nếu giá đúng thiết kế; cơi nới giá có thể là cải tạo trái phép | Đ33.5; Đ32.8.b NĐ 168 nếu tự ý thay đổi kích thước xe |
| Xe đạp, xe đạp điện, xe đạp máy | Xe thô sơ | Đ31.5: 1/3 thân xe, ≤1 m trước/sau, ≤0,4 m mỗi bên bánh |
| Ba gác đạp/đẩy, xích lô | Xe thô sơ ("xe tương tự") — cách hiểu, cần xác minh | Đ31.5; quy định tỉnh (Đ35.6) |
| Ba gác gắn máy, xe ba/bốn bánh tự chế | Thường là xe sản xuất, lắp ráp trái quy định | Đ9.8 Luật 36; tịch thu theo Đ14.4 NĐ 168 |
| Xe chở hàng bốn bánh có gắn động cơ, có đăng ký | Hợp lệ, chạy đúng giờ/khu vực tỉnh quy định | Đ48 |
| Xe máy kéo theo xe/vật (rơ-moóc tự chế, kéo xe khác) | Bị cấm | Đ33.3.đ; phạt Đ7.3.g |

App không kết luận "tự chế" chỉ từ ảnh: nhận dáng xe → hỏi có đăng ký, biển số không.

## 3. Các lỗi hay gặp (danh mục theo luật; tần suất thực tế chưa đo)

| Mã | Lỗi | Ví dụ hàng | Phạt (NĐ 168) | App phát hiện bằng |
|---|---|---|---|---|
| L1 | Lòi hai bên quá 0,3 m (xe máy) / 0,4 m (thô sơ) | Tôn, ván, ống chở ngang, bao tải hai bên | 400–600k (Đ36.2.b) | Ảnh phía sau + biển số/thẻ |
| L2 | Lòi sau quá 0,5 m (xe máy) / quá 1 m hoặc 1/3 thân (thô sơ) | Ống nước, sắt cây, thang | 400–600k | Ảnh bên hông + mẫu xe/thẻ |
| L3 | Cao quá 2 m (xe máy) | Thùng xốp, lồng, bao hàng chất cao | 400–600k | Ảnh phía sau, thấy chân bánh |
| L4 | Che biển số, đèn | Hàng buộc phía sau thấp | 300–400k (Đ36.1.b) | Không tìm thấy biển số/đèn hậu |
| L5 | Hàng vượt trước/sau không có báo hiệu đỏ | Mọi hàng lòi khỏi thân xe | 400–600k (Đ36.2.d) | Nhắc luôn; thử nhận diện cờ đỏ |
| L6 | Chằng buộc không chắc | Mọi loại | 300–400k (Đ36.1.a) | Checklist + hướng dẫn theo loại hàng |
| L7 | Người ngồi sau ôm/vác hàng | Tấm kính, thùng, cây dài | Lái 600–800k (Đ7.3.e); người ngồi sau 400–600k (Đ12.5.a) | Nhận diện người + hàng |
| L8 | Kéo theo xe/vật | Xe máy kéo ba gác, kéo xe hỏng | 600–800k (Đ7.3.g) | Nhận diện / hỏi |
| L9 | Xe lắp ráp trái quy định | Ba gác gắn máy, xe ba bánh tự chế | Tịch thu (Đ14.4) | Nhận dáng + hỏi đăng ký |
| L10 | Hàng rời, VLXD rơi vãi | Cát, xi măng vỡ bao, gạch | 400–600k (Đ36.2.c) | Nhận loại hàng → nhắc phủ/đóng bao |
| L11 | Vượt khối lượng cho phép | Xi măng, gạch, sắt | 400–600k (Đ36.2.a) | Danh mục/cân; không ước từ ảnh |

Việc đầu tiên ở thực địa: đếm tần suất L1–L11 tại 1–2 điểm để biết lỗi nào phổ biến nhất, rồi ưu tiên demo theo đó.

## 4. Kiến trúc

```
Điện thoại (PWA, chạy trên trình duyệt)
 ├─ Camera + hướng dẫn góc chụp (sau / hông)
 ├─ On-device: OpenCV.js (thẻ ArUco), bộ phát hiện biển số (YOLO nhỏ, ONNX Runtime Web),
 │             SAM 2 tiny / SlimSAM (chạm để khoanh hàng)
 ├─ Rule engine (JSON: luật theo loại xe, ngưỡng, mức phạt, điều khoản)
 └─ Bảng xe & dịch vụ (JSON: Lalamove/Ahamove/Grab, theo thành phố, ngày đọc)
Máy chủ nhỏ
 ├─ Nhận diện loại hàng + dáng xe (VLM qua API, hoặc bộ phân loại tự huấn luyện sau)
 ├─ Mô hình độ sâu (MoGe-2 / Depth Pro) để kiểm chéo — tùy chọn
 └─ Lưu thống kê ẩn danh (không lưu ảnh gốc; làm mờ mặt, biển số)
```

Kết quả mỗi lần chụp: loại xe, loại hàng, ước tính kích cỡ có khoảng sai số, đèn cho từng luật (L1–L11), mức phạt có thể gặp, cách sửa, xe thay thế + giá + deep link.

## 5. Lịch 25 ngày

| Tuần | Việc | Đầu ra |
|---|---|---|
| 1 (21–27/11) | Lõi: rule engine L1–L11, bảng xe, UI hai chế độ, nhập kích thước tay. Song song: đi 1–2 cửa hàng VLXD, chụp 30–50 xe + đo thước, đếm lỗi | App chạy với nhập tay; bộ ảnh có kết quả đo chuẩn |
| 2 (28/11–4/12) | Đo từ ảnh: thẻ ArUco, biển số làm thước, chạm-khoanh hàng; nhận diện loại hàng/dáng xe; khoảng sai số → đèn | Đo được trên bộ ảnh tuần 1 |
| 3 (5–11/12) | Chạy đánh giá trên ảnh chưa dùng để chỉnh: sai số cm, % xếp đúng, % vàng, số ca xanh sai. Gợi ý dịch vụ + deep link. Thử với chủ cửa hàng và người chở | Bảng kết quả cho mục 6 hồ sơ |
| 4 (12–14/12) | Quay video ≤5 phút (<25 MB), sửa bản mô tả, nộp | Hồ sơ hoàn chỉnh |

Cắt giảm nếu chậm: bỏ mô hình độ sâu và nhận diện cờ đỏ; giữ thẻ + biển số + nhập tay.

## 6. Rủi ro

- Biển số làm thước không đủ chính xác → giữ chế độ thẻ làm kết luận chính.
- Xe máy mỗi mẫu có giá đèo hàng khác nhau → bắt đầu với 5–10 mẫu phổ biến.
- Định nghĩa "vật cồng kềnh" không có số → L7 chỉ cảnh báo, không chấm đỏ theo số.
- License mô hình (SAM 3, một số mô hình độ sâu phi thương mại) → kiểm trước khi dùng.
- Không có số liệu tần suất lỗi trước thực địa → không ghi tỷ lệ % vào hồ sơ khi chưa đo.
