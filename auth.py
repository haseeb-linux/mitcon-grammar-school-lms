"""
Mitcon Grammar School LMS — Authentication
Login, logout, signup, role-based access.
Supports: superadmin, principal, teacher, student, parent, admin
"""
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Student, Teacher, Parent

auth_bp = Blueprint("auth", __name__)


# ============================================================
# ROLE DECORATORS
# ============================================================
def role_required(*roles):
    """Restrict a route to specific roles."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                flash("You don't have permission to access that page.", "danger")
                return redirect(url_for("auth.dashboard_redirect"))
            return f(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# LOGIN
# ============================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard_redirect"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember", False)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active_account:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=bool(remember))
            flash(f"Welcome back, {user.full_name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("auth.dashboard_redirect"))
        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")


# ============================================================
# LOGOUT
# ============================================================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ============================================================
# REDIRECT TO CORRECT DASHBOARD (by role)
# ============================================================
@auth_bp.route("/dashboard")
@login_required
def dashboard_redirect():
    role = current_user.role
    
    if role == "superadmin":
        return redirect(url_for("superadmin.dashboard"))
    elif role == "principal":
        return redirect(url_for("principal.dashboard"))
    elif role == "admin":
        return redirect(url_for("admin.dashboard"))
    elif role == "teacher":
        return redirect(url_for("teacher.dashboard"))
    elif role == "student":
        return redirect(url_for("student.dashboard"))
    elif role == "parent":
        return redirect(url_for("parent.dashboard"))
    
    flash("Unknown role. Please contact admin.", "danger")
    return redirect(url_for("auth.login"))


# ============================================================
# CHANGE PASSWORD
# ============================================================
@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old = request.form.get("old_password", "")
        new = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")

        if not current_user.check_password(old):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))
        if new != confirm:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("auth.change_password"))
        if len(new) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("auth.change_password"))

        current_user.set_password(new)
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect(url_for("auth.dashboard_redirect"))

    return render_template("auth/change_password.html")


# ============================================================
# PROFILE
# ============================================================
@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("auth/profile.html")