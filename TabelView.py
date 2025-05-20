import customtkinter as ctk
from tkinter import ttk

class TableView(ctk.CTkFrame):
    def __init__(self, master, columns, column_headers, data=None, height=300, on_select=None):
        """
        Args:
            master: Parent widget
            columns (list[str]): List of data keys for each column
            column_headers (list[str]): List of display names for each column header
            data (list[dict], optional): Initial data rows
            height (int, optional): Number of visible rows
            on_select (callable, optional): Callback for row selection
        """
        super().__init__(master)

        self.columns = columns
        self.keys = columns
        self.data = data or []
        self.on_select = on_select
        self.data_now = []

        # Create the Treeview
        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show='headings',
            height=height
        )
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Set up headings and column properties
        for col, header in zip(self.columns, column_headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=120)

        # Bind selection event if provided
        if self.on_select:
            self.tree.bind(
                "<<TreeviewSelect>>",
                lambda e: self.on_select(self.get_selected())
            )

        # Optional styling: increase row height
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Populate initial data if any
        if self.data:
            self.populate(self.data)

    def populate(self, rows: list[dict]):
        """Clear existing rows and insert new data rows."""
        self.tree.delete(*self.tree.get_children())
        self.data = rows
        for row in rows:
            values = [row.get(key, "") for key in self.keys]
            self.tree.insert("", "end", values=values)

    def get_selected(self):
        """Return the values of the currently selected row, or None if no selection."""
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]
