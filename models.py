"""
Mitcon Grammar School LMS — Database Models (Multi-Campus)
All tables: campuses, users, students, teachers, parents, classes, subjects,
diary, tests, test_results, papers, paper_results, attendance,
announcements, fees, timetable.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ============================================================
# CAMPUSES
# ============================================================
class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    principal_name = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "principal_name": self.principal_name,
        }


# ============================================================
# USERS (Base table for all roles)
# ============================================================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # superadmin, principal, teacher, student, parent
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=True)
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    campus = db.relationship("Campus", backref="users")

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "full_name": self.full_name,
            "campus_id": self.campus_id,
        }


# ============================================================
# CLASSES
# ============================================================
class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # KG1, Class 1, etc.
    section = db.Column(db.String(5), nullable=True)  # A, B, C
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)

    campus = db.relationship("Campus", backref="classes")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "section": self.section, "campus_id": self.campus_id}


# ============================================================
# TEACHERS
# ============================================================
class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    qualification = db.Column(db.String(120), nullable=True)
    subject_specialty = db.Column(db.String(80), nullable=True)
    joining_date = db.Column(db.Date, nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    user = db.relationship("User", backref="teacher_profile")
    campus = db.relationship("Campus", backref="teachers")

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "name": self.user.full_name if self.user else None,
            "subject": self.subject_specialty,
            "campus_id": self.campus_id,
        }


# ============================================================
# STUDENTS
# ============================================================
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    admission_no = db.Column(db.String(20), unique=True, nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    section = db.Column(db.String(5), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=True)
    admission_date = db.Column(db.Date, nullable=True)
    blood_group = db.Column(db.String(5), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    user = db.relationship("User", backref="student_profile")
    student_class = db.relationship("Class", backref="students")
    campus = db.relationship("Campus", backref="students")

    def to_dict(self):
        return {
            "id": self.id,
            "roll_no": self.roll_no,
            "name": self.user.full_name if self.user else None,
            "class": self.student_class.name if self.student_class else None,
            "section": self.section,
            "campus_id": self.campus_id,
        }


# ============================================================
# PARENTS
# ============================================================
class Parent(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    relation = db.Column(db.String(20), nullable=True)  # Father, Mother, Guardian
    occupation = db.Column(db.String(80), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=True)

    user = db.relationship("User", backref="parent_profile")
    children = db.relationship("Student", backref="parent", lazy=True)
    campus = db.relationship("Campus", backref="parents")


# ============================================================
# SUBJECTS
# ============================================================
class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    total_marks = db.Column(db.Integer, default=100)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    subject_class = db.relationship("Class", backref="subjects")
    subject_teacher = db.relationship("Teacher", backref="subjects")
    campus = db.relationship("Campus", backref="subjects")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "class": self.subject_class.name if self.subject_class else None}


# ============================================================
# DIARY
# ============================================================
class Diary(db.Model):
    __tablename__ = "diary"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    diary_class = db.relationship("Class", backref="diary_entries")
    diary_subject = db.relationship("Subject", backref="diary_entries")
    diary_teacher = db.relationship("Teacher", backref="diary_entries")
    campus = db.relationship("Campus", backref="diary_entries")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "subject": self.diary_subject.name if self.diary_subject else None,
            "title": self.title,
            "content": self.content,
        }


# ============================================================
# TESTS
# ============================================================
class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    total_marks = db.Column(db.Integer, default=100)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    test_class = db.relationship("Class", backref="tests")
    test_subject = db.relationship("Subject", backref="tests")
    campus = db.relationship("Campus", backref="tests")


class TestResult(db.Model):
    __tablename__ = "test_results"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=True)
    remarks = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    test = db.relationship("Test", backref="results")
    student = db.relationship("Student", backref="test_results")


# ============================================================
# PAPERS (Exams)
# ============================================================
class Paper(db.Model):
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    paper_date = db.Column(db.Date, nullable=False)
    total_marks = db.Column(db.Integer, default=100)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    paper_class = db.relationship("Class", backref="papers")
    paper_subject = db.relationship("Subject", backref="papers")
    campus = db.relationship("Campus", backref="papers")


class PaperResult(db.Model):
    __tablename__ = "paper_results"

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=True)
    remarks = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    paper = db.relationship("Paper", backref="results")
    student = db.relationship("Student", backref="paper_results")


# ============================================================
# ATTENDANCE
# ============================================================
class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # present, absent, leave, late
    marked_by = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    remarks = db.Column(db.String(200), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    student = db.relationship("Student", backref="attendance_records")
    campus = db.relationship("Campus", backref="attendance_records")

    __table_args__ = (
        db.UniqueConstraint("student_id", "date", name="uq_student_date_attendance"),
    )


# ============================================================
# ANNOUNCEMENTS
# ============================================================
class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    target = db.Column(db.String(30), default="all")  # all, teachers, students, parents, campus
    target_class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=True)
    posted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(10), default="normal")  # normal, high, urgent

    campus = db.relationship("Campus", backref="announcements")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date.isoformat() if self.date else None,
            "priority": self.priority,
            "campus_id": self.campus_id,
        }


# ============================================================
# FEES
# ============================================================
class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default="unpaid")  # paid, unpaid, partial
    paid_amount = db.Column(db.Float, default=0)
    paid_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.String(200), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    student = db.relationship("Student", backref="fees")
    campus = db.relationship("Campus", backref="fees")


# ============================================================
# TIMETABLE
# ============================================================
class Timetable(db.Model):
    __tablename__ = "timetable"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    start_time = db.Column(db.String(10), nullable=True)
    end_time = db.Column(db.String(10), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=False)

    tt_class = db.relationship("Class", backref="timetable")
    tt_subject = db.relationship("Subject", backref="timetable")
    campus = db.relationship("Campus", backref="timetable")