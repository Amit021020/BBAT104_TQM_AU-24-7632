
import sqlite3

from app.services.patient_service import (
    find_duplicate_patient,
    normalize_patient_name,
)


def test_patient_name_normalization():
    assert normalize_patient_name("  Rahul   Sharma ") == "rahul sharma"


def test_duplicate_patient_detection():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    connection.execute(
        """
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY,
            patient_code TEXT,
            name TEXT,
            phone TEXT
        )
        """
    )

    connection.execute(
        """
        INSERT INTO patients (id, patient_code, name, phone)
        VALUES (1, 'PAT-0001', 'Rahul Sharma', '9876543211')
        """
    )

    duplicate = find_duplicate_patient(
        connection,
        " rahul  sharma ",
        "9876543211",
    )

    assert duplicate is not None
    assert duplicate["id"] == 1

    connection.close()


def test_different_phone_is_not_duplicate():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    connection.execute(
        """
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY,
            patient_code TEXT,
            name TEXT,
            phone TEXT
        )
        """
    )

    connection.execute(
        """
        INSERT INTO patients (id, patient_code, name, phone)
        VALUES (1, 'PAT-0001', 'Rahul Sharma', '9876543211')
        """
    )

    duplicate = find_duplicate_patient(
        connection,
        "Rahul Sharma",
        "9876543212",
    )

    assert duplicate is None

    connection.close()
