"""Tầng chuẩn hóa chuỗi (Business Logic Layer).

Thuần Python, không phụ thuộc thư viện UI → dễ viết unit test.
"""
import re

import config

# Biên dịch sẵn regex một lần để tái sử dụng (nhanh hơn khi gọi nhiều lần).
_PUNCT_RE = re.compile(config.REGEX_PUNCTUATION, re.UNICODE)


def to_lowercase(text: str) -> str:
    """Chuyển toàn bộ văn bản về chữ thường."""
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Loại bỏ toàn bộ dấu câu/punctuation, giữ lại chữ-số-khoảng trắng.

    Dùng regex đã biên dịch sẵn → O(N).
    """
    return _PUNCT_RE.sub(" ", text)


def normalize(text: str, lowercase: bool = True, strip_punct: bool = True) -> str:
    """Chạy pipeline chuẩn hóa theo các tùy chọn được bật.

    Thứ tự: bỏ dấu câu trước, sau đó hạ chữ thường, rồi gộp khoảng trắng thừa.
    """
    if strip_punct:
        text = remove_punctuation(text)
    if lowercase:
        text = to_lowercase(text)
    # Gộp mọi khoảng trắng liên tiếp (gồm cả xuống dòng) thành một dấu cách.
    text = re.sub(r"\s+", " ", text).strip()
    return text
