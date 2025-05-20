from typing import List


class BaseModel:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch_all(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        return self.cursor.fetchall()

    def fetch_by_id(self, row_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (row_id,))
        return self.cursor.fetchone()

    def delete_by_id(self, row_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (row_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()

    def columns(self) -> List[str]:
        return []

    def column_headers(self) -> List[str]:
        return []


    def fields_for_add(self) -> list[str]:
        return []

    def fields_for_sort(self) -> list[str]:
        return []

    def fields_for_filtering(self) -> list[str]:
        return []

    @property
    def _select_query(self):
        return getattr(self, 'query', f"SELECT * FROM {self.table_name}")

    def filter(self, col: str, value, operator: str = 'LIKE'):
        query = f"{self._select_query} WHERE {col} {operator} %s"
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def sort(self, col: str, order: str = 'ASC'):
        query = f"{self._select_query} ORDER BY {col} {order}"
        self.cursor.execute(query)
        return self.cursor.fetchall()


class Departments(BaseModel):
    table_name = "departments"
    query= """
        SELECT 
            d.id,
            d.name AS department_name,
            pd.name AS parent_department
        FROM departments d
        LEFT JOIN departments pd ON d.parent_department_id = pd.id
        """

    def __init__(self, connection):
        super().__init__(connection)

    def fields_for_add(self) -> list[str]:
        return ["name", "parent_department_id"]

    def fields_for_sort(self) -> list[str]:
        return ["parent_department", "id"]

    def fields_for_filtering(self) -> list[str]:
        return ["department_name", "id", "parent_department_id"]

    def columns(self) -> list[str]:
        return ["id", "department_name", "parent_department"]
    def column_headers(self) -> list[str]:
        return ["ІД", "Назва відділу", "ID Батьківського відділу"]

    def fetch_all(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()


class Positions(BaseModel):
    table_name = "positions"
    query= """
        SELECT 
            p.id,
            p.title,
            d.name AS department,
            p.salary
        FROM positions p
        JOIN departments d ON p.department_id = d.id
        """

    def __init__(self, connection):
        super().__init__(connection)

    def get_by_department(self, department_id):
        self.cursor.execute("SELECT * FROM positions WHERE department_id = %s", (department_id,))
        return self.cursor.fetchall()

    def fetch_by_id(self, row_id):
        sql = """
        SELECT 
            p.id,
            p.title,
            d.name AS department,
            p.salary
        FROM positions p
        JOIN departments d ON p.department_id = d.id
        ORDER BY d.name, p.title
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetch_all(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def columns(self) -> List[str]:
        return ["id", "title", "department", "salary"]

    def column_headers(self) -> list[str]:
        return ["Id", "Імя", "Посада", "Депертамент", "Найм"]

    def fields_for_add(self) -> list[str]:
        return ["title", "department_id", "salary"]

    def fields_for_sort(self) -> list[str]:
        return ["salary", "name", "title"]

    def fields_for_filtering(self) -> list[str]:
        return ["salary", "name", "title"]


class Employees(BaseModel):
    table_name = "employees"
    query = """
               SELECT 
                   e.id,
                   CONCAT(e.last_name, ' ', e.first_name, ' ', COALESCE(e.middle_name, '')) AS full_name,
                   p.title AS position,
                   d.name AS department,
                   e.hire_date,
                   e.is_active
               FROM employees e
               JOIN positions p ON e.position_id = p.id
               JOIN departments d ON p.department_id = d.id
               """

    def __init__(self, connection):
        super().__init__(connection)

    def insert(self, data):
        sql = f"""
        INSERT INTO {self.table_name} (
            first_name, last_name, middle_name, date_of_birth,
            passport_number, tax_id, address, phone_number,
            email, hire_date, position_id, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["first_name"], data["last_name"], data.get("middle_name"),
            data["date_of_birth"], data.get("passport_number"), data.get("tax_id"),
            data.get("address"), data.get("phone_number"), data.get("email"),
            data["hire_date"], data["position_id"], data.get("is_active", True)
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def columns(self) -> List[str]:
        return ["id", "full_name", "position", "department", "hire_date", "is_active"]

    def column_headers(self) -> list[str]:
        return ["Id", "Імя", "Посада", "Депертамент", "Найм", "Статус"]

    def fields_for_add(self) -> list[str]:
        return ["title", "department_id", "salary"]

    def fields_for_sort(self) -> list[str]:
        return ["position", "department", "hire_date"]

    def fields_for_filtering(self) -> list[str]:
        return ["position", "department", "title", "department"]


class EmploymentActions(BaseModel):
    table_name = "employment_actions"
    query = """
            SELECT 
                e.id,
                CONCAT(e.last_name, ' ', e.first_name) AS full_name,
                ea.action_date,
                ea.reason,
                p.title AS previous_position
            FROM employment_actions ea
            JOIN employees e ON ea.employee_id = e.id
            LEFT JOIN positions p ON ea.new_position_id = p.id
            WHERE ea.action_type = 'terminate'
            """

    def __init__(self, connection):
        super().__init__(connection)

    def insert(self, data):
        sql = f"""
        INSERT INTO {self.table_name} (
            employee_id, action_type, action_date, reason, new_position_id
        ) VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data["employee_id"], data["action_type"], data["action_date"],
            data.get("reason"), data.get("new_position_id")
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def columns(self) -> List[str]:
        return ["id", "full_name", "action_date", "reason", "previous_position"]

    def column_headers(self) -> list[str]:
        return ["Id", "Імя", "Дата", "Причина", "Посада"]

    def fields_for_add(self) -> list[str]:
        return [
            "employee_id", "action_type", "action_date",
            "reason", "new_position_id"
        ]

    def fields_for_sort(self) -> list[str]:
        return ["full_name", "action_date"]

    def fields_for_filtering(self) -> list[str]:
        return ["full_name", "action_date"]


class LeaveRequests(BaseModel):
    table_name = "leave_requests"
    query = """
            SELECT 
                lr.id,
                CONCAT(e.last_name, ' ', e.first_name) AS full_name,
                lr.leave_type,
                lr.start_date,
                lr.end_date,
                lr.status,
                lr.reason
            FROM leave_requests lr
            JOIN employees e ON lr.employee_id = e.id
            ORDER BY lr.start_date DESC
            """

    def __init__(self, connection):
        super().__init__(connection)

    def insert(self, data):
        sql = f"""
        INSERT INTO {self.table_name} (
            employee_id, leave_type, start_date, end_date, reason, status
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data["employee_id"], data["leave_type"],
            data["start_date"], data["end_date"],
            data.get("reason"), data.get("status", "pending")
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def columns(self) -> List[str]:
        return ["id", "full_name", "leave_type", "start_date", "end_date", "status", "reason"]
    def column_headers(self) -> List[str]:
        return ["Id", "Імя", "Причина відсутності", "Поаток", "Кінець", "Статус", "Причина"]

    def fields_for_add(self) -> list[str]:
        return [
            "employee_id", "leave_type", "start_date",
            "end_date", "reason", "status"
        ]

    def fields_for_sort(self) -> list[str]:
        return ["full_name", "start_date", "status"]

    def fields_for_filtering(self) -> list[str]:
        return ["full_name", "start_date", "status"]


class Users(BaseModel):
    table_name = "users"

    def __init__(self, connection):
        super().__init__(connection)

    def insert(self, username, password_hash, role):
        sql = f"""
        INSERT INTO {self.table_name} (username, password_hash, role)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (username, password_hash, role))
        self.conn.commit()

    def fields_for_add(self) -> list[str]:
        return ["username", "password_hash", "role"]

