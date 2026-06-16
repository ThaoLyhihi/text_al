# BÁO CÁO BỔ SUNG TÍNH NĂNG — PHÂN TÍCH VĂN BẢN

> Tài liệu mô tả hai tính năng chuẩn hóa nâng cao được bổ sung cho ứng dụng
> *Phân tích văn bản (Text Analyzer)*: **chuẩn hóa từ viết tắt thông dụng** và
> **nhận diện từ ghép tiếng Việt**, cùng việc tích hợp thư viện **pyvi**.

---

## 1. Mục tiêu

| # | Tính năng | Mô tả |
|---|-----------|-------|
| 1 | Chuẩn hóa từ viết tắt | Tự động mở rộng các từ viết tắt/teen-code thông dụng về dạng đầy đủ (vd `ko` → `không`, `đc` → `được`, `hs` → `học sinh`). |
| 2 | Nhận diện từ ghép | Coi từ ghép tiếng Việt cấu tạo từ nhiều tiếng (vd `học sinh`, `việt nam`) là **một đơn vị** khi thống kê tần suất, thay vì tách rời thành các từ đơn. |

Hai tính năng giúp kết quả thống kê tần suất từ phản ánh đúng ngữ nghĩa tiếng Việt
hơn — `học sinh` được đếm như một khái niệm thay vì hai từ `học` và `sinh` rời rạc.

---

## 2. Kiến trúc & vị trí thay đổi

Ứng dụng giữ nguyên kiến trúc phân lớp; các thay đổi được đặt đúng tầng:

| Tầng | File | Thay đổi |
|------|------|----------|
| Cấu hình | `config.py` | Thêm từ điển `ABBREVIATIONS`, danh sách `COMPOUND_WORDS`, hằng `COMPOUND_JOINER`. |
| Logic | `core/preprocessor.py` | Thêm `expand_abbreviations()`, `join_compounds()` (+ pyvi/fallback); cập nhật `normalize()`. |
| Logic | `core/analyzer.py` | `analyze()` nhận thêm tham số `expand_abbr`, `detect_compounds`; nhãn Top N hiển thị thân thiện. |
| Giao diện | `ui/main_window.py` | Thêm 2 checkbox tùy chọn; cập nhật `get_options()`. |
| Controller | `main.py` | Hiển thị engine tách từ đang dùng khi khởi động. |
| Phụ thuộc | `requirements.txt` | Thêm `pyvi` (tùy chọn). |

---

## 3. Chi tiết kỹ thuật

### 3.1. Chuẩn hóa từ viết tắt

- Từ điển `ABBREVIATIONS` (khóa chữ thường) ánh xạ viết tắt → dạng đầy đủ.
- Hàm `expand_abbreviations()` dùng **một regex biên dịch sẵn** khớp theo ranh giới
  từ (`\b`), không phân biệt hoa/thường. Nhờ vậy:
  - Viết tắt dính dấu câu vẫn được mở rộng: `hs.` → `học sinh.`, `KO,` → `không,`.
  - Không đụng vào từ chứa chuỗi viết tắt như một phần con.
- Độ phức tạp: **O(N)** theo độ dài văn bản.

### 3.2. Nhận diện từ ghép — pyvi + fallback

Hàm `join_compounds()` nối các tiếng của một từ ghép bằng dấu `_` để tầng đếm
(`collections.Counter`) coi cụm đó là một "từ" duy nhất. Có **hai engine**:

| Engine | Khi nào dùng | Phạm vi |
|--------|--------------|---------|
| **pyvi** (`ViTokenizer`) | Khi import được thư viện | Mọi từ ghép tiếng Việt, kể cả 3+ tiếng (`công nghệ thông tin`). Dùng mô hình CRF. |
| Từ điển tĩnh (`COMPOUND_WORDS`) | Khi thiếu pyvi (fallback) | Giới hạn trong danh sách định nghĩa sẵn; dùng regex. |

Cờ `HAS_PYVI` được xác định một lần khi import (`try/except ImportError`), đảm bảo
ứng dụng **không bao giờ crash** vì thiếu thư viện.

### 3.3. Thứ tự pipeline trong `normalize()` — điểm mấu chốt

pyvi cần **dấu câu và chữ hoa** làm ngữ cảnh để tách từ chính xác (vd nhận diện
danh từ riêng `Việt Nam`). Do đó thứ tự được thiết kế lại:

```
1) Mở rộng viết tắt        (giữ nguyên dấu câu & hoa/thường)
2) Nhận diện từ ghép (pyvi) (chạy TRƯỚC khi bỏ dấu câu / hạ chữ thường)
3) Bỏ dấu câu              (ký tự '_' được giữ vì là ký tự chữ)
4) Hạ chữ thường
5) Gộp khoảng trắng thừa
```

> Bản fallback từ điển tĩnh cần văn bản đã sạch dấu + chữ thường nên chạy ở **bước 4.5**
> (sau khi hạ chữ thường).

---

## 4. Kết quả minh họa

**Đầu vào:**
> `Học sinh Việt Nam ko biết gì về công nghệ thông tin, hs trường đh. Việt Nam phát triển.`

**Văn bản chuẩn hóa (pyvi, bật cả 2 tùy chọn):**
> `học_sinh việt_nam không biết gì về công_nghệ thông_tin học_sinh trường đại_học việt_nam phát_triển`

**Top từ phổ biến:**

| Tần suất | Từ |
|:---:|----|
| 2 | học sinh |
| 2 | việt nam |
| 1 | công nghệ |
| 1 | thông tin |
| 1 | đại học |
| 1 | phát triển |

Nhận xét:
- `ko` → `không`; `hs` → `học sinh`; `đh` → `đại học` (chuẩn hóa viết tắt).
- `học sinh`, `việt nam`, `công nghệ`, `thông tin`, `phát triển` được gộp thành một
  đơn vị (nhận diện từ ghép) — `học sinh` và `việt nam` được đếm đúng **2 lần**.
- Hai tính năng phối hợp: `hs` nở thành `học sinh` rồi tiếp tục được gộp như từ ghép.

---

## 5. So sánh hai engine nhận diện từ ghép

| Tiêu chí | Từ điển tĩnh | pyvi |
|----------|--------------|------|
| Phạm vi | Chỉ các cụm định nghĩa sẵn (~52) | Gần như mọi từ ghép tiếng Việt |
| Từ ghép 3+ tiếng | Không | Có |
| Phụ thuộc | Không | `pyvi` + `scikit-learn`, `scipy`... |
| Tốc độ | Tức thì (regex) | Chậm hơn (chạy mô hình CRF) |
| Độ chính xác | Phụ thuộc danh sách | Cao, theo ngữ cảnh |

---

## 6. Hướng phát triển tiếp

- Cho phép người dùng **nạp từ điển viết tắt / từ ghép từ file ngoài** (`.csv`/`.json`).
- Thêm tùy chọn hiển thị từ ghép trong văn bản chuẩn hóa bằng dấu cách thay vì `_`.
- Tận dụng `ViPosTagger` của pyvi để thống kê theo **từ loại** (danh/động/tính từ).
