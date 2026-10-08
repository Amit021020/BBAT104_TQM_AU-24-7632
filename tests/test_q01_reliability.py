from pathlib import Path

from app.database.db import get_connection
from app.services.patient_service import create_patient
from app.services.doctor_service import create_doctor
from app.services.appointment_service import create_appointment
from app.services.medical_record_service import create_medical_record
from app.services.bill_service import create_bill
from app.services.user_service import create_user

from app.services.validation_service import validate_patient, validate_bill
from app.services.role_service import has_permission
from app.services.backup_service import get_backups
from app.services.audit_service import get_all_audit_logs
from app.services.error_recovery_service import run_database_operation


def get_first_patient_id():
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT id FROM patients ORDER BY id LIMIT 1"
        ).fetchone()
        return row["id"] if row else None
    finally:
        connection.close()


def get_first_doctor_id():
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT id FROM doctors ORDER BY id LIMIT 1"
        ).fetchone()
        return row["id"] if row else None
    finally:
        connection.close()


def test_q01_input_validation():
    invalid_patient = {
        "patient_code": "TEST-Q01",
        "name": "",
        "age": 150,
        "gender": "Male",
        "blood_group": "O+",
        "phone": "123",
        "address": "Test Address",
        "emergency_contact": "123",
    }

    errors = validate_patient(invalid_patient)

    assert len(errors) > 0
    assert any("name" in error for error in errors)
    assert any("Age" in error for error in errors)


def test_q01_bill_validation():
    invalid_bill = {
        "patient_id": 1,
        "amount": -500,
        "payment_status": "Pending",
        "bill_date": "2026-10-08",
    }

    errors = validate_bill(invalid_bill)

    assert "Bill amount cannot be negative." in errors


def test_q01_role_permissions():
    assert has_permission("Admin", "create_patients")
    assert has_permission("Admin", "delete_patients")

    assert has_permission("Doctor", "view_patients")

    assert has_permission("Staff", "view_patients")

    assert not has_permission("Doctor", "delete_patients")


def test_q01_backup_exists():
    backups = get_backups()

    assert len(backups) > 0

    for backup in backups:
        assert Path(backup).exists()


def test_q01_audit_logs_exist():
    logs = get_all_audit_logs()

    assert len(logs) > 0

    actions = {log["action"] for log in logs}

    assert "CREATE" in actions


def test_q01_error_recovery_rollback():
    def failing_operation(connection):
        connection.execute(
            """
            INSERT INTO patients
            (patient_code, name, age, gender, blood_group,
             phone, address, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ROLLBACK-TEST",
                "Rollback Test",
                30,
                "Male",
                "O+",
                "9999999999",
                "Test Address",
                "8888888888",
            ),
        )

        # Force the transaction to fail
        connection.execute(
            "INSERT INTO patients (invalid_column) VALUES (?)",
            ("FAIL",),
        )

    result = run_database_operation(failing_operation)

    assert result["success"] is False

    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM patients WHERE patient_code = ?",
            ("ROLLBACK-TEST",),
        ).fetchone()

        assert row is None
    finally:
        connection.close()