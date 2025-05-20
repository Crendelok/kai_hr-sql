from typing import List, Callable

import customtkinter as ctk

class Sort(ctk.CTkButton):
    def __init__(self, parent, columns: List[str], on_apply: Callable, **kwargs):
        super().__init__(parent, text="Сортурування", command=self._open_popup, **kwargs)
        self.columns = columns
        self.on_apply = on_apply
        self.parent = parent

    def _open_popup(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Sort")
        popup.geometry("300x250")

        ctk.CTkLabel(popup, text="Сортувати за:").pack(pady=(20, 5))
        col_menu = ctk.CTkOptionMenu(popup, values=self.columns)
        col_menu.pack()

        ctk.CTkLabel(popup, text="Порядок:").pack(pady=(15, 5))
        order_var = ctk.StringVar(value="ASC")
        ctk.CTkRadioButton(popup, text="Від найменьшого", variable=order_var, value="ASC").pack()
        ctk.CTkRadioButton(popup, text="Від найбільного", variable=order_var, value="DESC").pack()

        def _apply():
            column = col_menu.get()
            order = order_var.get()
            self.on_apply(column, order)
            popup.destroy()

        ctk.CTkButton(popup, text="Apply", command=_apply).pack(pady=20)
