# วิธีติดตั้ง MySQL สำหรับเชื่อมต่อกับ Django และ n8n

## ขั้นตอนที่ 1: ติดตั้ง MySQL Server

1. ดาวน์โหลด MySQL Installer จาก: https://dev.mysql.com/downloads/installer/
2. เลือก "MySQL Installer for Windows"
3. รันไฟล์ติดตั้ง และเลือก "Custom" หรือ "Server only"
4. ติดตั้ง MySQL Server 8.0 หรือสูงกว่า

## ขั้นตอนที่ 2: ตั้งค่า MySQL

ระหว่างติดตั้ง:
- เลือก "Development Computer" สำหรับ Config Type
- ตั้ง Root Password: `Chin7751499` (หรือ password ที่ต้องการ)
- สร้าง MySQL User (ถ้าต้องการ)
- เปิด port 3306

## ขั้นตอนที่ 3: สร้าง Database

เปิด MySQL Command Line Client หรือใช้ MySQL Workbench:

```sql
CREATE DATABASE carqueue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## ขั้นตอนที่ 4: แก้ไข Django settings.py

ไฟล์ `carqueue/settings.py` ควรมี:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carqueue_db',
        'USER': 'root',
        'PASSWORD': 'Chin7751499',  # ใส่ password ที่ตั้งไว้
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

## ขั้นตอนที่ 5: ติดตั้ง MySQL Client สำหรับ Python

```powershell
pip install mysqlclient
# หรือ
pip install pymysql
```

ถ้าใช้ pymysql ให้เพิ่มใน `mysite/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## ขั้นตอนที่ 6: Run Migration

```powershell
cd D:\Velvet\Virtual studio code\test\mysite
python manage.py migrate
```

## สำหรับ n8n

เมื่อ MySQL พร้อมแล้ว สามารถเชื่อมต่อจาก n8n ด้วยข้อมูล:
- Host: `127.0.0.1` (หรือ `localhost`)
- Port: `3306`
- Database: `carqueue_db`
- User: `root`
- Password: `Chin7751499`

## ทางเลือก: ใช้ SQLite ชั่วคราว

ถ้ายังไม่พร้อมติดตั้ง MySQL สามารถใช้ SQLite ก่อนได้:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

แล้วค่อย migrate ไป MySQL ทีหลัง
