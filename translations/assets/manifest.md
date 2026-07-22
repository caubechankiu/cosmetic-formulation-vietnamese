# Asset Manifest

Manifest này theo dõi hình, bảng, sơ đồ và biểu đồ đã được xử lý trong bản dịch để tránh dịch hoặc crop trùng khi layout PDF đẩy nội dung sang section khác.

## Quy ước

- `ID`: mã gốc trong sách, ví dụ `Bảng 1.1` hoặc `Hình 1.4`.
- `Loại`: `Bảng`, `Hình`, `Sơ đồ`, `Biểu đồ` hoặc loại phù hợp khác.
- `Section sở hữu`: section nơi đối tượng được nhắc đến hoặc giải thích đầu tiên, kể cả khi vị trí vật lý trên PDF nằm ở section sau.
- `Markdown`: file Markdown đang chứa bản dịch hoặc tham chiếu của đối tượng.
- `Asset file`: file crop trong `translations/assets/images/` nếu là hình/sơ đồ/biểu đồ; ghi `N/A` nếu bảng được dựng trực tiếp bằng Markdown.
- `Trang PDF`: trang vật lý nơi đối tượng xuất hiện trong PDF, nếu đã xác định.
- `Ghi chú`: dùng để ghi các trường hợp layout trôi, đã bỏ qua ở section sau, hoặc cần rà soát thêm.

## Đối tượng đã xử lý

| ID | Loại | Caption / mô tả | Section sở hữu | Markdown | Asset file | Trang PDF | Ghi chú |
|---|---|---|---|---|---|---|---|
| Bảng 1.1 | Bảng | Các công cụ để hiệp lực hóa trải nghiệm cảm quan | 1.1 | translations/markdown/1.1.senses-and-science-art-science-and-communication-and-their-role-in-cosmetic-products.md | N/A | 20 | Dựng lại bằng Markdown trong section sở hữu. |
