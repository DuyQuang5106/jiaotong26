# Track 2: chọn ý tưởng ngăn chuyến chở hàng không phù hợp

> **Cập nhật 20/11/2026:** T2-A đã được phát triển thành CHỞ VỪA. Xem [tài liệu ý tưởng hợp nhất](../track2_2026_11_20/CHO_VUA_y_tuong_vi.md). Các mục dưới đây giữ nguyên làm hồ sơ của lượt 19/11.

Ngày 19/11/2026, Asia/Bangkok. Tiếp tục nghiên cứu trong repo; giữ nguyên các báo cáo và dữ liệu gốc. Phạm vi là xe máy, phương tiện thô sơ và xe tự chế trong chủ đề người dùng cung cấp. Không lấy bài toán xe tải dài tại Sơn La làm bằng chứng trực tiếp cho track 2.

**Ưu tiên nghiên cứu T2-A: kiểm tra thực tế tại điểm xuất hàng, rồi giải quyết chuyến không phù hợp bằng cách xếp lại hoặc đổi phương tiện có thể thực hiện được.** T2-B có thể trở thành nhánh dịch vụ thay thế của dự án này. T2-C phù hợp nhóm có đối tác bán hàng/đóng gói; T2-D phù hợp nhóm cơ điện tử có điều kiện kiểm định. Đây là thứ tự theo mức khớp chủ đề và khả năng kiểm chứng, không phải điểm giám khảo hoặc xác suất thắng.

Chưa có cơ sở chấm bất kỳ ý tưởng nào “10/10” về hiệu quả, tính mới hoặc nhu cầu thị trường. Mục tiêu là phát triển một hồ sơ mạnh bằng phép thử có thể bác bỏ ý tưởng, không gán điểm tối đa cho đề xuất chưa thử.

## Căn cứ đã có

| Lớp bằng chứng | Đã xác nhận hoặc tính được | Giới hạn sử dụng |
| --- | --- | --- |
| Danh mục trong nước | 73 bản ghi; 0 tiêu đề khớp “cồng kềnh/quá khổ” | Không chứng minh thị trường trống hoặc cơ chế chưa tồn tại |
| Danh mục quốc tế mới | 121 ID; 11 được workbook gán track 2; 3 bản ghi thiếu năm | Phân loại biên tập, có ví dụ chỉ liên quan gián tiếp; không là 121 nghiên cứu độc lập |
| GT-08 | Đã kiểm lại 50 mask nhị phân trong lượt trước | Không tách nhãn hàng cồng kềnh; không có baseline tần suất hành vi này |
| GT-01/07/09 | Có các phân tích lịch sử với giới hạn đã ghi | Không xác định nhóm chở hàng, nhu cầu người dùng hoặc hiệu quả bốn đề xuất |
| Nguồn bổ sung địa phương | Bài trên cổng Đồng Nai ngày 01/09/2024 nêu khó khăn vận chuyển vào hẻm và áp lực nhận chuyến | Ghi nhận định tính, không đại diện hiện trạng 2026 hay tỷ lệ ngoài thực địa; xem S1 |

Hai workbook đầu vào được đọc bằng parser OOXML có sẵn và giữ nguyên hash. Số đếm/bộ lọc ở [inventory_scan.json](inventory_scan.json); 12 trường hợp ưu tiên đọc ở [international_prior_art_triage.csv](international_prior_art_triage.csv). Không sử dụng kết quả có giải để huấn luyện hoặc suy ra mô hình chấm giải.

**Diễn giải cần kiểm chứng:** bên bán hàng, người chở và người nhận có thể cần một phương án thay thế đủ thuận tiện để tránh chuyến không phù hợp. Đây là giả thuyết thiết kế, chưa phải nguyên nhân đã đo hoặc nhu cầu trả tiền đã xác nhận.

## T2-A. Chốt hàng đúng xe tại cửa hàng

**Hai câu giới thiệu:** Một cửa hàng kiểm tra cấu hình xe–hàng thực tế trước khi bàn giao, phát hiện trường hợp cần xem lại. Với trường hợp không phù hợp, hệ thống giúp hoàn tất phương án xếp lại hoặc chuyển sang phương tiện phù hợp, có ghi nhận kết quả chuyến đi.

**Ngách để xác minh trước:** cụm cửa hàng vật liệu xây dựng tại khu vực Biên Hòa/Long Khánh theo địa danh bài năm 2024; đây là đầu mối khảo sát, chưa phải địa điểm pilot đã có phép. Khi làm việc thực tế phải xác nhận địa chỉ/địa giới hiện tại. Nếu nhóm có đối tác ở địa phương khác, lợi thế tiếp cận và baseline thực quan trọng hơn địa danh đề xuất.

**Quy trình đề xuất:**

1. Trước bàn giao, đo hàng đã xếp lên xe tại vị trí đứng yên bằng thước/khung chuẩn hoặc thiết bị đã hiệu chuẩn; ghi loại xe, kích thước tham chiếu, khối lượng từ cân/thông số đáng tin và cách cố định. Không suy khối lượng từ ảnh.
2. Đối chiếu từng điều kiện đã xác minh cho đúng loại xe. Đầu ra là “cần xếp lại”, “cần đổi phương tiện” hoặc “cần kiểm tra thủ công”; kiểm đủ kích thước không đồng nghĩa chứng nhận toàn bộ an toàn.
3. Nếu có thể chia kiện/xếp lại mà vẫn đáp ứng các điều kiện thì cho người phụ trách xem phương án. Nếu một vật nguyên khối không thể đi phù hợp, chuyển loại phương tiện; không giải quyết bằng chia số chuyến giả tạo.
4. Đưa lựa chọn có thật: xe nào nhận được hàng, nhận khi nào, chi phí bao nhiêu, ai xác nhận. Có thể dùng bên vận tải hiện có; không cần tự xây sàn đặt xe.
5. Ghi chuyến đã hoàn tất như thế nào, kể cả bị hủy, bị từ chối, khách chuyển cửa hàng hoặc rời điểm theo cách chưa xác minh được. Bên bán phải tham gia trách nhiệm, không đẩy toàn bộ chi phí chờ/đổi xe lên người chở.

**Điểm đáng phát triển:** đo cấu hình thực tế ở thời điểm xuất hàng và theo dõi việc chuyển đổi thực sự. Máy phát hiện và cảnh báo chỉ là một bước; giá trị cần chứng minh nằm ở số chuyến không phù hợp được thay đổi thành công với gánh nặng vận hành chấp nhận được.

**Phương án đơn giản để so:** nhân viên dùng thước, cân và checklist, sau đó gọi bên vận tải có sẵn. Chỉ thêm camera/phần mềm nếu chứng minh lợi ích tăng thêm. Ảnh đơn lẻ không đủ suy kích thước mét nếu thiếu tham chiếu hình học; gần ngưỡng hoặc bị che khuất phải chuyển kiểm tra thủ công.

**Đã có giải pháp gần:** ZERO ODOL trong danh mục quốc tế (WIDEA-014, S3); kiểm tra phương tiện trong Safe to Load (WIDEA-111, S5); lựa chọn phương tiện/dịch vụ tại Lalamove (S6/S7). Đối tượng, thao tác và phạm vi khác nhau nên cần đối chiếu kỹ thuật đầy đủ. Chưa xác lập tính mới của T2-A.

**Bản thử đầu tiên:** biểu mẫu web, một trạm đo có chuẩn, danh mục xe/hàng và một đối tác xử lý chuyển xe. Làm “shadow mode” để đo chất lượng trước, không tự khóa động cơ hay thay điều khiển xe.

**Đo chính:** số lượt xuất hàng chưa đáp ứng tiêu chí đã khóa / tổng lượt xuất hàng được quan sát, tách theo người chấm độc lập. Đo thêm bỏ sót, cảnh báo sai, thời gian xử lý, chi phí thực và tỷ lệ phương án thay thế hoàn tất. Đây là outcome vận hành/hành vi, chưa là số tai nạn ngăn được.

**Điều kiện dừng:** cửa hàng không hợp tác; không có tình huống lặp; checklist thủ công đã giải quyết tương đương; phần lớn chuyến bị đẩy sang nơi khác; hoặc chuyển đổi chỉ thành công nhờ trợ giá không thể duy trì. Đạt điều kiện kích thước không cho phép hợp thức hóa xe tự chế hay xe không đủ điều kiện.

## T2-B. Chuyến xe chung cho cụm cửa hàng

**Hai câu giới thiệu:** Nhiều đơn nhỏ nhưng không phù hợp với xe máy có thể được xếp vào chuyến của một phương tiện phù hợp phục vụ cùng cụm cửa hàng. Cửa hàng thấy trước khung giờ, phần chi phí và phương án giao chặng cuối để quyết định trước lúc người chở nhận hàng.

**Ngách giả thuyết:** nhóm cửa hàng lân cận bán mặt hàng mà nhu cầu giao có thể chờ một khung giờ thỏa thuận. Nhu cầu, mật độ đơn và mức chờ chấp nhận được chưa được đo; không mặc định mọi chợ hoặc làng nghề đều phù hợp.

**Quy trình đề xuất:** thu thông tin đơn thật → loại phương án không đáp ứng điều kiện xe/hàng/đường tiếp cận → thử ghép đơn theo khung giờ → lấy báo giá thực → cửa hàng chấp nhận → kiểm lại cấu hình chất hàng trên chuyến chung. Không chỉ tối ưu thể tích; còn khối lượng, mặt hàng không đi chung, trình tự lấy/trả và giới hạn tiếp cận.

**Điểm cần tạo khác biệt:** cùng các cửa hàng chia sẻ một lựa chọn thay thế được xác nhận, gắn với những chuyến vốn cần đổi phương tiện. Dịch vụ nhiều điểm dừng đã tồn tại; thuật toán ghép đơn hoặc nhãn “logistics xanh” tự thân chưa đủ mới. Nano-hub và cho thuê e-cargo đã có prior art WIDEA-059/060 (S2); chưa chứng minh hiệu quả tương tự tại Việt Nam.

**Bản thử:** một người điều phối, bảng đơn, báo giá và một bên vận tải hiện có; chưa cần mua xe, xây hub hay kết nối API. T2-B có thể chạy độc lập hoặc là phương án thay thế cho T2-A.

**Đo chính:** tỷ lệ đơn cần đổi phương tiện được hoàn tất theo phương án đã kiểm; chi phí thực/đơn, thời gian chờ, nhu cầu trợ giá và tổng km phát sinh. Theo dõi cả chặng cuối, không chuyển việc chở không phù hợp từ đường lớn sang ngõ/hẻm.

**Điều kiện dừng:** thiếu đơn tương thích, khách không chấp nhận chờ, chi phí không cạnh tranh với đặt nhiều điểm hiện có, hoặc không có phương án tiếp cận người nhận đáp ứng điều kiện. Không gán tỷ lệ tiết kiệm giả định thành kết quả.

## T2-C. Đóng kiện vừa xe ngay từ lúc bán

**Hai câu giới thiệu:** Cửa hàng quyết định cách đóng kiện và loại phương tiện cùng lúc chốt đơn. Với mặt hàng có thể tháo lắp, lồng/xếp hoặc chia kiện theo hướng dẫn được xác nhận, công cụ đưa ra cách đóng gói cụ thể; vật nguyên khối không phù hợp được chuyển sang loại xe khác.

**Ngách giả thuyết:** cơ sở bán bao bì/đồ nhựa xếp lồng hoặc đồ gia dụng tháo lắp. Chọn một họ hàng trước, không cố tối ưu mọi hàng hóa. Chưa có bằng chứng trong dữ liệu hiện tại về tần suất lỗi đóng kiện tại các cơ sở này.

**Cơ chế đề xuất:** catalog SKU có số đo thật, khối lượng, khả năng tháo/lồng và ràng buộc cố định → đề xuất kiện và phương tiện → hướng dẫn đóng tại cửa hàng → đo lại kiện thực tế. Không dùng định mức thu nhỏ vật trên màn hình mà không kiểm đóng được. Mẫu khung/đệm phải được kiểm phù hợp, không cơi nới baga hoặc tự thay kết cấu xe.

**Giá trị cần chứng minh:** giảm trường hợp phải sửa phương án giao sau khi người chở tới, giữ tổng thời gian/chi phí và khả năng cố định phù hợp. Đây là giả thuyết, chưa là lợi ích đã đo.

**Bản thử và so sánh:** danh mục của một cửa hàng, hướng dẫn đóng bằng ảnh và phương án nhân viên giàu kinh nghiệm. Có thể thử trên bàn/xe đứng yên trước khi giao; chưa cần mô hình AI.

**Đo chính:** tỷ lệ phương án đóng được thực tế và đáp ứng toàn bộ tiêu chí đã khóa; thời gian đóng, số chuyến, hư hỏng và chi phí. Việc chia kiện có thể làm tăng số lượt đi/khối lượng công việc; phải báo cả bất lợi.

**Điều kiện dừng:** mặt hàng không thể thu gọn/chia an toàn, nhân viên đã làm tốt tương đương, số chuyến/chi phí tăng quá mức người dùng chấp nhận hoặc khách không đồng ý tháo/chia. Chưa tra đủ sản phẩm tối ưu đóng gói; không tuyên bố mới từ việc chưa thấy trong hai workbook.

## T2-D. Theo dõi dây chằng lỏng và hàng dịch chuyển

**Hai câu giới thiệu:** Thiết bị theo dõi thay đổi trạng thái dây chằng hoặc vị trí hàng trên một cấu hình đã được phép thử và đáp ứng điều kiện xe–hàng. Khi phát hiện tình trạng bất thường, thiết bị nhắc người chở kiểm tra tại vị trí dừng phù hợp.

**Ngách giả thuyết:** người chở thường xuyên cùng một họ kiện có khả năng cố định rõ. Chưa có dữ liệu tần suất dây lỏng/hàng dịch trong bộ hiện tại; phải quan sát để xác nhận nhu cầu trước chọn loại cảm biến.

**Cơ chế đề xuất:** cảm biến đo đại lượng liên quan độ căng và/hoặc dịch chuyển, có mốc sau khi cố định; phát hiện thay đổi kéo dài theo quy tắc đã hiệu chuẩn. Bắt đầu trên đồ gá có đo tham chiếu, với tình huống chằng đúng, lỏng, dịch và rung gây nhiễu. Cảm biến rung đơn lẻ không chứng minh hàng đã dịch; thiết bị không tự kéo siết hoặc can thiệp bộ phận chịu lực trong bản thử ban đầu.

**Prior art:** chỉ thị lực căng dây đã có (S8), vì vậy “gắn cảm biến lên dây” chưa là tính mới. Đóng góp tiềm năng phải ở khả năng dùng phù hợp cấu hình xe máy, chi phí, thời tiết, bảo trì và ít báo sai; tất cả chưa xác minh.

**Đo chính:** bỏ sót và cảnh báo sai trên các tình huống đồ gá chưa dùng để chỉnh ngưỡng, độ bền, pin và thời gian lắp. Thử hiện trường chỉ sau kiểm định/cho phép phù hợp. Không dùng cảnh báo tốt làm lý do chấp nhận hàng quá kích thước hoặc phương tiện không đáp ứng điều kiện.

**Điều kiện dừng:** không có nhu cầu lặp; cảnh báo sai/khó dùng; cảm biến không đo được điều cần biết; tăng hỏng hóc hoặc phân tâm; giải pháp dây/chằng đúng và kiểm tra thủ công đã đủ. Thiết bị có thể làm demo đẹp nhưng chưa ưu tiên bằng T2-A nếu nhóm thiếu năng lực kiểm định cơ khí.

## Hướng nào nên chọn

| Điều kiện nhóm thực sự có | Ưu tiên có điều kiện | Bằng chứng còn thiếu quyết định |
| --- | --- | --- |
| Tiếp cận được một cửa hàng và bên vận tải | T2-A | Có bao nhiêu chuyến cần thay đổi, chủ cửa hàng có thực hiện không, checklist hiện tại đã đủ chưa |
| Tiếp cận một cụm cửa hàng, nhiều đơn và bên điều phối | T2-B | Đơn tương thích, thời gian chờ, chi phí thật và giao chặng cuối |
| Có đối tác đóng gói/sản phẩm cụ thể | T2-C | Cấu hình đóng thực tế và lợi ích so nhân viên hiện tại |
| Có nhóm cơ điện tử và nơi kiểm định/đồ gá | T2-D | Nhu cầu về lỏng/dịch, độ đo đúng và rủi ro thiết bị |

**Đề xuất tên hồ sơ T2-A:** “Kiểm tra cấu hình xe–hàng tại điểm xuất và hỗ trợ chuyển phương tiện cho cửa hàng nhỏ”. Bản đầu nên có một cửa hàng, một họ hàng và một bên vận tải. Chưa cần thêm nhiều app, dashboard hoặc cảm biến vào cùng một prototype.

## Ba phép thử giúp ý tưởng mạnh lên

1. **Vấn đề có lặp không?** Quan sát tất cả lượt xuất trong những cửa sổ đã chọn, ghi cả lượt đạt và chưa đạt; hai người chấm một phần mẫu theo tiêu chí khóa trước. Ghi người từ chối tham gia và phạm vi thuận tiện của mẫu. Không công bố tỷ lệ chung của tỉnh từ một cửa hàng.
2. **Cách kiểm có đáng tin không?** So với thước/cân/checklist do người có chuyên môn xác nhận. Tách cấu hình, ngày và cửa hàng khi chia dữ liệu thử; không dùng nhiều ảnh cùng chuyến như nhiều chuyến độc lập. Báo sai số đo gần ngưỡng và trường hợp thiết bị không trả được kết quả.
3. **Có đổi được chuyến không?** Khi đã có phép và không để nhóm đối chứng cố tình đi không phù hợp, so quy trình hỗ trợ hiện có với quy trình hỗ trợ mới. Khóa chỉ số chính, điều kiện đủ và cách ghi chuyển đi nơi khác/hủy/chưa biết kết quả. Mỗi khách/đơn cần ID để tránh đếm trùng nhiều lần xếp lại. Mẫu lặp theo cửa hàng/ngày không được coi là độc lập toàn bộ.

Gợi ý hai tuần đầu chỉ nhằm xác minh khả thi: tuần đầu quan sát/đo quy trình hiện tại và đồng thiết kế; tuần sau thử vận hành giới hạn sau khi đủ điều kiện. Chưa có cỡ mẫu, mức cải thiện tối thiểu hay pilot đã chạy; không gán trước hiệu quả %, ngân sách hoặc công suất thống kê. Sau baseline mới khóa thiết kế/cỡ mẫu phù hợp. Quy định pháp lý, thông số nhà sản xuất và giới hạn dịch vụ vận tải là ba lớp khác nhau; chưa lập rulebook pháp lý để triển khai tự động trong lượt này.

## Dấu vết và tái lập

Chạy từ gốc repo, vào một output chưa tồn tại:

```powershell
python -X utf8 traffic-data-research/src/track2_evidence_scan.py --output traffic-data-research/reports/track2_scan_replay
```

Script chỉ tái lập quét hai workbook, không tự xác nhận claim web hoặc nhu cầu. [Nguồn bổ sung](source_checks.json) lưu URL, ngày đọc và phạm vi; không tự thêm chúng thành mã GT mới trong inventory 22 nguồn. [Danh sách 12 hướng đã xét](candidate_screening.json) giữ cả hướng tạm gác và lý do. Các nguồn web được xem trên bản live/cached của công cụ web, chưa có bản HTML raw mới lưu kèm; không gán checksum HTML giả.

Skill dùng cho lượt này: `brainstorming-research-ideas` (problem-first, stakeholder rotation, simplicity và lọc ứng viên); `Spreadsheets` (đọc bảng, phân biệt ghi nhận/diễn giải, không chỉnh workbook). Hướng dẫn kiểm chứng theo người/chuyến/cửa hàng tiếp tục dùng nguyên tắc từ checkpoint phương pháp đã đọc trước. Không huấn luyện mô hình hoặc chạy thử can thiệp. [Checkpoint trước và các giới hạn](../revalidation_2026_11_19_v2/README.md) vẫn có hiệu lực.

## Các nguồn đã đối chiếu

- **S1:** [Cổng Đồng Nai, bài 01/09/2024](https://dongnai.gov.vn/vi/news/trat-tu-an-toan-giao-thong/xe-ba-gac-cho-hang-cong-kenh-xe-3-4-banh-tu-che-am-anh-cua-nguoi-di-duong-46638.html). Chỉ dùng làm đầu mối địa phương định tính, không cập nhật luật hoặc ước lượng hiện trạng.
- **S2:** [EIT Urban Mobility, RAPTOR 2024](https://www.eiturbanmobility.eu/raptor-2024-kicks-off-in-13-european-cities/). Dự án e-cargo/nano-hub được mô tả cho pilot; không lấy lời giới thiệu làm hiệu quả đã đo.
- **S3:** [Dishub DIY, các dự án năm 2025](https://dishub.jogjaprov.go.id/bidang-lalu-lintas/lima-pelajar-terbaik-terpilih-sebagai-pelopor-keselamatan-lalu-lintas-diy-2025). Xác nhận có ZERO ODOL; chưa có đủ hồ sơ để benchmark thiết bị.
- **S4:** [Crashfree India, NextMile](https://crashfreeindia.org/campaigns/ideathon). Strategists/SafeMile liên quan cơ chế vận hành, không xác minh kết quả giảm tai nạn.
- **S5:** [FIA, Innovation Challenge 2024](https://www.fia.com/news/fostering-excellence-across-our-network-fia-innovation-challenge-2024-winners-revealed). Safe to Load là ví dụ kiểm tra/đào tạo trong vận tải hàng, khác đối tượng chính của track này.
- **S6:** [Lalamove, dịch vụ xe máy có baga](https://www.lalamove.com/vi-vn/driver/dich-vu-xe-may-co-baga). Ví dụ dịch vụ thương mại đang có, không là xác nhận an toàn mọi cấu hình.
- **S7:** [Lalamove FAQ](https://www.lalamove.com/vi-vn/faq). Giới hạn hàng theo loại xe và dịch vụ nhiều điểm đã được mô tả; cần baseline đối chiếu thật.
- **S8:** [LoadLok, cargo control](https://loadlok.com/blogs/news/types-of-equipment-for-securing-cargo). Ví dụ có chỉ thị lực căng, chưa là chứng minh phù hợp xe máy tại Việt Nam.
- **S9:** [UIT-ADrone](https://uit-together.github.io/datasets/UIT-ADrone/). Có nêu carrying bulky goods trong phạm vi nghiên cứu; các mask đã tải trước không phân tách hành vi này.
