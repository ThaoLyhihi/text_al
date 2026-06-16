"""Khung giao diện chính — Biến thể 2: Sidebar Control (Presentation Layer).

MainWindow là tầng View thuần: dựng layout, thu thập tùy chọn người dùng và render
kết quả. Mọi xử lý nghiệp vụ được ủy thác cho Controller qua các callback truyền vào.
"""
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import config
from ui import components

ctk.set_appearance_mode("dark")


class MainWindow(ctk.CTk):
    def __init__(self, on_execute=None, on_load_file=None, on_export=None):
        super().__init__()
        # Callback do Controller cung cấp.
        self._on_execute = on_execute
        self._on_load_file = on_load_file
        self._on_export = on_export

        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.minsize(*config.WINDOW_MIN_SIZE)
        self.configure(fg_color=config.COLOR_MAIN)

        # Lưới chính: cột trái (sidebar 25%) | cột phải (main 75%).
        self.grid_columnconfigure(0, weight=0, minsize=290)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._stat_cards: dict[str, components.StatCard] = {}
        self._chart_canvas = None

        self._build_sidebar()
        self._build_main_area()

    # ------------------------------------------------------------------ UI build
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=config.COLOR_SECONDARY, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)

        components.SectionTitle(sidebar, "Phân tích văn bản").grid(
            row=0, column=0, sticky="ew", padx=18, pady=(20, 4)
        )
        ctk.CTkLabel(
            sidebar,
            text="Text Analyzer • Dark Theme",
            text_color=config.COLOR_TEXT_MUTED,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 12))

        # --- Khu vực 4: Nút hành động (đặt trên cùng) ---
        components.make_secondary_button(sidebar, "📂  Tải File (.txt / .docx)", self._handle_load).grid(
            row=2, column=0, sticky="ew", padx=18, pady=6
        )
        components.make_primary_button(sidebar, "▶  Thực Thi", self._handle_execute).grid(
            row=3, column=0, sticky="ew", padx=18, pady=6
        )
        components.make_secondary_button(sidebar, "💾  Xuất báo cáo", self._handle_export).grid(
            row=4, column=0, sticky="ew", padx=18, pady=6
        )
        components.make_secondary_button(sidebar, "🗑  Xóa", self._handle_clear).grid(
            row=5, column=0, sticky="ew", padx=18, pady=(6, 16)
        )

        ctk.CTkFrame(sidebar, height=1, fg_color=config.COLOR_BORDER).grid(
            row=6, column=0, sticky="ew", padx=18, pady=4
        )

        # --- Khu vực 3: Tùy chọn ---
        ctk.CTkLabel(
            sidebar,
            text="TÙY CHỌN XỬ LÝ",
            text_color=config.COLOR_TEXT_MUTED,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, "bold"),
            anchor="w",
        ).grid(row=7, column=0, sticky="ew", padx=18, pady=(10, 4))

        self.var_lowercase = ctk.BooleanVar(value=True)
        self.var_strip_punct = ctk.BooleanVar(value=True)
        self.var_expand_abbr = ctk.BooleanVar(value=True)
        self.var_compounds = ctk.BooleanVar(value=True)
        self.var_counts = ctk.BooleanVar(value=True)
        self.var_top_n = ctk.BooleanVar(value=True)

        self._add_checkbox(sidebar, 8, "Chuyển thành chữ thường", self.var_lowercase)
        self._add_checkbox(sidebar, 9, "Xóa bỏ toàn bộ dấu câu", self.var_strip_punct)
        self._add_checkbox(sidebar, 10, "Chuẩn hóa từ viết tắt (ko → không)", self.var_expand_abbr)
        self._add_checkbox(sidebar, 11, "Nhận diện từ ghép (học sinh, việt nam)", self.var_compounds)
        self._add_checkbox(sidebar, 12, "Thống kê số lượng (từ, ký tự, câu)", self.var_counts)
        self._add_checkbox(sidebar, 13, "Tìm Top N từ phổ biến", self.var_top_n)

        # Ô nhập N.
        n_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        n_frame.grid(row=14, column=0, sticky="ew", padx=40, pady=(2, 14))
        ctk.CTkLabel(
            n_frame, text="Giá trị N:", text_color=config.COLOR_TEXT,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        ).pack(side="left")
        self.entry_n = ctk.CTkEntry(n_frame, width=70, justify="center")
        self.entry_n.insert(0, str(config.DEFAULT_N))
        self.entry_n.pack(side="left", padx=8)

        # Thanh trạng thái.
        self.status_label = ctk.CTkLabel(
            sidebar, text="Sẵn sàng.", text_color=config.COLOR_TEXT_MUTED,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), anchor="w", wraplength=250,
        )
        self.status_label.grid(row=15, column=0, sticky="sew", padx=18, pady=(10, 14))
        sidebar.grid_rowconfigure(15, weight=1)

    def _add_checkbox(self, master, row, text, variable):
        ctk.CTkCheckBox(
            master, text=text, variable=variable,
            text_color=config.COLOR_TEXT, fg_color=config.COLOR_EXECUTE,
            hover_color=config.COLOR_EXECUTE_HOVER,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        ).grid(row=row, column=0, sticky="w", padx=20, pady=4)

    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color=config.COLOR_MAIN, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)  # Khu vực 1 (nhập)
        main.grid_rowconfigure(1, weight=1)  # Tabs (xuất + biểu đồ)

        # --- Nửa trên: Khu vực 1 — văn bản gốc ---
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=1)
        components.SectionTitle(top, "1 • Văn bản gốc").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.input_text = ctk.CTkTextbox(
            top, fg_color=config.COLOR_SECONDARY, text_color=config.COLOR_TEXT,
            border_width=1, border_color=config.COLOR_BORDER,
            font=(config.FONT_FAMILY_MONO, config.FONT_SIZE_NORMAL), wrap="word",
        )
        self.input_text.grid(row=1, column=0, sticky="nsew")

        # --- Nửa dưới: Tab view ---
        self.tabview = ctk.CTkTabview(
            main, fg_color=config.COLOR_SECONDARY,
            segmented_button_selected_color=config.COLOR_EXECUTE,
            segmented_button_selected_hover_color=config.COLOR_EXECUTE_HOVER,
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 16))
        tab_norm = self.tabview.add("2 • Văn bản đã chuẩn hóa")
        tab_stats = self.tabview.add("Thống kê & Biểu đồ")

        # Tab 1: văn bản chuẩn hóa (read-only).
        tab_norm.grid_columnconfigure(0, weight=1)
        tab_norm.grid_rowconfigure(0, weight=1)
        self.output_text = ctk.CTkTextbox(
            tab_norm, fg_color=config.COLOR_CARD, text_color=config.COLOR_TEXT,
            font=(config.FONT_FAMILY_MONO, config.FONT_SIZE_NORMAL), wrap="word",
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")
        self.output_text.configure(state="disabled")

        # Tab 2: cards + biểu đồ.
        tab_stats.grid_columnconfigure(0, weight=1)
        tab_stats.grid_rowconfigure(1, weight=1)

        cards = ctk.CTkFrame(tab_stats, fg_color="transparent")
        cards.grid(row=0, column=0, sticky="ew", pady=(6, 10))
        for i in range(4):
            cards.grid_columnconfigure(i, weight=1)
        self._stat_cards["words"] = components.StatCard(cards, "Số từ")
        self._stat_cards["chars"] = components.StatCard(cards, "Số ký tự")
        self._stat_cards["sentences"] = components.StatCard(cards, "Số câu")
        self._stat_cards["unique"] = components.StatCard(cards, "Từ khác nhau")
        for i, key in enumerate(("words", "chars", "sentences", "unique")):
            self._stat_cards[key].grid(row=0, column=i, sticky="ew", padx=6)

        self.chart_frame = ctk.CTkFrame(tab_stats, fg_color=config.COLOR_CARD, corner_radius=10)
        self.chart_frame.grid(row=1, column=0, sticky="nsew", pady=(4, 4))
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self._chart_placeholder = ctk.CTkLabel(
            self.chart_frame, text="Biểu đồ Top N sẽ hiển thị sau khi Thực Thi.",
            text_color=config.COLOR_TEXT_MUTED, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        )
        self._chart_placeholder.grid(row=0, column=0)

    # ------------------------------------------------------------- callbacks
    def _handle_execute(self):
        if self._on_execute:
            self._on_execute()

    def _handle_load(self):
        if self._on_load_file:
            self._on_load_file()

    def _handle_export(self):
        if self._on_export:
            self._on_export()

    def _handle_clear(self):
        self.input_text.delete("1.0", "end")
        self.set_output_text("")
        for card in self._stat_cards.values():
            card.set_value(0)
        self._render_chart([])
        self.set_status("Đã xóa.")

    # ------------------------------------------------------------- View API
    def get_input_text(self) -> str:
        return self.input_text.get("1.0", "end-1c")

    def set_input_text(self, text: str) -> None:
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", text)

    def set_output_text(self, text: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.configure(state="disabled")

    def get_options(self) -> dict:
        """Đọc tùy chọn người dùng. N không hợp lệ → DEFAULT_N."""
        raw = self.entry_n.get().strip()
        try:
            n = int(raw)
            if n <= 0:
                raise ValueError
        except ValueError:
            n = config.DEFAULT_N
            self.entry_n.delete(0, "end")
            self.entry_n.insert(0, str(n))
        return {
            "lowercase": self.var_lowercase.get(),
            "strip_punct": self.var_strip_punct.get(),
            "expand_abbr": self.var_expand_abbr.get(),
            "detect_compounds": self.var_compounds.get(),
            "do_counts": self.var_counts.get(),
            "do_top_n": self.var_top_n.get(),
            "top_n": n,
        }

    def set_status(self, text: str) -> None:
        self.status_label.configure(text=text)

    def render_result(self, result) -> None:
        """Đổ AnalysisResult ra Tab văn bản, các StatCard và biểu đồ."""
        self.set_output_text(result.normalized_text)
        self._stat_cards["words"].set_value(f"{result.word_count:,}")
        self._stat_cards["chars"].set_value(f"{result.char_count:,}")
        self._stat_cards["sentences"].set_value(f"{result.sentence_count:,}")
        self._stat_cards["unique"].set_value(f"{result.unique_words:,}")
        self._render_chart(result.top_words)

    def _render_chart(self, top_words) -> None:
        # Dọn canvas/placeholder cũ.
        if self._chart_canvas is not None:
            self._chart_canvas.get_tk_widget().destroy()
            self._chart_canvas = None
        if self._chart_placeholder is not None:
            self._chart_placeholder.grid_forget()

        if not top_words:
            self._chart_placeholder.grid(row=0, column=0)
            return

        words = [w for w, _ in top_words][::-1]
        counts = [c for _, c in top_words][::-1]

        fig = Figure(figsize=(6, 3.4), dpi=100, facecolor=config.COLOR_CARD)
        ax = fig.add_subplot(111)
        ax.set_facecolor(config.COLOR_CARD)
        bars = ax.barh(words, counts, color=config.COLOR_ACCENT)
        ax.set_title("Top từ phổ biến", color=config.COLOR_TEXT, fontsize=12)
        ax.tick_params(colors=config.COLOR_TEXT, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(config.COLOR_BORDER)
        ax.bar_label(bars, padding=3, color=config.COLOR_TEXT, fontsize=8)
        ax.margins(x=0.12)
        fig.tight_layout()

        self._chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
