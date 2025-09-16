## **Project Documentation: Thesis Management System**

### **Project Overview**

#### **Project Goal**

The main goal of this project was to create a simple and effective system to manage all stages of a university thesis process. The system covers everything from the moment a student requests the thesis course until the defense session is held and the final grade is recorded.

#### **Brief Functional Description**

This application is a Command-Line Interface (CLI) based system with two primary user types: **Student** and **Professor**. All data, from user credentials to thesis statuses, is stored in **JSON** files, which act as our database. Students can log in, request a course, track its status, and eventually apply for a defense. Professors can manage student requests, appoint examiners for defense sessions, and submit final grades.

-----

### **Requirements**

  * **Python Version:** This project is compatible with **Python 3.6** and newer versions.
  * **Libraries / Packages Used:** This project requires **no external libraries**. All modules used, such as `json`, `os`, `datetime`, and `hashlib`, are part of Python's standard library. Therefore, you only need a standard Python installation to run it.

-----


### **Classes & Functions Explained**

The project uses several core classes to model its main entities:

  * **`User` Class (in `models.py`)**: A base class for all users, containing common attributes like `user_id` and `name`.
  * **`Student` & `Professor` Classes (in `models.py`)**: These classes inherit from the `User` class and add their specific attributes. For instance, the `Professor` class includes `supervision_capacity` and `examiner_capacity`.

The main functions are organized into different modules:

  * **`database.py` functions**: Includes `load_data` for reading from JSON files and `save_data` for writing to them.
  * **`auth.py` functions**: Includes `hash_password` for securing passwords and `login` for authenticating users.
  * **`services.py` functions**: This file contains the most functions, each implementing a specific rule or action, such as `submit_thesis_request` for students or `process_supervision_request` for professors.
  * **`cli.py` functions**: Functions in this file, often ending with `_view` (e.g., `student_menu`), are responsible for displaying information to the user and capturing their input.

-----

### **Implementation Details**

A key part of the implementation was managing professor **capacity**. The logic ensures that when a professor approves a request, their capacity is reduced. This slot remains occupied until the student's entire thesis process is complete and their final grade is recorded. After grading, the `submit_grade` function automatically increments the capacity for both the supervisor and the examiners.

To generate unique IDs for each request and thesis, the `uuid` library was used. This guarantees that no two entries will have the same ID, even if created at the same time.

-----

### ** How to Run**

To run this project on your local machine, follow these steps:

1.  First, clone or download the project from the GitHub repository.
2.  Ensure you have **Python 3** installed on your system.
3.  Before the first run, navigate to the `data/` directory and populate the `students.json`, `professors.json`, and `courses.json` files with some initial sample data.
4.  Open a terminal (like CMD, PowerShell, or Terminal) and use the `cd` command to navigate to the project's root folder.
5.  Finally, run the following command to start the application:
    ```bash
    python main.py
    ```
    The main menu of the application will then be displayed in your terminal.

