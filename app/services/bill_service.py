from app.services.reliable_operation_service import (
    execute_reliable_operation,
)
from app.database.db import get_connection


def create_bill(data, role="Admin", user_id=None):
    """Create a new bill."""

    def operation(connection):
        cursor = connection.execute(
            """
            INSERT INTO bills (
                patient_id,
                amount,
                payment_status,
                bill_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                data["patient_id"],
                data["amount"],
                data.get("payment_status", "Pending"),
                data["bill_date"],
            ),
        )

        return cursor.lastrowid

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="create_bills",
        module="bill",
        operation_name="create",
        data=data,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def get_all_bills(role="Admin"):
    """Return all bills ordered by ID."""

    if role not in ("Admin", "Staff"):
        return {
            "success": False,
            "message": "User does not have permission to view bills.",
        }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM bills
            ORDER BY id
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_bill(
    bill_id,
    data,
    role="Admin",
    user_id=None,
):
    """Update an existing bill."""

    def operation(connection):
        cursor = connection.execute(
            """
            UPDATE bills
            SET
                patient_id = ?,
                amount = ?,
                payment_status = ?,
                bill_date = ?
            WHERE id = ?
            """,
            (
                data["patient_id"],
                data["amount"],
                data.get("payment_status", "Pending"),
                data["bill_date"],
                bill_id,
            ),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="update_bills",
        module="bill",
        operation_name="update",
        data=data,
        record_id=bill_id,
        user_id=user_id,
    )

    if not result["success"]:
        return result

    return result["result"]


def delete_bill(
    bill_id,
    role="Admin",
    user_id=None,
):
    """Delete a bill."""

    def operation(connection):
        cursor = connection.execute(
            """
            DELETE FROM bills
            WHERE id = ?
            """,
            (bill_id,),
        )

        return cursor.rowcount > 0

    result = execute_reliable_operation(
        operation=operation,
        role=role,
        permission="delete_bills",
        module="bill",
        operation_name="delete",
        record_id=bill_id,
        user_id=user_id,
        data=None,
    )

    if not result["success"]:
        return result

    return result["result"]