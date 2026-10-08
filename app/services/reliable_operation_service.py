from app.services.validation_service import (
    validate_patient,
    validate_doctor,
    validate_appointment,
    validate_medical_record,
    validate_bill,
    validate_user,
)

from app.services.role_service import has_permission
from app.services.backup_service import create_backup
from app.services.audit_service import create_audit_log
from app.services.error_recovery_service import run_database_operation


VALIDATORS = {
    "patient": validate_patient,
    "doctor": validate_doctor,
    "appointment": validate_appointment,
    "medical_record": validate_medical_record,
    "bill": validate_bill,
    "user": validate_user,
}


def validate_data(module, data):
    validator = VALIDATORS.get(module)

    if validator is None:
        return [
            f"No validator found for module: {module}"
        ]

    return validator(data)


def check_permission(role, permission):
    return has_permission(role, permission)


def create_database_backup():
    try:
        backup_path = create_backup()

        if not backup_path:
            return {
                "success": False,
                "message": "Database backup failed."
            }

        return {
            "success": True,
            "backup_path": str(backup_path)
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


def execute_reliable_operation(
    operation,
    role,
    permission,
    module,
    operation_name,
    data=None,
    record_id=None,
    user_id=None,
    create_backup_before=True,
):
    # 1. Check user permission
    if not check_permission(role, permission):
        return {
            "success": False,
            "message": "User does not have permission for this operation."
        }

    # 2. Validate input
    if data is not None:
        errors = validate_data(module, data)

        if errors:
            return {
                "success": False,
                "message": "Input validation failed.",
                "errors": errors
            }

    # 3. Create backup before write operation
    if create_backup_before:
        backup_result = create_database_backup()

        if not backup_result["success"]:
            return {
                "success": False,
                "message": "Operation stopped because database backup failed.",
                "error": backup_result["message"]
            }

    # 4. Execute database operation with error recovery
    result = run_database_operation(operation)

    # 5. Handle database failure
    if not result["success"]:
        create_audit_log(
            action="FAILED",
            module=module,
            record_id=record_id,
            description=(
                f"{operation_name} failed: "
                f"{result['error']}"
            ),
            user_id=user_id,
        )

        return {
            "success": False,
            "message": "Database operation failed.",
            "error": result["error"]
        }

 

    # 6. Determine the record ID for the audit log
    audit_record_id = record_id

    if audit_record_id is None and operation_name.lower() == "create":
        audit_record_id = result["result"]

    # 7. Record successful operation
    create_audit_log(
        action=operation_name.upper(),
        module=module,
        record_id=audit_record_id,
        description=(
            f"{operation_name} completed successfully."
        ),
        user_id=user_id,
    )

    return {
        "success": True,
        "message": (
            f"{operation_name} completed successfully."
        ),
        "result": result["result"]
    }