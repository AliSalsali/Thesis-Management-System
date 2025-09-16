from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, password_hash):
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash

    @abstractmethod
    def get_dashboard(self):
        pass

class Student(User):
    def __init__(self, user_id, name, password_hash):
        super().__init__(user_id, name, password_hash)

    def get_dashboard(self):
        return f"Student Dashboard: {self.name} ({self.user_id})"

class Professor(User):
    def __init__(self, user_id, name, password_hash, supervision_capacity, examiner_capacity):
        super().__init__(user_id, name, password_hash)
        self.supervision_capacity = supervision_capacity
        self.examiner_capacity = examiner_capacity

    def get_dashboard(self):
        return (f"Professor Dashboard: {self.name} ({self.user_id})\n"
                f"Supervision Capacity: {self.supervision_capacity}\n"
                f"Examiner Capacity: {self.examiner_capacity}")

class ThesisCourse:
    def __init__(self, course_id, title, professor_id, year, semester, capacity, unit):
        self.course_id = course_id
        self.title = title
        self.professor_id = professor_id
        self.year = year
        self.semester = semester
        self.capacity = capacity
        self.unit = unit