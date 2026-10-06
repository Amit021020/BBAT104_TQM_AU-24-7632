from app.database.db import get_connection
from datetime import datetime


def create_patient(data):
    """Create a new patient and return the generated patient ID."""

    connection = get_connection()

    try:
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
                data["patient_code"],
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group"),
                data.get("phone"),
                data.get("address"),
                data.get("emergency_contact"),
                datetime.now().isoformat(timespec="seconds")
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_all_patients():
    """Return all patients ordered by their ID."""

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


def update_patient(patient_id, data):
    """Update an existing patient and return True if successful."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE patients
            SET
                patient_code = ?,
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
                data["patient_code"],
                data["name"],
                data["age"],
                data["gender"],
                data.get("blood_group"),
                data.get("phone"),
                data.get("address"),
                data.get("emergency_contact"),
                patient_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def delete_patient(patient_id):
    """Delete a patient and return True if a record was deleted."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM patients
            WHERE id = ?
            """,
            (patient_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()