ROLES = {
    "Admin": {
        "view_patients",
        "create_patients",
        "update_patients",
        "delete_patients",

        "view_doctors",
        "create_doctors",
        "update_doctors",
        "delete_doctors",

        "view_medical_records",
        "create_medical_records",
        "update_medical_records",
        "delete_medical_records",

        "manage_users",
        "view_audit_logs",
        "create_backups",

        "view_appointments",
        "create_appointments",
        "update_appointments",
        "delete_appointments",

        "view_bills",
        "create_bills",
        "update_bills",
        "delete_bills",
    },

    "Doctor": {
        "view_patients",
        "create_patients",
        "update_patients",

        "view_doctors",
        "create_doctors",
        "update_doctors",

        "view_medical_records",
        "create_medical_records",
        "update_medical_records",

        "view_appointments",
        "create_appointments",
        "update_appointments",
    },

    "Staff": {
        "view_patients",
        "create_patients",
        "update_patients",

        "view_doctors",

        "view_appointments",
        "create_appointments",
        "update_appointments",

        "view_bills",
        "create_bills",
        "update_bills",
    },
}


def get_permissions(role):
    return ROLES.get(role, set())


def has_permission(role, permission):
    permissions = get_permissions(role)

    return permission in permissions


def validate_role(role):
    return role in ROLES


def get_all_roles():
    return list(ROLES.keys())