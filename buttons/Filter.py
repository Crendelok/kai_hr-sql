import customtkinter as ctk
from typing import Callable, List

import customtkinter as ctk

class Filter(ctk.CTkButton):
    """
    A button that opens a filter dialog when clicked.
    Usage:
        btn = FilterWidget(parent, columns, callback)
        btn.pack(...)
    """
    def __init__(self, parent, columns: List[str], on_apply: Callable, **kwargs):
        """
        :param parent:    the parent CTk window or frame
        :param columns:   list of column names to choose from
        :param on_apply:  callback fn(column: str, value: str)
        """
        super().__init__(parent, text="Фільтрація", command=self._open_popup, **kwargs)
        self.columns = columns
        self.on_apply = on_apply
        self.parent = parent

    def _open_popup(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Фільтр")
        popup.geometry("300x200")

        ctk.CTkLabel(popup, text="Фільтрувати по:").pack(pady=(20, 5))
        col_menu = ctk.CTkOptionMenu(popup, values=self.columns)
        col_menu.pack()

        ctk.CTkLabel(popup, text="Значиння").pack(pady=(15, 5))
        value_entry = ctk.CTkEntry(popup)
        value_entry.pack()

        def _apply():
            column = col_menu.get()
            value = value_entry.get()
            self.on_apply(column, value)
            popup.destroy()

        ctk.CTkButton(popup, text="Застосувати", command=_apply).pack(pady=20)
