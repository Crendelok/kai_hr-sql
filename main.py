# main.py

import customtkinter as ctk

from db_connector import connect_db
from top_bar import top_bar_UI


class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Відділ кадрів")
        self.geometry("1200x1200")
        self.resizable(True, True)


        self.conn = connect_db()


        top_bar_UI(self, self.open_clients, self.open_rooms, self.open_bookings, self.open_services, self.leave_requests)

        self.content_frame = None
        self.center = ctk.CTkFrame(self)
        self.center.pack(fill="both", expand=True)

    def clear_center(self):
        if self.content_frame:
            self.content_frame.destroy()
            self.content_frame = None

    def open_clients(self):
        print("Хімнати")

    def open_rooms(self):
        print("Кімнати")

    def open_bookings(self):
        print("Бронювання")

    def open_services(self):
        print("Послуги")

    def leave_requests(self):
        print("Хуйослуги")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # або "dark"
    ctk.set_default_color_theme("blue")
    app = HotelApp()
    app.mainloop()
