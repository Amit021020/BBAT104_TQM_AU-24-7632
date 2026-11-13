
import sqlite3
import pytest

from app.services.appointment_service import (
    validate_doctor_working_hours,
)


@pytest.fixture
def connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.execute(
        """
        CREATE TABLE doctor_working_hours (
            doctor_id INTEGER,
            day_of_week INTEGER,
            start_time TEXT,
            end_time TEXT,
            is_active INTEGER
        )
        """
    )

    conn.execute(
        """
        INSERT INTO doctor_working_hours
        VALUES (2, 0, '09:00', '17:00', 1)
        """
    )

    yield conn
    conn.close()


def test_appointment_within_working_hours(connection):
    assert validate_doctor_working_hours(
        connection, 2, "2026-11-16", "09:00", 30
    )


def test_appointment_outside_working_hours(connection):
    with pytest.raises(ValueError):
        validate_doctor_working_hours(
            connection, 2, "2026-11-16", "17:00", 30
        )


def test_appointment_on_nonworking_day(connection):
    with pytest.raises(ValueError):
        validate_doctor_working_hours(
            connection, 2, "2026-11-17", "09:00", 30
        )


def test_appointment_crossing_closing_time(connection):
    with pytest.raises(ValueError):
        validate_doctor_working_hours(
            connection, 2, "2026-11-16", "16:30", 60
        )
