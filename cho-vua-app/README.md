# CHỞ VỪA — bản demo

Web app chạy trên điện thoại. Người dùng chọn loại xe và loại hàng, nhập hoặc đo kích thước từ ảnh. App trả về 4 phần: loại hàng, kích cỡ ước tính có khoảng sai số, 11 lỗi theo Luật 36/2024 kèm đèn xanh/vàng/đỏ, và xe phù hợp kèm giá.

Thiết kế: [tài liệu ý tưởng](../traffic-data-research/reports/track2_2026_11_20/CHO_VUA_y_tuong_vi.md) · [luật và mức phạt](../traffic-data-research/reports/track2_2026_11_20/luat_cho_hang_vi.md) · [đo từ ảnh](../traffic-data-research/reports/track2_2026_11_20/cv_do_kich_thuoc_vi.md) · [kế hoạch build](../docs/superpowers/plans/2026-11-20-cho-vua-demo.md)

## Chạy

```bash
npm install
npm test
npm run dev -- --host
```

Mở `http://<IP máy tính>:5173` trên điện thoại dùng cùng Wi-Fi. Nút chụp ảnh dùng `<input capture>`, mở được camera mà không cần HTTPS.

**Nhận diện loại hàng** cần server riêng, giữ khóa API ở phía máy tính:

```bash
npm run server
```

Server đọc thông tin đăng nhập Anthropic từ môi trường: `ANTHROPIC_API_KEY`, hoặc profile tạo bằng `ant auth login`. Thiếu thông tin đăng nhập thì server trả 503, và app chuyển sang chọn loại hàng bằng tay. Mỗi lần nhận diện là một lần gọi API có tính phí. Ảnh chỉ được gửi đi để nhận diện; server không lưu và không ghi log ảnh.

Đánh giá sai số từ CSV của chế độ thực địa:

```bash
python -X utf8 ../traffic-data-research/src/cho_vua_eval.py chovua_checks.csv --out ../traffic-data-research/reports/track2_2026_11_20/eval_<ngày>
```

## Giới hạn của bản demo

- **Số liệu giả định, có nhãn "giả định" trên giao diện:**
  - danh mục 10 loại hàng mẫu (`src/data/items.json`);
  - giá chở hàng xe máy: rộng 30–50 cm, dài 30–50 cm, cao 70–90 cm (`src/rules/predict.ts`).
  Cần thay bằng danh mục của cửa hàng thí điểm và số đo giá chở hàng ở thực địa.
- **Khi nào được ra đèn xanh:** E01–E03 chỉ ra 🟢 khi số đo đến từ thước hoặc từ thẻ chuẩn mà app tự tìm thấy. Nếu số đo đến từ góc chạm tay (biển số, hoặc thẻ không được nhận ra) hoặc từ kích thước điển hình kèm giá chở hàng giả định, đèn xanh bị hạ xuống 🟡 và có ghi lý do. Số đo bằng thước được ưu tiên hơn số đo ảnh cho từng kích thước.
- **Hằng số sai số khi đo ảnh** (`TAP_ERR_PX`, `OFF_PLANE_REL` trong `src/measure/measure.ts`) là tạm thời. Phải hiệu chỉnh trên ảnh thực địa bằng script đánh giá, với mẫu tách theo xe hoặc theo ngày.
- **Bảng xe** (`src/data/vehicles.json`) lấy từ trang công bố ngày 20/11/2026.
  - Lalamove chưa có công thức giá; chỉ xe van 500 kg của Ahamove có giá ước tính.
  - Bảng Hà Nội và trang Ba gác của Grab (năm 2022) cần kiểm lại.
- **Chưa có dự đoán trước** cho xe thô sơ và xe ba, bốn bánh. Hai loại này phải nhập số đo hoặc chụp ảnh.
- **Chưa làm:** quy định riêng theo tỉnh, tự phát hiện biển số (bản demo yêu cầu chạm 4 góc), và gọi API đặt xe thật (bản demo chỉ mở trang hoặc app của nền tảng).
- **Thư viện ArUco** (`src/vendor/js-aruco2`, giấy phép MIT) được chép vào repo dưới dạng ES module, vì gói npm không chạy được trong bundle của trình duyệt.

Phiếu kết quả ghi: *"Kết quả kiểm tra kích thước và cách xếp hàng, không thay thế việc kiểm tra, xử lý của cơ quan chức năng."*
