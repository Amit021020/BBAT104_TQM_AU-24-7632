# SRS Update — Q01 Reliability Requirements

## 1. Project Identification

**Project:** Hospital Management System
**Course:** BBAT104 – Fundamentals of TQM
**Student:** Amit Suyal
**Roll Number:** 02
**Quality Goal:** Q01 – Improve Reliability

---

## 2. System Objective

The Hospital Management System manages patient, doctor, appointment, medical record, billing, and user information.

The primary TQM objective is:

> Reduce patient wait times & prevent record duplication.

The assigned software quality objective is:

> Improve Reliability.

---

## 3. Functional Requirements

### FR-01 Patient Management

The system shall allow authorized users to create, view, update, and delete patient records.

### FR-02 Doctor Management

The system shall allow authorized users to create, view, update, and delete doctor records.

### FR-03 Appointment Management

The system shall allow authorized users to create, view, update, and delete appointments.

### FR-04 Medical Record Management

The system shall allow authorized users to create, view, update, and delete medical records.

### FR-05 Billing Management

The system shall allow authorized users to create, view, update, and delete bills.

### FR-06 User Management

The system shall allow authorized administrative users to manage system users and their roles.

---

# 4. Q01 Reliability Requirements

### QR-01 Auto Backup

Before protected database write operations, the system shall create a timestamped backup of the SQLite database.

### QR-02 Audit Logging

The system shall record important database operations in an audit log.

### QR-03 Input Validation

The system shall validate user input before database operations.

### QR-04 Error Recovery

The system shall rollback failed database transactions and return controlled error information.

### QR-05 User Roles

The system shall restrict protected operations according to the user's role and permissions.

---

# 5. Reliability Acceptance Criteria

| Requirement      | Acceptance Criteria                                      |
| ---------------- | -------------------------------------------------------- |
| Auto Backup      | Backup file created before protected write               |
| Audit Log        | Operation recorded with action/module/record information |
| Input Validation | Invalid data rejected before database write              |
| Error Recovery   | Failed transaction rolled back                           |
| User Roles       | Unauthorized operation rejected                          |
| Regression       | All reliability tests pass                               |

Current automated regression result:

```text
12 passed
0 failed
```

---

# 6. Non-Functional Requirements

### Reliability

The system should prevent invalid data and recover safely from database failures.

### Data Integrity

Foreign-key constraints and validation shall protect relationships and data correctness.

### Security

User roles shall restrict access to protected operations.

### Auditability

Important operations shall be traceable through audit logs.

### Maintainability

Reliability features shall be implemented through reusable service modules rather than duplicated across CRUD modules.

---

# 7. Scope

## In Scope

* Patient management
* Doctor management
* Appointment management
* Medical records
* Billing
* User management
* SQLite persistence
* Q01 reliability features
* Automated testing
* TQM analysis

## Out of Scope

* Real hospital deployment
* Real patient data
* Integration with external hospital systems
* Real payment gateways
* Production cloud hosting
* Medical decision-making

---

# 8. Quality Assurance Strategy

The project uses:

* Input validation
* Transaction rollback
* Automated testing
* Database backups
* Audit logging
* Role-based access control
* Defect logging
* FMEA
* SQC tools
* PDCA improvement

---

# 9. Test Strategy

The system is tested at service level using Pytest.

Tests cover:

* CRUD functionality
* Input validation
* Role permissions
* Backup creation
* Audit logging
* Error recovery
* Rollback behavior

The regression suite currently contains 12 passing tests.
