# Công nghệ đo kích thước hàng từ ảnh cho CHỞ VỪA

Ngày 20/11/2026. Đây là rà soát nhanh bằng tìm kiếm web, không phải systematic review. Chưa chạy thử mô hình nào trên ảnh xe thật. Các con số độ chính xác dưới đây là của tác giả hoặc nhà cung cấp công bố trên bài toán khác, chưa được kiểm trên xe máy chở hàng.

## 1. Vì sao khó hơn cảm giác ban đầu

AI hiện nay đo kích thước từ ảnh khá tốt **khi có vật tham chiếu nằm cùng mặt phẳng với vật cần đo**. Cái khó của CHỞ VỪA không nằm ở mô hình mà ở bài toán:

- **Ngưỡng luật hẹp.** Phải phân biệt hàng lòi 0,30 m với 0,35 m bên mỗi giá chở hàng, nên sai số cần nhỏ hơn khoảng 5 cm.
- **Mốc đo bị che.** Luật tính phần lòi *so với giá chở hàng*, mà cạnh giá thường bị chính hàng che.
- **Hàng không phải hộp.** Ống, tôn, bao, nệm có hình dạng lồi lõm và không cùng một mặt phẳng.
- **Chiều cao 2 m tính từ mặt đường**, nên ảnh phải thấy chân bánh xe.
- **Không ước được khối lượng từ ảnh.**

Một mô hình chỉ cần sai 5–10% trên khoảng cách vài mét là đã đủ đổi kết luận đạt thành không đạt.

## 2. Các lớp công nghệ có thể tích hợp

### 2.1 Lấy tỷ lệ (đổi pixel ra cm)

| Nguồn tỷ lệ | Cách dùng | Ưu điểm | Hạn chế |
|---|---|---|---|
| **Thẻ ArUco / thẻ in** gắn trên giá chở hàng | Phát hiện bằng OpenCV, tính phép biến đổi phối cảnh theo mặt phẳng thẻ | Chính xác nhất khi vật cùng mặt phẳng thẻ; chạy được ngay trên trình duyệt | Phải mang và gắn thẻ; thẻ càng nhỏ so với khung hình thì sai số càng lớn |
| **Biển số xe máy 190 × 140 mm** (QCVN 08:2024/BCA) | Phát hiện biển số ở ảnh chụp phía sau, dùng làm "thước có sẵn" | **Không cần thẻ.** Biển gắn phía sau, gần đúng mặt phẳng đo bề ngang | Biển nhỏ nên sai vài pixel ở cạnh biển bị khuếch đại; biển bị bẩn, nghiêng hoặc bị hàng che; ảnh chụp hông không thấy biển |
| **Kích thước biết trước của mẫu xe** (bánh xe, chiều dài cơ sở, bề ngang giá) | Nhận diện mẫu xe, tra bảng kích thước | Dùng được cho ảnh chụp hông để đo phần lòi phía sau | Cần bảng kích thước đáng tin; xe tự chế không có số liệu |
| **Mô hình ước độ sâu từ 1 ảnh** (MoGe-2, Depth Pro, UniDepthV2, Metric3D v2) | Dự đoán khoảng cách thật cho từng điểm ảnh, không cần vật tham chiếu | Không cần gì ngoài ảnh | Đo theo tỷ lệ thật vẫn là phần yếu hơn đo tương đối; cần GPU nên phải chạy trên máy chủ; phải kiểm license |
| **AR của điện thoại** (ARCore Raw Depth, ARKit; LiDAR trên iPhone Pro) | Đo từ nhiều khung hình khi người dùng lia máy | Không cần thẻ; ARCore Depth chạy trên phần lớn máy Android đang dùng, kèm ảnh độ tin cậy | Phải là app cài đặt, web khó dùng; chưa thấy số sai số công bố cho điện thoại |
| **Dựng 3D từ vài ảnh** (VGGT, MASt3R, AMB3R, MapAnything) | Chụp 2–4 ảnh, mô hình dựng lại hình 3D có tỷ lệ | Đo được cả phần lòi ra sau và bề ngang | Nặng, chạy trên máy chủ; benchmark 2025 cho thấy đầu ra theo tỷ lệ thật kém hơn đầu ra tương đối |

### 2.2 Tách vùng xe và hàng

- **SAM 2 / SAM 2.1** chạy được trên trình duyệt qua WebGPU và ONNX Runtime Web (ví dụ WebSAM). Có bản rút gọn SlimSAM khoảng 14 MB chạy bằng CPU cho máy không có WebGPU. Người dùng **chạm vào hàng một lần**, máy khoanh vùng. Cách này đáng tin hơn để máy tự đoán.
- **SAM 3** mạnh hơn nhưng nặng, và một số bản phân phối có giới hạn license. Chưa phù hợp cho bản demo.
- **YOLO-seg** tự huấn luyện để tự động nhận "xe máy", "hàng", "biển số". Cần dữ liệu có nhãn. Dataset UIT-ADrone có nhãn `carrying bulky goods` nhưng chụp từ drone, không dùng để đo được và chưa rõ license (xem báo cáo track 2 bổ sung). Roboflow có vài bộ "overloading" xe máy nhỏ, không rõ nguồn gốc.

### 2.3 Mô hình chat đọc ảnh (VLM)

Không dùng để đo cm. Các benchmark 2025–2026 (MM-Spatial, DepthLM, "Seeing Is Not Measuring") đều cho thấy VLM yếu khi ước kích thước theo đơn vị thật. Gắn thêm công cụ hình học giúp được nhiều chỉ khi đã có khung vật chính xác; bước phát hiện vật mới là nút thắt. Có thể dùng VLM cho việc phụ như nhận loại hàng hoặc kiểm hàng có che biển số không.

## 3. Thiết kế đề xuất: đèn xanh / vàng / đỏ theo độ bất định

Ý chính: **mỗi phép đo đi kèm một khoảng sai số**, rồi mới so với ngưỡng luật.

| Đèn | Điều kiện | App làm gì |
|---|---|---|
| 🟢 Xanh | Giá trị đo + sai số **vẫn dưới** ngưỡng | Cho đi, hiện nhắc chằng buộc |
| 🔴 Đỏ | Giá trị đo − sai số **vẫn trên** ngưỡng | Không đạt; gợi ý xếp lại hoặc gọi xe phù hợp kèm giá |
| 🟡 Vàng | Khoảng sai số chứa ngưỡng, hoặc ảnh thiếu mốc / bị che / mờ | Vẫn đưa luật và dịch vụ cho cả hai khả năng; mặc định gợi ý phương án an toàn; có tùy chọn đo kỹ hơn (thêm góc chụp, thẻ, thước) |

Ví dụ: đo được lòi bên phải 0,36 m ± 0,04 m. Khoảng là 0,32–0,40 m, nằm trọn trên 0,30 m → 🔴. Nếu đo 0,32 m ± 0,05 m thì khoảng 0,27–0,37 m chứa ngưỡng → 🟡.

Xe tự chế luôn là 🔴, bất kể kích thước.

Sai số được lấy từ: nguồn tỷ lệ đã dùng (thẻ chính xác hơn biển số, biển số hơn mô hình độ sâu), kích thước vật tham chiếu tính bằng pixel, góc chụp lệch bao nhiêu, và độ tin cậy của vùng tách. Lúc đầu đặt sai số theo bảng thực nghiệm (mục 5), không tự đặt cho đẹp.

### Luồng xử lý

1. **Hàng có trong danh mục:** báo ngay theo kích thước đã biết, không cần ảnh.
2. **Ảnh phía sau:** tìm thẻ, nếu không có thì tìm biển số → lấy tỷ lệ → chạm chọn hàng → đo bề ngang hai bên và chiều cao.
3. **Ảnh bên hông:** tìm thẻ, nếu không có thì dùng bánh xe / mẫu xe → đo phần lòi ra sau.
4. **Kiểm chéo:** mô hình độ sâu trên máy chủ để bắt lỗi lớn (ví dụ nhận nhầm biển số). Lệch quá nhiều giữa các nguồn → 🟡.
5. **Ghép kết quả** → đèn xanh / vàng / đỏ → nếu đỏ thì gợi ý xe phù hợp.

### Chạy ở đâu

- **Trên trình duyệt điện thoại:** OpenCV.js (thẻ ArUco), phát hiện biển số, SlimSAM hoặc SAM 2 tiny. Chạy được cả khi mạng yếu.
- **Trên máy chủ:** mô hình độ sâu và dựng 3D, chỉ dùng để kiểm chéo.

## 4. Điểm có thể nêu là đóng góp

Rà soát nhanh **chưa thấy** công cụ nào làm đủ ba việc sau. Đây chưa phải xác nhận tính mới:

1. **Dùng biển số xe máy (kích thước chuẩn theo luật) làm thước đo**, để đo phần hàng lòi ra so với giới hạn luật. Có các bài báo dùng biển số ô tô để ước khoảng cách, nhưng chưa thấy dùng để đo hàng trên xe máy.
2. **Đèn xanh/vàng/đỏ theo khoảng sai số:** app tự biết khi nào chưa chắc và chuyển sang người đo, không để AI quyết ở ca sát ngưỡng.
3. **Quy tắc theo Luật 36/2024 cho xe máy và xe thô sơ**, không chỉ hỏi "có vừa thùng xe không".

## 5. Phép thử cần làm trước khi đưa số vào hồ sơ

- **Mẫu:** 30–50 xe đã chất hàng tại 1–2 cửa hàng, nhiều loại hàng, nhiều góc chụp và điều kiện ánh sáng. Ghi riêng xe, ngày và cửa hàng.
- **Kết quả chuẩn:** hai người đo bằng thước, theo cách đo khóa trước.
- **Báo cáo theo từng nguồn tỷ lệ** (thẻ / biển số / mô hình độ sâu): sai số trung bình (cm), tỷ lệ xếp đúng đạt/không đạt, tỷ lệ ra 🟡, và **số ca 🟢 sai**. Đây là lỗi nguy hiểm nhất: hàng vượt mà app cho đi.
- **Không chỉnh ngưỡng trên chính mẫu dùng để báo kết quả.** Tách mẫu chỉnh và mẫu thử theo xe hoặc ngày.
- **Điều kiện dừng:** chế độ biển số có quá nhiều 🟢 sai, hoặc quá nhiều 🟡 đến mức đo thước nhanh hơn. Khi đó chỉ giữ chế độ có thẻ.

## 5b. Hướng ưu tiên (cập nhật 20/11): mỗi ảnh đều ra loại hàng + ước tính kích cỡ + luật + dịch vụ

Quyết định của người dùng: mỗi lần chụp, app **luôn nhận diện loại hàng và luôn cố gắng đo**. Kết quả là **một ước tính kích cỡ có khoảng sai số**. Thông tin luật và gợi ý dịch vụ được tính **cho đúng khoảng ước tính đó**. App không đợi đo chính xác mới trả lời, và không bỏ bước đo.

Lý do:
- Nhận diện "đây là bó ống nhựa / tủ lạnh / tấm tôn" đáng tin hơn đo cm. Mô hình đọc ảnh (VLM) hoặc bộ phân loại nhỏ làm tốt việc này. Nếu chưa chắc, app cho người dùng chọn 1 trong 3 gợi ý.
- Biết loại hàng thì **ước kích cỡ tốt hơn**: nhiều loại có kích thước phổ biến (ví dụ ống nhựa thường bán theo cây dài cố định). App có thể "bắt về" kích thước chuẩn gần nhất. Bảng kích thước chuẩn phải lấy từ danh mục hoặc nhà sản xuất, chưa lập.
- Người dùng luôn nhận được thông tin hữu ích, kể cả khi số đo chưa chắc, và biết **mình đang kiểm theo luật nào**.

### Mỗi kết quả gồm 4 phần

| Phần | Nội dung | Nguồn |
|---|---|---|
| 1. Loại hàng | "Bó ống nhựa (độ tin cậy cao)" | Nhận diện ảnh; danh mục cửa hàng nếu có |
| 2. Ước tính kích cỡ | "Dài khoảng 3,8–4,2 m, rộng ~0,3 m, cao ~0,3 m", ghi rõ đo bằng gì (thẻ / biển số / mẫu xe / mô hình độ sâu / kích thước chuẩn của loại hàng) | Ghép các nguồn ở mục 2–3; luôn có khoảng sai số |
| 3. Luật áp dụng | Với từng giới hạn liên quan: 🟢 / 🟡 / 🔴, so cả khoảng ước tính với ngưỡng. Ví dụ: "lòi sau ~3,3–3,7 m, luật cho ≤0,5 m → 🔴" | Rulebook theo loại xe (mục Giới hạn bên dưới) |
| 4. Dịch vụ phù hợp | Loại xe vừa với **cận trên** của khoảng ước tính, kèm giá công bố và nút mở app nền tảng | Bảng xe Lalamove / Ahamove / Grab |

Khối lượng không ước được từ ảnh. App chỉ đưa con số **ước theo loại hàng**, ghi rõ là ước, và ưu tiên số từ danh mục hoặc cân.

### Khi khoảng ước tính sát ngưỡng (🟡)

App **vẫn trả lời đầy đủ** thay vì dừng lại:
- *"Nếu phần lòi ≤0,5 m thì xe máy được. Nếu hơn thì nên chở bằng ba gác hoặc van 500 kg, khoảng X đ."*
- Có tùy chọn **đo kỹ hơn**: chụp thêm một góc, đặt thẻ, hoặc dùng thước. Đây là tùy chọn, không bắt buộc. Đo kỹ xong, khoảng ước tính hẹp lại và đèn được tính lại.
- Gợi ý dịch vụ mặc định chọn **phương án an toàn**, tức xe vừa với cận trên.

### Gợi ý dịch vụ theo khoảng ước tính

Từ khoảng ước tính kích cỡ, app suy ra yêu cầu về thùng xe (dài, rộng, cao, khối lượng) rồi lọc theo bảng xe đã công bố. Ví dụ dùng bảng Lalamove TP.HCM đọc ngày 20/11/2026, **chỉ minh họa**:

- **Bó ống dài 4 m:**
  - không đi được: xe máy (50×40×50 cm), xe máy có baga (60×50×60 cm), ba gác GrabExpress (1,7 m, theo trang năm 2022), van 500 kg (170 cm), tải 1.000 kg (300 cm);
  - vừa sát: tải 2.000 kg (400 cm);
  - tại Hà Nội: bảng ghi tải 2.000 kg dài 350 cm, nên phải lên loại lớn hơn.
- Phần hàng vượt thùng xe tải cũng có quy định riêng, chưa tra trong lượt này. Cần tra thêm trước khi ghi vào rulebook.

### Đã có ai làm "chụp ảnh → nhận diện đồ → gợi ý xe" chưa

Có, cho **chuyển nhà ở Mỹ**:
- [PackLogic](https://apps.apple.com/us/app/packlogic/id6759308470): quét phòng, nhận diện đồ, gợi ý cỡ xe tải và rơ-moóc.
- [Yembo](https://yembo.ai/visual-inventory?hsLang=en): kiểm kê đồ đạc bằng video cho các công ty chuyển nhà, ước cỡ xe và số người.

Tìm nhanh chưa thấy app giao hàng nào gợi ý xe từ ảnh món hàng. Curri gợi ý xe từ thông tin nhập tay. Khác biệt của CHỞ VỪA so với PackLogic/Yembo: quy tắc luật cho xe máy và xe thô sơ, bảng dịch vụ Việt Nam, và điểm dùng là quầy cửa hàng khi bán.

### Giới hạn

- **Rulebook theo loại hàng chưa được lập.** Hiện chỉ có các giới hạn đã đọc: Luật 36/2024 Điều 33 khoản 5 (xe máy), Điều 31 khoản 5 (xe thô sơ) và Điều 47 (xếp hàng, chằng buộc). Mức phạt theo Nghị định 168/2024 đã được Nghị định 238/2026 sửa đổi, cần đối chiếu văn bản hợp nhất. Hàng đặc thù (gas, xăng dầu, hóa chất, kính, động vật sống) cần tra riêng, chưa được khẳng định.
- Ảnh có thể chứa mặt người và biển số. Nên làm mờ hoặc không lưu ảnh gốc.

## 6. Việc cần kiểm thêm

- License của từng mô hình trước khi dùng (SAM 3 có giới hạn; một số mô hình độ sâu chỉ cho phi thương mại).
- Văn bản gốc QCVN 08:2024/BCA (Thông tư 81/2024/TT-BCA) cho kích thước biển số 190 × 140 mm. Biển số cũ trước 2025 có thể khác.
- Bảng kích thước các mẫu xe máy phổ biến lấy từ nhà sản xuất.

## Nguồn

- MoGe-2: [arXiv 2507.02546](https://arxiv.org/html/2507.02546v1) · MoGe-3: [arXiv 2607.17967](https://arxiv.org/pdf/2607.17967) · UniDepthV2: [arXiv 2502.20110](https://arxiv.org/html/2502.20110v2) · [Survey on Monocular Metric Depth Estimation](https://arxiv.org/html/2501.11841v4)
- Dựng 3D có tỷ lệ: [AMB3R, arXiv 2511.20343](https://arxiv.org/html/2511.20343v1) · [MapAnything, arXiv 2509.13414](https://arxiv.org/pdf/2509.13414) · [Benchmark mô hình nền 3D, arXiv 2506.01933](https://arxiv.org/pdf/2506.01933v3)
- VLM và đo kích thước: [MM-Spatial, arXiv 2503.13111](https://arxiv.org/html/2503.13111v2) · [Seeing Is Not Measuring, arXiv 2609.29073](https://arxiv.org/pdf/2609.29073) · [DepthLM, arXiv 2509.25413](https://arxiv.org/pdf/2509.25413v2)
- AR điện thoại: [ARCore Raw Depth](https://developers.google.com/ar/develop/java/depth/raw-depth?hl=en) · [Danh sách thiết bị ARCore](https://developers.google.com/ar/devices?authuser=2)
- Tách vùng trên trình duyệt: [WebSAM](https://github.com/Xevion/WebSAM) · [Labelbox – SAM2 trên trình duyệt](https://labelbox.com/blog/bringing-ai-to-the-browser-sam2-for-interactive-image-segmentation/) · [Qualcomm AI Hub – SAM 3](https://aihub.qualcomm.com/models/sam3)
- Đo bằng thẻ / điện thoại: [arXiv 2208.05319](https://arxiv.org/pdf/2208.05319) · [OpenCV forum – ArUco](https://forum.opencv.org/t/calculating-2d-dimensions-on-object-using-aruco/7686)
- Biển số làm thước: [arXiv 2604.12239](https://arxiv.org/pdf/2604.12239) · [arXiv 2607.00319](https://arxiv.org/pdf/2607.00319) · [Kích thước biển số xe mô tô theo QCVN 08:2024/BCA](https://thuvienphapluat.vn/hoi-dap-phap-luat/kich-thuoc-bien-so-xe-mo-to-la-bao-nhieu-theo-qcvn-08-2024bca-138041438.html)
- Dữ liệu: [Roboflow – MC overloading violation](https://universe.roboflow.com/peds-workspace-1618a/mc-overloading-violation) · [UIT-ADrone](https://uit-together.github.io/datasets/UIT-ADrone/)
- Ứng dụng đo kiện hàng: [PitneyShip](https://www.pitneybowes.com/us/support/article/000082682/measuring-a-package-in-the-pitneyship-mobile-app.html) · [vMeasure](https://apps.apple.com/us/app/-/id6736906563) · [FreightSizer](https://apps.apple.com/us/app/id6738141881)
