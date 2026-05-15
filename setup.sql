
-- TABLE: USERS (for login system)

CREATE TABLE users (
    username   VARCHAR2(50)  PRIMARY KEY,
    password   VARCHAR2(50)  NOT NULL,
    role       VARCHAR2(10)  NOT NULL CHECK (role IN ('ADMIN', 'USER'))
);


-- TABLE: EMPLOYEES

CREATE TABLE employees (
    emp_id     NUMBER        PRIMARY KEY,
    name       VARCHAR2(100) NOT NULL,
    department VARCHAR2(50),
    gender     VARCHAR2(10),
    salary     NUMBER(10, 2),
    contact    VARCHAR2(15)  UNIQUE
);


-- SAMPLE USERS

INSERT INTO users VALUES ('admin', 'admin123', 'ADMIN');
INSERT INTO users VALUES ('john',  'john123',  'USER');


-- SAMPLE EMPLOYEES

INSERT INTO employees VALUES (1001, 'Ahmad Ali',  'HR',          'Female', 75000,  '03001234567');
INSERT INTO employees VALUES (1002, 'Nouman Khan',      'IT',          'Male',   95000,  '03011234567');
INSERT INTO employees VALUES (1003, 'Sara Khan',      'Finance',     'Female', 28000,  '03021234567');
INSERT INTO employees VALUES (1004, 'Ahmed Raza',     'IT',          'Male',   120000, '03031234567');
INSERT INTO employees VALUES (1005, 'Maria Gul',      'HR',          'Female', 45000,  '03041234567');
INSERT INTO employees VALUES (1006, 'Usman Tariq',    'Operations',  'Male',   60000,  '03051234567');
INSERT INTO employees VALUES (1007, 'Hina Baig',      'Finance',     'Female', 25000,  '03061234567');
INSERT INTO employees VALUES (1008, 'Zain Malik',     'IT',          'Male',   88000,  '03071234567');
INSERT INTO employees VALUES (1009, 'Fatima Noor',    'Operations',  'Female', 32000,  '03081234567');
INSERT INTO employees VALUES (1010, 'Muhammad Saqlain',    'Management',  'Male',   150000, '03091234567');

COMMIT;

