"""
Mitcon Grammar School LMS — Flask Application Entry Point
"""
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user

from config import Config
from models import db, User, Announcement, Campus, Class, Diary, Student
from auth import auth_bp
from admin_routes import admin_bp
from superadmin_routes import superadmin_bp
from principal_routes import principal_bp


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


def create_app():
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    print("=" * 60)
    print(f"📁 Template Folder: {TEMPLATE_DIR}")
    print(f"📁 Static Folder:   {STATIC_DIR}")
    print(f"📁 Templates Exist: {os.path.exists(TEMPLATE_DIR)}")
    print(f"📁 login.html:      {os.path.exists(os.path.join(TEMPLATE_DIR, 'auth', 'login.html'))}")
    print("=" * 60)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access that page."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ============================================================
    # REGISTER BLUEPRINTS
    # ============================================================
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superadmin_bp)
    app.register_blueprint(principal_bp)

    # ============================================================
    # HOME ROUTE
    # ============================================================
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("auth.dashboard_redirect"))
        return render_template("index.html")

    # ============================================================
    # PUBLIC PAGES (No login required) — FAST VERSIONS
    # ============================================================

    @app.route("/announcements")
    def announcements():
        all_announcements = Announcement.query.order_by(
            Announcement.date.desc()
        ).limit(30).all()
        return render_template("announcements.html", announcements=all_announcements)

    # ------------------------------------------------------------
    # DIARY — Optimized (limit + no heavy joins)
    # ------------------------------------------------------------
    @app.route("/diary")
    def diary():
        campus_id = request.args.get("campus", type=int)
        class_name = request.args.get("class", "")

        query = Diary.query
        if campus_id:
            query = query.filter_by(campus_id=campus_id)
        if class_name:
            cls = Class.query.filter_by(name=class_name).first()
            if cls:
                query = query.filter_by(class_id=cls.id)

        # Only 12 entries, newest first
        diaries = query.order_by(Diary.date.desc()).limit(12).all()
        campuses = Campus.query.all()
        class_list = ["KG1", "KG2", "KG3"] + [f"Class {i}" for i in range(1, 11)]

        return render_template(
            "diary.html",
            diaries=diaries,
            campuses=campuses,
            class_list=class_list,
            selected_campus=campus_id,
            selected_class=class_name,
        )

    # ------------------------------------------------------------
    # TESTS — Static page
    # ------------------------------------------------------------
    @app.route("/tests")
    def tests():
        return render_template("tests.html")

    # ------------------------------------------------------------
    # ATTENDANCE — FAST VERSION (no random, no heavy queries)
    # ------------------------------------------------------------
    @app.route("/attendance")
    def attendance():
        campuses = Campus.query.all()

        # Pre-compute total students per campus (1 query per campus)
        campus_attendance = []
        total_students = 0
        total_present = 0

        for c in campuses:
            total = Student.query.filter_by(campus_id=c.id).count()

            # Simulated attendance: 92% present (deterministic)
            present = int(total * 0.92)
            absent = total - present
            pct = 92.0

            campus_attendance.append({
                "name": c.name,
                "code": c.code,
                "total": total,
                "present": present,
                "absent": absent,
                "pct": pct,
            })
            total_students += total
            total_present += present

        absent_count = total_students - total_present
        attendance_pct = round((total_present / total_students * 100), 1) if total_students else 0

        return render_template(
            "attendance.html",
            campus_attendance=campus_attendance,
            total_students=total_students,
            present_count=total_present,
            absent_count=absent_count,
            attendance_pct=attendance_pct,
        )

    # ------------------------------------------------------------
    # FEES — Static page
    # ------------------------------------------------------------
    @app.route("/fees")
    def fees():
        return render_template("fees.html")

    # ------------------------------------------------------------
    # MOBILE APP — Static page
    # ------------------------------------------------------------
    @app.route("/mobile-app")
    def mobile_app():
        return render_template("mobile-app.html")

    # ============================================================
    # CONTEXT PROCESSOR
    # ============================================================
    @app.context_processor
    def inject_school_info():
        return {
            "school_name": app.config["SCHOOL_NAME"],
            "school_tagline": app.config["SCHOOL_TAGLINE"],
            "academic_year": app.config["ACADEMIC_YEAR"],
        }

    # ============================================================
    # ERROR HANDLERS
    # ============================================================
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    # ============================================================
    # CREATE DATABASE + SEED ADMIN
    # ============================================================
    with app.app_context():
        db.create_all()
        _create_default_admin()

    return app


def _create_default_admin():
    if User.query.filter_by(role="admin").first() is None:
        admin = User(
            username="admin",
            email="admin@mitcon.edu.pk",
            full_name="School Administrator",
            role="admin",
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("\n✅ Default Admin Created: admin / admin123\n")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)