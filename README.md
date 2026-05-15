# Enterprise Employee Management System

A robust, 2-tier desktop application built with Python and Oracle Database. This system is designed to securely manage enterprise employee records, featuring a modern graphical user interface, strict role-based access control, real-time analytics, and advanced data filtering capabilities.

## Key Features

* **Role-Based Access Control (RBAC):** Secure login system that differentiates between Administrator and Standard User privileges. Administrators have full system control, while Standard Users are restricted to read-only search functionality.
* **Modern User Interface:** Built using CustomTkinter, moving away from legacy Tkinter designs to deliver a flat, responsive, and professional dashboard experience.
* **Advanced Search and Filtering:** A dynamic search engine that allows users to query the database by Employee ID, Name, Department, Gender, and specific Salary ranges simultaneously.
* **Real-Time Data Sorting:** Multi-level sorting capabilities allowing users to organize records by ID, Name, Salary, or Department in ascending or descending order.
* **Data Analytics Dashboard:** A dedicated statistics module that calculates and displays highest/lowest salaries, average payroll, total expense, and departmental distribution.
* **Secure Database Connectivity:** Utilizes fully parameterized SQL queries via the oracledb library to ensure strict protection against SQL injection attacks.
* **Data Export:** Built-in tools for Administrators to export displayed search results into CSV or plain text formats for external reporting.
* **User Management:** An integrated administrative tool to securely provision new user accounts or revoke access from existing standard users.

## Technologies Used

* **Frontend:** Python, CustomTkinter, Tkinter (ttk)
* **Backend Logic:** Python
* **Database:** Oracle Database (via oracledb)

## Prerequisites

Before running this application, ensure your local environment meets the following requirements:

1. Python 3.8 or higher installed.
2. An active instance of Oracle Database.
3. The following Python libraries installed:

    ```bash
    pip install customtkinter oracledb
    ```

## Database Setup

To run this application, you must first create the required tables in your Oracle Database. Connect to your database and execute the following SQL scripts:

    ```sql
    CREATE TABLE users (
        username VARCHAR2(50) PRIMARY KEY,
        password VARCHAR2(50) NOT NULL,
        role VARCHAR2(10) NOT NULL CHECK (role IN ('ADMIN', 'USER'))
    );

    CREATE TABLE employees (
        empid NUMBER PRIMARY KEY,
        name VARCHAR2(100) NOT NULL,
        department VARCHAR2(50),
        gender VARCHAR2(10),
        salary NUMBER(10, 2),
        contact VARCHAR2(15) UNIQUE
    );

    -- Insert a default admin account to access the system for the first time
    INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'ADMIN');
    COMMIT;
    ```

## Installation and Configuration

1. Clone this repository to your local machine.
2. Open the main Python script file.
3. Locate the Database Configuration section at the top of the file.
4. Update the connection parameters to match your local Oracle Database instance:

    ```python
    DB_USER     = "your_database_username"
    DB_PASSWORD = "your_database_password"
    DB_DSN      = "localhost:1521/orcl"
    ```

5. Run the application:

    ```bash
    python employee_management.py
    ```

## Usage Notes

* **Administrator Access:** Log in using an account with the ADMIN role to perform CRUD operations (Create, Read, Update, Delete), export data, and manage user accounts.
* **Standard Access:** Log in using an account with the USER role. The interface will automatically lock down administrative functions, allowing the user to safely query and view records without the risk of modifying the database.

## Screenshots

<img width="587" height="707" alt="image" src="https://github.com/user-attachments/assets/a3202e24-be6e-4715-9c45-2d5c7d72c74f" />


<img width="1919" height="1199" alt="image" src="https://github.com/user-attachments/assets/0875324b-982b-456a-866c-344094b56529" />


<img width="1179" height="1097" alt="image" src="https://github.com/user-attachments/assets/ff16e458-3ecc-47cc-b957-dd7ab7e029f1" />


---

