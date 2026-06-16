"""Điểm khởi động + Controller của ứng dụng Phân tích văn bản.

Controller điều phối giữa tầng View (ui/main_window.py) và tầng nghiệp vụ
(core/analyzer.py, utils/file_handler.py). View không biết gì về logic; Core không
biết gì về UI — mọi liên kết nằm tại đây.
"""
from tkinter import filedialog, messagebox

import config
from core import analyzer, preprocessor
from ui.main_window import MainWindow
from utils import file_handler


class Controller:
    def __init__(self):
        self.view = MainWindow(
            on_execute=self.handle_execute,
            on_load_file=self.handle_load_file,
            on_export=self.handle_export,
        )
        self.last_result = None
        # Cho người dùng biết bộ tách từ ghép đang hoạt động ở chế độ nào.
        engine = "pyvi (học máy)" if preprocessor.HAS_PYVI else "từ điển tĩnh"
        self.view.set_status(f"Sẵn sàng. Nhận diện từ ghép: {engine}.")

    # --------------------------------------------------------------- handlers
    def handle_execute(self):
        text = self.view.get_input_text()
        if not text.strip():
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập hoặc tải văn bản trước khi thực thi.")
            return
        opts = self.view.get_options()
        try:
            result = analyzer.analyze(text, **opts)
        except Exception as exc:  # an toàn: không để crash cửa sổ
            messagebox.showerror("Lỗi xử lý", f"Đã xảy ra lỗi khi phân tích:\n{exc}")
            return

        self.last_result = result
        self.view.render_result(result)
        top = result.top_words[0][0] if result.top_words else "—"
        self.view.set_status(
            f"Hoàn tất: {result.word_count:,} từ, {result.sentence_count:,} câu. "
            f"Từ phổ biến nhất: '{top}'."
        )

    def handle_load_file(self):
        path = filedialog.askopenfilename(
            title="Chọn file văn bản", filetypes=config.SUPPORTED_OPEN_TYPES
        )
        if not path:
            return
        try:
            content = file_handler.read_file(path)
        except (ValueError, RuntimeError) as exc:
            messagebox.showerror("Không đọc được file", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file:\n{exc}")
            return
        self.view.set_input_text(content)
        self.view.set_status(f"Đã tải: {path}")

    def handle_export(self):
        if self.last_result is None:
            messagebox.showinfo("Chưa có kết quả", "Hãy bấm 'Thực Thi' để tạo kết quả trước khi xuất.")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu báo cáo", defaultextension=".txt",
            filetypes=[("Tệp văn bản", "*.txt")], initialfile="bao_cao_phan_tich.txt",
        )
        if not path:
            return
        try:
            file_handler.export_report(path, self._build_report(self.last_result))
        except Exception as exc:
            messagebox.showerror("Lỗi", f"Không thể lưu báo cáo:\n{exc}")
            return
        self.view.set_status(f"Đã xuất báo cáo: {path}")
        messagebox.showinfo("Thành công", "Đã xuất báo cáo thành công.")

    # --------------------------------------------------------------- helpers
    @staticmethod
    def _build_report(result) -> str:
        lines = [
            "=" * 48,
            "      BÁO CÁO PHÂN TÍCH VĂN BẢN",
            "=" * 48,
            f"Số từ            : {result.word_count:,}",
            f"Số ký tự         : {result.char_count:,}",
            f"Số ký tự (≠space): {result.char_count_no_space:,}",
            f"Số câu           : {result.sentence_count:,}",
            f"Từ khác nhau     : {result.unique_words:,}",
            "",
            f"TOP {len(result.top_words)} TỪ PHỔ BIẾN NHẤT",
            "-" * 48,
        ]
        for i, (word, freq) in enumerate(result.top_words, 1):
            lines.append(f"{i:>2}. {word:<24} {freq:>6} lần")
        lines += ["", "-" * 48, "VĂN BẢN ĐÃ CHUẨN HÓA", "-" * 48, result.normalized_text]
        return "\n".join(lines)

    def run(self):
        self.view.mainloop()


def main():
    Controller().run()


if __name__ == "__main__":
    main()
