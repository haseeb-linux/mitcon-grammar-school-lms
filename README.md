<div align="center">

# 🎓 Mitcon Grammar School LMS

### A Comprehensive Multi-Campus Learning Management System

*Empowering Education Through Technology*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

[Features](#-key-features) • [Tech Stack](#-tech-stack) • [Screenshots](#-screenshots) • [Setup](#-installation--setup) • [Login](#-demo-credentials) • [Architecture](#-architecture)

</div>

---

## 📖 Overview

**Mitcon Grammar School LMS** is a production-grade, multi-campus Learning Management System built to digitize the complete academic workflow of a K-10 educational institution. Designed to serve **3,500+ students**, **175+ teachers**, and **7 principals** across **7 campuses**, this platform delivers a unified yet isolated experience for every stakeholder.

> 🎯 **Mission:** To replace paper-based academic management with a modern, accessible, and secure digital ecosystem for schools.

---

## ✨ Key Features

### 👥 Five-Role Access Control System
A sophisticated role-based architecture where every user sees only what they need to see.

| Role | Access Scope | Capabilities |
|------|-------------|--------------|
| 🔴 **Super Admin** | All 7 campuses | Full system control, cross-campus analytics |
| 🟠 **Principal** | Own campus only | Manage teachers, students, and announcements |
| 🔵 **Teacher** | Assigned classes | Mark attendance, post diary, enter marks |
| 🟢 **Student** | Own data only | View diary, results, and attendance |
| 🟣 **Parent** | Child's data | Monitor progress, fees, and attendance |

### 🏫 Multi-Campus Architecture
- **7 Campuses** with completely isolated data
- Independent principals and staff per campus
- Cross-campus analytics for Super Admin
- Campus-specific branding and announcements

### 📚 Academic Management
- **13 Classes** (KG1–KG10) with section support
- **630+ Subjects** mapped to classes and teachers
- Curriculum-aligned **chapter-wise diaries**
- **Auto-generated** roll numbers and admission numbers

### 📖 Daily Diary System
- Chapter-wise notes for every subject
- **10 short questions** per chapter
- Special diary format for KG classes (ABC + Urdu Alphabets)
- Date-wise tracking for parents and students

### 📊 Test & Paper Management
- Monthly tests starting January
- Term papers starting February
- Automated grade calculation (A+ to F)
- Downloadable report cards

### ✅ Attendance Tracking
- Daily attendance marking by teachers
- Campus-wise attendance reports
- Real-time updates for parents
- **92% average** attendance visualization

### 💰 Fee Management
- Class-wise fee structure (PKR 3,000–9,000)
- Digital receipts and payment tracking
- Scholarship management
- Late fee automation

### 📢 Announcements & Communication
- Public announcement page (no login required)
- Priority-based notices (Normal, High, Urgent)
- Motivational content integration
- Campus-specific and global announcements

### 📱 Mobile-First Design
- 100% responsive across all devices
- Progressive Web App (PWA) ready
- Mobile app coming soon

---

## 🛠️ Tech Stack

<table>
<tr>
<td valign="top" width="50%">

### Backend
- **Python 3.11+** — Core language
- **Flask 3.0** — Web framework
- **Flask-Login** — Session management
- **SQLAlchemy 2.0** — ORM
- **SQLite 3** — Database
- **Werkzeug** — Security (password hashing)

</td>
<td valign="top" width="50%">

### Frontend
- **HTML5** — Structure
- **CSS3** — Styling
- **Bootstrap 5.3** — UI framework
- **JavaScript (ES6+)** — Interactivity
- **Bootstrap Icons** — Iconography
- **Google Fonts** (Poppins, Inter)

</td>
</tr>
</table>

### 🏗️ Architecture Highlights
- **Blueprints** for modular routing
- **Multi-tenancy** via `campus_id` foreign keys
- **RBAC** (Role-Based Access Control)
- **Idempotent seeders** for reproducible data
- **Static file organization** (CSS/JS separation)

---

## 📊 Project Scale

<div align="center">

| 📈 Metric | 🎯 Count | 🎨 Details |
|:---------:|:--------:|:----------|
| **Campuses** | 7 | Independent data isolation |
| **Students** | 3,500+ | ~500 per campus |
| **Teachers** | 175+ | 25 per campus |
| **Principals** | 7 | One per campus |
| **Classes** | 91 | 13 per campus |
| **Subjects** | 630+ | 90 per campus |
| **Diary Entries** | 1,600+ | Chapter-wise with questions |
| **Lines of Code** | 6,000+ | Across 49 files |

</div>

---

## 📸 Screenshots

<div align="center">




## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git
- pip

### Step 1: Clone Repository
```bash
git clone https://github.com/haseeb-linux/mitcon-grammar-school-lms.git
cd mitcon-grammar-school-lms
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
SCHOOL_NAME=Mitcon Grammar School
SCHOOL_TAGLINE=A Great Place To Learn
ACADEMIC_YEAR=2025-2026
```

### Step 5: Seed Database (Run in Order)
```bash
# Core data
python seed_campuses.py           # 7 campuses
python seed_principals.py         # 7 principals
python seed_teachers.py           # 175 teachers

# Students (may take 2-3 minutes)
python seed_students_remaining.py # 3,500 students + parents

# Academic data
python seed_subjects.py           # 630+ subjects
python seed_diary.py              # 1,600+ diary entries
python seed_superadmin.py         # Super admin account
```

### Step 6: Launch Application
```bash
python app.py
```

🌐 Open your browser: **http://localhost:5000**

---

## 🔐 Demo Credentials

<div align="center">

| Role | Username | Password | Access |
|:----:|:--------:|:--------:|:------:|
| 🔴 **Super Admin** | `superadmin` | `super123` | All 7 campuses |
| 🟠 **Principal** | `principal.main` | `principal123` | Main Campus |
| 🔵 **Teacher** | `teacher.main01` | `teacher123` | Assigned classes |
| 🟢 **Student** | `student.main0001` | `student123` | Own data |
| 🟣 **Parent** | `parent.main0001` | `parent123` | Child's data |

</div>

### 🏫 All 7 Campus Principals

| Campus | Code | Username | Password |
|--------|------|----------|----------|
| Main | MAIN | `principal.main` | `principal123` |
| City | CITY | `principal.city` | `principal123` |
| Girls | GIRLS | `principal.girls` | `principal123` |
| Boys | BOYS | `principal.boys` | `principal123` |
| Junior | JUNIOR | `principal.junior` | `principal123` |
| Model Town | MODEL | `principal.model` | `principal123` |
| Garden | GARDEN | `principal.garden` | `principal123` |

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────┐
│              CLIENT (Browser)                    │
│         HTML · CSS · Bootstrap · JS              │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────────┐
│          FLASK APPLICATION (app.py)              │
│  ┌────────────────────────────────────────────┐ │
│  │        AUTHENTICATION (auth.py)             │ │
│  │     Flask-Login · Session Management        │ │
│  └────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────┐ │
│  │           BLUEPRINTS (Routes)               │ │
│  │  ┌──────┬─────────┬─────────┬────────────┐ │ │
│  │  │Admin │Principal│ Teacher │  Student   │ │ │
│  │  └──────┴─────────┴─────────┴────────────┘ │ │
│  └────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────┐ │
│  │         MODELS (SQLAlchemy ORM)             │ │
│  │  User · Student · Teacher · Campus · Diary  │ │
│  └────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         DATABASE (SQLite - mitcon.db)            │
│    16 Tables · Multi-Campus Isolation            │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mitcon-grammar-school-lms/
├── app.py                      # Main Flask app
├── config.py                   # Configuration
├── models.py                   # Database models (16 tables)
├── auth.py                     # Authentication blueprint
│
├── admin_routes.py             # Admin routes
├── superadmin_routes.py        # Super Admin routes
├── principal_routes.py         # Principal routes
├── teacher_routes.py           # Teacher routes
│
├── seed_campuses.py            # 7 campuses
├── seed_principals.py          # 7 principals
├── seed_teachers.py            # 175 teachers
├── seed_students_remaining.py  # 3,500 students
├── seed_subjects.py            # 630 subjects
├── seed_diary.py               # 1,600 diary entries
├── seed_superadmin.py          # Super admin
│
├── templates/                  # 40+ Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── admin/
│   ├── auth/
│   ├── principal/
│   ├── superadmin/
│   └── teacher/
│
├── static/                     # Static assets
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## 🎯 Roadmap

- [x] Multi-campus architecture
- [x] 5-role RBAC system
- [x] Diary management
- [x] Attendance tracking
- [x] Fee management
- [x] Public announcements
- [ ] Mobile app (React Native)
- [ ] SMS notifications
- [ ] Online fee payment gateway
- [ ] Live video classes
- [ ] AI-powered performance prediction
- [ ] Multi-language support (Urdu/English)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👨‍💻 Developer

<div align="center">

**Muhammad Haseeb**

[![GitHub](https://img.shields.io/badge/GitHub-haseeb--linux-181717?style=for-the-badge&logo=github)](https://github.com/haseeb-linux)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad_Haseeb-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/muhammad-haseeb-451264432)
[![Email](https://img.shields.io/badge/Email-bc250401284mha@vu.edu.pk-EA4335?style=for-the-badge&logo=gmail)](mailto:haseebarif112234@gmail.com)

*Computer Science Student · Virtual University of Pakistan*

</div>

---

<div align="center">

### ⭐ If you found this project helpful, please give it a star!

**Made with ❤️ by Muhammad Haseeb**

*Powered by @Haseeb.edu*

</div>
