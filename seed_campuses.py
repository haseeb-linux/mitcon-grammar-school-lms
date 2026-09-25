"""
Mitcon Grammar School LMS — Seed Campuses

Yeh script 7 campuses database mein add karti hai.
Chalane ka tarika:
    python seed_campuses.py
"""
from app import app
from models import db, Campus


CAMPUSES = [
    {
        "name": "Mitcon Main Campus",
        "code": "MAIN",
        "address": "Main Boulevard, Lahore",
        "phone": "+92 42 111-001-001",
        "email": "main@mitcon.edu.pk",
        "principal_name": "Mr. Muhammad Aslam",
    },
    {
        "name": "Mitcon City Campus",
        "code": "CITY",
        "address": "City Center, Lahore",
        "phone": "+92 42 111-001-002",
        "email": "city@mitcon.edu.pk",
        "principal_name": "Mrs. Ayesha Khan",
    },
    {
        "name": "Mitcon Girls Campus",
        "code": "GIRLS",
        "address": "Gulberg III, Lahore",
        "phone": "+92 42 111-001-003",
        "email": "girls@mitcon.edu.pk",
        "principal_name": "Mrs. Fatima Siddiqui",
    },
    {
        "name": "Mitcon Boys Campus",
        "code": "BOYS",
        "address": "DHA Phase 5, Lahore",
        "phone": "+92 42 111-001-004",
        "email": "boys@mitcon.edu.pk",
        "principal_name": "Mr. Hassan Raza",
    },
    {
        "name": "Mitcon Junior Campus",
        "code": "JUNIOR",
        "address": "Johar Town, Lahore",
        "phone": "+92 42 111-001-005",
        "email": "junior@mitcon.edu.pk",
        "principal_name": "Mrs. Sana Ahmed",
    },
    {
        "name": "Mitcon Model Town Campus",
        "code": "MODEL",
        "address": "Model Town Link Road, Lahore",
        "phone": "+92 42 111-001-006",
        "email": "model@mitcon.edu.pk",
        "principal_name": "Mr. Bilal Hussain",
    },
    {
        "name": "Mitcon Garden Campus",
        "code": "GARDEN",
        "address": "Garden Town, Lahore",
        "phone": "+92 42 111-001-007",
        "email": "garden@mitcon.edu.pk",
        "principal_name": "Mrs. Nadia Malik",
    },
]


def seed_campuses():
    with app.app_context():
        print("\n" + "=" * 60)
        print("🏫 Seeding Campuses...")
        print("=" * 60)

        added = 0
        for c in CAMPUSES:
            if not Campus.query.filter_by(code=c["code"]).first():
                db.session.add(Campus(**c))
                added += 1

        db.session.commit()

        print(f"\n✅ {added} new campuses added!")
        print(f"📊 Total Campuses: {Campus.query.count()}\n")
        print("All Campuses:")
        print("-" * 60)
        for campus in Campus.query.order_by(Campus.id).all():
            print(f"  [{campus.code}] {campus.name}")
            print(f"       Principal: {campus.principal_name}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_campuses()