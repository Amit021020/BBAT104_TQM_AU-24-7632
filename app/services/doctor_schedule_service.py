
from datetime import datetime, timedelta

from app.database.db import get_connection
from app.services.role_service import has_permission
from app.services.error_recovery_service import run_database_operation
from app.services.backup_service import create_backup
from app.services.audit_service import create_audit_log


def get_doctor_schedule(doctor_id):
    """Return the weekly schedule for a doctor."""

    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT *
            FROM doctor_working_hours
            WHERE doctor_id = ?
            ORDER BY day_of_week
            """,
            (doctor_id,),
        ).fetchall()

    finally:
        connection.close()


def save_doctor_schedule(
    doctor_id,
    day_of_week,
    start_time,
    end_time,
    is_active=True,
    role="Admin",
    user_id=None,
):
    """Create or update one day's working hours."""

    if not has_permission(role, "update_doctors"):
        return {
            "success": False,
            "message": "Permission denied.",
        }

    try:
        day_of_week = int(day_of_week)

        if day_of_week not in range(7):
            raise ValueError("Invalid day of week.")

        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        if start >= end:
            raise ValueError(
                "End time must be later than start time."
            )

        active = 1 if is_active else 0

    except (ValueError, TypeError) as error:
        return {
            "success": False,
            "message": str(error),
        }

    def operation(connection):
        connection.execute("BEGIN IMMEDIATE")

        doctor = connection.execute(
            "SELECT id FROM doctors WHERE id = ?",
            (doctor_id,),
        ).fetchone()

        if doctor is None:
            raise ValueError("Doctor does not exist.")

        connection.execute(
            """
            INSERT INTO doctor_working_hours (
                doctor_id,
                day_of_week,
                start_time,
                end_time,
                is_active
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(doctor_id, day_of_week)
            DO UPDATE SET
                start_time = excluded.start_time,
                end_time = excluded.end_time,
                is_active = excluded.is_active
            """,
            (
                doctor_id,
                day_of_week,
                start_time,
                end_time,
                active,
            ),
        )

        return True

    # Follow the same backup and audit principles
    # as the rest of the project.
    try:
        backup_path = create_backup()

        if not backup_path:
            raise RuntimeError("Database backup failed.")

    except Exception as error:
        return {
            "success": False,
            "message": str(error),
        }

    result = run_database_operation(operation)

    create_audit_log(
        action="UPDATE" if result["success"] else "FAILED",
        module="doctor_schedule",
        record_id=doctor_id,
        description=(
            "Doctor working hours updated."
            if result["success"]
            else f"Schedule update failed: {result['error']}"
        ),
        user_id=user_id,
    )

    if not result["success"]:
        return {
            "success": False,
            "message": result["error"],
        }

    return {
        "success": True,
        "message": "Working hours saved successfully.",
    }


def get_available_slots(
    doctor_id,
    appointment_date,
    duration_minutes=30,
):
    """Return free appointment slots for a doctor on a date."""

    duration_minutes = int(duration_minutes)

    if duration_minutes not in (30, 60):
        raise ValueError("Duration must be 30 or 60 minutes.")

    date = datetime.strptime(
        appointment_date,
        "%Y-%m-%d",
    ).date()

    connection = get_connection()

    try:
        schedule = connection.execute(
            """
            SELECT start_time, end_time
            FROM doctor_working_hours
            WHERE doctor_id = ?
              AND day_of_week = ?
              AND is_active = 1
            """,
            (doctor_id, date.weekday()),
        ).fetchone()

        if schedule is None:
            return []

        appointments = connection.execute(
            """
            SELECT appointment_time, duration_minutes
            FROM appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND status != 'Cancelled'
            """,
            (doctor_id, appointment_date),
        ).fetchall()

    finally:
        connection.close()

    start = datetime.strptime(
        f"{appointment_date} {schedule['start_time']}",
        "%Y-%m-%d %H:%M",
    )

    end = datetime.strptime(
        f"{appointment_date} {schedule['end_time']}",
        "%Y-%m-%d %H:%M",
    )

    duration = timedelta(minutes=duration_minutes)

    booked_intervals = []

    for appointment in appointments:
        booked_start = datetime.strptime(
            f"{appointment_date} {appointment['appointment_time']}",
            "%Y-%m-%d %H:%M",
        )

        booked_end = booked_start + timedelta(
            minutes=appointment["duration_minutes"]
        )

        booked_intervals.append((booked_start, booked_end))

    available = []
    current = start

    while current + duration <= end:
        slot_end = current + duration

        overlap = any(
            current < booked_end and slot_end > booked_start
            for booked_start, booked_end in booked_intervals
        )

        if not overlap:
            available.append(current.strftime("%H:%M"))

        current += timedelta(minutes=30)

    return available
