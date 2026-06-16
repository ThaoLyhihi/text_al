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
# Từ viết tắt thông dụng → dạng đầy đủ (dùng cho chuẩn hóa)
# ---------------------------------------------------------------------------
# Khóa luôn ở chữ thường; việc so khớp thực hiện trên token đã hạ chữ thường.
ABBREVIATIONS = {
    "ko": "không", "k": "không", "kg": "không", "khg": "không", "hok": "không",
    "đc": "được", "dc": "được", "dk": "được", "đk": "được",
    "vs": "với", "v": "với",
    "ng": "người", "ngta": "người ta",
    "bn": "bao nhiêu", "ntn": "như thế nào",
    "j": "gì", "z": "vậy", "zậy": "vậy",
    "wa": "quá", "qá": "quá", "qa": "quá",
    "bik": "biết", "bít": "biết", "bjt": "biết",
    "trc": "trước", "hnay": "hôm nay", "hqua": "hôm qua",
    "ace": "anh chị em", "ad": "admin", "tks": "cảm ơn", "thanks": "cảm ơn",
    "mn": "mọi người", "mng": "mọi người", "ae": "anh em",
    "sgk": "sách giáo khoa", "đh": "đại học", "thpt": "trung học phổ thông",
    "thcs": "trung học cơ sở", "hs": "học sinh", "sv": "sinh viên", "gv": "giáo viên",
    "vn": "việt nam", "tp": "thành phố", "hcm": "hồ chí minh",
    "cntt": "công nghệ thông tin",
}

# ---------------------------------------------------------------------------
# Từ ghép tiếng Việt 2 tiếng — gộp thành một đơn vị khi thống kê tần suất
# ---------------------------------------------------------------------------
# Mỗi phần tử là một cụm 2 tiếng (chữ thường, không dấu câu). Khi bật tùy chọn,
# các cụm này được nối bằng dấu '_' để Counter coi là một "từ" duy nhất.
COMPOUND_WORDS = [
    "học sinh", "sinh viên", "giáo viên", "giảng viên", "đại học",
    "việt nam", "hà nội", "hồ chí minh", "thành phố", "đất nước", "quê hương",
    "công nghệ", "thông tin", "máy tính", "phần mềm", "phần cứng", "dữ liệu",
    "trí tuệ", "nhân tạo", "lập trình", "khoa học", "kỹ thuật", "công nghiệp",
    "kinh tế", "xã hội", "chính trị", "văn hóa", "giáo dục", "y tế",
    "gia đình", "bạn bè", "thầy cô", "bố mẹ", "ông bà", "anh em",
    "cuộc sống", "công việc", "thời gian", "không gian", "môi trường", "tự nhiên",
    "hạnh phúc", "ước mơ", "tương lai", "hiện tại", "quá khứ",
    "phát triển", "tiến bộ", "hòa bình", "độc lập", "tự do", "thành công",
]

# Ký tự nối hai tiếng của một từ ghép trong văn bản đã chuẩn hóa.
COMPOUND_JOINER = "_"

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
