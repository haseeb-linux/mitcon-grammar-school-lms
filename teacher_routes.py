"""
Mitcon Grammar School LMS — Teacher Routes
Teacher: sirf apni classes ka access
"""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Student, Teacher, Class, Subject, Diary, Campus

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


def teacher_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "teacher":
            flash("Teacher access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def get_my_teacher():
    """Get current teacher's profile."""
    return Teacher.query.filter_by(user_id=current_user.id).first()


def get_my_campus():
    """Get current teacher's campus."""
    if current_user.campus_id:
        return Campus.query.get(current_user.campus_id)
    return None


def get_my_subjects(teacher):
    """Get subjects assigned to this teacher."""
    return Subject.query.filter_by(teacher_id=teacher.id).all()


@teacher_bp.route("/dashboard")
@login_required
@teacher_required
def dashboard():
    teacher = get_my_teacher()
    if not teacher:
        flash("Teacher profile not found.", "danger")
        return redirect(url_for("auth.logout"))
    
    campus = get_my_campus()
    my_subjects = get_my_subjects(teacher)
    
    # Get unique classes from my subjects
    my_classes = list(set([s.subject_class for s in my_subjects if s.subject_class]))
    
    # Count students in my classes
    class_ids = [c.id for c in my_classes]
    total_students = Student.query.filter(Student.class_id.in_(class_ids)).count() if class_ids else 0
    
    # Recent diary entries by me
    recent_diaries = Diary.query.filter_by(
        teacher_id=teacher.id
    ).order_by(Diary.date.desc()).limit(5).all()
    
    return render_template(
        "teacher/dashboard.html",
        teacher=teacher,
        campus=campus,
        my_classes=my_classes,
        my_subjects=my_subjects,
        total_students=total_students,
        recent_diaries=recent_diaries,
    )


@teacher_bp.route("/students")
@login_required
@teacher_required
def students():
    teacher = get_my_teacher()
    my_subjects = get_my_subjects(teacher)
    my_classes = list(set([s.subject_class for s in my_subjects if s.subject_class]))
    class_ids = [c.id for c in my_classes]
    
    students = Student.query.filter(Student.class_id.in_(class_ids)).limit(100).all() if class_ids else []
    
    return render_template(
        "teacher/students.html",
        teacher=teacher,
        students=students,
        my_classes=my_classes,
    )


@teacher_bp.route("/diary")
@login_required
@teacher_required
def diary():
    teacher = get_my_teacher()
    my_subjects = get_my_subjects(teacher)
    
    # Diary entries added by me
    my_diaries = Diary.query.filter_by(
        teacher_id=teacher.id
    ).order_by(Diary.date.desc()).limit(20).all()
    
    return render_template(
        "teacher/diary.html",
        teacher=teacher,
        my_subjects=my_subjects,
        my_diaries=my_diaries,
    )


@teacher_bp.route("/attendance")
@login_required
@teacher_required
def attendance():
    teacher = get_my_teacher()
    my_subjects = get_my_subjects(teacher)
    my_classes = list(set([s.subject_class for s in my_subjects if s.subject_class]))
    
    return render_template(
        "teacher/attendance.html",
        teacher=teacher,
        my_classes=my_classes,
    )


@teacher_bp.route("/marks")
@login_required
@teacher_required
def marks():
    teacher = get_my_teacher()
    my_subjects = get_my_subjects(teacher)
    
    return render_template(
        "teacher/marks.html",
        teacher=teacher,
        my_subjects=my_subjects,
    )