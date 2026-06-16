"""Tầng chuẩn hóa chuỗi (Business Logic Layer).

Thuần Python, không phụ thuộc thư viện UI → dễ viết unit test.
"""
import re

import config

# pyvi là tùy chọn: nếu cài được thì dùng bộ tách từ học máy (CRF) để nhận diện
# MỌI từ ghép tiếng Việt; nếu không, tự động fallback về từ điển tĩnh bên dưới.
try:
    from pyvi import ViTokenizer

    HAS_PYVI = True
except ImportError:  # pragma: no cover - phụ thuộc vào môi trường cài đặt
    ViTokenizer = None
    HAS_PYVI = False

# Biên dịch sẵn regex một lần để tái sử dụng (nhanh hơn khi gọi nhiều lần).
_PUNCT_RE = re.compile(config.REGEX_PUNCTUATION, re.UNICODE)

# Biên dịch sẵn một regex duy nhất khớp mọi cụm từ ghép (chữ thường) —
# sắp xếp cụm dài trước để ưu tiên khớp cụm dài nhất. O(N) trên độ dài văn bản.
_COMPOUND_RE = re.compile(
    r"\b(?:%s)\b"
    % "|".join(
        re.escape(c) for c in sorted(set(config.COMPOUND_WORDS), key=len, reverse=True)
    ),
    re.UNICODE,
)

# Regex khớp từ viết tắt ở dạng từ hoàn chỉnh (\b), không phân biệt hoa/thường —
# nhờ vậy 'hs.' hay 'KO,' vẫn được mở rộng mà không phá ký tự dấu câu xung quanh.
_ABBR_RE = re.compile(
    r"\b(?:%s)\b"
    % "|".join(
        re.escape(a) for a in sorted(config.ABBREVIATIONS, key=len, reverse=True)
    ),
    re.UNICODE | re.IGNORECASE,
)


def to_lowercase(text: str) -> str:
    """Chuyển toàn bộ văn bản về chữ thường."""
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Loại bỏ toàn bộ dấu câu/punctuation, giữ lại chữ-số-khoảng trắng.

    Dùng regex đã biên dịch sẵn → O(N).
    """
    return _PUNCT_RE.sub(" ", text)


def expand_abbreviations(text: str) -> str:
    """Thay thế từ viết tắt thông dụng bằng dạng đầy đủ (vd 'ko' → 'không').

    Khớp theo ranh giới từ (\\b) và không phân biệt hoa/thường nên giữ nguyên dấu
    câu xung quanh ('hs.' vẫn nở thành 'học sinh.') và không đụng vào từ chứa chuỗi
    viết tắt như một phần con. O(N) trên độ dài văn bản.
    """
    return _ABBR_RE.sub(lambda m: config.ABBREVIATIONS[m.group(0).lower()], text)


def _join_compounds_dict(text: str) -> str:
    """Fallback: nối từ ghép dựa trên từ điển tĩnh COMPOUND_WORDS bằng regex."""
    return _COMPOUND_RE.sub(lambda m: m.group(0).replace(" ", config.COMPOUND_JOINER), text)


def _join_compounds_pyvi(text: str) -> str:
    """Tách từ bằng pyvi (CRF). pyvi đã nối các tiếng của từ ghép bằng '_'.

    Chuẩn hóa ký tự nối về COMPOUND_JOINER để đồng nhất với phần còn lại của hệ thống.
    """
    tokenized = ViTokenizer.tokenize(text)
    if config.COMPOUND_JOINER != "_":
        tokenized = tokenized.replace("_", config.COMPOUND_JOINER)
    return tokenized


def normalize(
    text: str,
    lowercase: bool = True,
    strip_punct: bool = True,
    expand_abbr: bool = False,
    detect_compounds: bool = False,
) -> str:
    """Chạy pipeline chuẩn hóa theo các tùy chọn được bật.

    Thứ tự được thiết kế để bộ tách từ pyvi đạt độ chính xác cao nhất:
        1) Mở rộng viết tắt (giữ nguyên dấu câu & hoa/thường để pyvi có ngữ cảnh).
        2) Nhận diện từ ghép — pyvi cần dấu câu & chữ hoa (vd 'Việt Nam') nên chạy
           TRƯỚC khi bỏ dấu câu/hạ chữ thường. Bản fallback từ điển chạy SAU đó.
        3) Bỏ dấu câu (ký tự '_' nối từ ghép vẫn được giữ vì là ký tự chữ).
        4) Hạ chữ thường.
        5) Gộp khoảng trắng thừa.
    """
    if expand_abbr:
        text = expand_abbreviations(text)
    # pyvi: tách từ trên văn bản còn nguyên dấu câu & hoa/thường.
    if detect_compounds and HAS_PYVI:
        text = _join_compounds_pyvi(text)
    if strip_punct:
        text = remove_punctuation(text)
    if lowercase:
        text = to_lowercase(text)
    # Fallback từ điển tĩnh: cần văn bản đã sạch dấu & chữ thường để khớp ổn định.
    if detect_compounds and not HAS_PYVI:
        text = _join_compounds_dict(text if lowercase else to_lowercase(text))
    # Gộp mọi khoảng trắng liên tiếp (gồm cả xuống dòng) thành một dấu cách.
    text = re.sub(r"\s+", " ", text).strip()
    return text
