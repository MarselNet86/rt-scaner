import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()


async def db_start():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INT PRIMARY KEY,
      user_id BIGINT,
      notification BOOLEAN DEFAULT 1
    );
    """)

    db.commit()


async def user_exists(user_id):
    """Проверка на существование пользователя"""
    user = cur.execute("SELECT * FROM users WHERE user_id == (?)", [user_id]).fetchone()
    if not user:
        cur.execute("INSERT INTO users(user_id) VALUES (?)", [user_id])

    db.commit()


async def mailing():
    """Получить user_ids, где notification включены"""
    users = cur.execute("SELECT user_id FROM users WHERE notification == 1").fetchall()
    return users


async def check_notice(user_id):
    """Получить значение notification"""
    notification = cur.execute("SELECT notification FROM users WHERE user_id == (?)", [user_id]).fetchone()[0]
    return notification


async def switch_notice(user_id, toggle):
    if toggle == 'on':
        cur.execute("UPDATE users SET notification = 1 WHERE user_id == (?)", [user_id])

    elif toggle == 'off':
        cur.execute("UPDATE users SET notification = 0 WHERE user_id == (?)", [user_id])

    db.commit()
