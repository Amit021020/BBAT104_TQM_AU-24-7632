
from uuid import uuid4
from datetime import datetime

from app.database.db import get_connection
from app.services.reliable_operation_service import (
    execute_reliable_operation,
)


# --------------------------------------------------
# Custom Exceptions
# --------------------------------------------------

class DuplicatePatientError(Exception):
    """Raised when a possible duplicate patient exists."""
    pass


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def normalize_patient_name(name):
    """Normalize patient names for duplicate comparison."""
    return " ".join(str(name).strip().casefold().split())


def find_duplicate_patient(
    connection,
    name,
    phone,
    exclude_id=None,
):
    """
    Find a possible duplicate using normalized name
    and phone number.
    """

    if not phone or not str(phone).strip():
        return None

    normalized_name = normalize_patient_name(name)
    normalized_phone = str(phone).strip()

    rows = connection.execute(
        """
        SELECT id, patient_code, name, phone
        FROM patients
        WHERE phone = ?
        """,
        (normalized_phone,),
    ).fetchall()

    for row in rows:
        if exclude_id is not None and row["id"] == exclude_id:
            continue

        if normalize_patient_name(row["name"]) == normalized_name:
            return dict(row)

    return None


# --------------------------------------------------
# Create Patient
# --------------------------------------------------

def create_patient(data, role="Admin", user_id=None):
    """
    Create a patient with automatically generated
    database ID and patient code.
    """

    def operation(connection):

        # Acquire the SQLite write reservation before
        # checking for duplicates.
        connection.execute("BEGIN IMMEDIATE")

        duplicate = find_duplicate_patient(
            connection,
            data["name"],
            data.get("phone"),
        )

        if duplicate:
            raise DuplicatePatientError(
                f"Possible duplicate patient: "
                f"{duplicate['patient_code']} "
                f"(ID: {duplicate['id']})."
            )

        # Temporary unique code satisfies the
        # NOT NULL and UNIQUE database constraints.
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
                int(data["age"]),
                data["gender"],
                data.get("blood_group"),
                data.get("phone"),
                data.get("address"),
                data.get("emergency_contact"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        patient_id = cursor.lastrowid
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


# --------------------------------------------------
# Read Patients
# --------------------------------------------------

def get_all_patients(role="Admin"):
    """Return all patients ordered by ID."""

    if role not in ("Admin", "Doctor", "Staff"):
        return {
            "success": False,
            "message": (
                "User does not have permission "
                "to view patients."
            ),
        }

    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT *
            FROM patients
            ORDER BY id
            """
        ).fetchall()

    finally:
        connection.close()


def get_patient_by_id(patient_id, role="Admin"):
    """Return a single patient by ID."""

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
            FROM patients
            WHERE id = ?
            """,
            (patient_id,),
        ).fetchone()

    finally:
        connection.close()


# --------------------------------------------------
# Update Patient
# --------------------------------------------------

def update_patient(patient_id, data, role="Admin", user_id=None):
    """
    Update patient details while checking for
    duplicate records.
    """

    def operation(connection):

        # Serialize competing writes before the
        # duplicate check.
        connection.execute("BEGIN IMMEDIATE")

        duplicate = find_duplicate_patient(
            connection,
            data["name"],
            data.get("phone"),
            exclude_id=patient_id,
        )

        if duplicate:
            raise DuplicatePatientError(
                f"Possible duplicate patient: "
                f"{duplicate['patient_code']} "
                f"(ID: {duplicate['id']})."
            )

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
                int(data["age"]),
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


# --------------------------------------------------
# Delete Patient
# --------------------------------------------------

def delete_patient(patient_id, role="Admin", user_id=None):
    """Delete a patient if no dependent records exist."""

    def operation(connection):

        # Prevent deleting patients with related data.
        related_tables = (
            "appointments",
            "medical_records",
            "bills",
        )

        for table in related_tables:
            count = connection.execute(
                f"""
                SELECT COUNT(*)
                FROM {table}
                WHERE patient_id = ?
                """,
                (patient_id,),
            ).fetchone()[0]

            if count > 0:
                raise ValueError(
                    "Cannot delete patient because "
                    f"related records exist in {table}."
                )

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
