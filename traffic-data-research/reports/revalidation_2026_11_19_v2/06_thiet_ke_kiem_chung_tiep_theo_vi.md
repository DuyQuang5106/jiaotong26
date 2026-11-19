# Thiết kế kiểm chứng tiếp theo — chưa thu dữ liệu

[KẾ HOẠCH] Chưa có khảo sát hoặc thử nghiệm nào trong phần này đã diễn ra. Không dùng các bố trí sau làm kết quả thực nghiệm; chưa tuyển mẫu, phân nhóm hay tính công suất từ số giả định.

## Cổng chung trước prototype

1. Xác minh hiện trạng, đối tượng, vấn đề lặp và đối tác có quyền cho khảo sát. Giữ cả lượt không xảy ra tình huống để có mẫu số.
2. Lập định nghĩa outcome, đơn vị quan sát, quy tắc missing/exclusion, baseline, mức cải thiện tối thiểu có ý nghĩa và chi phí vận hành trước khi đánh giá hiệu quả.
3. Đọc hồ sơ gần nhất và cách làm hiện hành; sự khác biệt địa danh chưa chứng minh mới về cơ chế. Nếu không có lợi ích tăng thêm có thể kiểm nghiệm thì dừng.
4. Tách thiết kế thử thuật toán/giao diện, hành vi và tác động an toàn. Không nhân số frame, lượt chấm hoặc video thành số người/địa điểm độc lập.

## C07: cảnh báo gặp xe dài

Xác minh cơ chế bằng quan sát không can thiệp trước. Nếu còn khoảng trống, thử mô phỏng hoặc sân kín có kiểm soát và người có chuyên môn. Người lái là đơn vị thử; nhiều tình huống của cùng người là đo lặp. So cách hiện tại với hỗ trợ đề xuất; phân thứ tự ngẫu nhiên/cân bằng theo người, chặn theo kinh nghiệm và điều kiện nhìn. Dùng tình huống tương đương, kiểm carry-over/học bài; nếu không thể washout, chọn thiết kế nhóm song song thay crossover. Người chấm không biết điều kiện khi khả thi. Báo nhận biết đúng, cảnh báo sai/bỏ sót, thời gian hành động và phân tâm; không lấy cải thiện mô phỏng làm giảm tai nạn trên QL.6B.

## C02: kỹ năng học sinh

Đối tượng và kỹ năng phải được xác minh trước, có phép của đơn vị/phụ huynh khi cần. Nếu can thiệp theo lớp, lớp là đơn vị phân bổ; nhiều học sinh trong lớp không là các lần phân bổ độc lập. Chặn theo trường/khối và phân lớp ngẫu nhiên khi có đủ lớp ở cả hai điều kiện. Không dùng một lớp thử và một lớp đối chứng rồi coi hàng trăm học sinh là hàng trăm đơn vị độc lập. So bài hiện hành có cùng thời lượng, đánh giá tình huống mới ngay sau và sau khoảng duy trì đã khóa trước; ghi thiếu theo dõi và tránh rò nội dung giữa lớp.

## C08/C10: quy trình bảo trì

Baseline là thời gian/tỷ lệ xử lý hồ sơ thực tế, không phải số ô untreated. Mỗi nhiệm vụ có hạng mục, thời điểm mở/đóng và kiểm chứng hiện trường; nhiều ảnh cùng nhiệm vụ không là nhiều nhiệm vụ độc lập. Nếu chỉ một tổ áp dụng trước–sau, giữ là pilot khả thi có nhiễu theo mùa/nguồn lực; muốn suy nhân quả phải có nhiều tổ/địa bàn, đối chứng đồng thời và phân bổ phù hợp. Chưa có dữ liệu sự kiện/mưa để thử mô hình dự báo sạt lở.

## Công suất, phân tích và quyết định dừng

Chưa chốt cỡ mẫu vì chưa có mức cải thiện tối thiểu, biến thiên nền, ICC theo lớp/tổ, số đơn vị tiếp cận, tỷ lệ thiếu và thiết kế cuối. Thu pilot đo chất lượng/khả thi trước; sau đó dùng statistical-power với thiết kế đã khóa, không lấy effect quan sát thuận lợi làm “observed power” biện minh. Nêu rõ mọi lần xem dữ liệu trung gian và quy tắc dừng; không thử nhiều outcome/cửa sổ rồi chỉ báo kết quả thuận lợi. Không triển khai can thiệp trên đường công cộng từ prototype chưa thẩm định.
