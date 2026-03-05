import os
import platform
import sqlite3
from datetime import datetime

def get_db_path():
    app_name = "Taskemer"
    filename = "taskemer_db.db"

    if platform.system() == "Windows":
        base_dir = os.getenv("APPDATA")
    elif platform.system() == "Darwin":  # Mac
        base_dir = os.path.expanduser("~/Library/Application Support")
    else:  # Linux
        base_dir = os.path.expanduser("~/.local/share")

    data_dir = os.path.join(base_dir, app_name)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, filename)

DB_NAME = get_db_path()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (
                          id
                          INTEGER
                          PRIMARY
                          KEY
                          AUTOINCREMENT,
                          username
                          TEXT
                          UNIQUE,
                          password
                          TEXT
                      )''')

    # status: 0=Current, 1=Finished, 2=Removed
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        user_id
        INTEGER,
        name
        TEXT,
        description
        TEXT,
        priority
        INTEGER,
        status
        INTEGER
        DEFAULT
        0,
        created_at
        TEXT,
        FOREIGN
        KEY
                      (
        user_id
                      ) REFERENCES users
                      (
                          id
                      ))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS task_works
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        task_id
        INTEGER,
        work_desc
        TEXT,
        work_date
        TEXT,
        attachment
        TEXT,
        FOREIGN
        KEY
                      (
        task_id
                      ) REFERENCES tasks
                      (
                          id
                      ))''')

    conn.commit()
    conn.close()


def add_user(username, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.cursor().execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate(username, password):
    conn = sqlite3.connect(DB_NAME)
    res = conn.cursor().execute("SELECT id FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return res[0] if res else None


def add_task(user_id, name, desc, priority, initial_work=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (user_id, name, description, priority, created_at) VALUES (?, ?, ?, ?, ?)",
                   (user_id, name, desc, priority, date_now))
    task_id = cursor.lastrowid

    if initial_work:
        cursor.execute("INSERT INTO task_works (task_id, work_desc, work_date) VALUES (?, ?, ?)",
                       (task_id, initial_work, date_now))
    conn.commit()
    conn.close()


def get_current_tasks(user_id):
    conn = sqlite3.connect(DB_NAME)
    tasks = conn.cursor().execute("SELECT id, name, description, priority FROM tasks WHERE user_id=? AND status=0",
                                  (user_id,)).fetchall()
    conn.close()
    return tasks


def update_task_status(task_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()


def update_task_details(task_id, name, desc):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute("UPDATE tasks SET name=?, description=? WHERE id=?", (name, desc, task_id))
    conn.commit()
    conn.close()


def get_old_tasks(user_id):
    conn = sqlite3.connect(DB_NAME)
    tasks = conn.cursor().execute(
        "SELECT id, name, description, priority, status FROM tasks WHERE user_id=? AND status IN (1, 2)",
        (user_id,)).fetchall()
    conn.close()
    return tasks


def get_task_works(task_id):
    conn = sqlite3.connect(DB_NAME)
    # Fetch the attachment column too
    works = conn.cursor().execute(
        "SELECT id, work_desc, work_date, attachment FROM task_works WHERE task_id=? ORDER BY work_date DESC",
        (task_id,)
    ).fetchall()
    conn.close()
    return works


def add_task_work(task_id, desc, attachment=""):
    conn = sqlite3.connect(DB_NAME)
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.cursor().execute(
        "INSERT INTO task_works (task_id, work_desc, work_date, attachment) VALUES (?, ?, ?, ?)",
        (task_id, desc, date_now, attachment)
    )
    conn.commit()
    conn.close()

def delete_task_work(work_id):
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute("DELETE FROM task_works WHERE id=?", (work_id,))
    conn.commit()
    conn.close()


init_db()