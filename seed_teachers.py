"""
Mitcon Grammar School LMS — Seed Teachers

Yeh script har campus mein 25 teachers add karti hai.
Total: 175 teachers (25 per campus × 7 campuses)

Features:
- Real Pakistani names (male + female)
- Random subject assignment
- Random qualification
- Random experience (1-15 years)
- Employee ID format: <CAMPUS_CODE>-T<001-025>

Chalane ka tarika:
    python seed_teachers.py
"""
import random
from datetime import date, timedelta

from app import app
from models import db, User, Teacher, Campus


# ============================================================
# DATA POOLS
# ============================================================
MALE_NAMES = [
    "Muhammad Ahmed", "Ali Hassan", "Usman Khan", "Bilal Ahmed", "Hamza Ali",
    "Fahad Iqbal", "Saad Malik", "Zain Abbas", "Umar Farooq", "Talha Raza",
    "Imran Sheikh", "Kashif Mehmood", "Adeel Akhtar", "Naveed Anjum", "Rizwan Ali",
    "Shahid Iqbal", "Tariq Jameel", "Waqas Ahmed", "Yasir Nawaz", "Zubair Khan",
    "Arslan Tariq", "Danish Ali", "Ehsan Ullah", "Faizan Ahmed", "Gulfam Hussain",
    "Haris Bin Rashid", "Ibrahim Khalil", "Junaid Akram", "Khalid Mehmood", "Liaqat Ali",
    "Mubashir Hassan", "Nadeem Aslam", "Owais Raza", "Pervaiz Ahmed", "Qasim Ali",
    "Rashid Minhas", "Sajid Hussain", "Taimoor Khan", "Umair Siddiqui", "Waleed Ahmed",
    "Yousuf Raza", "Zahid Hussain", "Abdul Rehman", "Babar Azam", "Chaudhry Ahmad",
    "Dawood Ibrahim", "Ejaz Ahmed", "Farhan Saeed", "Ghulam Mustafa", "Hafiz Bilal",
]

FEMALE_NAMES = [
    "Ayesha Khan", "Fatima Ali", "Sana Ahmed", "Hira Malik", "Maryam Siddiqui",
    "Zainab Raza", "Areeba Hassan", "Amna Iqbal", "Rabia Nawaz", "Sadia Mehmood",
    "Noor Fatima", "Aiman Tariq", "Iqra Aslam", "Kiran Shahid", "Laiba Ahmed",
    "Mehwish Anjum", "Nadia Hussain", "Palwasha Khan", "Qurat ul Ain", "Rida Ali",
    "Saba Jameel", "Tahira Akram", "Uzma Rashid", "Varisha Khan", "Warda Saleem",
    "Yasmeen Akhtar", "Zoya Malik", "Afshan Ahmed", "Bushra Iqbal", "Chandni Raza",
    "Dua Fatima", "Eman Tariq", "Faryal Khan", "Ghazala Ahmed", "Hafsa Siddiqui",
    "Iqra Aziz", "Javeria Saud", "Komal Rizvi", "Lubna Khalid", "Mahnoor Baloch",
    "Nargis Ahmed", "Nida Yasir", "Parveen Akhtar", "Rani Ahmed", "Sajal Aly",
    "Sana Javed", "Shazia Manzoor", "Sobia Khan", "Ushna Shah", "Zara Sheikh",
]

SUBJECTS = [
    "Mathematics", "English", "Urdu", "Islamiat", "Pakistan Studies",
    "Physics", "Chemistry", "Biology", "Computer Science", "General Science",
    "Social Studies", "Arabic", "Health & Physical Education", "Art & Craft",
]

QUALIFICATIONS = [
    "M.Sc Mathematics", "M.A English", "M.A Urdu", "M.A Islamiat",
    "M.A Pakistan Studies", "M.Sc Physics", "M.Sc Chemistry", "M.Sc Biology",
    "MCS Computer Science", "B.Ed", "M.Ed", "BS Education",
    "M.Phil Education", "M.A Arabic", "B.Sc Physical Education",
]

PHONE_PREFIXES = ["300", "301", "302", "303", "321", "322", "333", "345"]


def random_phone():
    return f"+92 {random.choice(PHONE_PREFIXES)} {random.randint(1000000, 9999999)}"


def random_join_date():
    """Random date within last 1-15 years."""
    days_ago = random.randint(365, 365 * 15)
    return date.today() - timedelta(days=days_ago)


def seed_teachers():
    with app.app_context():
        print("\n" + "=" * 60)
        print("👨‍🏫 Seeding Teachers...")
        print("=" * 60)

        campuses = Campus.query.all()
        if not campuses:
            print("❌ No campuses found. Please run seed_campuses.py first.")
            return

        total_added = 0
        total_skipped = 0

        for campus in campuses:
            print(f"\n📚 Campus: {campus.name} [{campus.code}]")
            campus_added = 0

            # Mix male and female teachers
            all_names = random.sample(MALE_NAMES, 13) + random.sample(FEMALE_NAMES, 12)
            random.shuffle(all_names)

            for i, name in enumerate(all_names, start=1):
                employee_id = f"{campus.code}-T{i:03d}"
                username = f"teacher.{campus.code.lower()}{i:02d}"

                # Skip if exists
                if User.query.filter_by(username=username).first():
                    total_skipped += 1
                    continue

                # Create User
                user = User(
                    username=username,
                    email=f"{username}@mitcon.edu.pk",
                    full_name=name,
                    role="teacher",
                    phone=random_phone(),
                    campus_id=campus.id,
                )
                user.set_password("teacher123")
                db.session.add(user)
                db.session.flush()  # Get user.id

                # Create Teacher profile
                teacher = Teacher(
                    user_id=user.id,
                    employee_id=employee_id,
                    subject_specialty=random.choice(SUBJECTS),
                    qualification=random.choice(QUALIFICATIONS),
                    joining_date=random_join_date(),
                    campus_id=campus.id,
                )
                db.session.add(teacher)
                campus_added += 1
                total_added += 1

            db.session.commit()
            print(f"   ✅ {campus_added} teachers added")

        # ============ SUMMARY ============
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Total Teachers Added:   {total_added}")
        print(f"⏭️  Skipped (existing):    {total_skipped}")
        print(f"📊 Total Teachers in DB:   {Teacher.query.count()}")
        print("=" * 60)

        # Per-campus breakdown
        print("\n📚 Per-Campus Breakdown:")
        print("-" * 60)
        for campus in campuses:
            count = Teacher.query.filter_by(campus_id=campus.id).count()
            print(f"  [{campus.code:8s}] {campus.name:30s} → {count} teachers")

        print("\n🔑 Sample Login Credentials:")
        print("   Username: teacher.main01  | Password: teacher123")
        print("   Username: teacher.city01  | Password: teacher123")
        print("   Username: teacher.girls01 | Password: teacher123")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_teachers()