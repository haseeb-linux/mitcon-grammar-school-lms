"""
Mitcon Grammar School LMS — Seed Diary (Chapter-wise)

Har class ke liye subject-wise chapters + short questions add karta hai.

KG1-KG3: ABC, Urdu Alphabets, Counting
Class 1-10: Subject-wise chapters with 10 short questions

Chalane ka tarika:
    python seed_diary.py
"""
import random
from datetime import date, timedelta

from app import app
from models import db, Diary, Class, Subject, Teacher, Campus


# ============================================================
# KG DIARY (ABC + Urdu Alphabets)
# ============================================================
KG_DIARY = {
    "English": [
        ("Chapter 1: Alphabets A-E", [
            "Write capital A", "Write small a", "Write capital B",
            "Write small b", "Write capital C", "Write small c",
            "Write capital D", "Write small d", "Write capital E",
            "Write small e"
        ]),
        ("Chapter 2: Alphabets F-J", [
            "Write capital F", "Write small f", "Write capital G",
            "Write small g", "Write capital H", "Write small h",
            "Write capital I", "Write small i", "Write capital J",
            "Write small j"
        ]),
        ("Chapter 3: Alphabets K-O", [
            "Write capital K", "Write small k", "Write capital L",
            "Write small l", "Write capital M", "Write small m",
            "Write capital N", "Write small n", "Write capital O",
            "Write small o"
        ]),
        ("Chapter 4: Alphabets P-T", [
            "Write capital P", "Write small p", "Write capital Q",
            "Write small q", "Write capital R", "Write small r",
            "Write capital S", "Write small s", "Write capital T",
            "Write small t"
        ]),
        ("Chapter 5: Alphabets U-Z", [
            "Write capital U", "Write small u", "Write capital V",
            "Write small v", "Write capital W", "Write small w",
            "Write capital X", "Write small x", "Write capital Y",
            "Write small y"
        ]),
    ],
    "Urdu": [
        ("Chapter 1: Urdu Alphabets ا-خ", [
            "لکھیں: ا", "لکھیں: ب", "لکھیں: پ", "لکھیں: ت",
            "لکھیں: ٹ", "لکھیں: ث", "لکھیں: ج", "لکھیں: چ",
            "لکھیں: ح", "لکھیں: خ"
        ]),
        ("Chapter 2: Urdu Alphabets د-ض", [
            "لکھیں: د", "لکھیں: ڈ", "لکھیں: ذ", "لکھیں: ر",
            "لکھیں: ڑ", "لکھیں: ز", "لکھیں: ژ", "لکھیں: س",
            "لکھیں: ش", "لکھیں: ص"
        ]),
        ("Chapter 3: Urdu Alphabets ض-ق", [
            "لکھیں: ض", "لکھیں: ط", "لکھیں: ظ", "لکھیں: ع",
            "لکھیں: غ", "لکھیں: ف", "لکھیں: ق"
        ]),
        ("Chapter 4: Urdu Alphabets ک-ی", [
            "لکھیں: ک", "لکھیں: گ", "لکھیں: ل", "لکھیں: م",
            "لکھیں: ن", "لکھیں: و", "لکھیں: ہ", "لکھیں: ھ",
            "لکھیں: ء", "لکھیں: ی"
        ]),
    ],
    "Math": [
        ("Chapter 1: Counting 1-10", [
            "Write numbers 1 to 10", "Count and write: 1 apple",
            "Count and write: 2 balls", "Count and write: 3 cats",
            "Count and write: 4 dogs", "Count and write: 5 stars",
            "Count and write: 6 flowers", "Count and write: 7 birds",
            "Count and write: 8 pencils", "Count and write: 9 books"
        ]),
        ("Chapter 2: Counting 11-20", [
            "Write numbers 11 to 20", "Count 11-15", "Count 16-20",
            "Write 15 in words", "Write 20 in words", "Match numbers",
            "Fill in missing: 11, _, 13", "Fill in missing: 18, _, 20",
            "Count and write: 12", "Count and write: 19"
        ]),
        ("Chapter 3: Shapes", [
            "Draw a circle", "Draw a square", "Draw a triangle",
            "Draw a rectangle", "Draw a star", "Name the shape: ⬤",
            "Name the shape: ⬛", "Name the shape: ▲",
            "Count circles in the picture", "Count squares in the picture"
        ]),
    ],
    "Islamiat": [
        ("Chapter 1: Kalima", [
            "Read Kalima Tayyaba", "Read Kalima Shahadat",
            "Meaning of Kalima Tayyaba", "Write Kalima Tayyaba",
            "Learn Kalima Tamjeed", "Meaning of Kalima Tamjeed",
            "Learn Kalima Tawheed", "Learn Kalima Radd-e-Kufr",
            "Meaning of Kalima Astaghfar", "Recite all 6 Kalimas"
        ]),
        ("Chapter 2: Namaz", [
            "Names of 5 prayers", "Time of Fajr", "Time of Zuhr",
            "Time of Asr", "Time of Maghrib", "Time of Isha",
            "How many rakats in Fajr?", "How many rakats in Zuhr?",
            "Learn Wudu steps", "Learn Azan"
        ]),
    ],
    "Drawing": [
        ("Chapter 1: Basic Drawing", [
            "Draw a house", "Draw a tree", "Draw a sun",
            "Draw a flower", "Draw a fish", "Draw a bird",
            "Draw a car", "Draw a cat", "Draw a ball",
            "Color the rainbow"
        ]),
        ("Chapter 2: Colors", [
            "Name 5 colors", "Draw red apple", "Draw yellow sun",
            "Draw green leaf", "Draw blue sky", "Draw orange fruit",
            "Draw purple flower", "Draw pink butterfly",
            "Color a rainbow", "Mix colors: red + yellow"
        ]),
    ],
}


# ============================================================
# CLASS 1-10 DIARY (Subject-wise chapters + questions)
# ============================================================
CHAPTERS_BY_SUBJECT = {
    "Math": [
        "Numbers and Place Value",
        "Addition and Subtraction",
        "Multiplication and Division",
        "Fractions",
        "Decimals",
        "Geometry - Shapes",
        "Measurement",
        "Time and Money",
        "Data Handling",
        "Algebra Basics",
    ],
    "English": [
        "Nouns and Pronouns",
        "Verbs and Tenses",
        "Adjectives and Adverbs",
        "Prepositions",
        "Sentence Structure",
        "Punctuation",
        "Reading Comprehension",
        "Creative Writing",
        "Letter Writing",
        "Essay Writing",
    ],
    "Urdu": [
        "اسم اور فعل",
        "جملہ سازی",
        "نظم و نثر",
        "املا",
        "مضمون نویسی",
        "خط نویسی",
        "محاورے",
        "ضرب المثل",
        "خلاصہ نویسی",
        "تقریر",
    ],
    "Islamiat": [
        "Quran Majeed",
        "Namaz",
        "Roza",
        "Zakat",
        "Hajj",
        "Seerat-un-Nabi ﷺ",
        "Sahaba Ikram",
        "Akhlaqiyat",
        "Duaen",
        "Islamic History",
    ],
    "Pak Studies": [
        "Pakistan Movement",
        "Quaid-e-Azam",
        "Allama Iqbal",
        "Freedom Struggle",
        "Constitution of Pakistan",
        "National Symbols",
        "Geography of Pakistan",
        "Provinces of Pakistan",
        "Culture of Pakistan",
        "Economy of Pakistan",
    ],
    "Physics": [
        "Physical Quantities",
        "Motion and Force",
        "Work and Energy",
        "Matter and Its States",
        "Heat and Temperature",
        "Light and Optics",
        "Sound and Waves",
        "Electricity",
        "Magnetism",
        "Modern Physics",
    ],
    "Chemistry": [
        "Matter and Its Composition",
        "Atomic Structure",
        "Periodic Table",
        "Chemical Bonding",
        "Chemical Reactions",
        "Acids, Bases and Salts",
        "Metals and Non-Metals",
        "Organic Chemistry",
        "Environmental Chemistry",
        "Laboratory Safety",
    ],
    "Biology": [
        "Cell Structure",
        "Tissues and Organs",
        "Nutrition",
        "Respiration",
        "Transport in Plants",
        "Transport in Animals",
        "Reproduction",
        "Genetics",
        "Ecology",
        "Human Body Systems",
    ],
    "Computer": [
        "Introduction to Computers",
        "Hardware and Software",
        "MS Word",
        "MS Excel",
        "MS PowerPoint",
        "Internet Basics",
        "Email",
        "Programming Basics",
        "Cyber Safety",
        "Digital Citizenship",
    ],
    "General Science": [
        "Living and Non-Living Things",
        "Plants Around Us",
        "Animals Around Us",
        "Our Body",
        "Food and Nutrition",
        "Water",
        "Air",
        "Weather and Seasons",
        "Light and Sound",
        "Force and Motion",
    ],
    "Social Studies": [
        "My Family",
        "My School",
        "My Community",
        "Our Country",
        "Our Flag",
        "National Heroes",
        "Maps and Globes",
        "Our Environment",
        "Good Manners",
        "Helping Others",
    ],
}


def generate_questions(subject, chapter):
    """Generate 10 short questions for a chapter."""
    questions = []
    for i in range(1, 11):
        questions.append(f"Q{i}. Short question from {chapter} ({subject})")
    return questions


def get_diary_for_class(class_name):
    """Return list of (subject_name, chapter_title, questions) tuples."""
    if class_name in ["KG1", "KG2", "KG3"]:
        # KG: Use KG_DIARY
        entries = []
        for subject, chapters in KG_DIARY.items():
            for chapter_title, questions in chapters:
                entries.append((subject, chapter_title, questions))
        return entries
    else:
        # Class 1-10: Use CHAPTERS_BY_SUBJECT
        entries = []
        # Determine subjects for this class
        if class_name in ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"]:
            subjects = ["English", "Urdu", "Math", "Islamiat", "General Science", "Social Studies"]
        else:  # Class 6-10
            subjects = ["English", "Urdu", "Math", "Islamiat", "Pak Studies",
                       "Physics", "Chemistry", "Biology", "Computer"]

        for subject in subjects:
            chapters = CHAPTERS_BY_SUBJECT.get(subject, [])
            # Take 2 chapters per subject for variety
            for chapter in chapters[:2]:
                questions = generate_questions(subject, chapter)
                entries.append((subject, chapter, questions))

        return entries


def seed_diary():
    with app.app_context():
        print("\n" + "=" * 60)
        print("📖 Seeding Diary Entries...")
        print("=" * 60)

        campuses = Campus.query.all()
        if not campuses:
            print("❌ No campuses found.")
            return

        total_added = 0
        total_skipped = 0

        for campus in campuses:
            print(f"\n📚 Campus: {campus.name} [{campus.code}]")
            campus_added = 0

            # Get all classes of this campus
            classes = Class.query.filter_by(campus_id=campus.id).all()

            for cls in classes:
                # Get subjects for this class
                subjects = Subject.query.filter_by(class_id=cls.id, campus_id=campus.id).all()
                if not subjects:
                    continue

                # Subject name to ID map
                subject_map = {s.name: s for s in subjects}

                # Get diary entries for this class
                diary_entries = get_diary_for_class(cls.name)

                for subject_name, chapter_title, questions in diary_entries:
                    subject = subject_map.get(subject_name)
                    if not subject:
                        continue

                    # Check if exists
                    existing = Diary.query.filter_by(
                        class_id=cls.id,
                        subject_id=subject.id,
                        title=chapter_title,
                        campus_id=campus.id
                    ).first()

                    if existing:
                        total_skipped += 1
                        continue

                    # Find a teacher for this subject
                    teacher = Teacher.query.filter_by(
                        campus_id=campus.id,
                        subject_specialty=subject_name
                    ).first()
                    if not teacher:
                        teacher = Teacher.query.filter_by(campus_id=campus.id).first()

                    # Content: 10 questions joined with newlines
                    content = "\n".join(questions)

                    diary = Diary(
                        class_id=cls.id,
                        subject_id=subject.id,
                        teacher_id=teacher.id if teacher else None,
                        date=date.today() - timedelta(days=random.randint(1, 7)),
                        title=chapter_title,
                        content=content,
                        campus_id=campus.id,
                    )
                    db.session.add(diary)
                    campus_added += 1
                    total_added += 1

            db.session.commit()
            print(f"   ✅ {campus_added} diary entries added")

        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Total Diary Entries Added:  {total_added}")
        print(f"⏭️  Skipped (existing):        {total_skipped}")
        print(f"📊 Total Diary in DB:          {Diary.query.count()}")
        print("=" * 60)

        # Per-campus
        print("\n📚 Per-Campus Diary Count:")
        print("-" * 60)
        for campus in campuses:
            count = Diary.query.filter_by(campus_id=campus.id).count()
            print(f"  [{campus.code:8s}] {campus.name:30s} → {count} entries")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_diary()