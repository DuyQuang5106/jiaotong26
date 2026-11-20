# Track 2 – Báo cáo bổ sung bằng chứng (20/11/2026)

**Nguồn đầu vào:** 73 ý tưởng trong nước `IDEA-xxx` và 121 ý tưởng quốc tế `WIDEA-xxx`. Không chỉnh sửa bản gốc; xuất **`track2_enrichment_2026.xlsx`** với 5 sheet yêu cầu.

## 1. Phạm vi hoàn thành

- `competition_2026`: **32** dòng: danh sách **8 giám khảo**, hồ sơ và mốc thi, các nguồn về tiêu chí năm 2025, những thông tin chưa được công bố năm 2026.
- `track2_evidence`: **54** dòng, chia thành luật và quy định địa phương, số liệu xử lý, tai nạn có tên vụ, phương án vận chuyển, chuyển đổi nghề, dataset camera và prior art.
- `mechanism_enrichment`: **109** dòng, trong đó **22** dòng có bổ sung nội dung từ nguồn mới; những dòng khác được giữ với trạng thái **CHƯA TRA CỨU SÂU** và không tự suy cơ chế từ tên tác phẩm.
- `record_corrections`: **6** dòng hiệu chỉnh đề nghị (không thay bản gốc); `search_log`: **44** lượt/trang hoặc nhóm truy vấn được ghi lại.

**Giới hạn cần hiểu:** Không phải toàn bộ 70 cơ chế trong nước và 34 cơ chế quốc tế đều đã được kiểm chứng chi tiết. Với những bài chưa truy xuất hồ sơ kỹ thuật, bảng ghi rõ nguồn công bố nhan đề và tình trạng chưa điều tra sâu. Các số liệu xử phạt là số **phát hiện/xử lý trong từng đợt**, không ước lượng tổng số vụ vi phạm thực tế. Mẫu vụ tai nạn không đại diện thống kê toàn quốc.

## 2. Năm phát hiện quan trọng nhất cho Chủ đề 2

1. **Có vị trí can thiệp trước khi xe rời cửa hàng trong luật.** Điều 47 khoản 1(c,d) Luật **36/2024/QH15** yêu cầu kiểm tra xếp hàng và chằng buộc chắc chắn. Điều 33 khoản 5 quy định giới hạn hàng trên xe máy: mỗi bên giá đèo **0,3 m**, phía sau **0,5 m**, chiều cao từ mặt đường **2 m**. Đây là các biến đầu vào có thể đưa vào công cụ kiểm tra cấu hình xe–hàng. [Luật toàn văn](https://xaydungchinhsach.chinhphu.vn/toan-van-luat-trat-tu-an-toan-giao-thong-duong-bo-119240909105718285.htm).
2. **Bằng chứng vi phạm đủ cụ thể để mô tả vấn đề, nhưng không phải tỷ lệ hiện mắc.** Tại Hà Nội, từ **15/7 đến 1/8/2026**, CSGT xử lý **242 trường hợp chở hàng cồng kềnh**, trong tổng **472 trường hợp** thuộc các nhóm hành vi được báo cáo; con số này không đồng nghĩa Hà Nội có 242 người vi phạm trong kỳ. [Nguồn VTV](https://vtv.vn/csgt-ha-noi-xu-ly-gan-500-xe-tu-che-cho-hang-cong-kenh-100260803224303027.htm).
3. **Tai nạn có cơ chế liên quan trực tiếp tới kích thước hàng.** Vụ ngày **09/06/2026** trên đường Nguyễn Trãi có báo cáo phần hàng cồng kềnh va vào tay lái người đi xe máy khác; ngày **25/06/2026** tại Đồng Tháp người lái chở vật cồng kềnh va chạm ô tô và bị thương. Đây là minh chứng dạng *case*, không chứng minh tác động nhân quả ở mức dân số. [Dân trí](https://dantri.com.vn/thoi-su/tai-xe-cho-hang-cong-kenh-khien-nguoi-di-xe-may-bi-nga-xuong-duong-20260610092910889.htm) · [VTV](https://vtv.vn/cho-hang-cong-kenh-xe-may-va-cham-o-to-o-giao-lo-100260628093932832.htm).
4. **Vận tải thay thế đã có nhưng cần đánh giá ma sát tại điểm bán.** Ahamove công bố giá xe tải 500 kg tại TP.HCM **124.000đ/2 km đầu**, thêm **11.600đ/km từ 2–10 km**; **ước tính 5 km là 158.800đ**, chưa tính phụ phí và không phải báo giá app. Grab mô tả xe van/tải dưới 1.000 kg. Nhóm nên đo biến quyết định chuyển đổi: phí/đơn, thời gian đợi xe, tần suất đơn nhỏ, đường vào ngõ, tải trọng và kích thước thùng. [Ahamove](https://ahamove.com/service/aha-truck/price) · [Grab](https://www.grab.com/vn/terms-policies/transport-delivery-logistics/).
5. **Có prior art quốc tế gần với hướng “kiểm tra tải trước chuyến”.** `WIDEA-014` ZERO ODOL/KENDEDES LCC được sở giao thông Yogyakarta xác nhận giải Nhất cấp tỉnh và giải Ba quốc gia 2025; **chưa tìm thấy mô tả mạch cảm biến hoặc độ chính xác**. `WIDEA-060` Don Cicleto, startup **Tây Ban Nha**, từng được chọn pilot tại **Brussels** cho mô hình nano-hub chuyển hàng sang cargo bike. Cần kiểm tra tính khác biệt của giải pháp nhóm so với hai hướng “phát hiện quá tải” và “chuyển tải chặng cuối”. [Yogyakarta](https://dishub.jogjaprov.go.id/bidang-lalu-lintas/lima-pelajar-terbaik-terpilih-sebagai-pelopor-keselamatan-lalu-lintas-diy-2025) · [EIT](https://www.eiturbanmobility.eu/raptor-2024-kicks-off-in-13-european-cities/).

## 3. Mâu thuẫn hoặc chưa có đủ căn cứ

- **Hạn nộp:** [`/the-le`](https://sangkienatgt.dantri.com.vn/the-le) ghi **“trước ngày 15/12/2026”**, trong khi [`/gioi-thieu`](https://sangkienatgt.dantri.com.vn/gioi-thieu) ghi **“đến hết ngày 15/12/2026”**. Để an toàn, **nộp trước ngày 15/12**.
- **Thang điểm 2026:** **KHÔNG TÌM THẤY** tỷ trọng số học trên thể lệ/giới thiệu/BGK; tiêu chí 2025 chỉ để tham khảo.
- **Nội dung đơn ZIP:** **KHÔNG ĐỌC ĐƯỢC** hai ZIP mẫu qua phương tiện truy cập hiện có; bảng chỉ ghi các thành phần hồ sơ xuất hiện trên thể lệ, không bịa tên các ô biểu mẫu.
- **WIDEA-014:** nguồn viết “**Loud Cell Combination**”; không tự đổi thành “Load Cell” nếu chưa thấy tài liệu kỹ thuật. Không có thông số cảm biến, độ chính xác, mức hoàn thiện.
- **WIDEA-060:** bản gốc ghi xuất xứ **Bỉ**, nhưng EIT ghi rõ **Spanish startup**; cần sửa riêng nguồn gốc đội thành **Tây Ban Nha** và địa điểm pilot **Brussels, Bỉ**. Bản gốc vẫn giữ nguyên.
- **IDEA-033:** bài viết Dân trí về năm 2024 có nơi gọi eTraffic giải Nhất, trong khi danh sách giải ghi Nhì; ghi mâu thuẫn, chưa sửa dữ liệu cũ.
- **WIDEA-008/009/010:** nguồn NextMile nêu cơ chế và giải nhưng không xác nhận năm trong trang đã đọc; chưa điền năm.
- **UIT-ADrone:** 51 video, 206.194 frames, có nhãn `carrying bulky goods`, format COCO và `.npy`, nhưng **KHÔNG TÌM THẤY license cụ thể** ngay trang dự án; không được mặc nhiên coi dữ liệu được phép dùng thương mại. [Dataset](https://uit-together.github.io/datasets/UIT-ADrone/).
- **Nghị định 238/2026/NĐ-CP** có hiệu lực 15/08/2026, sửa đổi Nghị định 168/2024/NĐ-CP. Các mức phạt trong bảng gắn với điều khoản Nghị định 168 và có lưu ý kiểm tra văn bản hợp nhất; không tự khẳng định mức phạt bị thay đổi khi chưa thấy quy định sửa cụ thể. [Nguồn chính phủ](https://xaydungchinhsach.chinhphu.vn/nghi-dinh-so-238-2026-nd-cp-sua-doi-quy-dinh-xu-phat-vi-pham-giao-thong-duong-bo-tru-diem-phuc-hoi-diem-giay-phep-lai-xe-119260630142033452.htm).
- **Quy định TP.HCM 2026** cho phép hoạt động kinh doanh vận tải bằng mô tô/xe thô sơ 24 giờ có ngoại lệ; vì thế không thể nói **mọi** xe ba bánh đều bị cấm. Cần phân loại xe hợp lệ và xe tự chế/không đủ điều kiện. [Sở Tư pháp TP.HCM](https://sotuphap.hochiminhcity.gov.vn/tin-tuc-su-kien/-/asset_publisher/emZ19pfF3Yyq/content/tp-ho-chi-minh-ban-hanh-quy-dinh-ve-su-dung-xe-mo-to-xe-gan-may-xe-tho-so-de-kinh-doanh-van-chuyen-hanh-khach-hang-hoa-?enableXemTheoNgay=true&p_p_auth=G2vv16nY).

## 4. Việc còn thiếu theo thứ tự ưu tiên

1. Nhóm tự tải và kiểm tra trực tiếp hai file ZIP mẫu để ghi chính xác các trường khai báo; xác minh trực tiếp hạn cuối trên website BTC.
2. Thu thập định lượng ở cửa hàng: **đơn có kích thước vượt giới hạn**, **không có xe phù hợp**, **thời gian chờ xe tải**, **chi phí giao hàng thực** (ngoài phạm vi nghiên cứu dữ liệu hiện tại).
3. Truy tìm hồ sơ thuyết trình/video/bản mô tả từng ý tưởng được đánh dấu `CHƯA TRA CỨU SÂU` trong Excel, đặc biệt các `IDEA-xxx` nhóm giải Nhất/Nhì.
4. Tìm hợp đồng/license của UIT-ADrone và tải file `train.json/test.json` để xác minh mapping nhãn bulky, số mẫu dương và quyền sử dụng.
5. Lấy báo giá app cụ thể cho **5 km Hà Nội/TP.HCM** theo mẫu hàng (tủ lạnh, bao xi măng) với thời điểm và địa chỉ thực; hiện chưa có giá được xác nhận cho tất cả kịch bản.

## 5. Quy tắc dùng trong báo cáo dự thi

Không cộng số xử phạt khác kỳ; không coi giá dịch vụ tự công bố là giá giao dịch; không coi việc đạt giải là xác nhận hiệu quả; không suy cơ chế từ tên mô hình; không coi mẫu tai nạn trên báo là tỷ lệ sự cố; và không dùng tiêu chí năm 2025 như quy định năm 2026.
