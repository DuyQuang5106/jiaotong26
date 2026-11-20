# CHỞ VỪA — tài liệu ý tưởng hợp nhất (track 2)

**Phiên bản:** 20/11/2026. Hạn nộp: trước 15/12/2026.
**Trạng thái:** ý tưởng đã có thiết kế, căn cứ pháp lý và rà soát công nghệ. **Chưa có dữ liệu thực địa, chưa có prototype, chưa đo độ chính xác.**

Tài liệu này hợp nhất ý tưởng T2-A trong [báo cáo track 2 ngày 19/11](../track2_2026_11_19/README.md) với các đề xuất của trưởng nhóm trong buổi làm việc 20/11. Mục 10 ghi nguồn gốc từng ý và các hướng đã cân nhắc nhưng không theo. Khi tài liệu này khác với README 19/11, **tài liệu này là bản mới hơn**. Các giới hạn bằng chứng của README 19/11 vẫn giữ nguyên.

---

## 1. Một câu

> **Chụp ảnh món hàng (hoặc xe đã chất hàng) → CHỞ VỪA cho biết đó là hàng gì, cỡ khoảng bao nhiêu, vướng luật nào, và nên chở bằng xe gì, giá bao nhiêu, ngay tại cửa hàng, trước khi xe lăn bánh.**

Câu kể cho giám khảo: *"Chặn chuyến chở sai luật ngay tại nguồn, và lo luôn phương án chở đúng."*

## 2. Vấn đề

- Xe máy, xe ba gác, xe thô sơ và xe tự chế chở hàng cồng kềnh vẫn phổ biến ở các tuyến phố bán vật liệu xây dựng, nội thất, điện máy.
- Hà Nội xử lý 242 trường hợp chở hàng cồng kềnh chỉ trong 15/7–1/8/2026 (VTV). Đây là số bị phát hiện, không phải tổng số vi phạm.
- Đã có tai nạn do hàng lòi ra ngoài xe, ví dụ 9/6/2026 trên đường Nguyễn Trãi (Dân trí). Đây là ca đơn lẻ, không phải tỷ lệ.
- Biện pháp hiện nay (tuần tra, phạt, tịch thu) đều tác động **sau khi xe đã ra đường**. Còn quyết định chở bằng xe gì và xếp hàng thế nào lại diễn ra **trước đó, tại nơi bán hàng**.
- Người chở thường không biết luật cụ thể: hàng được lòi bao nhiêu, phải gắn gì, xe nào là hợp lệ.

## 3. Định vị: chốt tuân thủ tại nguồn, dịch vụ đi kèm

CHỞ VỪA là **công cụ giúp chuyến hàng tuân thủ luật ngay từ nguồn**. Dịch vụ gọi xe thay thế là phần đi kèm, để làm đúng luật cũng là cách thuận tiện nhất.

Thể lệ Chủ đề 2 yêu cầu giải pháp *"giám sát và ngăn chặn xe máy, phương tiện thô sơ, xe tự chế chở hàng cồng kềnh"*, đồng thời mang lại phương án vận chuyển phù hợp, an toàn, thuận tiện hơn. CHỞ VỪA đáp ứng ba phần:

| Thể lệ | CHỞ VỪA |
|---|---|
| Ngăn chặn | Kiểm tra và cảnh báo trước khi xe rời cửa hàng |
| Giám sát | Dữ liệu tổng hợp ẩn danh: mặt hàng, tuyến phố, khung giờ hay vượt. Cơ quan chức năng dùng để chọn nơi tuyên truyền, tuần tra |
| Phương án thuận tiện | Gợi ý loại xe phù hợp kèm giá, mở thẳng app vận chuyển |

**Giới hạn của định vị:** app **không có quyền xử phạt**. Không dùng chữ "thực thi luật" trong hồ sơ; dùng "chốt kiểm tra tuân thủ tại nguồn". Muốn có sức ràng buộc thì đi qua những đơn vị có quyền đặt quy định: ban quản lý chợ hoặc tuyến phố đưa vào quy chế, phường cấp nhãn "cửa hàng giao hàng đúng luật", hoặc nền tảng vận tải yêu cầu đơn đi qua bước kiểm tra.

**Vì sao vẫn cần dịch vụ:** nếu app chỉ báo "không đạt", cửa hàng sợ mất khách, người chở mất cuốc, khách phải trả thêm, và sẽ không ai dùng app. Dịch vụ thay thế là lý do người ta chịu mở app.

## 4. Hành trình: bắt đầu từ lúc định chở, không phải sau khi đã gọi xe

App vào cuộc **từ lúc khách mua hàng hoặc lúc định chở hàng**, không đợi xe tới rồi mới kiểm.

1. Khách chốt mua, ví dụ 10 cây ống nhựa dài 4 m tại một cửa hàng vật liệu xây dựng.
2. Nhân viên hoặc khách chụp ảnh món hàng. Nếu hàng có trong danh mục cửa hàng thì chọn mã hàng.
3. CHỞ VỪA trả kết quả (mục 5). Nếu đèn đỏ, app đề xuất cách chở đúng luật kèm giá.
4. Khách chọn phương án. App mở app vận chuyển với loại xe đã chọn, hoặc gợi ý xếp lại hay chia kiện.
5. Nếu vẫn chở bằng xe máy hoặc ba gác: chụp xe đã chất hàng để kiểm lại, nhận phiếu kết quả và lời nhắc (cờ đỏ, chằng buộc).

Lợi ích cho từng bên:
- **Khách và người chở:** tránh bị phạt 300–800 nghìn hoặc bị tịch thu xe, biết ngay phương án và giá.
- **Cửa hàng:** ít đơn bị từ chối hay hàng hỏng dọc đường, có thể thu thêm từ dịch vụ giao hàng.
- **Nền tảng vận chuyển:** nhận thêm đơn xe van, xe tải đúng loại.

Ai trả tiền là **giả thuyết, phải phỏng vấn mới biết**: hoa hồng giới thiệu từ nền tảng, phí thuê bao của chuỗi cửa hàng, hoặc tài trợ của địa phương.

## 5. Kết quả của mỗi lần chụp

**Lần chụp nào app cũng nhận diện loại hàng và cố gắng đo.** App không đợi đo chính xác mới trả lời, và không bỏ bước đo. Mỗi lần chụp trả về bốn phần:

| Phần | Ví dụ (bó ống nhựa, định chở bằng xe máy) |
|---|---|
| **1. Loại hàng** | "Bó ống nhựa", độ tin cậy cao |
| **2. Ước tính kích cỡ, có khoảng sai số** | "Dài khoảng 3,8–4,2 m", ghi rõ đo bằng gì (thẻ / biển số / mẫu xe / mô hình độ sâu / kích thước chuẩn của loại hàng) |
| **3. Luật áp dụng, mỗi giới hạn một đèn** | "Lòi phía sau hơn 3 m, luật cho tối đa 0,5 m → 🔴. Hàng vượt phía sau phải gắn báo hiệu đỏ." |
| **4. Dịch vụ phù hợp** | Loại xe chở vừa ngay cả với **số lớn nhất** trong khoảng ước tính, kèm giá công bố và nút mở app nền tảng |

**Đèn xanh / vàng / đỏ gắn với khoảng sai số:**

| Đèn | Khi nào | App làm gì |
|---|---|---|
| 🟢 | Cộng cả sai số vào vẫn dưới ngưỡng | Cho đi, nhắc chằng buộc và báo hiệu |
| 🔴 | Trừ cả sai số đi vẫn trên ngưỡng | Không đạt; gợi ý xếp lại hoặc gọi xe phù hợp kèm giá |
| 🟡 | Ngưỡng nằm trong khoảng sai số, hoặc ảnh thiếu mốc / bị che / mờ | **Vẫn trả lời đầy đủ** cho cả hai khả năng ("nếu ≤0,5 m thì xe máy được; nếu hơn thì van 500 kg khoảng X đ"); mặc định gợi ý phương án an toàn; có nút **"Đo kỹ hơn"** (thêm góc chụp, đặt thẻ, dùng thước) để thu hẹp khoảng sai số |

- Xe tự chế, không có đăng ký thì luôn 🔴.
- **Khối lượng không ước từ ảnh.** App chỉ đưa con số ước theo loại hàng, ghi rõ là ước, và dùng số từ danh mục hoặc cân nếu có.
- Người dùng luôn thấy **mình đang kiểm theo luật nào** trước khi được mời đo kỹ. Đây là cách giảm thao tác chính.

**Phiếu kết quả:** in ra hoặc gửi mã QR cho người chở, ghi kết quả kiểm tra và thời điểm.
- Phiếu **không** phải chứng nhận an toàn, và **không** phải bằng chứng pháp lý cho cửa hàng, vì người bị phạt là người lái.
- Phiếu giúp người chở biết trước nguy cơ bị phạt, và giúp cửa hàng áp dụng chính sách "chỉ giao khi đạt".

**Thống kê:** số đơn đã kiểm, tỷ lệ phải xếp lại hoặc đổi xe, mặt hàng hay vượt. Dữ liệu được tổng hợp ẩn danh. Không lưu ảnh gốc có mặt người hoặc biển số.

## 6. Bộ luật app kiểm

Chi tiết và trích dẫn ở [luat_cho_hang_vi.md](luat_cho_hang_vi.md). Nghị định 238/2026 không sửa các mức phạt dưới đây.

### 11 lỗi hay gặp

1. Hàng lòi hai bên quá 0,3 m mỗi bên giá chở hàng (xe máy) hoặc quá 0,4 m mỗi bên bánh (xe thô sơ).
2. Hàng lòi phía sau quá 0,5 m so với giá chở hàng (xe máy), hoặc quá 1/3 thân xe hay quá 1 m phía trước/sau (xe thô sơ).
3. Hàng chất cao quá 2 m tính từ mặt đường. Chỉ áp dụng cho xe máy; luật không đặt giới hạn chiều cao cho xe thô sơ.
4. Hàng che biển số hoặc đèn.
5. Hàng lòi trước hoặc sau mà không gắn báo hiệu đỏ (ban đêm phải có đèn).
6. Chằng buộc không chắc.
7. Người ngồi sau ôm hoặc vác hàng (và người lái mang vác vật cồng kềnh).
8. Xe kéo theo xe hoặc vật khác.
9. Dùng xe sản xuất, lắp ráp trái quy định ("xe tự chế").
10. Hàng rời, vật liệu xây dựng rơi vãi.
11. Chở vượt khối lượng cho phép của xe.

**Mức phạt:**
- Người lái xe máy: 300–800 nghìn đồng tùy lỗi.
- Người lái xe thô sơ: 150–600 nghìn đồng (mang vác hoặc kéo theo là 150–250 nghìn).
- Xe sản xuất, lắp ráp trái quy định: bị tịch thu.
- Các lỗi của xe máy mà gây tai nạn: 10–14 triệu đồng và trừ 10 điểm.

Danh sách này lập theo các điều luật. **Chưa biết lỗi nào phổ biến hơn lỗi nào**, nên việc đầu tiên khi ra thực địa là đếm số lần gặp từng lỗi (mục 11). Lỗi nào hay gặp nhất thì làm kỹ trước trong prototype.

### Bảng chi tiết

| Mức | Quy định | Phạt (người lái) | App kiểm bằng |
|---|---|---|---|
| **Lõi** | Xe máy: ≤0,3 m mỗi bên giá đèo hàng, ≤0,5 m sau giá, cao ≤2 m (Luật 36, Điều 33 khoản 5) | 400–600k, vượt khổ (Nghị định 168, Điều 36 khoản 2 điểm b) | Ước tính kích cỡ + đèn |
| **Lõi** | Xe thô sơ: ≤1/3 thân xe và ≤1 m trước/sau, ≤0,4 m mỗi bên bánh (Điều 31 khoản 5) | 400–600k (Điều 36 khoản 2 điểm b) | Ước tính kích cỡ + đèn |
| **Lõi** | Không che đèn, biển số (Điều 47 khoản 1 điểm d) | 300–400k (Điều 36 khoản 1 điểm b) | Ảnh chụp phía sau: không thấy biển số hoặc đèn hậu thì cảnh báo |
| **Lõi** | Hàng vượt trước/sau phải có báo hiệu đỏ, ban đêm có đèn (Điều 47 khoản 1 điểm e) | 400–600k (Điều 36 khoản 2 điểm d) | Luôn nhắc khi hàng lòi khỏi thân xe |
| **Lõi** | Xe sản xuất, lắp ráp trái quy định (Điều 9 khoản 8) | Tịch thu xe (Điều 14 khoản 4) | Nhận diện dáng xe, rồi hỏi đăng ký và biển số. Không tự kết luận chỉ từ ảnh, vì xe bốn bánh chở hàng có đăng ký vẫn hợp lệ (Điều 48) |
| Phụ | Mang vác vật cồng kềnh (Điều 33 khoản 3 điểm đ, khoản 4) | 600–800k người lái (Điều 7 khoản 3 điểm e); 400–600k người ngồi sau | Nhận diện người ôm hoặc vác hàng. Luật không định nghĩa "cồng kềnh" bằng số |
| Checklist | Chằng buộc chắc chắn; hàng rời không rơi vãi; khối lượng cho phép | 300–600k | Hướng dẫn theo loại hàng, người dùng xác nhận |
| Địa phương | Kinh doanh vận chuyển bằng xe máy, xe thô sơ; giờ và khu vực cho xe bốn bánh chở hàng (Điều 47 khoản 2, Điều 48 khoản 2) | Theo tỉnh | Bộ quy định theo tỉnh, **chưa lập** |

Khi gợi ý xe tải thay thế, app chỉ chọn xe mà **hàng nằm gọn trong thùng**, vì Điều 49 có yêu cầu riêng cho ô tô.

### Luật có đủ rõ để phạt không?

**Phần lớn đủ rõ, và CSGT đang phạt nhiều.** Các giới hạn 0,3 m, 0,5 m, 2 m, 0,4 m, 1 m và 1/3 thân xe đều ghi bằng số trong luật, mức phạt cũng cụ thể. Một số số liệu báo chí:

- **Hà Nội, 15/7–1/8/2026:** xử lý 242 trường hợp chở hàng cồng kềnh, trong tổng 472 trường hợp thuộc các nhóm được báo cáo. Cùng nguồn có 86 trường hợp dùng xe tự sản xuất, lắp ráp và 135 trường hợp kéo theo xe hoặc vật khác ([VTV, 04/8/2026](https://vtv.vn/csgt-ha-noi-xu-ly-gan-500-xe-tu-che-cho-hang-cong-kenh-100260803224303027.htm)).
- **Hà Nội, tuần 17–23/9/2026:** thêm 78 trường hợp chở hàng cồng kềnh ([Cổng TTĐT Thăng Long, 28/9/2026](https://thanglong.chinhphu.vn/ha-noi-xu-ly-hon-8400-truong-hop-vi-pham-giao-thong-trong-1-tuan-103260928173812008.htm)).
- **TP.HCM:** riêng Đội CSGT Hàng Xanh đã lập hồ sơ tịch thu 176 xe ba bánh tự chế từ đầu năm 2026 ([Thanh Niên, 22/4/2026](https://thanhnien.vn/may-chem-di-dong-tu-xe-ba-gac-cho-hang-cong-kenh-khien-nguoi-tphcm-lo-so-185260420223334375.htm)).

Con số 242/472 đã được đối chiếu trong [báo cáo bổ sung](../../../data/track2_enrichment_2026_summary.md). Các số 86, 135, 78 và 176 lấy từ bản mô tả nháp, **chưa mở lại nguồn để kiểm**. Đây đều là số trường hợp bị phát hiện và xử lý trong từng đợt, không phải tổng số vi phạm, và không được cộng các đợt với nhau.

**Chỉ có hai chỗ thật sự mơ hồ:**
- **"Vật cồng kềnh" không có định nghĩa bằng số.** CSGT đánh giá tại chỗ, nên hai người có thể hiểu khác nhau. Chưa tìm thấy tài liệu nào mô tả cách CSGT áp dụng tiêu chí này. Vì vậy app chỉ **cảnh báo** lỗi này, không ra kết luận chắc chắn.
- **Chủ hàng và cửa hàng không bị phạt.** Luật có đủ căn cứ để phạt người lái, nhưng không có điều khoản nào cho bên giao hàng.

**Khoảng trống CHỞ VỪA lấp vào:** xử phạt phụ thuộc tuần tra và thường diễn ra theo từng đợt cao điểm, nên nhiều khả năng rất nhiều chuyến sai luật không bị phát hiện. Đây là **nhận định chưa đo**: chưa có số liệu về tỷ lệ bị phát hiện. CHỞ VỪA kiểm tra ngay từ đầu, trước khi xe ra đường, nên không phụ thuộc vào việc có CSGT ở đó hay không.

## 7. Công nghệ

Chi tiết ở [cv_do_kich_thuoc_vi.md](cv_do_kich_thuoc_vi.md).

- **Nhận diện loại hàng:** mô hình đọc ảnh (VLM) hoặc bộ phân loại nhỏ. Chưa chắc thì cho người dùng chọn 1 trong 3 gợi ý.
- **Ước tính kích cỡ:** ghép nhiều nguồn tỷ lệ.
  - **Thẻ ArUco** đặt trên giá chở hàng: chính xác nhất.
  - **Biển số xe máy 190 × 140 mm** (QCVN 08:2024/BCA): "thước" có sẵn trên mọi xe, nằm ngay ở ảnh chụp phía sau.
  - **Kích thước biết trước của mẫu xe:** dùng cho ảnh chụp bên hông.
  - **Kích thước chuẩn của loại hàng** (ví dụ ống bán theo cây dài cố định): làm tròn số đo về kích thước chuẩn gần nhất.
  - **Mô hình ước độ sâu từ một ảnh** (MoGe-2, Depth Pro, UniDepthV2): chỉ để kiểm chéo, bắt lỗi lớn.
- **Khoanh vùng hàng:** SAM 2 chạy trên trình duyệt. Người dùng chạm vào hàng một lần.
- **Không dùng VLM để đo cm.** Các benchmark 2025–2026 cho thấy VLM yếu ở việc này.
- **Nền tảng:** web app chạy trên điện thoại. Phần nặng (ước độ sâu) chạy trên máy chủ.
- **Dựng app bằng agent:** phần mềm làm được nhanh. **Bằng chứng thì không**: vẫn phải đo xe thật tại cửa hàng.

## 8. Dịch vụ thay thế: lớp gợi ý trên các nền tảng có sẵn

CHỞ VỪA **không làm sàn vận chuyển riêng**. App chọn đúng loại xe rồi chuyển khách sang Lalamove, Ahamove hoặc Grab, tức là hợp tác chứ không cạnh tranh.

Ví dụ bó ống 4 m tại TP.HCM, theo bảng Lalamove đọc ngày 20/11/2026:

| Loại xe | Dài tối đa | Chở ống 4 m? |
|---|---|---|
| Xe máy / xe máy có baga | 50 / 60 cm | ❌ |
| Ba gác GrabExpress | 1,7 m (trang năm 2022) | ❌ |
| Van 500 kg | 170 cm | ❌ |
| Tải 1.000 kg | 300 cm | ❌ |
| Tải 2.000 kg | 400 cm | ✅ vừa sát |

Tại Hà Nội, bảng ghi tải 2.000 kg dài 350 cm. Lalamove hiện để người dùng **tự chọn xe** theo kích thước hàng.

## 9. Khác gì những thứ đã có

| Đã có | Làm gì | CHỞ VỪA khác ở đâu |
|---|---|---|
| CSGT tuần tra, xử phạt | Bắt khi xe đã ra đường | Kiểm tại nguồn, trước khi xe lăn bánh; bổ trợ chứ không thay thế |
| Lalamove, Ahamove, Grab | Công bố giới hạn từng loại xe; người dùng tự chọn; có plugin báo giá lúc thanh toán | Tự gợi ý xe từ ảnh; bao cả **chuyến khách tự gọi xe ôm hoặc tự chở**, là những chuyến nền tảng không kiểm được |
| UniHop, Curri, Locus (Mỹ) | Tự chọn xe theo kích thước nhập tay | Từ ảnh; theo **luật cho xe máy, xe thô sơ**; dịch vụ ở Việt Nam |
| PackLogic, Yembo (Mỹ, chuyển nhà) | Chụp hoặc quét đồ, gợi ý cỡ xe tải | Kiểm hàng lòi ra so với **ngưỡng luật**; dùng tại quầy bán hàng; có phần xe máy |
| IKEA, ItemFits, CarGo-Fit | Kiểm hàng có vừa cốp ô tô; giúp đặt giao hàng nếu không vừa | Đối tượng là xe máy và xe thô sơ; cửa hàng truyền thống không bán online |
| PitneyShip, vMeasure, FreightSizer | Đo hộp hàng bằng camera hoặc LiDAR | Đo **xe đã chất hàng** so với giá chở hàng; dùng biển số làm thước |
| ZERO ODOL (Indonesia 2025) | Thiết bị đo tải gắn trên xe | Xét cả kích thước, che biển số, báo hiệu; không cần gắn thiết bị lên xe |
| Thước dây + tờ checklist | Cách rẻ nhất | **Phải chứng minh hơn ở chỗ:** biết ngay luật nào, gọi xe thay thế có giá, có dữ liệu. Nếu không hơn thì dừng (mục 12) |

**Tính mới chưa được xác lập.** Các so sánh trên dựa vào tìm nhanh. Trong hồ sơ nên viết "điểm khác so với…", không viết "chưa có công cụ nào".

## 10. Nguồn gốc các ý và những gì đã gác

**Ý của trưởng nhóm đã đưa vào thiết kế:**

| Ý | Đánh giá | Trong tài liệu |
|---|---|---|
| Đo từ hình ảnh để giảm thao tác | Giữ; cần vật tham chiếu và khoảng sai số | Mục 5, 7 |
| Dùng computer vision hiện nay, đo bằng vật tham chiếu | Giữ; thêm biển số làm thước, VLM không dùng để đo | Mục 7 |
| Đèn xanh / vàng / đỏ | Giữ; gắn với khoảng sai số | Mục 5 |
| Bắt đầu từ lúc định chở hàng, gợi ý dịch vụ trước | Giữ; giải quyết câu hỏi "ai được lợi" | Mục 4 |
| App là đơn vị đảm bảo tuân thủ luật, dịch vụ chỉ đi kèm | Giữ, đổi chữ thành "chốt tuân thủ tại nguồn" vì app không có quyền phạt | Mục 3 |
| Chụp ảnh → nhận diện loại hàng → luật liên quan, hữu ích cả khi đo chưa chính xác | Giữ | Mục 5 |
| Gợi ý dịch vụ theo từng món hàng | Giữ | Mục 5, 8 |
| Người dùng phải biết mình đo để tuân thủ luật gì | Giữ | Mục 5 |
| Luôn cố gắng đo và đưa ước tính, kèm luật và dịch vụ cho trường hợp đó | Giữ; đây là quyết định cuối về luồng | Mục 5 |
| Dựng app bằng agent | Giữ cho phần mềm; không thay được dữ liệu thực địa | Mục 7, 11 |
| Danh sách 11 lỗi hay gặp, đếm lỗi ở thực địa trước | Giữ; sửa phạm vi chiều cao (chỉ xe máy) và mức phạt xe thô sơ | Mục 6, 11 |
| Luật đủ rõ để phạt; khoảng trống là xử phạt theo đợt | Giữ; ghi rõ phần "nhiều chuyến không bị phát hiện" là nhận định chưa đo | Mục 6 |
| Kế hoạch build 4 tuần | Giữ; ghép với thu bằng chứng | Mục 11 |

**Đã cân nhắc nhưng không theo:**
- **Sàn liệt kê và so giá dịch vụ vận chuyển riêng.** Không mới, trùng hướng L06 đã gác, và phải cạnh tranh với nền tảng lớn. Thay bằng lớp gợi ý (mục 8).
- **Dùng VLM để đo cm.** Độ chính xác chưa đủ.
- **"Phiếu giúp cửa hàng chứng minh đã làm đúng".** Không có căn cứ, vì luật chỉ phạt người lái.
- **Chỉ đo khi thật cần.** Đã đổi thành luôn đo và ước tính (mục 5).

## 11. Kế hoạch build và thu bằng chứng (20/11 → nộp trước 15/12, khoảng 24 ngày)

| Tuần | Phần mềm | Thực địa / hồ sơ |
|---|---|---|
| **1** | Bộ luật cho 11 lỗi (mục 6); bảng loại xe và giá dịch vụ (mục 8); giao diện hai chế độ: **nhập kích thước bằng tay** (bản đầu) và **chụp ảnh** (khung sẵn, làm tiếp ở tuần 2) | Ra 1–2 cửa hàng vật liệu xây dựng: **đếm số lần gặp từng lỗi trong 11 lỗi**, trên tổng mọi lượt xuất hàng quan sát được; chụp 30–50 xe đã chất hàng và đo bằng thước (hai người đo); phỏng vấn chủ cửa hàng, người chở, khách |
| **2** | Đo từ ảnh: thẻ chuẩn, biển số làm thước, chạm vào ảnh để khoanh vùng hàng; nhận diện loại hàng và dáng xe (xe máy, thô sơ, ba gác, xe tự chế) | Tiếp tục chụp nếu mẫu chưa đủ đa dạng (loại hàng, góc, ánh sáng) |
| **3** | Đánh giá sai số trên ảnh thật; gắn nút mở thẳng app Lalamove, Ahamove, Grab | Cho người dùng thật thử tại cửa hàng; ghi thời gian thao tác và phản hồi |
| **4** | Sửa lỗi, đóng gói bản demo | Quay video ≤5 phút, dưới 25 MB, tại cửa hàng; sửa bản mô tả .docx theo tài liệu này, điền mục 6 bằng số thật; nộp trước 15/12 |

Phần mềm có thể dựng bằng agent. Phần thực địa thì nhóm phải tự làm.

**Các chỉ số khóa trước khi đo:**
- số lần gặp từng lỗi trên tổng lượt xuất hàng quan sát được;
- tỷ lệ chuyến được đổi sang phương án đúng luật thành công;
- thời gian và chi phí tăng thêm;
- sai số đo so với thước, theo từng nguồn tỷ lệ (thẻ / biển số / mô hình độ sâu), cùng tỷ lệ 🟡 và **số ca 🟢 sai**.

Mỗi chỉ số so với cách cửa hàng đang làm hiện nay. Không chỉnh ngưỡng sai số trên chính mẫu dùng để báo kết quả.

## 12. Rủi ro và điều kiện dừng

- **Cửa hàng không hợp tác, hoặc khách bỏ sang chỗ khác khi bị báo đỏ.** Phải đổi lợi ích trao cho cửa hàng, hoặc đổi điểm đặt app.
- **Sai số đo bằng biển số quá lớn, hoặc nhiều ca 🟢 sai.** Chỉ giữ chế độ có thẻ, hoặc chỉ giữ nhận diện + luật + dịch vụ.
- **Thước và checklist giải quyết tương đương.** Khi đó phần ảnh không có giá trị tăng thêm; giữ phần luật và dịch vụ.
- **Gợi ý xe chỉ khả thi nhờ trợ giá.** Không bền.
- **Quy định địa phương khác biệt nhiều.** Thí điểm ở một tỉnh, đọc văn bản của tỉnh đó trước.
- **Quyền riêng tư ảnh.** Làm mờ, không lưu ảnh gốc.

## 13. Việc pháp lý và kỹ thuật còn mở

- Có văn bản nào sửa Luật 36/2024 hay không; thông tư về khổ giới hạn xếp hàng cho xe tải, và bộ nào đang có thẩm quyền ban hành.
- Quy định của TP.HCM, Hà Nội, Đồng Nai về xe máy, xe thô sơ chở hàng kinh doanh và xe bốn bánh chở hàng.
- Văn bản gốc QCVN 08:2024/BCA về kích thước biển số; biển số cũ trước 2025 có thể khác.
- Bảng kích thước giá chở hàng và thân xe theo mẫu xe phổ biến.
- License của mô hình nhận diện, tách vùng, ước độ sâu.
- Kiểm trực tiếp app Lalamove và Haravan xem có tự gợi ý xe không.

## Tài liệu liên quan

- [Báo cáo track 2 ngày 19/11: bốn hướng T2-A…D](../track2_2026_11_19/README.md)
- [Luật chở hàng và phần app kiểm được](luat_cho_hang_vi.md)
- [Công nghệ đo kích thước từ ảnh](cv_do_kich_thuoc_vi.md)
- [Bổ sung bằng chứng track 2: số liệu xử phạt, tai nạn, giá dịch vụ](../../../data/track2_enrichment_2026_summary.md)
- [Nguyên tắc chọn ý tưởng và checklist](../../../AGENTS.md)
- [Bản mô tả dự thi (nháp)](../../../submission_2026/Ban_mo_ta_san_pham_CHO_VUA_draft.docx), chưa cập nhật theo các mục 3–5, 7–9 của tài liệu này
