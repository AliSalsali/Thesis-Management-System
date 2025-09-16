import uuid
from datetime import datetime, timedelta
from src.database import load_data, save_data

# --- Status Constants ---
STATUS_PENDING = "Pending Professor Approval"
STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"
STATUS_DEFENSE_PENDING = "Pending Defense Approval"
STATUS_DEFENSE_APPROVED = "Approved for Defense"
STATUS_DEFENDED = "Defended"

# --- Helper Functions ---
def find_item_by_id(item_list, item_id, id_key='id'):
    for item in item_list:
        if item.get(id_key) == item_id:
            return item
    return None

# --- Student Services ---
def get_available_courses():
    courses = load_data('courses.json')
    return [c for c in courses if c.get('capacity', 0) > 0]

def submit_thesis_request(student_id, course_id):
    requests = load_data('requests.json')
    courses = load_data('courses.json')

    if any(r['student_id'] == student_id and r['status'] != STATUS_REJECTED for r in requests):
        return False, "You already have an active or approved request."

    course = find_item_by_id(courses, course_id, 'course_id')
    if not course or course['capacity'] <= 0:
        return False, "Course not found or its capacity is full."

    new_request = {
        "request_id": str(uuid.uuid4()),
        "type": "course_request",
        "student_id": student_id,
        "course_id": course_id,
        "professor_id": course['professor_id'],
        "request_date": datetime.now().isoformat(),
        "status": STATUS_PENDING
    }
    requests.append(new_request)
    save_data('requests.json', requests)
    return True, "Your request has been successfully submitted."

def get_student_request_status(student_id):
    requests = load_data('requests.json')
    return [r for r in requests if r.get('student_id') == student_id and r.get('type') == 'course_request']

def submit_defense_request(student_id, title, abstract, keywords, pdf_path, image_path):
    requests = load_data('requests.json')
    
    approved_request = next((r for r in requests if r['student_id'] == student_id and r['status'] == STATUS_APPROVED), None)
    
    if not approved_request:
        return False, "You do not have an approved thesis course."

    approval_date = datetime.fromisoformat(approved_request['approval_date'])
    if datetime.now() < approval_date + timedelta(days=90):
        return False, "At least 3 months must have passed since your course approval date."

    new_defense_req = {
        "request_id": str(uuid.uuid4()),
        "type": "defense_request",
        "student_id": student_id,
        "course_request_id": approved_request['request_id'],
        "professor_id": approved_request['professor_id'],
        "submission_date": datetime.now().isoformat(),
        "status": STATUS_DEFENSE_PENDING,
        "details": {
            "title": title,
            "abstract": abstract,
            "keywords": keywords,
            "pdf_path": pdf_path,
            "image_path": image_path
        }
    }
    requests.append(new_defense_req)
    save_data('requests.json', requests)
    return True, "Your defense request has been successfully submitted."

# --- Professor Services ---
def get_supervision_requests(professor_id):
     
    requests = load_data('requests.json')
    return [r for r in requests if r['professor_id'] == professor_id and r['type'] == 'course_request' and r['status'] == STATUS_PENDING]

def process_supervision_request(professor_id, request_id, action):
     
    requests = load_data('requests.json')
    professors = load_data('professors.json')
    courses = load_data('courses.json')

    request = find_item_by_id(requests, request_id, 'request_id')
    professor = find_item_by_id(professors, professor_id, 'user_id')

    if not request or request['professor_id'] != professor_id:
        return False, "Request not found."

    if action == 'approve':
        if professor['supervision_capacity'] <= 0:
            return False, "Your supervision capacity is full."
        
        request['status'] = STATUS_APPROVED
        request['approval_date'] = datetime.now().isoformat()
        professor['supervision_capacity'] -= 1
        
        course = find_item_by_id(courses, request['course_id'], 'course_id')
        if course:
            course['capacity'] -= 1

    elif action == 'reject':
        request['status'] = STATUS_REJECTED
    else:
        return False, "Invalid action."

    save_data('requests.json', requests)
    save_data('professors.json', professors)
    save_data('courses.json', courses)
    return True, f"Request has been successfully {'approved' if action == 'approve' else 'rejected'}."

def get_defense_requests(professor_id):
     
    requests = load_data('requests.json')
    return [r for r in requests if r['professor_id'] == professor_id and r['type'] == 'defense_request' and r['status'] == STATUS_DEFENSE_PENDING]

def process_defense_request(professor_id, request_id, defense_date, internal_examiner_id, external_examiner_id):
     
    requests = load_data('requests.json')
    theses = load_data('theses.json')
    professors = load_data('professors.json')

    request = find_item_by_id(requests, request_id, 'request_id')
    if not request or request['professor_id'] != professor_id:
        return False, "Defense request not found."

    internal_examiner = find_item_by_id(professors, internal_examiner_id, 'user_id')
    external_examiner = find_item_by_id(professors, external_examiner_id, 'user_id')

    if not internal_examiner or internal_examiner['examiner_capacity'] <= 0:
        return False, "Internal examiner not found or their capacity is full."
    if not external_examiner or external_examiner['examiner_capacity'] <= 0:
        return False, "External examiner not found or their capacity is full."

    new_thesis = {
        "thesis_id": str(uuid.uuid4()),
        "student_id": request['student_id'],
        "supervisor_id": professor_id,
        "title": request['details']['title'],
        "abstract": request['details']['abstract'],
        "keywords": request['details']['keywords'],
        "pdf_path": request['details']['pdf_path'],
        "image_path": request['details']['image_path'],
        "defense_date": defense_date,
        "examiners": [internal_examiner_id, external_examiner_id],
        "status": STATUS_DEFENSE_APPROVED,
        "grade": None,
        "scores": {}
    }
    theses.append(new_thesis)
    
    request['status'] = 'Finalized'
    internal_examiner['examiner_capacity'] -= 1
    external_examiner['examiner_capacity'] -= 1

    save_data('requests.json', requests)
    save_data('theses.json', theses)
    save_data('professors.json', professors)
    
    return True, "Defense session has been successfully scheduled."

def get_assigned_defenses(professor_id):
     
    theses = load_data('theses.json')
    return [t for t in theses if professor_id in t['examiners'] and t['grade'] is None]

def submit_grade(thesis_id, examiner_id, score):
     
    theses = load_data('theses.json')
    professors = load_data('professors.json')

    thesis = find_item_by_id(theses, thesis_id, 'thesis_id')
    if not thesis:
        return False, "Thesis not found."

    thesis['scores'][examiner_id] = score
    
    if len(thesis['scores']) == 2:
        final_score = sum(thesis['scores'].values()) / 2
        grade_map = {range(90, 101): 'A', range(80, 90): 'B', range(70, 80): 'C'}
        thesis['grade'] = next((g for r, g in grade_map.items() if final_score in r), 'D')
        thesis['status'] = STATUS_DEFENDED

        supervisor = find_item_by_id(professors, thesis['supervisor_id'], 'user_id')
        if supervisor:
            supervisor['supervision_capacity'] += 1
        
        for ex_id in thesis['examiners']:
            examiner = find_item_by_id(professors, ex_id, 'user_id')
            if examiner:
                examiner['examiner_capacity'] += 1
        
        save_data('professors.json', professors)

    save_data('theses.json', theses)
    return True, "Grade submitted successfully."

# --- Search Service ---
def search_theses(query, search_by):
     
    theses = load_data('theses.json')
    results = []
    query = query.lower()
    
    for thesis in theses:
        if thesis['status'] != STATUS_DEFENDED:
            continue

        match = False
        if search_by == 'title' and query in thesis['title'].lower():
            match = True
        elif search_by == 'author' and query in thesis['student_id'].lower():
            match = True
        elif search_by == 'supervisor' and query in thesis['supervisor_id'].lower():
            match = True
        elif search_by == 'keywords' and query in thesis['keywords'].lower():
            match = True
        
        if match:
            results.append(thesis)
            
    return results