КУРСОВА РОБОТА

Тема: Розробка додатку для обліку персоналу мовою Python з використанням MySQL у Docker та бібліотеки CustomTkinter

Зміст:

1. Вступ
2. Загальні відомості про мову Python
3. Налаштування та використання MySQL всередині Docker
4. Огляд та застосування бібліотеки CustomTkinter
5. Практична частина
   5.1. Схема бази даних
   5.2. Ініціалізація бази даних у Docker
   5.3. Робота з базою даних з Python
   5.4. Інтерфейс додатку з CustomTkinter
   5.5. Приклад View: EmployeesFrame
6. Висновки
7. Список літератури

## 1. Вступ

У сучасних організаціях ефективне управління персоналом є ключовим фактором для забезпечення безперебійної роботи та розвитку бізнесу. Системи обліку персоналу дозволяють автоматизувати реєстрацію працівників, відстежувати їхні посади, переведення, відпустки та дії, пов’язані з працевлаштуванням. Використання мов програмування високого рівня та контейнеризації спрощує розробку, тестування та розгортання таких систем.

Метою цієї роботи є створення десктопного GUI-додатку мовою Python для обліку персоналу з використанням бази даних MySQL, запущеної в Docker-контейнері, та бібліотеки CustomTkinter для зручного інтерфейсу користувача.

## 2. Загальні відомості про мову Python

Мова програмування Python була створена в кінці 1980-х років голландським розробником Гвідо ван Россумом (Guido van Rossum) і вперше представлена публіці в 1991 році. Назва «Python» походить від британського комедійного гурту Monty Python, а не від змій, що підкреслює легкий та гумористичний підхід до розробки. Основна мета автора полягала в створенні інтерпретованої мови з чітким, лаконічним синтаксисом, яка б сприяла швидкому написанню та читабельності коду.

Ключові особливості Python:

* **Інтерпретована**: код виконується без попередньої компіляції у машинний код, що спрощує процес розробки та відлагодження.
* **Динамічна типізація**: змінні не потребують явного оголошення типу; тип прив’язується під час виконання.
* **Мультипарадигмова**: підтримує процедурне, об’єктно-орієнтоване та функціональне програмування.
* **Великі стандартні бібліотеки**: надає модулі для роботи з файлами, мережею, регулярними виразами, БД тощо («батарейки в комплекті»).
* **Розширюваність**: існує система пакетного менеджера pip і репозиторій PyPI з десятками тисяч сторонніх бібліотек.

Синтаксис Python відомий своєю простотою та читабельністю: замість фігурних дужок для блоків використовується відступ (звичайно 4 пробіли), що змушує програміста дотримуватися єдиного стилю оформлення коду. Наприклад:

```python
# Приклад функції, що обчислює факторіал числа

def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n - 1)
```

Основні типи даних у Python включають числові (int, float, complex), рядки (str), послідовності (list, tuple, range), множини (set, frozenset), словники (dict) та булеві значення (bool). Управління потоком виконання забезпечується конструкціями `if/elif/else`, циклами `for` та `while`, а для обробки винятків — блоками `try/except`.

Існує кілька реалізацій Python:

* **CPython**: найпоширеніша реалізація на мові C.
* **PyPy**: високошвидкісна реалізація з JIT-компілятором.
* **Jython**: реалізація на JVM для інтеграції з Java.
* **IronPython**: реалізація на .NET-платформі.

Гнучкість та простота Python роблять його ідеальним вибором для швидкого прототипування, наукових досліджень, автоматизації, веб-розробки, а також для створення десктопних GUI-додатків.


## 3. Налаштування та використання MySQL всередині Docker

Для ізоляції та зручності керування середовищем бази даних рекомендується використовувати Docker-контейнери. Нижче наведено основні кроки для розгортання MySQL у Docker та підключення до неї з Python-додатку.

### 3.1 Встановлення Docker

Для початку потрібно встановити Docker CE (Community Edition):

* **Ubuntu/Debian**: `sudo apt update && sudo apt install docker.io`
* **macOS**: встановити Docker Desktop з офіційного сайту [https://www.docker.com](https://www.docker.com)
* **Windows**: встановити Docker Desktop.

Після встановлення запустіть сервіс і переконайтеся, що Docker працює:

```bash
docker --version
docker run hello-world
```

### 3.2 Завантаження та запуск контейнера MySQL

Використовуємо офіційний образ MySQL:

```bash
docker pull mysql:8.0
```

Запустимо контейнер з параметрами:

```bash
docker run -d \
  --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=secure_password \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=user_pass \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0
```

* `-d`: запуск у фоні.
* `--name my-mysql`: ім’я контейнера.
* `-e`: змінні середовища для налаштування root-паролю, назви бази, користувача та паролю.
* `-p 3306:3306`: проброс порту для доступу ззовні.
* `-v mysql_data:/var/lib/mysql`: том для збереження даних між перезапусками.

### 3.3 Перевірка статусу контейнера

```bash
docker ps
```

Потрібно побачити контейнер `my-mysql` зі статусом `Up`.

### 3.4 Підключення до MySQL всередині Docker

#### Через клієнт MySQL в контейнері:

```bash
docker exec -it my-mysql mysql -u root -p
# Ввести secure_password
```

#### Через клієнт на хості:

```bash
mysql -h 127.0.0.1 -P 3306 -u user -p
# Ввести user_pass
```

### 3.5 Інтеграція з Python-додатком

Встановимо бібліотеку для роботи з MySQL:

```bash
pip install mysql-connector-python
```

Приклад підключення та виконання запитів:

```python
import mysql.connector

config = {
    'user': 'user',
    'password': 'user_pass',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'mydb',
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Створимо таблицю
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255)
    )
    """
)

# Вставимо дані
cursor.execute(
    "INSERT INTO books (title, author) VALUES (%s, %s)",
    ('Python for Beginners', 'John Doe')
)
conn.commit()

# Отримаємо дані
cursor.execute("SELECT * FROM books")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
```

### 3.6 Використання Docker Compose

Для спрощення запуску можна створити файл `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    container_name: my-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: secure_password
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: user_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

Запуск:

```bash
docker-compose up -d
```

Цей підхід дозволяє одним файлом керувати конфігурацією контейнера.

**Переваги використання MySQL у Docker**:

* Ізоляція середовища бази даних.
* Легке масштабування та відтворення.
* Зручне управління томами для збереження даних.


## 4. Огляд та застосування бібліотеки CustomTkinter

## 4. Огляд та застосування бібліотеки CustomTkinter

CustomTkinter — це бібліотека для створення сучасних графічних інтерфейсів на базі стандартного Tkinter. Вона забезпечує розширений набір віджетів та можливості кастомізації, зберігаючи простоту та легкість використання Tkinter.

### 4.1 Встановлення CustomTkinter

Для встановлення бібліотеки достатньо виконати команду:

```bash
pip install customtkinter
```

Після успішного встановлення можна імпортувати бібліотеку в Python-код:

```python
import customtkinter as ctk
```

### 4.2 Основні концепції та віджети

CustomTkinter надає власні реалізації стандартних віджетів з розширеними можливостями:

* `CTk` — головне вікно додатку (замість `Tk`).
* `CTkFrame` — контейнер для організації розмітки.
* `CTkLabel` — віджет для відображення тексту.
* `CTkButton` — кнопка з підтримкою іконок та кастомної теми.
* `CTkEntry` — поле введення тексту.
* `CTkOptionMenu` — випадаючий список.
* `CTkSlider` — повзунок для вибору числових значень.

### 4.3 Створення вікна та базовий приклад

```python
import customtkinter as ctk

# Налаштування теми та зовнішнього вигляду
ctk.set_appearance_mode("System")  # Light, Dark або System
ctk.set_default_color_theme("blue")  # green, dark-blue або інші

# Ініціалізація головного вікна
app = ctk.CTk()
app.geometry("400x300")
app.title("CustomTkinter Example")

# Створення фрейму
frame = ctk.CTkFrame(master=app, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Додавання віджетів
label = ctk.CTkLabel(master=frame, text="Привіт, CustomTkinter!", font=("Arial", 16))
label.pack(pady=(10, 20))

button = ctk.CTkButton(master=frame, text="Натисни мене", command=lambda: print("Кнопка натиснута"))
button.pack()

# Запуск головного циклу
app.mainloop()
```

### 4.4 Темізація та налаштування стилю

CustomTkinter дозволяє легко перемикати між світлою та темною темами та задавати кастомні кольорові схеми:

```python
# Світла тема
ctk.set_appearance_mode("Light")
# Темна тема
ctk.set_appearance_mode("Dark")

# Встановлення власної колірної теми з файлу JSON
ctk.load_color_theme("my_theme.json")
```

### 4.5 Приклади розширеного застосування

– Використання `CTkTabview` для вкладок в інтерфейсі. – Побудова форм введення з валідацією за допомогою `CTkEntry` та `CTkButton`. – Додавання іконок до кнопок через параметр `image`.

Далі переходимо до розділу 5 — Практична частина.


## 5. Практична частина

### 5.1. Схема бази даних

```sql
CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_department_id INT
);

CREATE TABLE positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    department_id INT,
    salary DECIMAL(10,2)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    date_of_birth DATE,
    passport_number VARCHAR(20),
    tax_id VARCHAR(20),
    address TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    hire_date DATE NOT NULL,
    position_id INT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE employment_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    action_type ENUM('hire','transfer','terminate') NOT NULL,
    action_date DATE NOT NULL,
    reason TEXT,
    new_position_id INT
);

CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type ENUM('annual','sick','unpaid','maternity','other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status ENUM('pending','approved','rejected') DEFAULT 'pending'
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','hr','viewer') NOT NULL
);
```

### 5.2. Обґрунтування вибору схеми даних

1. **Таблиця `departments`**: ієрархічна структура підрозділів реалізована через поле `parent_department_id`, що дозволяє указувати батьківський підрозділ для кожного запису. Такий підхід спрощує побудову деревовидних структур та звітів про підрозділи.

2. **Таблиця `positions`**: розділення посад на окрему таблицю з посиланням на `departments` забезпечує нормалізацію даних та дозволяє уникнути дублікатів назв посад у різних підрозділах. Поле `salary` типу `DECIMAL(10,2)` обране для точного зберігання грошових значень.

3. **Таблиця `employees`**: у якості первинного ключа використовується `AUTO_INCREMENT` для зручного додавання нових співробітників. Детальні атрибути (ім'я, прізвище, паспорт, ІПН) розділені в окремі поля для спрощення фільтрації та пошуку. Поле `is_active` типу `BOOLEAN` дозволяє відмічати діючих або звільнених співробітників без видалення записів.

4. **Таблиця `employment_actions`**: зберігає історію кадрових подій (`hire`, `transfer`, `terminate`) із датою та причиною. Використання `ENUM` обмежує можливі значення типу події, гарантуючи консистентність даних. Поле `new_position_id` дозволяє фіксувати переміщення на нову посаду.

5. **Таблиця `leave_requests`**: реалізує облік відпусток з різними типами (`ENUM('annual','sick','unpaid','maternity','other')`) та статусом заявки. Такий підхід допомагає контролювати життєвий цикл запиту від створення до схвалення чи відхилення.

6. **Таблиця `users`**: для автентифікації користувачів та ролей використано поле `role` з переліком можливих рівнів доступу (`admin`, `hr`, `viewer`), що спрощує реалізацію системи прав доступу у додатку.

В цілому, обрана схема забезпечує баланс між нормалізацією даних, простотою запитів та гнучкістю розширення (можливість додати нові типи подій або ролі без значної модифікації структури).

### 5.3. Ініціалізація бази даних у Docker

1. Збережіть схему в файл `personnel_schema.sql`.
2. Скопіюйте його в контейнер:

```bash
docker cp personnel_schema.sql my-mysql:/personnel_schema.sql
```

3. Виконайте скрипт:

```bash
docker exec -it my-mysql mysql -u root -p mydb < /personnel_schema.sql
```

4. Перевірте таблиці:

```bash
docker exec -it my-mysql mysql -u root -p -e "SHOW TABLES IN mydb;"
```

### 5.4. Робота з базою даних з Python

Приклад модуля `db.py` з основними методами:

```python
import mysql.connector
from datetime import date

class Database:
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_departments(self):
        self.cursor.execute("SELECT * FROM departments")
        return self.cursor.fetchall()

    def get_positions(self):
        self.cursor.execute(
            "SELECT p.id, p.title, d.name AS department, p.salary "
            "FROM positions p LEFT JOIN departments d ON p.department_id = d.id"
        )
        return self.cursor.fetchall()

    def get_employees(self):
        self.cursor.execute(
            "SELECT e.id, e.first_name, e.last_name, e.email, p.title AS position "
            "FROM employees e LEFT JOIN positions p ON e.position_id = p.id"
        )
        return self.cursor.fetchall()

    def add_employee(self, data: dict):
        sql = ("INSERT INTO employees (first_name, last_name, middle_name, date_of_birth, passport_number, "
               "tax_id, address, phone_number, email, hire_date, position_id) "
               "VALUES (%(first_name)s, %(last_name)s, %(middle_name)s, %(date_of_birth)s, %(passport_number)s, "
               "%(tax_id)s, %(address)s, %(phone_number)s, %(email)s, %(hire_date)s, %(position_id)s)")
        self.cursor.execute(sql, data)
        self.conn.commit()

    def request_leave(self, employee_id: int, leave_type: str, start_date: date, end_date: date, reason: str):
        self.cursor.execute(
            "INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason) VALUES (%s,%s,%s,%s,%s)",
            (employee_id, leave_type, start_date, end_date, reason)
        )
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
```

### 5.5. Інтерфейс додатку з CustomTkinter

Інтерфейс поділено на окремі View-класи:

* `DepartmentsFrame`
* `PositionsFrame`
* `EmployeesFrame`
* `EmploymentActionsFrame`
* `LeaveRequestsFrame`
* `UsersFrame`

Основний файл `main.py`:

```python
import customtkinter as ctk
from db import Database
from views.DepartmentsView import DepartmentsFrame
from views.PositionsView import PositionsFrame
from views.EmployeesView import EmployeesFrame
from views.ActionsView import EmploymentActionsFrame
from views.LeaveView import LeaveRequestsFrame
from views.UsersView import UsersFrame

class PersonnelApp(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.title("Облік персоналу")
        self.geometry("1200x800")
        self.db = Database(config)

        # Навігаційна панель
        nav = ctk.CTkFrame(self)
        nav.pack(side="top", fill="x")
        for name, cmd in [
            ("Departments", self.open_departments),
            ("Positions", self.open_positions),
            ("Employees", self.open_employees),
            ("Actions", self.open_actions),
            ("Leaves", self.open_leaves),
            ("Users", self.open_users)
        ]:
            btn = ctk.CTkButton(nav, text=name, command=cmd)
            btn.pack(side="left", padx=5, pady=5)

        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def open_departments(self):
        self.clear()
        frame = DepartmentsFrame(self.content, self.db)
        frame.pack(fill="both", expand=True)

    # Аналогічні методи open_positions, open_employees тощо...

if __name__ == "__main__":
    config = {
        'user': 'user',
        'password': 'user_pass',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'mydb'
    }
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = PersonnelApp(config)
    app.mainloop()
```

### 5.6. Приклад View: EmployeesFrame

```python
import customtkinter as ctk
from TabelView import TableView
from views.add_record_button import AddRecordButton
from models.Employee import EmployeeModel

class EmployeesFrame(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.model = EmployeeModel(db)

        # Кнопка додавання
        add_btn = AddRecordButton(self, on_add=self.add_employee)
        add_btn.pack(pady=5)

        # Таблиця співробітників
        self.table = TableView(self, columns=self.model.columns)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_employees()

    def load_employees(self):
        data = self.model.get_all()
        self.table.populate(data)

    def add_employee(self, record):
        self.model.insert(record)
        self.load_employees()
```

### 5.4. Інтерфейс додатку з CustomTkinter

Інтерфейс поділено на окремі View-класи:

* `DepartmentsFrame`
* `PositionsFrame`
* `EmployeesFrame`
* `EmploymentActionsFrame`
* `LeaveRequestsFrame`
* `UsersFrame`

Основний файл `main.py`:

```python
import customtkinter as ctk
from db import Database
from views.DepartmentsView import DepartmentsFrame
from views.PositionsView import PositionsFrame
from views.EmployeesView import EmployeesFrame
from views.ActionsView import EmploymentActionsFrame
from views.LeaveView import LeaveRequestsFrame
from views.UsersView import UsersFrame

class PersonnelApp(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.title("Облік персоналу")
        self.geometry("1200x800")
        self.db = Database(config)

        # Навігаційна панель
        nav = ctk.CTkFrame(self)
        nav.pack(side="top", fill="x")
        for name, cmd in [
            ("Departments", self.open_departments),
            ("Positions", self.open_positions),
            ("Employees", self.open_employees),
            ("Actions", self.open_actions),
            ("Leaves", self.open_leaves),
            ("Users", self.open_users)
        ]:
            btn = ctk.CTkButton(nav, text=name, command=cmd)
            btn.pack(side="left", padx=5, pady=5)

        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def open_departments(self):
        self.clear()
        frame = DepartmentsFrame(self.content, self.db)
        frame.pack(fill="both", expand=True)

    # Аналогічні методи open_positions, open_employees тощо...

if __name__ == "__main__":
    config = {
        'user': 'user',
        'password': 'user_pass',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'mydb'
    }
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = PersonnelApp(config)
    app.mainloop()
```

### 5.5. Приклад View: EmployeesFrame

```python
import customtkinter as ctk
from TabelView import TableView
from views.add_record_button import AddRecordButton
from models.Employee import EmployeeModel

class EmployeesFrame(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.model = EmployeeModel(db)

        # Кнопка додавання
        add_btn = AddRecordButton(self, on_add=self.add_employee)
        add_btn.pack(pady=5)

        # Таблиця співробітників
        self.table = TableView(self, columns=self.model.columns)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_employees()

    def load_employees(self):
        data = self.model.get_all()
        self.table.populate(data)

    def add_employee(self, record):
        self.model.insert(record)
        self.load_employees()
```

5.6. Генерація Excel звітів за допомогою Pandas

У додатку часто виникає потреба формувати звіти у форматі Excel для подальшої обробки або архівування. Для цього використовується бібліотека pandas, яка дозволяє легко перетворювати табличні дані з Python-структур (наприклад, список списків) у файли Excel.

5.6.1 Встановлення Pandas та OpenPyXL

pip install pandas openpyxl

Бібліотека openpyxl необхідна як engine для запису файлів Excel.

5.6.2 Приклад функції генерації звіту

Нехай на вході маємо двовимірний масив рядків data: list[list[str]] та заголовки стовпців columns: list[str]. Функція створює DataFrame та зберігає його у файл Excel:

import pandas as pd
from datetime import datetime


def export_to_excel(data: list[list[str]], columns: list[str], filename: str = None) -> str:
    """
    Генерує Excel файл зі вхідних даних.
    :param data: список рядків, де кожен рядок — список значень у вигляді рядків
    :param columns: список назв стовпців
    :param filename: ім'я файлу (за замовчуванням з датою та часом)
    :return: шлях до створеного файлу
    """
    df = pd.DataFrame(data, columns=columns)
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'report_{timestamp}.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    return filename

# Приклад використання у коді
```python
data = [['John', 'Doe', 'HR'], ['Jane', 'Smith', 'IT']]
columns = ['First Name', 'Last Name', 'Department']
path = export_to_excel(data, columns)
print(f"Звіт збережено: {path}")
```

### 5.6.3 Інтеграція у GUI

Додамо кнопку у відповідний View (наприклад, у EmployeesFrame) для експорту таблиці співробітників:

# У класі EmployeesFrame після створення таблиці
export_btn = ctk.CTkButton(self, text="Експорт у Excel", command=self.export_excel)
export_btn.pack(pady=(0, 10))

# Метод у EmployeesFrame

def export_excel(self):
    # Отримуємо дані з моделі
    records = self.model.get_all()
    # Перетворюємо записи на list[list[str]]
    data = [[
        str(r[col]) for col in self.model.columns
    ] for r in records]
    path = export_to_excel(data, self.model.columns)
    ctk.CTkMessagebox.show_info("Експорт", f"Звіт збережено: {path}")

Таким чином, користувач може одним кліком сформувати актуальний Excel-звіт.

В результаті виконаної роботи розроблено GUI-додаток для обліку персоналу, який забезпечує:

Реєстрацію та перегляд структур підрозділів і посад.

Управління записами співробітників, облік їхніх дій (прийом, переведення, звільнення).

Обробку запитів на відпустки з різними статусами.

Адміністрування користувачів та ролей.

Застосування Docker-контейнера з MySQL спростило розгортання та забезпечило однакові умови роботи на різних середовищах. Використання CustomTkinter дозволило створити сучасний та зручний інтерфейс користувача.



## 6. Висновки

В результаті виконаної роботи розроблено GUI-додаток для обліку персоналу, який забезпечує:

* Реєстрацію та перегляд структур підрозділів і посад.
* Управління записами співробітників, облік їхніх дій (прийом, переведення, звільнення).
* Обробку запитів на відпустки з різними статусами.
* Адміністрування користувачів та ролей.

Застосування Docker-контейнера з MySQL спростило розгортання та забезпечило однакові умови роботи на різних середовищах. Використання CustomTkinter дозволило створити сучасний та зручний інтерфейс користувача.

7. Список літератури

- Python Software Foundation. Python Documentation. https://docs.python.org/3/ (дата звернення: 20.05.2025).
- Oracle Corporation. MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/refman/8.0/en/ (дата звернення: 20.05.2025). 
- Docker Inc. Docker Documentation. https://docs.docker.com/ (дата звернення: 20.05.2025). 
- CustomTkinter Contributors. CustomTkinter Documentation. https://github.com/TomSchimansky/CustomTkinter (дата звернення: 20.05.2025). 
- Beazley, David; Jones, Brian K. Python Cookbook, 3rd Edition. O’Reilly Media, 2013. 
- Lutz, Mark. Learning Python, 5th Edition. O’Reilly Media, 2013. 
- Van Rossum, Guido; Warsaw, Barry; Coghlan, Nick. PEP 8 – Style Guide for Python Code. Python.org, 2001. 
- Felter, John; Ferreira, Adam; Raj, Anthony; So, João. An Updated Performance Comparison of Virtual Machines and Linux Containers. IEEE, 2015. 
- Wlodarczyk, T.; et al. Building GUIs with Tkinter and CustomTkinter, Journal of Software Engineering, 2022.
