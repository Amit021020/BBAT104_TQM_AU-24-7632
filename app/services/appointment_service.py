from datetime import datetime

from app.database.db import get_connection
from app.services.reliable_operation_service import (
    execute_reliable_operation,
)


def create_appointment(data, role="Admin", user_id=None):
    """Create a new appointment."""

    def operation(connection):
        cursor = connection.execute(
            """
            INSERT INTO appointments (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["appointment_date"],
                data["appointment_time"],
                data.get("reason"),
                data.get("status", "Scheduled"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        return cursor.lastrowid

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="create_appointments",
        module="appointment",
        operation_name="create",
        data=data,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def get_all_appointments(role="Admin"):
    """Return all appointments ordered by ID."""

    if role not in ("Admin", "Doctor", "Staff"):
        return {
            "success": False,
            "message": "User does not have permission to view appointments.",
        }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM appointments
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_appointment(
    appointment_id,
    data,
    role="Admin",
    user_id=None,
):
    """Update an existing appointment."""

    def operation(connection):
        cursor = connection.execute(
            """
            UPDATE appointments
            SET
                patient_id = ?,
                doctor_id = ?,
                appointment_date = ?,
                appointment_time = ?,
                reason = ?,
                status = ?
            WHERE id = ?
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["appointment_date"],
                data["appointment_time"],
                data.get("reason"),
                data.get("status", "Scheduled"),
                appointment_id,
            ),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="update_appointments",
        module="appointment",
        operation_name="update",
        data=data,
        record_id=appointment_id,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def delete_appointment(
    appointment_id,
    role="Admin",
    user_id=None,
):
    """Delete an appointment."""

    def operation(connection):
        cursor = connection.execute(
            """
            DELETE FROM appointments
            WHERE id = ?
            """,
            (appointment_id,),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="delete_appointments",
        module="appointment",
        operation_name="delete",
        record_id=appointment_id,
        user_id=user_id,
        data=None,
    )

    if not result["success"]:
        return result

    return result["result"]