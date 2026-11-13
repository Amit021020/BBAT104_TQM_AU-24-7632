
from uuid import uuid4
from datetime import datetime

from app.services.reliable_operation_service import execute_reliable_operation
from app.database.db import get_connection


def create_patient(data, role="Admin", user_id=None):
    """Create a patient with an automatically generated ID and code."""

    def operation(connection):
        # Temporary unique code satisfies the database UNIQUE constraint.
        temporary_code = f"TMP-{uuid4().hex}"

        cursor = connection.execute(
            """
            INSERT INTO patients (
                patient_code,
                name,
                age,
                gender,
                blood_group,
                phone,
                address,
                emergency_contact,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                temporary_code,
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group"),
                data.get("phone"),
                data.get("address"),
                data.get("emergency_contact"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        # SQLite generates the numeric patient ID.
        patient_id = cursor.lastrowid

        # Generate a readable code from the database ID.
        patient_code = f"PAT-{patient_id:04d}"

        connection.execute(
            """
            UPDATE patients
            SET patient_code = ?
            WHERE id = ?
            """,
            (patient_code, patient_id),
        )

        return patient_id

    # The reliability layer handles permissions, validation,
    # backups, audit logging and error recovery.
    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="create_patients",
        module="patient",
        operation_name="create",
        data=data,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def get_all_patients(role="Admin"):
    """Return all patients ordered by their ID."""

    if role not in ("Admin", "Doctor", "Staff"):
        return {
            "success": False,
            "message": "User does not have permission to view patients.",
        }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM patients
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_patient(patient_id, data, role="Admin", user_id=None):
    """Update an existing patient."""

   
    def operation(connection):
        cursor = connection.execute(
            """
            UPDATE patients
            SET
                name = ?,
                age = ?,
                gender = ?,
                blood_group = ?,
                phone = ?,
                address = ?,
                emergency_contact = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group"),
                data.get("phone"),
                data.get("address"),
                data.get("emergency_contact"),
                patient_id,
            ),
        )

        return cursor.rowcount > 0


    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="update_patients",
        module="patient",
        operation_name="update",
        data=data,
        record_id=patient_id,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def delete_patient(patient_id, role="Admin", user_id=None):
    """Delete a patient."""

    def operation(connection):
        cursor = connection.execute(
            """
            DELETE FROM patients
            WHERE id = ?
            """,
            (patient_id,),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="delete_patients",
        module="patient",
        operation_name="delete",
        record_id=patient_id,
        user_id=user_id,
        data=None,
    )

    if not result["success"]:
        return result

    return result["result"]