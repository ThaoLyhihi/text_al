"""Tầng tiện ích đọc/ghi file (Utility Layer).

Hỗ trợ đọc .txt và .docx, xuất báo cáo .txt. Mã hóa UTF-8 để giữ tiếng Việt có dấu.
"""
import os


def read_file(path: str) -> str:
    """Đọc nội dung văn bản từ file .txt hoặc .docx.

    Raises:
        ValueError: định dạng không hỗ trợ.
        RuntimeError: thiếu thư viện python-docx khi đọc .docx.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return _read_txt(path)
    if ext == ".docx":
        return _read_docx(path)
    raise ValueError(f"Định dạng không được hỗ trợ: '{ext}'. Chỉ chấp nhận .txt hoặc .docx.")


def _read_txt(path: str) -> str:
    # errors='replace' để không crash với file mã hóa lạ.
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _read_docx(path: str) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError(
            "Cần cài 'python-docx' để đọc file .docx (pip install python-docx)."
        ) from exc
    document = Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def export_report(path: str, report_text: str) -> None:
    """Ghi báo cáo thống kê ra file .txt (UTF-8)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
