# Exam Result Management System

A modern Django-based Exam Result Management System designed to simplify the management of student academic records for administrators, teachers, and students. The system provides student registration, subject management, mark entry, result generation, grade calculation, and report card management in an efficient and user-friendly manner.

### Login Page
> Dual-role login with Admin and Student toggle

### Admin Dashboard
> Overview of students, subjects, and results

### Student Result Dashboard
> Personalized result view with GPA and grade summary

---

## ✨ Features

### 👨‍💼 Admin Role
- Secure admin login
- Add, edit, and manage student profiles
- Enter and update marks for multiple subjects
- Auto grade calculation (O, A+, A, B+, B, C, U)
- View all results filtered by student
- Department and subject management

### 🎓 Student Role
- Login using Register Number + Password
- View personalized result dashboard
- See marks, grades, credits per subject
- GPA calculation displayed prominently
- Pass/Fail status for each subject
- Semester-wise result filtering

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.14, Django 6.0 |
| Database | SQLite3 |
| Frontend | HTML5, CSS3 (Custom) |
| Auth | Django Custom User Model |
| Version Control | Git & GitHub



---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/college-result-system.git
cd college-result-system
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install django pillow
```

### 4. Run migrations
```bash
cd result_portal
python manage.py makemigrations results
python manage.py migrate
```

### 5. Create admin user
```bash
python manage.py createsuperuser
```

### 6. Set admin role
```bash
python manage.py shell -c "
from results.models import CustomUser
u = CustomUser.objects.get(username='admin')
u.role = 'admin'
u.save()
print('Admin role set!')
"
```

### 7. Add sample data
```bash
python manage.py shell -c "
from results.models import Department, Subject
d = Department.objects.create(name='Computer Science Engineering', code='CSE')
Subject.objects.create(name='Mathematics', code='MA101', department=d, credits=4, semester=1)
Subject.objects.create(name='Programming in C', code='CS101', department=d, credits=4, semester=1)
Subject.objects.create(name='Physics', code='PH101', department=d, credits=3, semester=1)
print('Sample data created!')
"
```

### 8. Run the server
```bash
python manage.py runserver
```

### 9. Open browser
```bash
http://127.0.0.1:8000/login/
```

## 📁 Project Structure

```bash
college_result_system/
│
├── manage.py
├── db.sqlite3
├── static/
├── media/
│
├── result_portal/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── results/
│   ├── __init__.py
│   ├── models.py          # CustomUser, Student, Subject, Result
│   ├── views.py           # All view logic
│   ├── forms.py           # Student and Result forms
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Django admin setup
│   ├── apps.py
│   ├── migrations/
│   │
│   └── templates/
│       └── results/
│           ├── login.html
│           ├── admin_dashboard.html
│           ├── student_dashboard.html
│           ├── student_list.html
│           ├── add_student.html
│           ├── add_result.html
│           ├── manage_results.html
│           └── edit_student.html
│
└── README.md



