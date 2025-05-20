# database.py
from typing import Tuple

import mysql.connector

from models import BaseModel, Departments, Positions, Employees, LeaveRequests, EmploymentActions, Users


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="never-put-passwords-in-files",
        database="personnel"
    )

def all_models() -> tuple[Departments, Positions, Employees, LeaveRequests, EmploymentActions, Users]:
    connection = connect_db()

    return (
        Departments(connection),
        Positions(connection),
        Employees(connection),
        LeaveRequests(connection),
        EmploymentActions(connection),
        Users(connection),
    )

