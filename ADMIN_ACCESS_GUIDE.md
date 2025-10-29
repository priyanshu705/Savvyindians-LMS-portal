# 🔐 ADMIN/SUPERUSER ACCESS GUIDE
**Django LMS - SavvyIndians Platform**

---

## ✅ SUPERUSER CREATED SUCCESSFULLY!

**Username**: `admin`  
**Email**: `admin@savvyindians.com`  
**Password**: [You just set this]

---

## 🌐 HOW TO ACCESS AS ADMIN

### **1. Django Admin Panel** (Full Database Access)

#### **On Localhost** (Development):
1. Make sure server is running:
   ```bash
   python manage.py runserver
   ```

2. Open browser and go to:
   ```
   http://127.0.0.1:8000/admin/
   ```

3. Login with:
   - **Username**: `admin`
   - **Password**: [your password]

#### **On Render** (Production):
1. Go to:
   ```
   https://savvyindians-lms-portal-2.onrender.com/admin/
   ```

2. Create superuser in Render Shell first:
   ```bash
   python manage.py createsuperuser
   ```

3. Login with your credentials

---

## 📊 WHAT YOU CAN DO IN ADMIN PANEL

### **Users Management**
- ✅ View all registered users
- ✅ Add/edit/delete users
- ✅ Change user permissions
- ✅ Make users staff/superuser
- ✅ View user profiles and details

### **Course Management**
- ✅ Create/edit/delete courses
- ✅ Manage course content
- ✅ Upload course materials
- ✅ Assign courses to students
- ✅ Set course schedules

### **Quiz/Assessment Management**
- ✅ Create quizzes and exams
- ✅ Add questions
- ✅ Set grading criteria
- ✅ View student results

### **Content Management**
- ✅ Manage news and events
- ✅ Upload videos and files
- ✅ Control notifications
- ✅ Manage programs

### **Database Operations**
- ✅ View all database tables
- ✅ Add/edit/delete records
- ✅ Run database queries
- ✅ Export data

---

## 🗄️ DIRECT DATABASE ACCESS

### **Option 1: pgAdmin** (GUI Tool)

1. **Download pgAdmin**: https://www.pgadmin.org/download/

2. **Connect to PostgreSQL**:
   - **Host**: `dpg-d40qm7ili9vc73bshqig-a.oregon-postgres.render.com`
   - **Port**: `5432`
   - **Database**: `lmsdb_28b7`
   - **Username**: `lmsdb_28b7_user`
   - **Password**: `WCL8o8WhiO3RaaNjWBvZv85GwbdQ2zg5`

3. **Browse tables**:
   - `accounts_user` - All users
   - `accounts_student` - Student profiles
   - `course_course` - Courses
   - `quiz_quiz` - Quizzes
   - `result_takenCourse` - Student enrollments

### **Option 2: DBeaver** (Free GUI)

1. **Download DBeaver**: https://dbeaver.io/download/

2. **Create New Connection**:
   - Database: PostgreSQL
   - Use same credentials as above

### **Option 3: Command Line (psql)**

```bash
psql postgresql://lmsdb_28b7_user:WCL8o8WhiO3RaaNjWBvZv85GwbdQ2zg5@dpg-d40qm7ili9vc73bshqig-a.oregon-postgres.render.com/lmsdb_28b7
```

---

## 🔍 USEFUL ADMIN COMMANDS

### **View All Users**
```bash
python manage.py shell
```
```python
from accounts.models import User
users = User.objects.all()
for user in users:
    print(f"{user.username} - {user.email} - {'Admin' if user.is_superuser else 'User'}")
```

### **Make User Admin**
```bash
python manage.py shell
```
```python
from accounts.models import User
user = User.objects.get(username='someuser')
user.is_staff = True
user.is_superuser = True
user.save()
print(f"{user.username} is now an admin!")
```

### **View All Courses**
```bash
python manage.py shell
```
```python
from course.models import Course
courses = Course.objects.all()
for course in courses:
    print(f"{course.title} - {course.code}")
```

### **View Database Statistics**
```bash
python manage.py shell
```
```python
from accounts.models import User, Student
from course.models import Course
from quiz.models import Quiz

print(f"Total Users: {User.objects.count()}")
print(f"Total Students: {Student.objects.count()}")
print(f"Total Courses: {Course.objects.count()}")
print(f"Total Quizzes: {Quiz.objects.count()}")
```

---

## 📱 MOBILE ACCESS

You can also access the admin panel from mobile:
```
https://savvyindians-lms-portal-2.onrender.com/admin/
```

The admin panel is responsive and works on tablets/phones!

---

## 🔐 SECURITY TIPS

### **DO**:
✅ Use strong passwords for superuser accounts  
✅ Create separate admin accounts for different people  
✅ Use 2FA if available  
✅ Regularly backup database  
✅ Limit superuser access to trusted people  

### **DON'T**:
❌ Share superuser credentials  
❌ Use simple passwords  
❌ Give admin access to students  
❌ Leave admin panel open on public computers  
❌ Expose database credentials publicly  

---

## 🚀 QUICK START GUIDE

### **Localhost (Right Now)**:

1. **Server is already running** ✅
2. **Superuser created**: `admin` ✅
3. **Open**: http://127.0.0.1:8000/admin/
4. **Login** with your credentials
5. **Start managing** users, courses, content!

### **Production (Render)**:

1. Go to Render Dashboard → Shell
2. Run: `python manage.py createsuperuser`
3. Create admin credentials
4. Visit: https://savvyindians-lms-portal-2.onrender.com/admin/
5. Login and manage!

---

## 📊 ADMIN PANEL FEATURES

### **Dashboard**
- Overview of all data
- Quick actions
- Recent activity

### **Users Section**
- Users table (all registered users)
- Groups (for permissions)
- Student profiles
- Staff members

### **Courses Section**
- Courses list
- Programs
- Course allocations
- Uploads (videos, files)

### **Assessments**
- Quizzes
- Questions
- Results
- Progress tracking

### **Content**
- News & Events
- Sessions/Semesters
- Notifications

---

## 🛠️ ADVANCED DATABASE OPERATIONS

### **Export Data to CSV**
```bash
python manage.py shell
```
```python
import csv
from accounts.models import User

with open('users_export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Is Active'])
    
    for user in User.objects.all():
        writer.writerow([user.username, user.email, user.first_name, 
                        user.last_name, user.is_active])

print("Users exported to users_export.csv")
```

### **Bulk Create Users**
```python
from accounts.models import User

users_data = [
    {'username': 'student1', 'email': 'student1@test.com', 'password': 'pass123'},
    {'username': 'student2', 'email': 'student2@test.com', 'password': 'pass123'},
]

for data in users_data:
    user = User.objects.create_user(**data)
    print(f"Created: {user.username}")
```

---

## 📞 NEED HELP?

### **Common Issues**:

**Q: Can't login to admin panel**  
A: Make sure you created a superuser with `createsuperuser` command

**Q: Getting "Page not found"**  
A: Admin URL is `/admin/` not `/admin`

**Q: Forgot admin password**  
A: Run `python manage.py changepassword admin`

**Q: Want to see database in Excel**  
A: Use pgAdmin or DBeaver to export tables to CSV

---

## ✅ SUMMARY

**Admin Panel URL (Localhost)**:
```
http://127.0.0.1:8000/admin/
```

**Admin Panel URL (Production)**:
```
https://savvyindians-lms-portal-2.onrender.com/admin/
```

**Credentials**:
- Username: `admin`
- Email: `admin@savvyindians.com`
- Password: [You set this]

**You now have full control over**:
- Users & Permissions
- Courses & Content
- Quizzes & Assessments
- Database Records
- Site Configuration

---

**🎉 You're all set to manage your LMS platform!**
