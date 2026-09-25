"""
Seed remaining students (cities other than MAIN)
"""
import random
from datetime import date, timedelta
from app import app
from models import db, User, Student, Parent, Teacher, Class, Campus  # ⬅️ Teacher added


# Same name pools as before
MALE_FIRST = [
    "Ahmed", "Ali", "Hassan", "Hussain", "Usman", "Bilal", "Hamza", "Fahad",
    "Saad", "Zain", "Umar", "Talha", "Imran", "Kashif", "Adeel", "Naveed",
    "Rizwan", "Shahid", "Tariq", "Waqas", "Yasir", "Zubair", "Arslan", "Danish",
    "Ehsan", "Faizan", "Gulfam", "Haris", "Ibrahim", "Junaid", "Khalid", "Liaqat",
    "Mubashir", "Nadeem", "Owais", "Pervaiz", "Qasim", "Rashid", "Sajid", "Taimoor",
    "Umair", "Waleed", "Yousuf", "Zahid", "Babar", "Dawood", "Ejaz", "Farhan",
    "Ghulam", "Hafiz",
]
FEMALE_FIRST = [
    "Ayesha", "Fatima", "Sana", "Hira", "Maryam", "Zainab", "Areeba", "Amna",
    "Rabia", "Sadia", "Noor", "Aiman", "Iqra", "Kiran", "Laiba", "Mehwish",
    "Nadia", "Palwasha", "Qurat", "Rida", "Saba", "Tahira", "Uzma", "Varisha",
    "Warda", "Yasmeen", "Zoya", "Afshan", "Bushra", "Chandni", "Dua", "Eman",
    "Faryal", "Ghazala", "Hafsa", "Javeria", "Komal", "Lubna", "Mahnoor", "Nargis",
    "Nida", "Parveen", "Rani", "Sajal", "Shazia", "Sobia", "Ushna", "Zara",
    "Huma", "Saira",
]
LAST_NAMES = [
    "Khan", "Ahmed", "Ali", "Malik", "Sheikh", "Raza", "Hussain", "Iqbal",
    "Siddiqui", "Abbas", "Farooq", "Mehmood", "Akhtar", "Anjum", "Jameel",
    "Nawaz", "Tariq", "Aslam", "Hassan", "Baig", "Chaudhry", "Butt", "Qureshi",
    "Awan", "Gill", "Mirza", "Shah", "Syed", "Hashmi", "Zaidi",
]
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
AREAS = ["Gulberg", "DHA", "Model Town", "Johar Town", "Garden Town", "Faisal Town"]
CITIES = ["Lahore", "Karachi", "Islamabad", "Rawalpindi", "Faisalabad"]
PHONE_PREFIXES = ["300", "301", "302", "303", "321", "322", "333", "345", "311", "312"]


def random_phone():
    return f"+92 {random.choice(PHONE_PREFIXES)} {random.randint(1000000, 9999999)}"


def random_dob_for_class(class_name):
    age_map = {"KG1": 4, "KG2": 5, "KG3": 6, "Class 1": 7, "Class 2": 8,
               "Class 3": 9, "Class 4": 10, "Class 5": 11, "Class 6": 12,
               "Class 7": 13, "Class 8": 14, "Class 9": 15, "Class 10": 16}
    age = age_map.get(class_name, 10)
    days = age * 365 + random.randint(-180, 180)
    return date.today() - timedelta(days=days)


def random_address():
    return f"House {random.randint(1, 999)}, {random.choice(AREAS)}, {random.choice(CITIES)}"


def generate_student_name(gender):
    first = random.choice(MALE_FIRST if gender == "Male" else FEMALE_FIRST)
    return f"{first} {random.choice(LAST_NAMES)}"


def generate_parent_name(last_name, relation):
    first = random.choice(MALE_FIRST if relation == "Father" else FEMALE_FIRST)
    return f"{first} {last_name}"


def get_class_distribution():
    return [("KG1", 40), ("KG2", 40), ("KG3", 40),
            ("Class 1", 40), ("Class 2", 40), ("Class 3", 40),
            ("Class 4", 40), ("Class 5", 40), ("Class 6", 40),
            ("Class 7", 35), ("Class 8", 35), ("Class 9", 35), ("Class 10", 35)]


def seed_students_remaining():
    with app.app_context():
        print("\n" + "=" * 60)
        print("🎓 Seeding REMAINING Students...")
        print("=" * 60)

        campuses = Campus.query.all()
        for campus in campuses:
            existing = Student.query.filter_by(campus_id=campus.id).count()
            if existing >= 500:
                print(f"⏭️  {campus.code}: Already has {existing} students - skipping")
                continue

            print(f"\n📚 Campus: {campus.name} [{campus.code}]")
            campus_students = 0
            campus_parents = 0

            classes = Class.query.filter_by(campus_id=campus.id).all()
            if not classes:
                class_names = ["KG1", "KG2", "KG3"] + [f"Class {i}" for i in range(1, 11)]
                for name in class_names:
                    cls = Class(name=name, campus_id=campus.id)
                    db.session.add(cls)
                db.session.commit()
                classes = Class.query.filter_by(campus_id=campus.id).all()

            class_map = {c.name: c for c in classes}
            distribution = get_class_distribution()
            roll_num = existing

            for class_name, count in distribution:
                cls = class_map.get(class_name)
                if not cls:
                    continue

                for _ in range(count):
                    roll_num += 1
                    gender = random.choice(["Male", "Female"])
                    full_name = generate_student_name(gender)
                    last_name = full_name.split()[-1]
                    roll_no = f"{campus.code}-2026-{roll_num:04d}"
                    admission_no = f"ADM-{campus.code}-{roll_num:04d}"

                    relation = random.choice(["Father", "Mother"])
                    parent_name = generate_parent_name(last_name, relation)
                    parent_username = f"parent.{campus.code.lower()}{roll_num:04d}"

                    parent_user = User(
                        username=parent_username,
                        email=f"{parent_username}@mitcon.edu.pk",
                        full_name=parent_name,
                        role="parent",
                        phone=random_phone(),
                        campus_id=campus.id,
                    )
                    parent_user.set_password("parent123")
                    db.session.add(parent_user)
                    db.session.flush()

                    parent_profile = Parent(
                        user_id=parent_user.id,
                        relation=relation,
                        occupation=random.choice([
                            "Businessman", "Engineer", "Doctor", "Teacher",
                            "Government Officer", "Army Officer", "Shopkeeper",
                            "Banker", "Accountant", "Lawyer",
                        ]),
                        campus_id=campus.id,
                    )
                    db.session.add(parent_profile)
                    db.session.flush()
                    campus_parents += 1

                    student_username = f"student.{campus.code.lower()}{roll_num:04d}"
                    student_user = User(
                        username=student_username,
                        email=f"{student_username}@mitcon.edu.pk",
                        full_name=full_name,
                        role="student",
                        campus_id=campus.id,
                    )
                    student_user.set_password("student123")
                    db.session.add(student_user)
                    db.session.flush()

                    student = Student(
                        user_id=student_user.id,
                        roll_no=roll_no,
                        admission_no=admission_no,
                        class_id=cls.id,
                        section=random.choice(["A", "B", "C"]),
                        date_of_birth=random_dob_for_class(class_name),
                        gender=gender,
                        address=random_address(),
                        parent_id=parent_profile.id,
                        admission_date=date.today() - timedelta(days=random.randint(30, 365)),
                        blood_group=random.choice(BLOOD_GROUPS),
                        campus_id=campus.id,
                    )
                    db.session.add(student)
                    campus_students += 1

            db.session.commit()
            print(f"   ✅ {campus_students} students + {campus_parents} parents added")

        print("\n" + "=" * 60)
        print("📊 FINAL SUMMARY")
        print("=" * 60)
        print(f"📊 Total Students:  {Student.query.count()}")
        print(f"📊 Total Parents:   {Parent.query.count()}")
        print(f"📊 Total Teachers:  {Teacher.query.count()}")
        print("=" * 60)

        for campus in campuses:
            count = Student.query.filter_by(campus_id=campus.id).count()
            print(f"  [{campus.code:8s}] → {count} students")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_students_remaining()