import pyodbc
import bcrypt
from datetime import datetime, date

# 🔧 Підключення до бази
conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=HabitMaster;Trusted_Connection=yes;'
)
cursor = conn.cursor()

def register_user(username, password):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("INSERT INTO Users (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return "OK"
    except:
        return "FAIL"

def login_user(username, password):
    cursor.execute("SELECT id, password_hash FROM Users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        user_id, hashed = row
        if bcrypt.checkpw(password.encode(), hashed.encode()):
            return str(user_id)
    return "FAIL"

def add_habit(user_id, name):
    try:
        cursor.execute("INSERT INTO Habits (user_id, name) VALUES (?, ?)", (user_id, name))
        conn.commit()
        return "OK"
    except:
        return "FAIL"

def get_habits(user_id):
    cursor.execute("SELECT id, name FROM Habits WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def mark_habit_done(habit_id):
    try:
        today = date.today().strftime('%Y-%m-%d')  # ← ключова зміна!
        cursor.execute(
            "INSERT INTO HabitLogs (habit_id, log_date, done) VALUES (?, ?, ?)",
            (habit_id, today, 1)
        )
        conn.commit()
        return "OK"
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return "FAIL"

def change_habit(habit_id, new_name):
    try:
        cursor.execute("UPDATE Habits SET name = ? WHERE id = ?", (new_name, habit_id))
        conn.commit()
        return "OK"
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return "FAIL"

def delete_habit(habit_id):
    try:
        # Видаляємо також логи, щоб уникнути помилок зв'язку
        cursor.execute("DELETE FROM HabitLogs WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM Habits WHERE id = ?", (habit_id,))
        conn.commit()
        return "OK"
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return "FAIL"


def get_habit_stats(habit_id):
    cursor.execute("SELECT COUNT(*) FROM HabitLogs WHERE habit_id = ? AND done = 1", (habit_id,))
    count = cursor.fetchone()[0]
    return f"Completed {count} times"
