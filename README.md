# Phân tích văn bản (Text Analyzer)

Ứng dụng desktop (Dark Theme) đếm từ/ký tự/câu, chuẩn hóa chuỗi và hiển thị Top N từ
phổ biến kèm biểu đồ. Kiến trúc phân lớp: `core/` (logic), `ui/` (giao diện),
`utils/` (đọc/ghi file), `main.py` (Controller). Chi tiết yêu cầu: [1.md](1.md).

## Cài đặt & chạy
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Linux cần thêm gói hệ thống Tk: `sudo apt install python3-tk`.

## Sử dụng
1. Gõ/paste văn bản vào ô **Văn bản gốc**, hoặc bấm **Tải File** (.txt/.docx).
2. Chọn tùy chọn ở sidebar:
   - **Chữ thường** / **Bỏ dấu câu** — chuẩn hóa cơ bản.
   - **Chuẩn hóa từ viết tắt** — mở rộng viết tắt thông dụng (`ko`→`không`, `đc`→`được`...).
   - **Nhận diện từ ghép** — gộp từ ghép tiếng Việt (`học sinh`, `việt nam`) thành một đơn vị khi đếm.
   - **Thống kê** / **Top N** + giá trị N.
3. Bấm **Thực Thi** → xem văn bản chuẩn hóa (Tab 1) và thống kê + biểu đồ (Tab 2).
4. **Xuất báo cáo** ra file `.txt`.

Có sẵn `samples/sample.txt` để thử nhanh.

## Nhận diện từ ghép (pyvi)
Tính năng nhận diện từ ghép ưu tiên dùng thư viện **pyvi** (bộ tách từ tiếng Việt
học máy) để nhận diện chính xác mọi từ ghép. Nếu không cài được pyvi, ứng dụng **tự
động fallback** về từ điển tĩnh trong [config.py](config.py) và vẫn chạy bình thường.
Dòng trạng thái khi khởi động cho biết engine nào đang hoạt động.

Chi tiết các tính năng chuẩn hóa nâng cao: xem [BAO_CAO.md](BAO_CAO.md).
