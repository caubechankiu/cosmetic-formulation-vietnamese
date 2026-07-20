# AGENTS.md

## Mục tiêu repo

Repo này dùng để dịch cuốn `Cosmetic-Formulation.pdf` sang tiếng Việt và lưu bản dịch dưới dạng Markdown.

## Tổng quan cuốn sách

`Cosmetic-Formulation.pdf` là sách chuyên ngành về công thức mỹ phẩm, tập trung vào nền tảng khoa học, cảm quan sản phẩm, nguyên liệu, hệ nền công thức, quy trình phát triển và đánh giá sản phẩm mỹ phẩm. Khi dịch, cần giữ văn phong phù hợp với độc giả làm R&D, formulation, QA/QC hoặc nghiên cứu mỹ phẩm: rõ nghĩa kỹ thuật, tự nhiên trong tiếng Việt, và nhất quán thuật ngữ.

## Cấu trúc hiện tại

- `Cosmetic-Formulation.pdf`: PDF gốc.
- `translations/markdown/table-of-contents.md`: mục lục của cuốn sách và là nguồn theo dõi tiến độ duy nhất; section đã dịch xong phải được gắn link tới file Markdown bản dịch tương ứng, section chưa có link là chưa dịch.
- `translations/glossary.md`: bảng thuật ngữ dùng nhất quán.
- `translations/markdown/`: nơi lưu các file Markdown bản dịch.
- `translations/assets/images/`: nơi lưu hình ảnh hoặc sơ đồ nếu cần.
- `README.md`: bản tổng hợp được tạo tự động từ các section đã dịch.
- `scripts/build-readme.py`: script tạo lại `README.md` từ các file Markdown đã được link trong mục lục.

## Quy ước bắt buộc

- Chỉ tạo và cập nhật bản dịch ở định dạng Markdown.
- Tất cả nội dung Markdown phải dùng tiếng Việt có dấu.
- `translations/markdown/table-of-contents.md` là nguồn theo dõi tiến độ duy nhất.
- Xác định tiến độ dịch dựa trên link trong `translations/markdown/table-of-contents.md`: mục đã gắn link tới file Markdown là đã dịch, mục chưa có link là chưa dịch.
- Mỗi section trong mục lục phải được dịch ra một file Markdown riêng; không gộp nhiều section vào cùng một file chương.
- Link trong `translations/markdown/table-of-contents.md` của section đã dịch phải trỏ tới file Markdown riêng của chính section đó.
- Không dịch các section có tiêu đề `References`, `Bibliography`, `Index` hoặc các mục tài liệu tham khảo/mục lục tra cứu tương đương; không tạo file Markdown riêng và không cần gắn link cho các mục này trong mục lục.
- Có thể dịch nhiều section ngắn trong cùng một lượt nếu chúng liên tiếp trong mục lục, cùng cụm nội dung, và nằm trên cùng một trang hoặc trong một phạm vi trang rất ngắn (1 đến 2 trang). Dù dịch chung một lượt, vẫn phải tạo một file Markdown riêng cho từng section và cập nhật link riêng cho từng section trong mục lục.
- Khi nội dung gốc bị ngắt qua trang PDF, hãy gộp câu/đoạn lại để bản dịch đọc liền mạch.
- Giữ văn phong tiếng Việt tự nhiên, nhưng không làm sai ý nghĩa kỹ thuật.
- Dùng thuật ngữ nhất quán theo `translations/glossary.md`; nếu gặp thuật ngữ mới quan trọng, cập nhật bảng thuật ngữ.
- Với hình ảnh, sơ đồ, biểu đồ hoặc minh họa trong sách, phải crop trực tiếp từ file PDF gốc và lưu vào `translations/assets/images/`; không tự dựng lại bằng Mermaid, SVG, ASCII art hoặc công cụ vẽ khác.
- Sau khi dịch xong một hoặc nhiều section và cập nhật mục lục/glossary/assets, phải chạy `python3 scripts/build-readme.py` để tạo lại `README.md` trước khi commit.
- Sau khi build `README.md`, phải commit các thay đổi liên quan đến bản dịch rồi push lên remote hiện tại; không chờ người dùng yêu cầu riêng thao tác commit/push.

## Quy trình dịch đề xuất

1. Đọc `translations/markdown/table-of-contents.md` để biết phần đã dịch và phần tiếp theo cần dịch. Mục đã có link là đã dịch; mục chưa có link là chưa dịch, trừ các mục `References`, `Bibliography`, `Index` hoặc tài liệu tham khảo/mục lục tra cứu tương đương thì bỏ qua. Dùng chính file này để xác định tiêu đề và mốc trang của section. Khi trích xuất PDF, lấy từ trang bắt đầu của section đó đến hết trang bắt đầu của section kế tiếp, tức là bao gồm cả trang mốc của section kế tiếp (ví dụ section bắt đầu trang 15 và section kế tiếp bắt đầu trang 21 thì trích xuất trang 15-21). Chỉ trích xuất các trang cần thiết từ PDF, không đọc toàn bộ file. Nếu phần trích xuất lẫn nội dung của section trước hoặc sau, hãy bỏ qua phần thừa khi dịch.
2. Dịch section vào một file Markdown riêng phù hợp trong `translations/markdown/`. Không ghi tiếp section mới vào file chương hoặc file section khác.
3. Cập nhật `translations/markdown/table-of-contents.md`: chuyển tiêu đề section vừa dịch thành link tương đối tới file Markdown bản dịch tương ứng, hoặc cập nhật link hiện có nếu đổi tên file.
4. Cập nhật `translations/glossary.md` nếu có thuật ngữ mới hoặc cần thống nhất cách dịch.
5. Nếu section có hình ảnh, sơ đồ, biểu đồ hoặc minh họa, crop vùng hình tương ứng từ PDF gốc, lưu dưới `translations/assets/images/`, rồi tham chiếu bằng đường dẫn tương đối trong file Markdown của section.
6. Chạy `python3 scripts/build-readme.py` để tạo lại `README.md` từ các section đã dịch.
7. Commit các thay đổi liên quan đến bản dịch, rồi push commit lên remote hiện tại.

## Quy tắc mặc định khi người dùng yêu cầu dịch tiếp

- Nếu người dùng yêu cầu dịch tiếp nhưng không nói rõ dịch section nào hoặc dịch đến đâu, tự đọc `translations/markdown/table-of-contents.md` để tìm section chưa dịch đầu tiên, bỏ qua các mục không cần dịch như `References`, `Bibliography`, `Index`.
- Sau đó chọn các section chưa dịch liên tiếp trong phạm vi nhiều nhất 10 trang PDF tính từ trang bắt đầu của section chưa dịch đầu tiên. Không chọn vượt quá mốc trang bắt đầu + 10, trừ khi cần lấy thêm trang mốc của section kế tiếp để trích xuất đủ phần cuối theo quy trình trích xuất PDF.
- Trong phạm vi 10 trang đó, nếu có các section ngắn đủ điều kiện thì gom thành cụm section ngắn; nếu có section dài thì xử lý riêng theo thứ tự mục lục.
- Nếu section kế tiếp bắt đầu ngoài phạm vi 10 trang, dừng trước section đó và không dịch lấn sang phần ngoài phạm vi.
- Sau khi dịch xong phạm vi đã chọn, vẫn phải tạo file riêng cho từng section, cập nhật mục lục, glossary/assets nếu cần, chạy build README, commit và push.

## Quy trình dịch cụm section ngắn

- Có thể gom các section ngắn thành một cụm dịch nếu tất cả điều kiện sau đều đúng: các section chưa dịch nằm liên tiếp trong `translations/markdown/table-of-contents.md`; thuộc cùng một section cha gần nhất; cùng trang bắt đầu hoặc tổng phạm vi trích xuất chỉ khoảng 1-2 trang PDF; và không có section dài, hình lớn, bảng lớn hoặc mốc chương mới chen giữa.
- Ví dụ: các section `1.2.1`, `1.2.2` và `1.2.3` cùng thuộc `1.2`, đều bắt đầu ở trang 21, nên có thể trích xuất một lần quanh trang 21 và dịch trong cùng một lượt.
- Khi trích xuất PDF cho cụm section ngắn, lấy từ trang bắt đầu của section đầu tiên trong cụm đến hết trang bắt đầu của section ngay sau cụm. Nếu phần trích xuất lẫn nội dung ngoài cụm, chỉ dịch đúng nội dung thuộc các section trong cụm.
- Trong lúc dịch cụm, phải tách rõ ranh giới từng section theo heading gốc. Không được gộp nội dung của nhiều section vào cùng một file.
- Sau khi dịch cụm, tạo một file Markdown riêng cho từng section, đặt tên theo quy ước chung, rồi cập nhật từng dòng tương ứng trong `translations/markdown/table-of-contents.md` thành link riêng.
- Nếu trong cụm có thuật ngữ mới hoặc hình/sơ đồ/bảng cần crop, xử lý glossary và assets như khi dịch từng section riêng lẻ.

## Quy trình dịch nhiều section

- Khi dịch nhiều section trong một lượt, xử lý tuần tự theo thứ tự trong `translations/markdown/table-of-contents.md`; không dịch song song nhiều section hoặc nhiều cụm section để tránh xung đột ở mục lục, glossary và assets.
- Với section dài, xử lý từng section riêng. Với các section ngắn đủ điều kiện, có thể xử lý theo `Quy trình dịch cụm section ngắn`.
- Khi công cụ agent phụ khả dụng, agent chính phải dùng agent phụ cho từng section dài hoặc từng cụm section ngắn.
- Nếu công cụ agent phụ không khả dụng, agent chính phải báo lỗi và dừng quy trình dịch nhiều section; không tự xử lý batch thay cho agent phụ.
- Agent chính chỉ giao một section dài hoặc một cụm section ngắn cho agent phụ tại một thời điểm và chờ agent phụ hoàn thành trước khi giao phần kế tiếp.
- Trong lúc chờ agent phụ dịch, agent chính không cần làm thêm việc nào khác; chỉ đợi agent phụ hoàn thành rồi mới tiếp tục.
- Khi agent phụ kết thúc, agent chính chỉ cần xác nhận agent phụ đã hoàn thành hay báo lỗi gì; không cần kiểm tra lại chi tiết toàn bộ bản dịch của section hoặc cụm section đó.
- Khi hoàn thành toàn bộ batch, chạy `python3 scripts/build-readme.py`, commit và push lên remote hiện tại; không cần rà soát lại chi tiết toàn bộ bản dịch của từng section.

## Quy ước định dạng

- Giữ cấu trúc heading, danh sách, bảng, code block và chú thích hình gần với bản gốc.
- Nếu cần dùng hình hoặc sơ đồ, phải dùng ảnh crop từ PDF gốc, lưu vào `translations/assets/images/` và tham chiếu bằng đường dẫn tương đối trong Markdown.
- Không thêm diễn giải dài ngoài nội dung sách, trừ khi người dùng yêu cầu.

## Quy ước đặt tên file

- Dùng tên file tiếng Anh, chữ thường, phân tách bằng dấu gạch ngang, theo từng section.
- Nên đặt tên có số mục nối với tên tiêu đề để dễ tra cứu, ví dụ: `1.cosmetic-products-science-and-senses.md`, `1.1.senses-and-science.md`, `1.2.1.verbatim.md`.
- Các file cấp phần hoặc chương chỉ dùng cho nội dung mở đầu tương ứng nếu chính mục phần/chương đó được dịch; không dùng làm nơi chứa toàn bộ các section con.

## Ghi chú về chất lượng

- Ưu tiên bản dịch dễ đọc cho người làm nghiên cứu và phát triển chuyên ngành mỹ phẩm Việt Nam.
- Có thể giữ một số thuật ngữ tiếng Anh quen thuộc trong ngành như `emulsion`, `surfactant`, `polymer`, `in vitro`, `in vivo`, `claims`, `skin feel` nếu dịch thuần Việt làm câu khó hiểu hơn.
- Khi giữ thuật ngữ tiếng Anh, nên dùng nhất quán trong toàn bộ bản dịch.
