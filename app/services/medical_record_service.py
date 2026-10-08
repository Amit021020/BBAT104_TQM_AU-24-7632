from app.services.reliable_operation_service import (
    execute_reliable_operation,
)
from app.database.db import get_connection


def create_medical_record(data, role="Admin", user_id=None):
    """Create a new medical record."""

    def operation(connection):
        cursor = connection.execute(
            """
            INSERT INTO medical_records (
                patient_id,
                doctor_id,
                diagnosis,
                prescription,
                notes,
                record_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["diagnosis"],
                data.get("prescription"),
                data.get("notes"),
                data["record_date"],
            ),
        )

        return cursor.lastrowid

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="create_medical_records",
        module="medical_record",
        operation_name="create",
        data=data,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def get_all_medical_records(role="Admin"):
    """Return all medical records ordered by ID."""

    if role not in ("Admin", "Doctor"):
        return {
            "success": False,
            "message": (
                "User does not have permission "
                "to view medical records."
            ),
        }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM medical_records
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_medical_record(
    record_id,
    data,
    role="Admin",
    user_id=None,
):
    """Update an existing medical record."""

    def operation(connection):
        cursor = connection.execute(
            """
            UPDATE medical_records
            SET
                patient_id = ?,
                doctor_id = ?,
                diagnosis = ?,
                prescription = ?,
                notes = ?,
                record_date = ?
            WHERE id = ?
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["diagnosis"],
                data.get("prescription"),
                data.get("notes"),
                data["record_date"],
                record_id,
            ),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="update_medical_records",
        module="medical_record",
        operation_name="update",
        data=data,
        record_id=record_id,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def delete_medical_record(
    record_id,
    role="Admin",
    user_id=None,
):
    """Delete a medical record."""

    def operation(connection):
        cursor = connection.execute(
            """
            DELETE FROM medical_records
            WHERE id = ?
            """,
            (record_id,),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="delete_medical_records",
        module="medical_record",
        operation_name="delete",
        record_id=record_id,
        user_id=user_id,
        data=None,
    )

    if not result["success"]:
        return result

    return result["result"]