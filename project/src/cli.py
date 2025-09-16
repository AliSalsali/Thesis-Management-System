import os
from src import auth, services

current_user = None
user_type = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_enter():
    input("\nPress Enter to return to the menu...")

def main_menu():
    global current_user, user_type
    while True:
        clear_screen()
        print("Welcome to the Thesis Management System")
        print("="*40)
        if current_user:
            print(f"Logged in as: {current_user['name']} ({user_type.capitalize()})")
            if user_type == 'student':
                student_menu()
            else:
                professor_menu()
        else:
            print("1. Login as Student")
            print("2. Login as Professor")
            print("3. Search Thesis Archive")
            print("4. Exit")
            choice = input("> ")
            if choice == '1':
                login_menu('student')
            elif choice == '2':
                login_menu('professor')
            elif choice == '3':
                search_menu()
            elif choice == '4':
                print("Goodbye!")
                break

def login_menu(u_type):
    global current_user, user_type
    user_type = u_type
    print(f"\n--- Login as {u_type.capitalize()} ---")
    user_id_prompt = "Student ID: " if u_type == 'student' else "Professor ID: "
    user_id = input(user_id_prompt)
    password = input("Password: ")
    user_data = auth.login(user_type, user_id, password)
    if user_data:
        current_user = user_data
        print("Login successful!")
    else:
        user_type = None
        print("Invalid credentials.")
    wait_for_enter()

def logout():
    global current_user, user_type
    current_user = None
    user_type = None
    print("You have been successfully logged out.")
    wait_for_enter()

def student_menu():
    while current_user:
        clear_screen()
        print(f"--- Student Menu: {current_user['name']} ---")
        print("1. Request Thesis Course")
        print("2. View Request Status")
        print("3. Submit Defense Request")
        print("4. Search Archive")
        print("5. Change Password")
        print("6. Logout")
        choice = input("> ")
        if choice == '1':
            request_thesis_course_view()
        elif choice == '2':
            view_student_requests_view()
        elif choice == '3':
            submit_defense_request_view()
        elif choice == '4':
            search_menu()
        elif choice == '5':
            change_password_view()
        elif choice == '6':
            logout()
            break
        else:
            print("Invalid option.")
            wait_for_enter()
    
def professor_menu():
     while current_user:
        clear_screen()
        print(f"--- Professor Menu: {current_user['name']} ---")
        print("1. View/Process Supervision Requests")
        print("2. View/Process Defense Requests")
        print("3. View Assigned Defenses (as Examiner)")
        print("4. Submit Grade")
        print("5. Search Archive")
        print("6. Change Password")
        print("7. Logout")
        choice = input("> ")
        if choice == '1':
            manage_supervision_requests_view()
        elif choice == '2':
            manage_defense_requests_view()
        elif choice == '3':
            view_assigned_defenses_view()
        elif choice == '4':
            submit_grade_view()
        elif choice == '5':
            search_menu()
        elif choice == '6':
            change_password_view()
        elif choice == '7':
            logout()
            break
        else:
            print("Invalid option.")
            wait_for_enter()

def request_thesis_course_view():
    clear_screen()
    print("--- Available Thesis Courses ---")
    courses = services.get_available_courses()
    if not courses:
        print("No courses with available capacity at the moment.")
    else:
        for c in courses:
            print(f"ID: {c['course_id']}, Title: {c['title']}, Professor: {c['professor_id']}, Capacity: {c['capacity']}")
        
        course_id = input("\nEnter the ID of the course you want to request: ")
        success, message = services.submit_thesis_request(current_user['user_id'], course_id)
        print(message)
    wait_for_enter()

def view_student_requests_view():
    clear_screen()
    print("--- Your Request Status ---")
    requests = services.get_student_request_status(current_user['user_id'])
    if not requests:
        print("You have not submitted any requests.")
    else:
        for r in requests:
            print(f"Request ID: {r['request_id']}, Course ID: {r['course_id']}, Status: {r['status']}")
    wait_for_enter()

def submit_defense_request_view():
    clear_screen()
    print("--- Submit Defense Request ---")
    title = input("Thesis Title: ")
    abstract = input("Abstract: ")
    keywords = input("Keywords (comma-separated): ")
    pdf_path = input("Path to thesis PDF file: ")
    image_path = input("Path to first page image file: ")

    success, message = services.submit_defense_request(
        current_user['user_id'], title, abstract, keywords, pdf_path, image_path
    )
    print(message)
    wait_for_enter()

def manage_supervision_requests_view():
    clear_screen()
    print("--- Pending Supervision Requests ---")
    requests = services.get_supervision_requests(current_user['user_id'])
    if not requests:
        print("There are no new requests.")
    else:
        for r in requests:
            print(f"ID: {r['request_id']}, Student: {r['student_id']}")
        
        req_id = input("\nEnter request ID to process: ")
        action = input("Approve or reject? (type 'approve' or 'reject'): ")
        if action.lower() in ['approve', 'reject']:
            success, message = services.process_supervision_request(current_user['user_id'], req_id, action.lower())
            print(message)
        else:
            print("Invalid action.")
    wait_for_enter()

def manage_defense_requests_view():
    clear_screen()
    print("--- Pending Defense Requests ---")
    requests = services.get_defense_requests(current_user['user_id'])
    if not requests:
        print("There are no pending defense requests.")
    else:
        for r in requests:
            print(f"ID: {r['request_id']}, Student: {r['student_id']}, Title: {r['details']['title']}")
        
        req_id = input("\nEnter defense request ID to approve: ")
        defense_date = input("Enter defense date (YYYY-MM-DD): ")
        internal_examiner = input("Enter Internal Examiner's Professor ID: ")
        external_examiner = input("Enter External Examiner's Professor ID: ")
        
        success, message = services.process_defense_request(
            current_user['user_id'], req_id, defense_date, internal_examiner, external_examiner
        )
        print(message)
    wait_for_enter()
    
def view_assigned_defenses_view():
    clear_screen()
    print("--- Defenses Assigned to You as Examiner ---")
    theses = services.get_assigned_defenses(current_user['user_id'])
    if not theses:
        print("No defenses have been assigned to you for grading.")
    else:
        for t in theses:
            print(f"Thesis ID: {t['thesis_id']}, Student: {t['student_id']}, Title: {t['title']}, Date: {t['defense_date']}")
    wait_for_enter()

def submit_grade_view():
    clear_screen()
    print("--- Submit Final Grade ---")
    theses = services.get_assigned_defenses(current_user['user_id'])
    if not theses:
        print("You have no defenses to grade at this time.")
    else:
        for t in theses:
             print(f"Thesis ID: {t['thesis_id']}, Student: {t['student_id']}")
        
        thesis_id = input("\nEnter the Thesis ID to grade: ")
        try:
            score = int(input("Enter your score (0-100): "))
            if 0 <= score <= 100:
                success, message = services.submit_grade(thesis_id, current_user['user_id'], score)
                print(message)
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid integer.")
    wait_for_enter()
    
def search_menu():
    clear_screen()
    print("--- Search Thesis Archive ---")
    print("Search by: 1. Title 2. Author (Student ID) 3. Supervisor (Prof ID) 4. Keywords")
    choice = input("> ")
    search_by_map = {'1': 'title', '2': 'author', '3': 'supervisor', '4': 'keywords'}
    
    if choice in search_by_map:
        search_by = search_by_map[choice]
        query = input(f"Enter search term for '{search_by}': ")
        results = services.search_theses(query, search_by)
        
        if not results:
            print("No results found.")
        else:
            print("\n--- Search Results ---")
            for r in results:
                print(f"Title: {r['title']}, Author: {r['student_id']}, Supervisor: {r['supervisor_id']}, Grade: {r['grade']}")
                print(f"  Abstract: {r['abstract'][:100]}...")
                print("-" * 20)
    else:
        print("Invalid option.")
    wait_for_enter()

def change_password_view():
    clear_screen()
    print("--- Change Password ---")
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    if new_password == confirm_password:
        success = auth.change_password_in_db(user_type, current_user['user_id'], new_password)
        if success:
            print("Password changed successfully.")
        else:
            print("An error occurred while changing the password.")
    else:
        print("Passwords do not match.")
    wait_for_enter()