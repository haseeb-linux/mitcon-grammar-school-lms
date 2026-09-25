"""
Mitcon Grammar School LMS — Configuration
"""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # Database
    DATA_DIR = os.path.join(BASE_DIR, "database")
    os.makedirs(DATA_DIR, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(DATA_DIR, 'mitcon.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # School Info
    SCHOOL_NAME = os.environ.get("SCHOOL_NAME", "Mitcon Grammar School")
    SCHOOL_TAGLINE = os.environ.get("SCHOOL_TAGLINE", "Learn. Grow. Succeed.")
    ACADEMIC_YEAR = os.environ.get("ACADEMIC_YEAR", "2026-2027")

    # Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

    # Classes
    CLASSES = ["KG1", "KG2", "KG3"] + [f"Class {i}" for i in range(1, 11)]
    SECTIONS = ["A", "B", "C"]