from datetime import datetime

from app.services.reliable_operation_service import (
    execute_reliable_operation,
)
from app.database.db import get_connection


def create_doctor(data, role="Admin", user_id=None):
    """Create a new doctor."""

    
    def operation(connection):
        connection.execute("BEGIN IMMEDIATE")

        # Generate a temporary unique code.
        from uuid import uuid4
        temporary_code = f"TMP-{uuid4().hex}"

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
                temporary_code,
                data["name"],
                data["specialization"],
                data["department"],
                data.get("phone"),
                data.get("email"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        doctor_id = cursor.lastrowid
        doctor_code = f"DOC-{doctor_id:04d}"

        connection.execute(
            """
            UPDATE doctors
            SET doctor_code = ?
            WHERE id = ?
            """,
            (doctor_code, doctor_id),
        )

        return doctor_id

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


def get_doctor_by_id(doctor_id, role="Admin"):
    """Retrieve a single doctor by ID."""

    if role not in ("Admin", "Doctor", "Staff"):
        return {
            "success": False,
            "message": "Permission denied.",
        }

    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT *
            FROM doctors
            WHERE id = ?
            """,
            (doctor_id,),
        ).fetchone()

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
    """Delete a doctor only when no appointments reference them."""

    def operation(connection):
        connection.execute("BEGIN IMMEDIATE")

        appointment_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            WHERE doctor_id = ?
            """,
            (doctor_id,),
        ).fetchone()[0]

        if appointment_count > 0:
            raise ValueError(
                "Cannot delete doctor: existing appointments "
                "are linked to this doctor."
            )

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