"""
Mitcon Grammar School LMS — Seed Test Data

Yeh script test ke liye sample data add karti hai:
- 1 Admin (agar nahi hai)
- 1 Teacher
- 1 Student + Parent
- 1 Announcement

Chalane ka tarika:
    python seed_test_data.py
"""
from app import app
from models import db, User, Student, Teacher, Parent, Class, Announcement


def seed_test_data():
    with app.app_context():
        print("\n" + "=" * 60)
        print("🌱 Seeding Test Data...")
        print("=" * 60)

        # ============ TEACHER ============
        if not User.query.filter_by(username='teacher1').first():
            teacher_user = User(
                username='teacher1',
                email='teacher1@mitcon.edu.pk',
                full_name='Ms. Fatima Ali',
                role='teacher',
                phone='+92 300 1234567'
            )
            teacher_user.set_password('teacher123')
            db.session.add(teacher_user)
            db.session.commit()

            teacher = Teacher(
                user_id=teacher_user.id,
                employee_id='TCH001',
                subject_specialty='Mathematics',
                qualification='M.Sc Mathematics'
            )
            db.session.add(teacher)
            db.session.commit()
            print("✅ Teacher created: teacher1 / teacher123")
        else:
            print("ℹ️  Teacher already exists")

        # ============ PARENT ============
        if not User.query.filter_by(username='parent1').first():
            parent_user = User(
                username='parent1',
                email='parent1@mitcon.edu.pk',
                full_name='Mr. Muhammad Khan',
                role='parent',
                phone='+92 321 7654321'
            )
            parent_user.set_password('parent123')
            db.session.add(parent_user)
            db.session.commit()

            parent = Parent(
                user_id=parent_user.id,
                relation='Father',
                occupation='Businessman'
            )
            db.session.add(parent)
            db.session.commit()
            print("✅ Parent created: parent1 / parent123")
        else:
            print("ℹ️  Parent already exists")

        # ============ STUDENT ============
        if not User.query.filter_by(username='student1').first():
            student_user = User(
                username='student1',
                email='student1@mitcon.edu.pk',
                full_name='Ahmed Khan',
                role='student',
                phone='+92 300 9876543'
            )
            student_user.set_password('student123')
            db.session.add(student_user)
            db.session.commit()

            # Find parent
            parent = Parent.query.first()
            # Find class
            cls = Class.query.filter_by(name='Class 5').first()

            student = Student(
                user_id=student_user.id,
                roll_no='STU001',
                admission_no='ADM2026001',
                class_id=cls.id if cls else 1,
                section='A',
                parent_id=parent.id if parent else None,
                gender='Male'
            )
            db.session.add(student)
            db.session.commit()
            print("✅ Student created: student1 / student123")
        else:
            print("ℹ️  Student already exists")

        # ============ ANNOUNCEMENT ============
        admin = User.query.filter_by(role='admin').first()
        if admin and Announcement.query.count() == 0:
            ann = Announcement(
                title='Welcome to Mitcon LMS',
                content='Assalam-o-Alaikum! Welcome to the new Mitcon Grammar School Learning Management System. Parents and students can now view diaries, results, and announcements online.',
                target='all',
                posted_by=admin.id,
                priority='high'
            )
            db.session.add(ann)
            db.session.commit()
            print("✅ Announcement created")
        else:
            print("ℹ️  Announcement already exists")

        # ============ SUMMARY ============
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        print(f"👤 Total Users:        {User.query.count()}")
        print(f"👨‍🎓 Total Students:     {Student.query.count()}")
        print(f"👨‍🏫 Total Teachers:     {Teacher.query.count()}")
        print(f"👨‍👩‍👧 Total Parents:      {Parent.query.count()}")
        print(f"📚 Total Classes:      {Class.query.count()}")
        print(f"📢 Total Announcements: {Announcement.query.count()}")
        print("=" * 60)
        print("\n🔑 LOGIN CREDENTIALS:")
        print("   Admin:   admin / admin123")
        print("   Teacher: teacher1 / teacher123")
        print("   Student: student1 / student123")
        print("   Parent:  parent1 / parent123")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_test_data()