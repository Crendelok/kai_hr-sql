import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from typing import List, Callable

class Importing(ctk.CTkButton):
    """
    A button that exports a 2D list of strings to an Excel (.xlsx) file.

    Usage:
        btn = Importing(parent, data_callable, columns)
    """
    def __init__(self,
                 parent,
                 data_source: Callable[[], List[List[str]]],
                 columns: List[str],
                 text: str = "Експорт",
                 default_filename: str = "table.xlsx",
                 **kwargs):
        """
        :param parent: Parent CTk widget
        :param data_source: Callable returning current table data as List of rows
        :param columns: List of column names for header row in Excel
        :param text: Button text
        :param default_filename: Suggested filename in save dialog
        """
        super().__init__(parent, text=text, command=self._export, **kwargs)
        self.parent = parent
        self.data_source = data_source
        self.columns = columns
        self.default_filename = default_filename

    def _export(self):
        file_path = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*")],
            initialfile=self.default_filename,
            title="Save as Excel"
        )
        if not file_path:
            return
        try:
            data = self.data_source()
            df = pd.DataFrame(data, columns=self.columns)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Успіх", f"Експортовано до {file_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося експортувати: {e}")
