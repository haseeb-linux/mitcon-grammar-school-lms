"""
Mitcon Grammar School LMS — Super Admin Routes
Super Admin: saare 7 campuses ka access
"""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import (
    db, User, Student, Teacher, Parent, Class, Subject,
    Campus, Announcement, Diary
)

superadmin_bp = Blueprint("superadmin", __name__, url_prefix="/superadmin")


def superadmin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "superadmin":
            flash("Super Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


@superadmin_bp.route("/dashboard")
@login_required
@superadmin_required
def dashboard():
    # All campuses
    campuses = Campus.query.all()
    
    # Global stats
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_parents = Parent.query.count()
    total_classes = Class.query.count()
    total_subjects = Subject.query.count()
    total_announcements = Announcement.query.count()
    
    # Per-campus stats
    campus_stats = []
    for campus in campuses:
        campus_stats.append({
            "campus": campus,
            "students": Student.query.filter_by(campus_id=campus.id).count(),
            "teachers": Teacher.query.filter_by(campus_id=campus.id).count(),
            "classes": Class.query.filter_by(campus_id=campus.id).count(),
            "principals": User.query.filter_by(campus_id=campus.id, role="principal").count(),
        })
    
    return render_template(
        "superadmin/dashboard.html",
        campuses=campuses,
        campus_stats=campus_stats,
        total_students=total_students,
        total_teachers=total_teachers,
        total_parents=total_parents,
        total_classes=total_classes,
        total_subjects=total_subjects,
        total_announcements=total_announcements,
    )


@superadmin_bp.route("/campus/<int:campus_id>")
@login_required
@superadmin_required
def campus_detail(campus_id):
    campus = Campus.query.get_or_404(campus_id)
    
    students = Student.query.filter_by(campus_id=campus.id).limit(50).all()
    teachers = Teacher.query.filter_by(campus_id=campus.id).all()
    classes = Class.query.filter_by(campus_id=campus.id).all()
    announcements = Announcement.query.filter_by(campus_id=campus.id).order_by(
        Announcement.date.desc()
    ).limit(10).all()
    
    return render_template(
        "superadmin/campus_detail.html",
        campus=campus,
        students=students,
        teachers=teachers,
        classes=classes,
        announcements=announcements,
    )


@superadmin_bp.route("/campuses")
@login_required
@superadmin_required
def campuses():
    all_campuses = Campus.query.all()
    return render_template("superadmin/campuses.html", campuses=all_campuses)


@superadmin_bp.route("/all-students")
@login_required
@superadmin_required
def all_students():
    students = Student.query.limit(100).all()
    return render_template("superadmin/all_students.html", students=students)


@superadmin_bp.route("/all-teachers")
@login_required
@superadmin_required
def all_teachers():
    teachers = Teacher.query.limit(100).all()
    return render_template("superadmin/all_teachers.html", teachers=teachers)