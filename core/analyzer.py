"""Tầng phân tích & thống kê văn bản (Business Logic Layer).

Cung cấp các phép đếm O(N) và trích xuất Top N từ phổ biến bằng collections.Counter.
Thuần Python — không import UI.
"""
import re
from collections import Counter
from dataclasses import dataclass, field

import config
from core import preprocessor


@dataclass
class AnalysisResult:
    """Gói toàn bộ kết quả phân tích để Controller/UI tiêu thụ."""
    normalized_text: str = ""
    char_count: int = 0           # Đếm trên văn bản gốc (gồm khoảng trắng)
    char_count_no_space: int = 0  # Không tính khoảng trắng
    word_count: int = 0
    sentence_count: int = 0
    unique_words: int = 0
    top_words: list = field(default_factory=list)  # list[tuple[str, int]]


def count_characters(text: str) -> tuple[int, int]:
    """Đếm ký tự trên văn bản GỐC (trước chuẩn hóa) để giữ độ chính xác.

    Trả về (tổng_ký_tự, ký_tự_không_tính_khoảng_trắng).
    """
    total = len(text)
    no_space = len(re.sub(r"\s", "", text))
    return total, no_space


def count_sentences(text: str) -> int:
    """Đếm số câu dựa trên các dấu kết thúc câu '.', '?', '!'.

    Một chuỗi liên tiếp các dấu kết thúc (vd '?!', '...') chỉ tính là một câu.
    Văn bản không rỗng nhưng thiếu dấu kết thúc vẫn được tính là 1 câu.
    """
    terminators = set(config.SENTENCE_TERMINATORS)
    count = 0
    prev_was_terminator = False
    has_content = False
    for ch in text:
        if not ch.isspace():
            has_content = True
        if ch in terminators:
            if not prev_was_terminator:
                count += 1
            prev_was_terminator = True
        else:
            prev_was_terminator = False
    # Có nội dung nhưng không kết thúc bằng dấu câu → tính phần còn lại là 1 câu.
    if has_content and not text.rstrip().endswith(tuple(terminators)):
        count += 1
    return count


def get_word_frequencies(normalized_text: str) -> Counter:
    """Đếm tần suất từ trên văn bản ĐÃ chuẩn hóa bằng Counter — O(N)."""
    words = normalized_text.split()
    return Counter(words)


def analyze(
    text: str,
    lowercase: bool = True,
    strip_punct: bool = True,
    do_counts: bool = True,
    do_top_n: bool = True,
    top_n: int = config.DEFAULT_N,
) -> AnalysisResult:
    """Hàm điều phối phân tích chính.

    Đếm số liệu thô trên văn bản gốc trước, rồi chuẩn hóa và thống kê tần suất.
    Mọi nhánh đều O(N), không có vòng lặp lồng nhau.
    """
    result = AnalysisResult()

    # 1) Đếm số liệu thô trên văn bản GỐC.
    if do_counts:
        result.char_count, result.char_count_no_space = count_characters(text)
        result.sentence_count = count_sentences(text)

    # 2) Chuẩn hóa.
    result.normalized_text = preprocessor.normalize(
        text, lowercase=lowercase, strip_punct=strip_punct
    )

    # 3) Tần suất từ (dùng cho cả word_count và top_n).
    freqs = get_word_frequencies(result.normalized_text)
    if do_counts:
        result.word_count = sum(freqs.values())
        result.unique_words = len(freqs)

    # 4) Top N.
    if do_top_n:
        n = top_n if isinstance(top_n, int) and top_n > 0 else config.DEFAULT_N
        result.top_words = freqs.most_common(n)

    return result
