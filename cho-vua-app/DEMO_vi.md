# Kịch bản demo CHỞ VỪA (video ≤5 phút, dưới 25 MB)

Quay tại cửa hàng vật liệu xây dựng thí điểm. Cần chuẩn bị:
- in [thẻ chuẩn](public/the-chuan-aruco.svg) ở tỷ lệ 100%, rồi dùng thước kiểm viền đen đúng 15 cm;
- một thước dây;
- chạy `npm run server` nếu muốn quay cảnh nhận diện bằng ảnh.

Cột "Đã kiểm" ghi tình trạng ngày 20/11/2026: ✅ = đã có test tự động khớp kết quả mong đợi; ⏳ = phải thử trên điện thoại thật với ảnh thật.

| # | Cảnh | Thao tác | Kết quả mong đợi | Đã kiểm |
|---|---|---|---|---|
| 1 | Ống nhựa 4 m lúc bán, khách định chở bằng xe máy | Lúc bán → Xe máy → Ống nhựa → nhập dài 400 cm → Xem kết quả | 🔴 E02, lòi phía sau khoảng 3,2–3,7 m. Xe gợi ý đầu tiên: **Xe tải 2500kg** (thùng 400 cm của Tải 2000kg quá sát với ống 4 m cộng sai số). Bấm **Mở Lalamove** | ✅ test + đã đi luồng trong trình duyệt |
| 2 | Thùng carton nhỏ đã chất trên xe máy, chụp từ phía sau | (a) Dán thẻ chuẩn → Chụp ảnh phía sau → app tự tìm thẻ → chạm 6 điểm. (b) Không có thẻ: chạm 4 góc biển số | (a) 🟢 E01–E03, nhắc chằng buộc. (b) 🟡 "đo bằng góc chạm tay, chưa hiệu chỉnh"; nhập số đo thước thì mới ra 🟢 | ⏳ cần ảnh thật |
| 3 | Tủ lạnh dựng đứng trên xe máy | Lúc bán → Xe máy → Tủ lạnh → nhập cao 160 cm | 🔴 E03 (cao 2,29–2,51 m). Chưa nhập chiều cao thì chỉ ra 🟡 | ✅ test |
| 4 | Hàng che biển số | Kiểm nhanh: "Biển số và đèn có nhìn thấy rõ không?" → Không | 🔴 E04, phạt 300.000–400.000đ | ✅ test |
| 5 | Xe ba bánh gắn máy không có đăng ký | Xe ba, bốn bánh có gắn máy → Kiểm nhanh: "Xe có đăng ký và biển số không?" → Không | 🔴 E09, tịch thu phương tiện; vẫn gợi ý xe thay thế | ✅ test |

Cảnh phụ nếu còn thời gian:
- chụp ảnh món hàng để nhận diện loại hàng (cần server);
- bấm **Phiếu kết quả** để hiện mã QR;
- mở **Thực địa** → nhập số đo thước → Xuất CSV.

## Ghi lại sau khi chạy trên điện thoại thật

Ghi vào đây cảnh nào lệch so với kết quả mong đợi, và lý do.

- (chưa chạy trên điện thoại)
