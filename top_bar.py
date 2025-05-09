from typing import Optional, Callable, List

import customtkinter as ctk


def top_bar_UI(self, departments: Callable, positions: Callable, employees: Callable, employment_actions: Callable, leave_requests: Callable):
    # Заголовок
    ctk.CTkLabel(self, text="Облік відділу кадрів", font=("Arial", 24)).pack(pady=20)

    # Кнопки переходу до модулів
    btn_frame = ctk.CTkFrame(self)
    btn_frame.pack(pady=10)

    ctk.CTkButton(btn_frame, text="Відділи", width=200, command=departments).grid(row=0, column=0, padx=10, pady=5)
    ctk.CTkButton(btn_frame, text="Посади", width=200, command=positions).grid(row=0, column=1, padx=10, pady=5)
    ctk.CTkButton(btn_frame, text="Працівники", width=200, command=employees).grid(row=0, column=2, padx=10, pady=5)
    ctk.CTkButton(btn_frame, text="Працівники_Дії", width=200, command=employment_actions).grid(row=0, column=3, padx=10, pady=5)
    ctk.CTkButton(btn_frame, text="Відпустки і лікарняні", width=200, command=leave_requests).grid(row=0, column=4, padx=10, pady=5)