"""
Mitcon Grammar School LMS — Seed Super Admin

Super Admin banao jo saare 7 campuses ka data dekh sake.

Chalane ka tarika:
    python seed_superadmin.py
"""
from app import app
from models import db, User, Campus


def seed_superadmin():
    with app.app_context():
        print("\n" + "=" * 60)
        print("👑 Seeding Super Admin...")
        print("=" * 60)

        username = "superadmin"

        if User.query.filter_by(username=username).first():
            print(f"⏭️  Super Admin '{username}' already exists")
            print("=" * 60 + "\n")
            return

        superadmin = User(
            username=username,
            email="superadmin@mitcon.edu.pk",
            full_name="Super Administrator",
            role="superadmin",
            phone="+92 300 0000000",
            campus_id=None,  # No specific campus — saare campuses ka access
        )
        superadmin.set_password("super123")
        db.session.add(superadmin)
        db.session.commit()

        print("\n✅ Super Admin created!")
        print("=" * 60)
        print("🔑 LOGIN CREDENTIALS:")
        print("   Username: superadmin")
        print("   Password: super123")
        print("=" * 60)
        print("\n📊 Campus Access: ALL 7 CAMPUSES")
        for c in Campus.query.all():
            print(f"   ✓ [{c.code}] {c.name}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_superadmin()