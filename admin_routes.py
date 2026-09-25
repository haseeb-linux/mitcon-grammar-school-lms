"""
Mitcon Grammar School LMS — Admin Routes
"""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Student, Teacher, Parent, Class, Subject, Announcement

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {
        "total_students": Student.query.count(),
        "total_teachers": Teacher.query.count(),
        "total_parents": Parent.query.count(),
        "total_classes": Class.query.count(),
        "total_announcements": Announcement.query.count(),
    }
    recent_announcements = Announcement.query.order_by(
        Announcement.date.desc()
    ).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, recent_announcements=recent_announcements)


@admin_bp.route("/students")
@login_required
@admin_required
def students():
    all_students = Student.query.all()
    return render_template("admin/students.html", students=all_students)


@admin_bp.route("/teachers")
@login_required
@admin_required
def teachers():
    all_teachers = Teacher.query.all()
    return render_template("admin/teachers.html", teachers=all_teachers)


@admin_bp.route("/classes")
@login_required
@admin_required
def classes():
    all_classes = Class.query.all()
    return render_template("admin/classes.html", classes=all_classes)


@admin_bp.route("/announcements")
@login_required
@admin_required
def announcements():
    all_announcements = Announcement.query.order_by(Announcement.date.desc()).all()
    return render_template("admin/announcements.html", announcements=all_announcements)