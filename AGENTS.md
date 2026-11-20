# Nguyên tắc Chọn & Đánh giá Ý tưởng Dự thi (AGENTS.md)

> Nhập từ `Downloads/AGENTS.md` ngày 20/11/2026. Đường dẫn được trỏ lại vào repo này và số liệu được đối chiếu với `ideas_normalized.csv` và `global_traffic_contest_ideas_2023_2026.xlsx`. Những chỗ đã hiệu chỉnh có ghi **[Đối chiếu]**. Khi có mâu thuẫn, quy tắc bằng chứng trong [RESEARCH_OBJECTIVE.md](RESEARCH_OBJECTIVE.md) được ưu tiên: không suy ra công thức chấm giải hoặc hiệu quả từ lịch sử có giải.

## I. Ba nguyên tắc cốt lõi (bộ lọc thực chiến 5 giây)

Mọi ý tưởng, giải pháp và bản mô tả sản phẩm cho cuộc thi **Sáng kiến An toàn Giao thông** cần qua 3 tiêu chí:

1. **Hiểu ngay trong 5 giây:** người không học kỹ thuật nghe tên bài là hình dung ra ngay tình huống ngoài đường và thấy *"cái này cần thật"*.
2. **Triển khai độc lập, ít vướng rào cản thể chế:** ví dụ một bộ cảnh báo điểm mù có thể mua về gắn thẳng lên xe tải và chạy ngay ngày mai. **[Đối chiếu]** Camera gắn trên cột vẫn cần xin phép đơn vị quản lý hạ tầng; đừng coi đó là ví dụ "độc lập hoàn toàn".
3. **Có sản phẩm sờ nắm được hoặc chạy thật trên dữ liệu ngoài đường:** nên ưu tiên bản mẫu chạy thử (*prototype / video thực địa*) hơn đề tài nặng mô hình toán và chỉ chạy trên mô phỏng. **[Đối chiếu]** Đây là định hướng rút ra từ danh sách bài có giải (I05, I10), chưa phải điểm giám khảo đã đo.

---

## II. Điểm chung của các ý tưởng từng đạt giải

> **Nguồn trong repo:**
> • **73 bản ghi trong nước (2022–2025):** [10_quy_luat_y_tuong_vi.md](traffic-data-research/reports/discovery/10_quy_luat_y_tuong_vi.md), [ideas_normalized.csv](traffic-data-research/reports/discovery/tables/ideas_normalized.csv) và [idea_patterns.json](traffic-data-research/reports/discovery/idea_patterns.json). Gồm 67 bài *Sáng kiến ATGT Việt Nam* và 6 bài *Data For Life*. **55 bài `AWARDED`**, 14 vào shortlist nhưng không có tên trong danh sách giải, 4 chưa xác minh kết quả.
> • **121 bản ghi Việt Nam & quốc tế (2023–2026):** [global_traffic_contest_ideas_2023_2026.xlsx](data/global_traffic_contest_ideas_2023_2026.xlsx) và [README](global_traffic_contest_ideas_README.md). Gồm 21 nhóm cuộc thi/chương trình, **78 `AWARDED`** và **20 `SELECTED_PILOT`**. `SELECTED_PILOT` là được chọn thí điểm đô thị, không phải giải xếp hạng.
>
> **[Đối chiếu]** 70/73 mô tả cơ chế trong nước được suy ra từ tiêu đề bài (I10). Các "quy luật" dưới đây là mẫu hình trong danh sách công bố, không phải quan hệ nhân quả giữa tính năng và việc đạt giải.

### 1. Công thức định vị: `[Thiết bị / công cụ cụ thể] + [gắn cho ai / ở đâu] + [chặn ngay 1 hành vi / điểm mù nguy hiểm]` (I03, I04)
Các bài đạt giải cao thường đóng gói thành **một sản phẩm cụ thể đặt đúng điểm ra quyết định của người lái hoặc lực lượng chức năng**:
* **Giải Nhất 2025 (`IDEA-011`):** *Hệ thống cảnh báo điểm mù chủ động "Vành đai ánh sáng"*, gắn trên xe tải lớn.
* **Giải Nhất 2025 (`IDEA-028`):** *Hệ thống khóa thông minh phân quyền và xác thực độ tuổi điều khiển phương tiện*.
* **Giải Nhất 2025 (`IDEA-002`):** *Hộp điện thoại thông minh (Safety Box)*.
* **Giải Nhất 2024 (`IDEA-031`):** *Camera xử phạt vi phạm và phân tích giao thông thông minh*. **Giải Nhất Data For Life 2023 (`IDEA-072`):** *Ứng dụng AI trong phát hiện biển số ô tô giả*. **[Đối chiếu]** Repo không ghi thông số "250 km/h, 4G/5G" của IDEA-031; muốn dùng thì phải dẫn nguồn riêng.
* **Giải Nhì 2024 (`IDEA-032`):** *Thiết bị cảnh báo điểm mù ở khúc cua nguy hiểm*. **Giải Nhì 2025 (`IDEA-014`):** *Thiết bị cảnh báo điểm mù xe có tải trọng lớn*. (Mã `WIDEA-014` trong workbook quốc tế là ZERO ODOL, một bài khác.)

Cùng mẫu này, I03 còn lưu ý: chỉ thêm một cảnh báo thì không tự tạo ra khác biệt. Cần nói rõ cảnh báo cho ai, trước tình huống gì, và người nhận phải làm gì sau đó.

### 2. Nhóm "Điều tiết & đèn tín hiệu" rất đông (15/73 bài trong nước, 13 có giải); các bài thuật toán/mô phỏng thuần ghi nhận dừng ở Khuyến khích (I01)
* Năm nào cũng có đề tài đèn tín hiệu và điều tiết, ví dụ `IDEA-013`, `IDEA-033`, `IDEA-041`, `IDEA-043`, `IDEA-054`, `IDEA-055`.
* *Học tăng cường đa tác tử cho bài toán giảm ùn tắc* (`IDEA-054`, 2023) và *Mô phỏng và tối ưu hạ tầng giao thông hỗn hợp dựa trên AIoT* (`IDEA-013`, 2025) đều được ghi **Khuyến khích**.
* Các bài **Nhì** cùng nhóm có sản phẩm cụ thể hoặc kết hợp phát hiện vi phạm/phân luồng: trụ đảo di động (`IDEA-041`, 2023), AI điều tiết và phát hiện đi ngược chiều (`IDEA-043`, 2023), eTraffic (`IDEA-033`, 2024). **[Đối chiếu]** Riêng `IDEA-033` có nguồn ghi Nhất và nguồn ghi Nhì; repo đang giữ Nhì. Ngoài ra `IDEA-055` (bỏ đèn đỏ, phân luồng lại tại Hà Nội/TP.HCM) được ghi **Nhất 2022**: giải pháp tổ chức giao thông không có thiết bị vẫn có thể đạt giải cao.
* Quốc tế (`WIDEA-063` Greenflow, `WIDEA-036` 5S/ADB 2026, USDOT Intersection Safety Challenge): nhấn mạnh đo xung đột cận va chạm (near-miss/TTC/PET) và luồng xe từ cảm biến/camera thực địa. **[Đối chiếu]** Đây là đọc định tính từ mô tả công bố.

### 3. Giải pháp cơ khí/vật lý đơn giản nhưng trúng vấn đề vẫn có giải; không bắt buộc "nhồi" AI (I05)
* Trụ đảo di động (`IDEA-041`, Nhì 2023), móc khóa nhắc không lái xe khi uống rượu bia (`IDEA-040`, Nhì 2023), cọc tiêu tái chế cổng trường (`IDEA-049`, Khuyến khích 2023).
* **Quy tắc:** không phức tạp hóa bằng AI/Deep Learning nếu một cơ chế vật lý, quy trình hoặc thiết bị cảnh báo đơn giản giải quyết được nhanh hơn, rẻ hơn và tin cậy hơn. Luôn so với phương án thủ công đơn giản nhất.

### 4. Gắn với một địa danh/điểm nóng cụ thể thuyết phục hơn đề tài "vĩ mô toàn quốc" (I06)
* 4/5 ví dụ có tên địa bàn được ghi có giải, ví dụ đường Hồ Chí Minh qua **Đắk Nông** (`IDEA-062`, Ba 2022) và hai cổng trường tại **Lâm Đồng** (`IDEA-051`, Khuyến khích 2023). Mẫu chỉ có 5 ví dụ.
* RAPTOR 2024 (`SELECTED_PILOT`): các dự án gắn với thách thức của một thành phố cụ thể. **[Đối chiếu]** Bản gốc ghi "100% dự án gắn chặt 1 nút giao/1 khu phố, có đo baseline trước–sau", nhưng repo chưa kiểm chứng đủ 20 dự án nên không dùng con số này.

### 5. Khớp đúng chủ đề và đối tượng của mùa thi (I07, I09)
* Năm 2025 có 3 chủ đề × 10 bài vào chung khảo, mỗi chủ đề trao giải riêng. Lý do đạt giải năm cũ không tự áp sang năm mới.
* **Chủ đề 1 (*"Đường đông vẫn thông"*):** 15/73 bài trong nước thuộc nhóm điều tiết/đèn tín hiệu. **[Đối chiếu]** Bản gốc ghi "78 bài quốc tế làm về nút giao/đèn tín hiệu" là sai: 78/121 bản ghi quốc tế chỉ được *phân loại biên tập* gần chủ đề 1, còn cụm "An toàn nút giao" có 15 bản ghi. Muốn nổi bật cần chỉ ra khác biệt về cơ chế vận hành thực tế và **có số đo/video trên nút giao thật**.
* **Chủ đề 2 (*"Đúng hàng – Đúng phương tiện"*):** 0/73 tên bài trong nước khớp "cồng kềnh/quá khổ" (I09); 11/121 bản ghi quốc tế được phân loại biên tập gần chủ đề 2. Đây là hướng ít trùng *trong mẫu công bố*, **không phải bằng chứng thị trường trống**. Vẫn phải đối chiếu prior art gần (ZERO ODOL `WIDEA-014`, Safe to Load `WIDEA-111`, nano-hub `WIDEA-059/060`, Lalamove/Ahamove).

### 6. Prototype và bằng chứng thực nghiệm quan trọng hơn lượt bình chọn (I08, I10)
* Năm 2025 có **10 bài có giải không nằm trong top bình chọn online** (I08). Bình chọn, có giải và hạng giải là ba tín hiệu khác nhau.
* **[Đối chiếu] Tiêu chí chấm:** thang điểm/trọng số chính thức 2026 **chưa được công bố**. Tiêu chí chung kết 2025 của BTC (chỉ tham khảo) gồm: sáng tạo; khả năng ứng dụng và phát triển; thu hút đầu tư; chất lượng mô hình mẫu; thuyết trình/phản biện. Sheet `RUBRIC` trong workbook quốc tế có tiêu chí của ADB, UNITAR, EU và một rubric *nghiên cứu, không chính thức*. Năm trụ cột dưới đây là cách gộp của nhóm để tự kiểm, **không phải rubric của BGK**:
  1. **Sáng tạo / khác biệt về cơ chế** so với giải pháp đã có (VCAM 2024, eTraffic 2024, Vành đai ánh sáng 2025…).
  2. **Khả năng ứng dụng thực tế và triển khai độc lập.**
  3. **Chất lượng prototype và dữ liệu kiểm chứng**: so với baseline đang vận hành, không chỉ so với "không làm gì".
  4. **Khả năng thu hút đầu tư và nhân rộng** với chi phí hợp lý.
  5. **Thuyết trình và phản biện** trước các tình huống lỗi (fail-safe).

---

## III. Checklist bắt buộc trước khi chốt đề tài 2026

Trước khi viết báo cáo hoặc code cho một ý tưởng, trả lời đủ 5 câu. Mỗi câu có phiên bản cho Chủ đề 2, vì track 2 đang là phạm vi ưu tiên của repo.

- [ ] **Câu 1 (5 giây):** nghe tên đề tài và câu tóm tắt 1 dòng, người bình thường có hình dung ngay ra cảnh ngoài đường không?
- [ ] **Câu 2 (độc lập thể chế):** ngày mai mang thiết bị/phần mềm ra thử, nhóm có tự làm được mà **không cần mở tủ đèn tín hiệu, can thiệp hạ tầng hay sửa kết cấu xe** không? *Chủ đề 2:* chỉ cần một cửa hàng và một bên vận tải đồng ý là thử được không?
- [ ] **Câu 3 (sờ được, chạy trên dữ liệu thật):** ở vòng chung kết, có **thiết bị/ứng dụng chạy trực tiếp trên dữ liệu hoặc video quay thật tại điểm nóng** không, hay chỉ có slide và mô phỏng? *Chủ đề 2:* có đo trên xe đã chất hàng thật tại điểm xuất hàng không?
- [ ] **Câu 4 (không trùng bài cũ):** đề tài khác gì với **VCAM (Nhất 2024)**, **eTraffic (Nhì 2024)**, **Cảnh báo khúc cua (Nhì 2024)**, **Vành đai ánh sáng (Nhất 2025)**, **MARL giảm ùn tắc (Khuyến khích 2023)**? *Chủ đề 2:* khác gì với **ZERO ODOL**, **Safe to Load**, giới hạn hàng của **Lalamove/Ahamove/GrabExpress** và **nano-hub/cargo bike**?
- [ ] **Câu 5 (đo so với hiện trạng):** chỉ số cải thiện được đo so với **hiện trạng đang vận hành** như thế nào? *Chủ đề 1:* thời gian khóa nút, xung đột near-miss, độ nhạy, tỷ lệ báo giả. *Chủ đề 2:* tỷ lệ lượt xuất hàng không đạt / tổng lượt quan sát, tỷ lệ chuyến được đổi phương tiện thành công, thời gian chờ, chi phí thực, bỏ sót và cảnh báo sai so với thước/cân/checklist.

Thêm một câu cho mọi ý tưởng: **ai được lợi đủ để tự nguyện dùng**, và ai trả chi phí khi kết quả là "không phù hợp"?
