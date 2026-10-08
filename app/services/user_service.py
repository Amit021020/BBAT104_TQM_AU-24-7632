import hashlib
from datetime import datetime

from app.database.db import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(data["password"])

    cursor.execute(
        """
        INSERT INTO users
        (username, password_hash, role, created_at, is_active)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["username"],
            password_hash,
            data["role"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("is_active", 1),
        ),
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        ORDER BY id
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


def update_user(user_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(data["password"])

    cursor.execute(
        """
        UPDATE users
        SET username = ?,
            password_hash = ?,
            role = ?,
            is_active = ?
        WHERE id = ?
        """,
        (
            data["username"],
            password_hash,
            data["role"],
            data.get("is_active", 1),
            user_id,
        ),
    )

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted