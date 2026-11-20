# Test case nhập tay — CHỞ VỪA

16 trường hợp để bấm thử trên app bằng số liệu nhập tay, không cần ảnh. Cả 16 trường hợp cũng chạy tự động trong `tests/manualCases.test.ts` (`npm test`), nên kết quả mong đợi dưới đây đã được kiểm.

## Cách nhập

| Bước trên app | Nhập gì |
|---|---|
| 1. Tình huống | **Lúc bán — chưa chất hàng** hoặc **Xe đã chất hàng**; loại xe; khu vực (mặc định TP.HCM, 5 km) |
| 2. Loại hàng | Bấm chọn loại hàng; Số lượng (mặc định 1) |
| 3. Kích thước → **Nhập tay** | **Dài / Rộng / Cao**: kích thước cả lô hàng. Khi chọn "Xe đã chất hàng" thì có thêm **Lòi bên trái / phải / sau** (xe thô sơ có thêm **trước**) và **Cao từ mặt đường** |
| 4. Kiểm nhanh | Các câu Có / Không / Không rõ; chiều dài thân xe (chỉ xe thô sơ); khối lượng hàng; tải cho phép của xe |

**Câu trả lời mặc định của bộ test.** App mở ra với mọi câu ở "Không rõ". Khi một trường hợp không ghi gì khác, hãy chọn:
- Biển số và đèn có nhìn thấy rõ không? → **Có**
- Hàng lòi trước/sau đã gắn báo hiệu đỏ chưa? → **Có**
- Hàng đã chằng buộc chắc chắn chưa? → **Có**
- Người lái hoặc người ngồi sau có ôm, vác hàng không? → **Không**
- Xe có kéo theo xe hoặc vật khác không? → **Không**
- Hàng rời đã đóng bao hoặc che phủ chưa? (chỉ hiện với bao xi măng) → **Có**
- Xe có đăng ký và biển số không? (chỉ hiện với xe ba, bốn bánh) → **Có**

**Mỗi số cm nhập tay được hiểu là ±1 cm**, vì thước đo cũng có sai số. Vì vậy nhập đúng bằng ngưỡng sẽ ra 🟡 (xem TC06a).

## Các trường hợp

Ký hiệu: 🟢 xanh, 🟡 vàng, 🔴 đỏ, "–" là lỗi không áp dụng nên không hiện. Cột "Đèn cần thấy" chỉ ghi những lỗi đáng chú ý; các lỗi khác có thể xanh.

| # | Tình huống | Nhập | Đèn cần thấy | Kết quả chung | Xe gợi ý |
|---|---|---|---|---|---|
| TC01 | Ống nhựa 4 m lúc bán, xe máy, TP.HCM | Lúc bán · Xe máy · Ống nhựa · Dài **400** | E02 🔴 (lòi sau khoảng 3,2–3,7 m) · E01 🟢 · E03 🟢 · E05 🟢 · E11 🟡 (chưa có khối lượng) | 🔴 Không đạt | Đầu tiên: **Xe tải 2500kg** |
| TC02 | Như TC01 nhưng ở Hà Nội | Như TC01, Khu vực **Hà Nội** | E02 🔴 | 🔴 | "Không có xe phù hợp trong bảng cho HN" |
| TC03 | Thùng carton đã đo, lúc bán, xe máy | Lúc bán · Xe máy · Thùng carton · Dài **40** Rộng **30** Cao **30** · Khối lượng **10** · Tải xe **150** | E01–E03 🟢 · E05 🟢 · E11 🟢 | 🟢 Đạt | Có **Xe máy** trong danh sách |
| TC04 | Tủ lạnh dựng đứng, lúc bán, xe máy | Lúc bán · Xe máy · Tủ lạnh · Cao **160** | E03 🔴 (cao khoảng 2,29–2,51 m) | 🔴 | Đầu tiên: **Xe tải 1500kg** |
| TC05 | Xe máy đã chất, mọi số đo ổn | Xe đã chất · Xe máy · Thùng carton · Lòi trái **20** phải **20** sau **30** · Cao từ mặt đường **150** · Khối lượng **20** · Tải xe **150** | E01–E08 🟢 · E11 🟢 | 🟢 Đạt | – |
| TC06a | Lòi sau đúng 50 cm | Như TC05, Lòi sau **50** | E02 🟡 (49–51 cm, sát ngưỡng 50) | 🟡 Cần kiểm thêm | – |
| TC06b | Lòi sau 49 cm | Như TC05, Lòi sau **49** | E02 🟢 (48–50 cm) | 🟢 | – |
| TC07 | Lòi bên trái quá 30 cm | Như TC05, Lòi trái **35** | E01 🔴 | 🔴 | – |
| TC08 | Hàng cao quá 2 m | Như TC05, Cao từ mặt đường **205** | E03 🔴 | 🔴 | – |
| TC09 | Xe thô sơ chở cửa gỗ | Xe đã chất · **Xe thô sơ** · Cửa gỗ · Lòi trái **35** phải **35** sau **70** trước **10** · Chiều dài thân xe **180** · Khối lượng **30** · Tải xe **100** | E01 🟢 (giới hạn 40 cm mỗi bên bánh) · E02 🔴 (giới hạn 180/3 = 60 cm) · E03 – (xe thô sơ không có giới hạn cao) | 🔴 | – |
| TC10 | Xe thô sơ, chưa nhập thân xe | Như TC09 nhưng Lòi trái **10** phải **10** sau **30**, **bỏ trống** chiều dài thân xe | E02 🟡 (chưa kiểm được quy tắc 1/3 thân xe) | 🟡 | – |
| TC11 | Xe ba bánh gắn máy không đăng ký | Xe đã chất · **Xe ba, bốn bánh có gắn máy** · Thùng carton · số đo như TC05 · "Xe có đăng ký và biển số không?" → **Không** | E09 🔴 (tịch thu phương tiện) · E01 🟢 | 🔴 | Vẫn có gợi ý xe thay thế |
| TC12 | 4 bao xi măng, chưa đo, chưa che | Lúc bán · Xe máy · Bao xi măng · Số lượng **4** · "Hàng rời đã đóng bao hoặc che phủ chưa?" → **Không** · Tải xe **150** · không nhập kích thước, không nhập khối lượng | E10 🔴 · E11 🔴 (4 × 50 = 200 kg > 150) · E01–E03 🟡 (chưa đo, kích thước giả định) | 🔴 | – |
| TC13 | Che biển số, người ngồi sau ôm hàng | Như TC05 · Biển số rõ → **Không** · Ôm, vác hàng → **Có** | E04 🔴 · E07 🟡 (luật không định nghĩa "cồng kềnh" bằng số nên chỉ cảnh báo) | 🔴 | – |
| TC14 | Xe máy kéo theo xe đẩy | Như TC05 · Kéo theo xe → **Có** | E08 🔴 | 🔴 | – |
| TC15 | Số đo ổn, bỏ trống phần Kiểm nhanh | Như TC05 nhưng các câu **Không rõ** và **không** nhập khối lượng, tải xe | E04–E08 🟡 · E11 🟡 | 🟡 | – |

## Những điểm nên để ý khi thử

- **TC06a và TC06b:** nhập đúng bằng ngưỡng (50 cm) vẫn ra vàng, vì số đo có thể là 51 cm. Đây là cách app tránh báo xanh sai.
- **TC12:** chưa đo kích thước thì app không bao giờ cho E01–E03 xanh, vì nó chỉ dựa trên kích thước điển hình và giá chở hàng giả định.
- **TC01:** app gợi ý xe tải 2500 kg chứ không phải 2000 kg, vì thùng xe 2000 kg dài đúng 400 cm, quá sát với ống 4 m cộng sai số.
- **TC03 — lỗi nhỏ đã biết:** xe bán tải có thể đứng đầu danh sách gợi ý dù hàng rất nhỏ, vì Lalamove không công bố tải trọng của xe bán tải.
- **Lòi trái/phải/sau chỉ hiện khi đã chọn "Xe đã chất hàng"** ở bước 1.

## Ghi kết quả thử

| # | Ngày | Thiết bị | Đúng như bảng? | Ghi chú |
|---|---|---|---|---|
| TC01 | | | | |
