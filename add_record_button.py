import customtkinter as ctk
from typing import List

class AddRecordButton(ctk.CTkButton):
    def __init__(self, master, fields: List[str], on_submit, button_text="Додати запис"):
        super().__init__(master, text=button_text, command=self.open_form)
        self.fields = fields
        self.on_submit = on_submit

    def open_form(self):
        AddFormWindow(self.fields, self.on_submit)


class AddFormWindow(ctk.CTkToplevel):
    def __init__(self, fields: List[str], on_submit):
        super().__init__()
        self.title("Додати запис")
        self.geometry("600x600")
        self.fields = fields
        self.on_submit = on_submit
        self.entries = {}

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=20, pady=20)

        for i, field in enumerate(fields):
            label = ctk.CTkLabel(form_frame, text=field)
            entry = ctk.CTkEntry(form_frame, placeholder_text=field)
            label.grid(row=i, column=0, sticky="w", pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        submit_btn = ctk.CTkButton(self, text="Зберегти", command=self.submit)
        submit_btn.pack(pady=10)

    def submit(self):
        data = {field: self.entries[field].get() for field in self.fields}
        if any(v.strip() == "" for v in data.values()):
            return  # можна додати попередження
        self.on_submit(data)
        self.destroy()
