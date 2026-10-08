from datetime import datetime

from app.services.reliable_operation_service import (
    execute_reliable_operation,
)
from app.database.db import get_connection


def create_doctor(data, role="Admin", user_id=None):
    """Create a new doctor."""

    def operation(connection):
        cursor = connection.execute(
            """
            INSERT INTO doctors (
                doctor_code,
                name,
                specialization,
                department,
                phone,
                email,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["doctor_code"],
                data["name"],
                data["specialization"],
                data["department"],
                data.get("phone"),
                data.get("email"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        return cursor.lastrowid

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="create_doctors",
        module="doctor",
        operation_name="create",
        data=data,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def get_all_doctors(role="Admin"):
    """Return all doctors ordered by ID."""

    if role not in ("Admin", "Doctor", "Staff"):
        return {
            "success": False,
            "message": "User does not have permission to view doctors.",
        }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM doctors
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_doctor(doctor_id, data, role="Admin", user_id=None):
    """Update an existing doctor."""

    def operation(connection):
        cursor = connection.execute(
            """
            UPDATE doctors
            SET
                doctor_code = ?,
                name = ?,
                specialization = ?,
                department = ?,
                phone = ?,
                email = ?
            WHERE id = ?
            """,
            (
                data["doctor_code"],
                data["name"],
                data["specialization"],
                data["department"],
                data.get("phone"),
                data.get("email"),
                doctor_id,
            ),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="update_doctors",
        module="doctor",
        operation_name="update",
        data=data,
        record_id=doctor_id,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def delete_doctor(doctor_id, role="Admin", user_id=None):
    """Delete a doctor."""

    def operation(connection):
        cursor = connection.execute(
            """
            DELETE FROM doctors
            WHERE id = ?
            """,
            (doctor_id,),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="delete_doctors",
        module="doctor",
        operation_name="delete",
        record_id=doctor_id,
        user_id=user_id,
        data=None,
    )

    if not result["success"]:
        return result

    return result["result"]