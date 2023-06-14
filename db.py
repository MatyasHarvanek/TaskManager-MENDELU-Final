import sqlite3
from datetime import datetime


def get_db_connection():
    conn = sqlite3.connect('udelej_to.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_task(name, description, user_id=None):
    created_at = datetime.now()

    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        INSERT INTO task (name, description, is_done, created_at, user_id) 
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, False, created_at, user_id))

    conn.commit()
    conn.close()


def create_user(name, password):

    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        INSERT INTO user (id, name, password) VALUES (?,?,?)
    ''', (None, name, password))

    conn.commit()
    conn.close()


def get_tasks_without_user():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        SELECT * FROM task
        WHERE user_id IS NULL
        ORDER BY is_done ASC, id DESC
    ''')

    tasks = c.fetchall()
    conn.close()

    return tasks


def mark_task_as_done(task_id, user_id=None):
    conn = get_db_connection()
    c = conn.cursor()

    if user_id:
        c.execute('''
            UPDATE task 
            SET is_done = True
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
    else:
        c.execute('''
            UPDATE task 
            SET is_done = True
            WHERE id = ? AND user_id IS NULL
                ''', (task_id,))

    conn.commit()
    conn.close()


def get_history(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        SELECT * FROM task
        WHERE user_id IS NULL OR user_id = ?
        ORDER BY is_done ASC, id DESC
    ''', (user_id,))

    tasks = c.fetchall()
    conn.close()

    return tasks


def mark_task_as_undone(task_id, user_id=None):
    conn = get_db_connection()
    c = conn.cursor()

    if user_id:
        c.execute('''
            UPDATE task 
            SET is_done = False
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))
    else:
        c.execute('''
            UPDATE task 
            SET is_done = False
            WHERE id = ? AND user_id IS NULL
                ''', (task_id,))

    conn.commit()
    conn.close()


def get_user(name):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM user WHERE name = ?', (name,))

    user = c.fetchone()
    user = user if user else None

    conn.close()

    return user


def get_user_tasks(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        SELECT * FROM task
        WHERE user_id = ?
        ORDER BY is_done ASC, id DESC
    ''', (user_id,))

    tasks = c.fetchall()

    conn.close()

    return tasks


def checkIfUserExists(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT name FROM user
        WHERE name = ?
    ''', [username])

    user = c.fetchone()
    return user is not None
