"""Các widget tái sử dụng cho giao diện (Presentation Layer)."""
import customtkinter as ctk

import config


class StatCard(ctk.CTkFrame):
    """Thẻ hiển thị một số liệu thống kê: tiêu đề nhỏ + giá trị lớn."""

    def __init__(self, master, title: str, value: str = "0", **kwargs):
        super().__init__(
            master,
            fg_color=config.COLOR_CARD,
            corner_radius=10,
            border_width=1,
            border_color=config.COLOR_BORDER,
            **kwargs,
        )
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            text_color=config.COLOR_TEXT_MUTED,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        )
        self.title_label.pack(padx=14, pady=(12, 0), anchor="w")

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            text_color=config.COLOR_TEXT,
            font=(config.FONT_FAMILY, config.FONT_SIZE_CARD_VALUE, "bold"),
        )
        self.value_label.pack(padx=14, pady=(0, 12), anchor="w")

    def set_value(self, value) -> None:
        self.value_label.configure(text=str(value))


class SectionTitle(ctk.CTkLabel):
    """Nhãn tiêu đề khu vực."""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master,
            text=text,
            text_color=config.COLOR_TEXT,
            font=(config.FONT_FAMILY, config.FONT_SIZE_TITLE, "bold"),
            anchor="w",
            **kwargs,
        )


def make_primary_button(master, text: str, command) -> ctk.CTkButton:
    """Nút hành động chính (xanh lá)."""
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=config.COLOR_EXECUTE,
        hover_color=config.COLOR_EXECUTE_HOVER,
        text_color="#FFFFFF",
        font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, "bold"),
        height=40,
        corner_radius=8,
    )


def make_secondary_button(master, text: str, command) -> ctk.CTkButton:
    """Nút phụ (xám tối)."""
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=config.COLOR_SECONDARY_BTN,
        hover_color=config.COLOR_SECONDARY_BTN_HOVER,
        text_color=config.COLOR_TEXT,
        font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
        height=36,
        corner_radius=8,
    )
