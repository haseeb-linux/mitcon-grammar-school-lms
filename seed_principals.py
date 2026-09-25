"""
Mitcon Grammar School LMS — Seed Principals

Yeh script har campus ka 1 principal add karti hai.
Total: 7 principals (1 per campus)

Chalane ka tarika:
    python seed_principals.py
"""
from app import app
from models import db, User, Campus


PRINCIPALS = [
    {"campus_code": "MAIN",   "username": "principal.main",   "name": "Mr. Muhammad Aslam",   "phone": "+92 300 1111111"},
    {"campus_code": "CITY",   "username": "principal.city",   "name": "Mrs. Ayesha Khan",     "phone": "+92 300 2222222"},
    {"campus_code": "GIRLS",  "username": "principal.girls",  "name": "Mrs. Fatima Siddiqui", "phone": "+92 300 3333333"},
    {"campus_code": "BOYS",   "username": "principal.boys",   "name": "Mr. Hassan Raza",      "phone": "+92 300 4444444"},
    {"campus_code": "JUNIOR", "username": "principal.junior", "name": "Mrs. Sana Ahmed",      "phone": "+92 300 5555555"},
    {"campus_code": "MODEL",  "username": "principal.model",  "name": "Mr. Bilal Hussain",    "phone": "+92 300 6666666"},
    {"campus_code": "GARDEN", "username": "principal.garden", "name": "Mrs. Nadia Malik",     "phone": "+92 300 7777777"},
]


def seed_principals():
    with app.app_context():
        print("\n" + "=" * 60)
        print("👔 Seeding Principals...")
        print("=" * 60)

        added = 0
        skipped = 0

        for p in PRINCIPALS:
            campus = Campus.query.filter_by(code=p["campus_code"]).first()
            if not campus:
                print(f"⚠️  Campus not found: {p['campus_code']}")
                continue

            existing = User.query.filter_by(username=p["username"]).first()
            if existing:
                skipped += 1
                continue

            user = User(
                username=p["username"],
                email=f"{p['username']}@mitcon.edu.pk",
                full_name=p["name"],
                role="principal",
                phone=p["phone"],
                campus_id=campus.id,
            )
            user.set_password("principal123")
            db.session.add(user)
            added += 1

        db.session.commit()

        print(f"\n✅ {added} principals added!")
        print(f"⏭️  {skipped} skipped (already existed)")
        print(f"📊 Total Principals: {User.query.filter_by(role='principal').count()}\n")

        print("All Principals:")
        print("-" * 60)
        for p in User.query.filter_by(role="principal").all():
            campus = Campus.query.get(p.campus_id)
            print(f"  {p.username:25s} | {p.full_name:25s} | {campus.code if campus else 'N/A'}")

        print("\n🔑 Login Credentials:")
        print("   Username: principal.main  | Password: principal123")
        print("   Username: principal.city  | Password: principal123")
        print("   Username: principal.girls | Password: principal123")
        print("   Username: principal.boys  | Password: principal123")
        print("   Username: principal.junior| Password: principal123")
        print("   Username: principal.model | Password: principal123")
        print("   Username: principal.garden| Password: principal123")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_principals()