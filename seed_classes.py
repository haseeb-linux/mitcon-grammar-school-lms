"""
Mitcon Grammar School LMS — Seed Classes Script

Yeh script database mein KG1 se Class 10 tak saari classes add karti hai.
Ek baar chalane se 13 classes ban jayengi.

Chalane ka tarika:
    python seed_classes.py
"""
from app import app
from models import db, Class


def seed_classes():
    """Saari classes (KG1 to Class 10) database mein add karo."""
    with app.app_context():
        class_names = ["KG1", "KG2", "KG3"] + [f"Class {i}" for i in range(1, 11)]
        
        added = 0
        for name in class_names:
            if not Class.query.filter_by(name=name).first():
                db.session.add(Class(name=name))
                added += 1
        
        db.session.commit()
        
        total = Class.query.count()
        print("\n" + "=" * 60)
        print(f"✅ {added} new classes added!")
        print(f"📊 Total Classes in Database: {total}")
        print("=" * 60)
        print("\nAll Classes:")
        for c in Class.query.order_by(Class.id).all():
            print(f"  → {c.name}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_classes()