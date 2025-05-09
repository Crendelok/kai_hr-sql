# table_view.py

import customtkinter as ctk
from tkinter import ttk

class TableView(ctk.CTkFrame):
    def __init__(self, master, columns, data=None, height=300, on_select=None):
        super().__init__(master)

        self.columns = columns
        self.data = data or []
        self.on_select = on_select

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=height)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Додаємо колонки
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Подія вибору
        if self.on_select:
            self.tree.bind("<<TreeviewSelect>>", lambda e: self.on_select(self.get_selected()))

        # Стилізація (не обов'язково, але покращує вигляд)
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

    def populate(self, rows):
        # Очистити старі дані
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Додати нові дані
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]
