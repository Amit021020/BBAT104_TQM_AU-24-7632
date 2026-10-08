# BBAT104 TQM — Hospital Management System

## Project Information

| Field                 | Details                                                |
| --------------------- | ------------------------------------------------------ |
| Course                | BBAT104 – Fundamentals of Total Quality Management     |
| Academic Session      | 2026–27                                                |
| Student Name          | Amit Suyal                                             |
| Roll Number           | 02                                                     |
| Baseline System       | Hospital Management System                             |
| Assigned Quality Goal | Q01 – Improve Reliability                              |
| Core TQM Goal         | Reduce patient wait times & prevent record duplication |
| Language              | Python 3.x                                             |
| Database              | SQLite3                                                |
| Testing               | Pytest                                                 |
| Version Control       | Git / GitHub                                           |

---

## 1. Project Overview

This project implements a Hospital Management System developed as part of the BBAT104 Fundamentals of Total Quality Management course.

The system provides structured management of:

* Patients
* Doctors
* Appointments
* Medical Records
* Bills
* Users

The project applies Total Quality Management principles to software development, with particular emphasis on reliability, error prevention, process control, auditability, and continuous improvement.

For Roll Number 02, the assigned Quality Goal is:

> **Q01 – Improve Reliability**

The five reliability features implemented are:

1. Auto Backup
2. Audit Log
3. Input Validation
4. Error Recovery
5. User Roles

---

## 2. TQM Objective

The baseline Hospital Management System is intended to support the TQM objective:

> **Reduce patient wait times & prevent record duplication.**

The Q01 reliability goal strengthens the system by preventing invalid data, controlling access to operations, recovering safely from database failures, maintaining audit records, and protecting database data through automatic backups.

---

## 3. System Features

### 3.1 Patient Management

The system supports:

* Create patient
* View patients
* Update patient
* Delete patient

Patient information includes:

* Patient code
* Name
* Age
* Gender
* Blood group
* Phone
* Address
* Emergency contact

### 3.2 Doctor Management

The system supports:

* Create doctor
* View doctors
* Update doctor
* Delete doctor

Doctor information includes:

* Doctor code
* Name
* Specialization
* Department
* Phone
* Email

### 3.3 Appointment Management

The system supports:

* Create appointment
* View appointments
* Update appointment
* Delete appointment

Appointments maintain relationships between patients and doctors.

### 3.4 Medical Record Management

The system supports:

* Create medical record
* View medical records
* Update medical record
* Delete medical record

Medical records maintain patient and doctor relationships.

### 3.5 Billing Management

The system supports:

* Create bill
* View bills
* Update bill
* Delete bill

Bill information includes:

* Patient
* Amount
* Payment status
* Bill date

### 3.6 User Management

The system supports:

* Create user
* View users
* Update users
* Delete users

Passwords are stored using hashing rather than plain-text storage.

---

# 4. Q01 – Improve Reliability

The assigned Quality Goal for Roll Number 02 is Q01 – Improve Reliability.

The five required reliability features are implemented as follows.

## 4.1 Auto Backup

Before database write operations, the system creates a timestamped backup of the SQLite database.

Example:

```text
backups/
├── hospital_backup_20261008_163247.db
├── hospital_backup_20261008_163248.db
└── hospital_backup_20261008_163530.db
```

Backup responsibilities are implemented in:

```text
app/services/backup_service.py
```

The backup system:

* Creates the backup directory when required
* Creates timestamped database copies
* Lists available backups
* Supports restoration of a backup

---

## 4.2 Audit Log

Important database operations are recorded in the `audit_logs` table.

The audit system records:

* Action
* Module
* Record ID
* User ID
* Description
* Timestamp

Examples of recorded operations include:

```text
CREATE
UPDATE
DELETE
FAILED
```

Audit functionality is implemented in:

```text
app/services/audit_service.py
```

This provides traceability for important system operations.

---

## 4.3 Input Validation

The system validates user input before database operations.

Validation is implemented in:

```text
app/services/validation_service.py
```

Examples include:

* Required-field validation
* Age range validation
* Phone number validation
* Email validation
* Date validation
* Numeric bill amount validation
* User/password validation

For example, a negative bill amount is rejected:

```text
Input validation failed.
Bill amount cannot be negative.
```

This follows the TQM principle of error prevention (Poka-Yoke).

---

## 4.4 Error Recovery

Database operations are executed through a common reliability layer.

Implemented in:

```text
app/services/error_recovery_service.py
```

The system:

1. Starts a database operation.
2. Commits when successful.
3. Rolls back when an exception occurs.
4. Returns a structured failure response.
5. Records failed operations in the audit log.

Rollback testing has confirmed that failed transactions do not leave partial database changes.

---

## 4.5 User Roles

Role-based permissions are implemented in:

```text
app/services/role_service.py
```

The system currently supports:

* Admin
* Doctor
* Staff

Permissions control which operations each role can perform.

Example:

```text
Admin
 ├── View
 ├── Create
 ├── Update
 ├── Delete
 └── Manage reliability-related operations

Doctor
 ├── View relevant records
 ├── Create relevant records
 └── Update relevant records

Staff
 ├── View permitted records
 └── Perform permitted operational tasks
```

Unauthorized operations are rejected by the reliability layer.

---

# 5. Reliability Integration Layer

The five Q01 features are integrated through:

```text
app/services/reliable_operation_service.py
```

The common operation flow is:

```text
User Request
     ↓
Role Permission Check
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

This provides a consistent quality-control process across the system.

---

# 6. System Architecture

```text
                    Hospital Management System
                              │
                              ▼
                         User / UI Layer
                              │
                              ▼
                       Service Layer
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Patient Service     Doctor Service     Appointment Service
          │                   │                   │
          ├───────────────────┼───────────────────┤
          │                   │                   │
          ▼                   ▼                   ▼
 Medical Record Service   Bill Service       User Service
                              │
                              ▼
                  Reliable Operation Layer
                              │
          ┌───────────────┬───┴────┬──────────────┐
          │               │        │              │
          ▼               ▼        ▼              ▼
     Validation       Backup    Error         Audit Log
                                  Recovery
          │
          ▼
      Role Control
          │
          ▼
       SQLite DB
```

---

# 7. Database

The system uses SQLite3 for persistent data storage.

Main tables:

```text
users
patients
doctors
appointments
medical_records
bills
audit_logs
```

Foreign-key constraints are enabled to protect relationships between records.

Database initialization is handled by:

```text
app/database/db.py
```

Database file:

```text
database/hospital.db
```

---

# 8. Project Structure

```text
BBAT104_TQM_AU-24-7632/
│
├── app/
│   ├── database/
│   │   └── db.py
│   │
│   ├── models/
│   │
│   └── services/
│       ├── patient_service.py
│       ├── doctor_service.py
│       ├── appointment_service.py
│       ├── medical_record_service.py
│       ├── bill_service.py
│       ├── user_service.py
│       ├── backup_service.py
│       ├── audit_service.py
│       ├── validation_service.py
│       ├── error_recovery_service.py
│       ├── role_service.py
│       └── reliable_operation_service.py
│
├── backups/
├── database/
│   └── hospital.db
│
├── docs/
│   ├── SRS.md
│   ├── ARCHITECTURE.md
│   └── DATABASE_DESIGN.md
│
├── logs/
├── sqc/
│
├── tests/
│   ├── test_crud.py
│   └── test_q01_reliability.py
│
├── README.md
├── .gitignore
└── .venv/
```

---

# 9. Testing

Automated tests are implemented using Pytest.

The current regression suite contains:

```text
12 passed
0 failed
```

The tests verify:

* Base CRUD functionality
* Input validation
* Bill validation
* Role permissions
* Database backups
* Audit logs
* Error recovery and rollback

Run the tests with:

```bash
.venv/bin/python3 -m pytest -v
```

---

# 10. TQM Principles Applied

## Customer Focus

The system focuses on reliable hospital operations and reducing problems that can affect patients and staff.

## Continuous Improvement (Kaizen)

The system is developed incrementally and tested after each major improvement.

## Process-Centric Approach

Important hospital processes are being mapped using TQM tools such as SIPOC and process analysis.

## Fact-Based Decision Making

Defect logs, testing results, FMEA risk scores, and SQC tools are used to identify and prioritize problems.

## Error Prevention (Poka-Yoke)

Input validation prevents invalid information from entering the database.

---

# 11. TQM Analysis

The project will use the following TQM tools:

* SIPOC Process Analysis
* CTQ Tree
* FMEA Matrix
* RPN Calculation
* Defect Log
* Checksheet
* Pareto Analysis
* Fishbone/Ishikawa Diagram
* PDCA Cycle

These artifacts will be maintained in the `sqc/` and `docs/` directories as the project progresses.

---

# 12. Installation

### Requirements

* Python 3.x
* Git
* VS Code or another Python IDE

### Setup

Clone the repository:

```bash
git clone <repository-url>
cd BBAT104_TQM_AU-24-7632
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install testing dependency:

```bash
.venv/bin/python3 -m pip install pytest
```

Run the test suite:

```bash
.venv/bin/python3 -m pytest -v
```

---

# 13. Quality Evidence

Current Q01 implementation evidence includes:

* Successful CRUD tests
* Successful validation tests
* Successful role-permission tests
* Successful database backup creation
* Successful audit-log generation
* Successful transaction rollback testing
* 12/12 automated tests passing

---

# 14. Project Status

### Completed

* [x] Project environment
* [x] Repository structure
* [x] SRS
* [x] Architecture documentation
* [x] Database design
* [x] Patient CRUD
* [x] Doctor CRUD
* [x] Appointment CRUD
* [x] Medical Record CRUD
* [x] Bill CRUD
* [x] User CRUD
* [x] Auto Backup
* [x] Audit Log
* [x] Input Validation
* [x] Error Recovery
* [x] User Roles
* [x] Q01 integration
* [x] Q01 regression testing

### Upcoming

* [ ] SIPOC
* [ ] CTQ Tree
* [ ] FMEA Matrix
* [ ] RPN Analysis
* [ ] Defect Log
* [ ] Checksheets
* [ ] Pareto Analysis
* [ ] Fishbone Diagram
* [ ] PDCA Cycle
* [ ] User Manual
* [ ] Final screenshots/evidence
* [ ] GitHub Issues
* [ ] 30+ meaningful commits
* [ ] Final demonstration and viva preparation

---

# 15. Academic Deliverables

The project documentation is organized around the BBAT104 evaluation requirements:

### Review 1 – Setup & SRS

* GitHub repository
* System Architecture
* SRS
* Scope

### Review 2 – Base System & CRUD

* Functional CRUD modules
* Assigned Q01 reliability features

### Review 3 – FMEA & Risk

* FMEA Matrix
* RPN calculations
* SIPOC
* CTQ Tree
* Defect Logging

### Review 4 – SQC & Continuous Improvement

* Pareto Chart
* Fishbone Diagram
* Checksheets
* PDCA Cycle

### Final Demonstration

* Working system
* Test evidence
* Defect-handling explanation
* TQM viva preparation

---

## 16. Author

**Amit Suyal**
Roll Number: **2410301002**
Course: **BBAT104 – Fundamentals of Total Quality Management**
Academic Session: **2026–27**
