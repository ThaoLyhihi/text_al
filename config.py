"""Cấu hình tập trung cho toàn ứng dụng Phân tích văn bản.

Mọi hằng số về màu sắc, font, giá trị mặc định và regex được khai báo tại đây để
các tầng khác (ui/, core/) import dùng chung, tránh "magic value" rải rác.
"""

# ---------------------------------------------------------------------------
# Bảng màu Dark Theme (phong cách VS Code / Discord)
# ---------------------------------------------------------------------------
COLOR_MAIN = "#2B2D31"          # Nền chủ đạo
COLOR_SECONDARY = "#252526"     # Nền Text Area / Sidebar
COLOR_BORDER = "#3E3E42"        # Đường viền phân chia
COLOR_TEXT = "#F2F3F5"          # Màu chữ chính
COLOR_TEXT_MUTED = "#9AA0A6"    # Màu chữ phụ (label, chú thích)
COLOR_EXECUTE = "#238636"       # Nút "Thực thi"
COLOR_EXECUTE_HOVER = "#2EA043"
COLOR_SECONDARY_BTN = "#3A3D41"  # Nút phụ
COLOR_SECONDARY_BTN_HOVER = "#4A4D51"
COLOR_CARD = "#313338"          # Nền các StatCard
COLOR_ACCENT = "#0E639C"        # Màu nhấn (biểu đồ, tiêu đề card)

# ---------------------------------------------------------------------------
# Font chữ
# ---------------------------------------------------------------------------
FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 13
FONT_SIZE_TITLE = 18
FONT_SIZE_CARD_VALUE = 26
FONT_FAMILY_MONO = "Consolas"

# ---------------------------------------------------------------------------
# Giá trị mặc định nghiệp vụ
# ---------------------------------------------------------------------------
DEFAULT_N = 10                  # Số lượng từ phổ biến hiển thị mặc định

# ---------------------------------------------------------------------------
# Regular Expression dùng cho chuẩn hóa & tách câu
# ---------------------------------------------------------------------------
# Loại bỏ mọi ký tự KHÔNG phải chữ-số-khoảng trắng (giữ tiếng Việt có dấu nhờ \w + re.UNICODE).
REGEX_PUNCTUATION = r"[^\w\s]"
# Ký tự kết thúc câu.
SENTENCE_TERMINATORS = ".?!"

# ---------------------------------------------------------------------------
# Cấu hình cửa sổ
# ---------------------------------------------------------------------------
APP_TITLE = "Phân tích văn bản — Text Analyzer"
WINDOW_SIZE = "1180x720"
WINDOW_MIN_SIZE = (940, 600)

# Định dạng file được hỗ trợ khi mở
SUPPORTED_OPEN_TYPES = [
    ("Văn bản & Word", "*.txt *.docx"),
    ("Tệp văn bản", "*.txt"),
    ("Tài liệu Word", "*.docx"),
    ("Tất cả", "*.*"),
]
