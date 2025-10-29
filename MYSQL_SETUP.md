# MySQL Setup Guide for SavvyIndians LMS

## 📦 Prerequisites

### 1. Install MySQL Server

**Windows:**
- Download MySQL Installer: https://dev.mysql.com/downloads/installer/
- Install MySQL Server 8.0 or higher
- Set root password during installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### 2. Install Python MySQL Client

```bash
pip install mysqlclient
```

**If installation fails on Windows:**
1. Download wheel file: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
2. Install: `pip install mysqlclient-xxx.whl`

---

## 🗄️ Local Database Setup

### Step 1: Create Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE savvyindians_lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user (optional, can use root)
CREATE USER 'savvyindians'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON savvyindians_lms.* TO 'savvyindians'@'localhost';
FLUSH PRIVILEGES;

# Exit MySQL
EXIT;
```

### Step 2: Configure Environment Variables

Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# MySQL Database Configuration
DB_NAME=savvyindians_lms
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### Step 3: Run Migrations

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (if any)
python manage.py loaddata programs_fixture.json
```

### Step 4: Test Connection

```bash
python manage.py dbshell
```

---

## 🚀 Production Database Setup (Render.com)

### Option 1: Render MySQL (Recommended)

1. **Create MySQL Database on Render:**
   - Go to: https://dashboard.render.com/
   - Click "New" → "MySQL"
   - Database Name: `savvyindians_lms`
   - Region: Choose closest to your web service
   - Plan: Free tier (limited) or Paid

2. **Get Connection URL:**
   - After creation, copy the "External Database URL"
   - Format: `mysql://user:password@host:port/dbname`

3. **Add Environment Variable on Render:**
   - Go to your web service settings
   - Environment → Add Variable
   - Key: `DATABASE_URL`
   - Value: Paste the MySQL URL
   - Save changes

### Option 2: External MySQL (PlanetScale, AWS RDS, etc.)

**PlanetScale (Free tier available):**
```bash
# 1. Create account: https://planetscale.com/
# 2. Create database: savvyindians-lms
# 3. Get connection string
# 4. Add to Render as DATABASE_URL
```

**Format:**
```
mysql://username:password@host.connect.psdb.cloud/database?ssl={"rejectUnauthorized":true}
```

---

## 🔧 Troubleshooting

### Error: "mysqlclient not installed"

**Solution:**
```bash
pip install mysqlclient==2.2.4
```

### Error: "Access denied for user"

**Solution:**
```bash
# Reset MySQL root password
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Error: "Can't connect to MySQL server"

**Solution:**
```bash
# Check MySQL service is running
# Windows:
net start MySQL80

# Linux:
sudo systemctl start mysql
sudo systemctl status mysql

# macOS:
brew services start mysql
```

### Error: "Database doesn't exist"

**Solution:**
```bash
mysql -u root -p -e "CREATE DATABASE savvyindians_lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

---

## 📊 Verify Setup

### 1. Check Database Connection

```bash
python manage.py check --database default
```

### 2. List Tables

```bash
python manage.py dbshell
SHOW TABLES;
EXIT;
```

### 3. Check Data

```bash
python check_db.py
```

---

## 🔄 Migration from SQLite to MySQL

### Export Data from SQLite

```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

### Import to MySQL

```bash
# 1. Switch to MySQL in .env
# 2. Run migrations
python manage.py migrate

# 3. Load data
python manage.py loaddata data_backup.json

# 4. Create superuser (if needed)
python manage.py ensure_superuser
```

---

## ✅ Expected Configuration

**requirements.txt:**
```
mysqlclient==2.2.4
```

**settings.py:**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME", default="savvyindians_lms"),
        "USER": config("DB_USER", default="root"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**Production (settings_minimal.py):**
```python
# Uses DATABASE_URL from Render
# Format: mysql://user:password@host:port/dbname
```

---

## 🎯 Next Steps

1. ✅ Install MySQL Server locally
2. ✅ Create database: `savvyindians_lms`
3. ✅ Configure `.env` file
4. ✅ Install `mysqlclient` package
5. ✅ Run migrations: `python manage.py migrate`
6. ✅ Create superuser
7. ✅ Test locally: `python manage.py runserver`
8. ✅ Set up production MySQL on Render
9. ✅ Add `DATABASE_URL` to Render environment
10. ✅ Deploy and test production

---

## 📞 Support

If you encounter any issues:
1. Check MySQL service is running
2. Verify `.env` file has correct credentials
3. Test connection: `python manage.py dbshell`
4. Check logs: `python manage.py runserver` output
