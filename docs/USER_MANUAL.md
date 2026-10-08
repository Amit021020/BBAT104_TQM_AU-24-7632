# Hospital Management System — User Manual

## 1. Introduction

This manual explains how to use the BBAT104 Hospital Management System.

The system manages patients, doctors, appointments, medical records, bills, and users while applying reliability controls based on Q01 – Improve Reliability.

---

## 2. System Roles

### Admin

The Admin has the highest level of system access and can perform administrative operations such as managing records, users, backups, and audit information.

### Doctor

Doctors can access patient and medical information required for their operational responsibilities.

### Staff

Staff can perform permitted operational tasks such as viewing and managing appropriate patient and appointment information.

---

## 3. Patient Management

### Create Patient

Enter:

* Patient code
* Name
* Age
* Gender
* Blood group
* Phone
* Address
* Emergency contact

The system validates the entered information before saving it.

### View Patients

The patient list displays stored patient records.

### Update Patient

Select the required patient and modify the permitted information.

### Delete Patient

Delete the selected patient only when the operation is permitted by the user's role.

---

## 4. Doctor Management

Doctors can be managed using:

* Create
* Read
* Update
* Delete

Doctor information includes specialization, department, phone, and email.

---

## 5. Appointment Management

Appointments connect patients with doctors.

Required information includes:

* Patient
* Doctor
* Appointment date
* Appointment time
* Reason
* Status

Foreign-key validation prevents appointments from referencing nonexistent patients or doctors.

---

## 6. Medical Records

Medical records maintain:

* Patient
* Doctor
* Diagnosis
* Prescription
* Notes
* Record date

Access is controlled according to user role.

---

## 7. Billing

Bills contain:

* Patient
* Amount
* Payment status
* Bill date

The system prevents invalid negative bill amounts.

Example rejected input:

```text
Amount = -500
```

Result:

```text
Input validation failed.
Bill amount cannot be negative.
```

---

## 8. User Management

Users contain:

* Username
* Password hash
* Role
* Active status

Supported roles:

```text
Admin
Doctor
Staff
```

Passwords are not stored as plain text.

---

# 9. Reliability Features

## Auto Backup

Before write operations, the system creates a timestamped database backup.

Backup files are stored in:

```text
backups/
```

---

## Audit Log

Important operations are recorded automatically.

Examples:

```text
CREATE
UPDATE
DELETE
FAILED
```

The audit log provides traceability of system activity.

---

## Input Validation

Invalid data is rejected before reaching the database.

Examples:

* Missing required fields
* Invalid age
* Invalid phone number
* Invalid email
* Negative bill amount
* Invalid user information

---

## Error Recovery

Database failures trigger transaction rollback.

This prevents incomplete database transactions from leaving inconsistent data.

---

## User Roles

The system checks whether the current user has permission before executing protected operations.

Unauthorized operations return a controlled failure response.

---

# 10. Testing

Run:

```bash
.venv/bin/python3 -m pytest -v
```

The current Q01 regression suite has:

```text
12 passed
0 failed
```

---

# 11. Backup Verification

Backups can be inspected from:

```text
backups/
```

Example:

```text
hospital_backup_20261008_163530.db
```

---

# 12. Audit Verification

Audit records are stored in the:

```text
audit_logs
```

database table.

Each record contains an action, module, record identifier where available, description, user identifier where available, and timestamp.

---

# 13. Error Handling

When an operation fails, the system returns a structured error rather than allowing an uncontrolled database exception to crash the operation.

Example:

```text
{
    "success": false,
    "message": "Input validation failed.",
    "errors": [...]
}
```

---

# 14. Troubleshooting

### Tests do not run

Use the project virtual environment:

```bash
.venv/bin/python3 -m pytest -v
```

### Database is missing

The database is located at:

```text
database/hospital.db
```

Database initialization is handled by the application database module.

### Validation rejects data

Check the required fields and expected formats before submitting the operation.

### Permission denied

Verify that the current user's role has the required permission.

---

# 15. Reliability Workflow

The normal write-operation workflow is:

```text
User Request
     ↓
Permission Check
     ↓
Input Validation
     ↓
Database Backup
     ↓
Database Operation
     ↓
Commit / Rollback
     ↓
Audit Log
     ↓
Result
```

This workflow is the core implementation of Q01 – Improve Reliability.
