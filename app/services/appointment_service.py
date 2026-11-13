from datetime import datetime, timedelta

from app.database.db import get_connection
from app.services.reliable_operation_service import (
    execute_reliable_operation,
)


class AppointmentConflictError(Exception):
    """Raised when a doctor already has an overlapping appointment."""
    pass


def validate_appointment_slot(date, time, duration):
    """Validate and calculate appointment start and end."""

    start = datetime.strptime(
        f"{date} {time}",
        "%Y-%m-%d %H:%M",
    )

    duration = int(duration)

    if duration not in (30, 60):
        raise ValueError(
            "Consultation duration must be 30 or 60 minutes."
        )

    end = start + timedelta(minutes=duration)

    if end.date() != start.date():
        raise ValueError(
            "Appointments cannot cross midnight."
        )

    return start, end


def find_appointment_conflict(
    connection,
    doctor_id,
    appointment_date,
    appointment_time,
    duration_minutes,
    exclude_id=None,
):
    """Return an overlapping appointment, if one exists."""

    new_start, new_end = validate_appointment_slot(
        appointment_date,
        appointment_time,
        duration_minutes,
    )

    existing = connection.execute(
        """
        SELECT
            id,
            appointment_date,
            appointment_time,
            duration_minutes,
            status
        FROM appointments
        WHERE doctor_id = ?
          AND appointment_date = ?
          AND status != 'Cancelled'
        """,
        (doctor_id, appointment_date),
    ).fetchall()

    for appointment in existing:

        if exclude_id is not None:
            if appointment["id"] == exclude_id:
                continue

        existing_start, existing_end = validate_appointment_slot(
            appointment["appointment_date"],
            appointment["appointment_time"],
            appointment["duration_minutes"],
        )

        # Two time intervals overlap when:
        # new_start < existing_end AND new_end > existing_start
        if new_start < existing_end and new_end > existing_start:
            return dict(appointment)

    return None



def validate_doctor_working_hours(
    connection,
    doctor_id,
    appointment_date,
    appointment_time,
    duration_minutes,
):
    """Ensure an appointment fits within a doctor's working hours."""

    start, end = validate_appointment_slot(
        appointment_date,
        appointment_time,
        duration_minutes,
    )

    schedule = connection.execute(
        """
        SELECT start_time, end_time
        FROM doctor_working_hours
        WHERE doctor_id = ?
          AND day_of_week = ?
          AND is_active = 1
        """,
        (doctor_id, start.weekday()),
    ).fetchone()

    if schedule is None:
        raise ValueError(
            "Doctor is not scheduled to work on this day."
        )

    working_start = datetime.strptime(
        f"{appointment_date} {schedule['start_time']}",
        "%Y-%m-%d %H:%M",
    )

    working_end = datetime.strptime(
        f"{appointment_date} {schedule['end_time']}",
        "%Y-%m-%d %H:%M",
    )

    if start < working_start or end > working_end:
        raise ValueError(
            "Appointment is outside the doctor's working hours."
        )

    if start.minute not in (0, 30):
        raise ValueError(
            "Appointments must start on a 30-minute boundary."
        )

    return True

def create_appointment(data, role="Admin", user_id=None):
    """Create an appointment without double-booking a doctor."""

    def operation(connection):
        # Lock the database for this write transaction.
        connection.execute("BEGIN IMMEDIATE")

        duration = int(data.get("duration_minutes", 30))

        # Validate the date, time, and duration.
        validate_appointment_slot(
            data["appointment_date"],
            data["appointment_time"],
            duration,
        )
        validate_doctor_working_hours(
            connection=connection,
            doctor_id=data["doctor_id"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            duration_minutes=duration,
        )
        # Prevent overlapping appointments.
        conflict = find_appointment_conflict(
            connection=connection,
            doctor_id=data["doctor_id"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            duration_minutes=duration,
        )

        if conflict:
            raise AppointmentConflictError(
                "Doctor is already booked during this time."
            )

        cursor = connection.execute(
            """
            INSERT INTO appointments (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                duration_minutes,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["appointment_date"],
                data["appointment_time"],
                duration,
                data.get("reason"),
                "Scheduled",
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
    """Update an appointment while preventing scheduling conflicts."""

    def operation(connection):
        connection.execute("BEGIN IMMEDIATE")

        duration = int(data.get("duration_minutes", 30))
        status = data.get("status", "Scheduled")

        validate_appointment_slot(
            data["appointment_date"],
            data["appointment_time"],
            duration,
        )

        if status not in (
            "Scheduled",
            "In Progress",
            "Completed",
            "Cancelled",
        ):
            raise ValueError("Invalid appointment status.")

        if status != "Cancelled":
            conflict = find_appointment_conflict(
                connection=connection,
                doctor_id=data["doctor_id"],
                appointment_date=data["appointment_date"],
                appointment_time=data["appointment_time"],
                duration_minutes=duration,
                exclude_id=appointment_id,
            )

            if conflict:
                raise AppointmentConflictError(
                    "Doctor is already booked during this time."
                )
        if status != "Cancelled":
            validate_doctor_working_hours(
                connection=connection,
                doctor_id=data["doctor_id"],
                appointment_date=data["appointment_date"],
                appointment_time=data["appointment_time"],
                duration_minutes=duration,
            )
        cursor = connection.execute(
            """
            UPDATE appointments
            SET
                patient_id = ?,
                doctor_id = ?,
                appointment_date = ?,
                appointment_time = ?,
                duration_minutes = ?,
                reason = ?,
                status = ?
            WHERE id = ?
            """,
            (
                data["patient_id"],
                data["doctor_id"],
                data["appointment_date"],
                data["appointment_time"],
                duration,
                data.get("reason"),
                status,
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