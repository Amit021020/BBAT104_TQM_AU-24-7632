
from datetime import timedelta

from app.services.appointment_service import (
    validate_appointment_slot,
    find_appointment_conflict,
)


def test_thirty_minute_duration():
    start, end = validate_appointment_slot(
        "2026-11-14", "09:00", 30
    )

    assert end - start == timedelta(minutes=30)


def test_sixty_minute_duration():
    start, end = validate_appointment_slot(
        "2026-11-14", "09:00", 60
    )

    assert end - start == timedelta(minutes=60)


def test_invalid_duration():
    try:
        validate_appointment_slot(
            "2026-11-14", "09:00", 45
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid duration was accepted")

import sqlite3

from app.services.appointment_service import (
    find_appointment_conflict,
)


def create_test_database():
    """Create an isolated in-memory appointment database."""

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.execute(
        """
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    conn.execute(
        """
        INSERT INTO appointments (
            doctor_id,
            appointment_date,
            appointment_time,
            duration_minutes,
            status
        )
        VALUES (1, '2026-11-14', '09:00', 30, 'Scheduled')
        """
    )

    conn.commit()
    return conn


def test_overlapping_appointment():
    conn = create_test_database()

    try:
        conflict = find_appointment_conflict(
            connection=conn,
            doctor_id=1,
            appointment_date="2026-11-14",
            appointment_time="09:15",
            duration_minutes=30,
        )

        assert conflict is not None
    finally:
        conn.close()


def test_adjacent_appointment_allowed():
    conn = create_test_database()

    try:
        conflict = find_appointment_conflict(
            connection=conn,
            doctor_id=1,
            appointment_date="2026-11-14",
            appointment_time="09:30",
            duration_minutes=30,
        )

        assert conflict is None
    finally:
        conn.close()


def test_different_doctor_allowed():
    conn = create_test_database()

    try:
        conflict = find_appointment_conflict(
            connection=conn,
            doctor_id=2,
            appointment_date="2026-11-14",
            appointment_time="09:00",
            duration_minutes=30,
        )

        assert conflict is None
    finally:
        conn.close()


def test_completed_slot_remains_reserved():
    conn = create_test_database()

    try:
        conn.execute(
            "UPDATE appointments SET status = 'Completed'"
        )
        conn.commit()

        conflict = find_appointment_conflict(
            connection=conn,
            doctor_id=1,
            appointment_date="2026-11-14",
            appointment_time="09:00",
            duration_minutes=30,
        )

        assert conflict is not None
    finally:
        conn.close()
