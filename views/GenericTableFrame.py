import customtkinter as ctk

from TabelView import TableView
from add_record_button import AddRecordButton
from buttons.Filter import Filter
from buttons.Importing import Importing
from buttons.SortButton import Sort
from models import BaseModel


class GenericTableFrame(ctk.CTkFrame):
    def __init__(self, master, model_instance: BaseModel, title_text="Дані"):
        super().__init__(master)
        self.model = model_instance
        self.fields = self.model.fields_for_add or self.model.columns
        self.title_text = title_text

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        title = ctk.CTkLabel(header_frame, text=self.title_text, font=("Arial", 20))
        title.pack(side="left")

        AddRecordButton(
            master=header_frame,
            fields=self.model.fields_for_add(),
            on_submit=self.handle_add_record,
            button_text="➕ Додати запис"
        ).pack(side="right")

        Filter(
            header_frame,
            self.model.fields_for_filtering(),
            lambda col, v: self.table.populate(self.model.filter(col, str(v)))
        ).pack(side="right", padx=10)

        Sort(header_frame, self.model.fields_for_sort(),
             lambda col, ord: self.table.populate(self.model.sort(col, ord))
             ).pack(side="right", padx=10)

        # всередині TableView.__init__
        Importing(header_frame, data_source=lambda: self.table.data, columns=self.model.columns()).pack(side="right", padx=10)

        self.table = TableView(self, self.model.columns(), self.model.column_headers())
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def handle_add_record(self, data):
        self.model.insert(data)
        self.load_data()

    def load_data(self):
        rows = self.model.fetch_all()
        self.table.populate(rows)
