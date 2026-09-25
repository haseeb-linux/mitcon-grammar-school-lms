"""
Mitcon Grammar School LMS — Principal Routes
Principal: sirf apne campus ka access
"""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import (
    db, User, Student, Teacher, Parent, Class, Subject,
    Campus, Announcement, Diary
)

principal_bp = Blueprint("principal", __name__, url_prefix="/principal")


def principal_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "principal":
            flash("Principal access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def get_my_campus():
    """Get current principal's campus."""
    if current_user.campus_id:
        return Campus.query.get(current_user.campus_id)
    return None


@principal_bp.route("/dashboard")
@login_required
@principal_required
def dashboard():
    campus = get_my_campus()
    if not campus:
        flash("No campus assigned to your account.", "danger")
        return redirect(url_for("auth.logout"))
    
    # Campus-specific stats
    total_students = Student.query.filter_by(campus_id=campus.id).count()
    total_teachers = Teacher.query.filter_by(campus_id=campus.id).count()
    total_parents = Parent.query.filter_by(campus_id=campus.id).count()
    total_classes = Class.query.filter_by(campus_id=campus.id).count()
    total_subjects = Subject.query.filter_by(campus_id=campus.id).count()
    
    recent_announcements = Announcement.query.filter_by(campus_id=campus.id).order_by(
        Announcement.date.desc()
    ).limit(5).all()
    
    return render_template(
        "principal/dashboard.html",
        campus=campus,
        total_students=total_students,
        total_teachers=total_teachers,
        total_parents=total_parents,
        total_classes=total_classes,
        total_subjects=total_subjects,
        recent_announcements=recent_announcements,
    )


@principal_bp.route("/students")
@login_required
@principal_required
def students():
    campus = get_my_campus()
    students = Student.query.filter_by(campus_id=campus.id).limit(100).all()
    return render_template("principal/students.html", students=students, campus=campus)


@principal_bp.route("/teachers")
@login_required
@principal_required
def teachers():
    campus = get_my_campus()
    teachers = Teacher.query.filter_by(campus_id=campus.id).all()
    return render_template("principal/teachers.html", teachers=teachers, campus=campus)


@principal_bp.route("/classes")
@login_required
@principal_required
def classes():
    campus = get_my_campus()
    classes = Class.query.filter_by(campus_id=campus.id).all()
    return render_template("principal/classes.html", classes=classes, campus=campus)


@principal_bp.route("/announcements")
@login_required
@principal_required
def announcements():
    campus = get_my_campus()
    announcements = Announcement.query.filter_by(campus_id=campus.id).order_by(
        Announcement.date.desc()
    ).all()
    return render_template("principal/announcements.html", announcements=announcements, campus=campus)