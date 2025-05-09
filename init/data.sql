-- Департаменти
INSERT INTO departments (name, parent_department_id) VALUES
('Адміністрація', NULL),
('Відділ кадрів', 1),
('Фінансовий відділ', 1),
('Інформаційні технології', 1);

-- Посади
INSERT INTO positions (title, department_id, salary) VALUES
('HR-менеджер', 2, 18000.00),
('Бухгалтер', 3, 20000.00),
('Системний адміністратор', 4, 25000.00),
('Головний менеджер', 1, 30000.00);

-- Працівники
INSERT INTO employees (first_name, last_name, middle_name, date_of_birth, passport_number, tax_id, address, phone_number, email, hire_date, position_id, is_active) VALUES
('Іван', 'Петренко', 'Миколайович', '1985-03-12', 'АН123456', '1234567890', 'м. Київ, вул. Хрещатик, 10', '+380501234567', 'ivan.petrenko@example.com', '2020-01-15', 1, TRUE),
('Олена', 'Ковальчук', 'Ігорівна', '1990-06-24', 'ВК654321', '9876543210', 'м. Львів, вул. Січових Стрільців, 5', '+380673214567', 'olena.kovalchuk@example.com', '2021-03-01', 2, TRUE),
('Андрій', 'Шевченко', 'Володимирович', '1988-11-02', 'СН345678', '1112223334', 'м. Харків, вул. Полтавський Шлях, 15', '+380931234567', 'andriy.shevchenko@example.com', '2019-07-22', 3, TRUE);

-- Дії працевлаштування
INSERT INTO employment_actions (employee_id, action_type, action_date, reason, new_position_id) VALUES
(1, 'hire', '2020-01-15', 'Початок роботи у компанії', 1),
(2, 'hire', '2021-03-01', 'Початок роботи у компанії', 2),
(3, 'hire', '2019-07-22', 'Початок роботи у компанії', 3);

-- Заяви на відпустку
INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason, status) VALUES
(1, 'annual', '2024-07-01', '2024-07-15', 'Планова щорічна відпустка', 'approved'),
(2, 'sick', '2024-05-05', '2024-05-10', 'ГРВІ', 'approved'),
(3, 'unpaid', '2024-08-01', '2024-08-20', 'Особисті причини', 'pending');

-- Користувачі системи
INSERT INTO users (username, password_hash, role) VALUES
('admin', '$2b$12$abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef', 'admin'),
('hr_user', '$2b$12$qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty', 'hr'),
('viewer1', '$2b$12$zxcvbzxcvbzxcvbzxcvbzxcvbzxcvbzxcvbzxcvbzxcvbzxcvbzx', 'viewer');
