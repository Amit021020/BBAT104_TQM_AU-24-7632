import re


def validate_required(data, fields):
    errors = []

    for field in fields:
        value = data.get(field)

        if value is None or str(value).strip() == "":
            errors.append(f"{field} is required.")

    return errors


def validate_patient(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            ["patient_code", "name", "age", "gender"],
        )
    )

    if "age" in data:
        try:
            age = int(data["age"])

            if age < 0 or age > 120:
                errors.append("Age must be between 0 and 120.")

        except (TypeError, ValueError):
            errors.append("Age must be a valid number.")

    if data.get("phone"):
        if not re.fullmatch(r"\d{10}", str(data["phone"])):
            errors.append("Phone number must contain 10 digits.")

    if data.get("emergency_contact"):
        if not re.fullmatch(
            r"\d{10}",
            str(data["emergency_contact"]),
        ):
            errors.append(
                "Emergency contact must contain 10 digits."
            )

    return errors


def validate_doctor(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            ["doctor_code", "name", "specialization", "department"],
        )
    )

    if data.get("phone"):
        if not re.fullmatch(r"\d{10}", str(data["phone"])):
            errors.append("Phone number must contain 10 digits.")

    if data.get("email"):
        if not re.fullmatch(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            str(data["email"]),
        ):
            errors.append("Invalid email address.")

    return errors


def validate_appointment(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            [
                "patient_id",
                "doctor_id",
                "appointment_date",
                "appointment_time",
            ],
        )
    )

    return errors


def validate_medical_record(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            [
                "patient_id",
                "doctor_id",
                "diagnosis",
                "record_date",
            ],
        )
    )

    return errors


def validate_bill(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            ["patient_id", "amount", "bill_date"],
        )
    )

    if "amount" in data:
        try:
            amount = float(data["amount"])

            if amount < 0:
                errors.append("Bill amount cannot be negative.")

        except (TypeError, ValueError):
            errors.append("Bill amount must be a valid number.")

    return errors


def validate_user(data):
    errors = []

    errors.extend(
        validate_required(
            data,
            ["username", "password", "role"],
        )
    )

    if data.get("username"):
        if len(str(data["username"])) < 3:
            errors.append(
                "Username must contain at least 3 characters."
            )

    if data.get("password"):
        if len(str(data["password"])) < 6:
            errors.append(
                "Password must contain at least 6 characters."
            )

    return errors