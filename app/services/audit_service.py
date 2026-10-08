from app.database.db import get_connection
from datetime import datetime


def create_audit_log(
    action,
    module,
    record_id=None,
    description=None,
    user_id=None,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs
        (user_id, action, module, record_id, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            action,
            module,
            record_id,
            description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    log_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return log_id


def get_all_audit_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        ORDER BY id
        """
    )

    logs = cursor.fetchall()

    conn.close()

    return logs


def get_logs_by_module(module):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        WHERE module = ?
        ORDER BY id
        """,
        (module,),
    )

    logs = cursor.fetchall()

    conn.close()

    return logs