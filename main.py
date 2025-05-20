# main.py

import customtkinter as ctk

from db_connector import all_models
from models import BaseModel
from top_bar import top_bar_UI
from views.GenericTableFrame import GenericTableFrame


class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Відділ кадрів")
        self.geometry("1200x1200")
        self.resizable(True, True)


        (self.depatment,
         self.positions,
         self.employees,
         self.leave_requests,
         self.employeesActions,
         self.users
         ) = all_models()


        top_bar_UI(self, self.open_department, self.open_positions, self.open_employees, self.open_employees_actions, self.open_leave_requests)

        self.content_frame = None
        self.center = ctk.CTkFrame(self)
        self.center.pack(fill="both", expand=True)

    def clear_center(self):
        if self.content_frame:
            self.content_frame.destroy()
            self.content_frame = None

    def open_view(self, model: BaseModel, tittle: str):
        self.clear_center()
        self.content_frame = GenericTableFrame(self.center, model, tittle)
        self.content_frame.pack(fill="both", expand=True)


    def open_department(self):
        self.open_view(self.depatment, "Департамент")

    def open_positions(self):
        self.open_view(self.positions, "Посади")

    def open_employees(self):
        self.open_view(self.employees, "Персонал")

    def open_employees_actions(self):
        self.open_view(self.employeesActions, "Лог змін")

    def open_leave_requests(self):
        self.open_view(self.leave_requests, "Лог Відсутності")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # або "dark"
    ctk.set_default_color_theme("blue")
    app = HotelApp()
    app.mainloop()
