# Software Requirements Specification (SRS)

## BBAT104 – Fundamentals of TQM

### Hospital Management System

**Student Name:** Amit Suyal
**Roll Number:** 2
**Academic Session:** 2026–27
**Quality Goal:** Q01 – Improve Reliability
**Version:** 1.0

---

# 1. Introduction

## 1.1 Purpose

The purpose of this project is to develop a desktop-based Hospital Management System that provides a structured way to manage essential hospital information and operations.

The system will provide CRUD functionality for major hospital entities and will incorporate reliability-focused features associated with Quality Goal Q01.

The five reliability features are:

1. Automatic Backup
2. Audit Log
3. Input Validation
4. Error Recovery
5. User Roles

The project also applies Total Quality Management principles and Statistical Quality Control techniques to evaluate and continuously improve software quality.

---

## 1.2 Problem Statement

Manual or poorly controlled management of hospital information can result in:

* Incorrect patient information
* Duplicate or incomplete records
* Unauthorized data modification
* Loss of important database information
* Difficulty tracing user actions
* Application failures without proper recovery
* Inconsistent data entry

The proposed system addresses these problems through centralized data management, validation, access control, auditing, backup and recovery mechanisms.

---

# 2. Project Objectives

The primary objectives are:

1. Develop a functional Hospital Management System.
2. Provide CRUD operations for major hospital entities.
3. Improve software reliability through the assigned Q01 features.
4. Prevent invalid data from entering the system.
5. Maintain an audit trail of important user actions.
6. Protect hospital data using role-based access.
7. Provide automatic database backup.
8. Provide mechanisms for recovering from application or data-related errors.
9. Apply TQM principles to software development.
10. Measure and improve software quality using SQC tools.

---

# 3. Scope

## 3.1 In Scope

The system will include:

* User authentication
* Role-based access
* Patient management
* Doctor management
* Appointment management
* Medical record management
* Billing management
* Input validation
* Automatic database backup
* Audit logging
* Error handling and recovery
* SQLite database storage
* Defect logging
* TQM quality analysis
* SQC charts and analysis

## 3.2 Out of Scope

The system will not initially include:

* Real hospital hardware integration
* Online payment gateway integration
* Real-world insurance processing
* External hospital information-system integration
* Cloud deployment
* Real patient medical data

The project is intended as an academic software and quality-management demonstration.

---

# 4. Users and Roles

The system will use role-based access control.

## 4.1 Administrator

The administrator will be able to:

* Manage users
* Manage patients
* Manage doctors
* Manage appointments
* Manage medical records
* Manage billing records
* View audit logs
* Perform backup and recovery operations
* View system information

## 4.2 Doctor

The doctor will be able to:

* View assigned patient information
* View appointments
* Create and update medical records
* View relevant patient history

## 4.3 Receptionist

The receptionist will be able to:

* Register patients
* Update patient information
* Manage appointments
* View doctors
* View basic patient information

Access to administrative functions will be restricted.

---

# 5. Functional Requirements

## FR-01 User Authentication

The system shall allow registered users to log in using valid credentials.

## FR-02 Role-Based Access

The system shall restrict functionality according to the authenticated user's role.

## FR-03 Patient Management

The system shall allow authorized users to:

* Create patient records
* View patient records
* Update patient records
* Delete patient records

## FR-04 Doctor Management

The system shall allow authorized users to:

* Create doctor records
* View doctor records
* Update doctor records
* Delete doctor records

## FR-05 Appointment Management

The system shall allow authorized users to:

* Create appointments
* View appointments
* Update appointments
* Cancel or delete appointments

## FR-06 Medical Record Management

Authorized users shall be able to create and manage medical records associated with patients.

## FR-07 Billing Management

Authorized users shall be able to create, view, update and manage billing records.

## FR-08 Input Validation

The system shall validate user input before storing information in the database.

Examples include:

* Required-field validation
* Numeric validation
* Phone-number validation
* Date validation
* Duplicate-data validation

## FR-09 Automatic Backup

The system shall create database backups according to the defined backup mechanism.

The backup process shall avoid interrupting normal application operation.

## FR-10 Audit Logging

The system shall record important user actions.

An audit entry shall contain information such as:

* User
* Action
* Module
* Timestamp
* Result

## FR-11 Error Recovery

The system shall handle expected application and database errors without unnecessarily terminating the application.

The system shall provide appropriate error messages and recovery mechanisms where possible.

## FR-12 Data Persistence

The system shall store application data using SQLite.

## FR-13 Quality Records

The project shall maintain defect records and quality-analysis data for TQM and SQC activities.

---

# 6. Non-Functional Requirements

## NFR-01 Reliability

The system should minimize data loss and provide mechanisms for backup, auditing, validation and recovery.

## NFR-02 Usability

The graphical interface should provide clear navigation, understandable labels and meaningful error messages.

## NFR-03 Security

Access to system functionality shall be controlled according to user roles.

Passwords shall not be stored as plain text.

## NFR-04 Data Integrity

The system should prevent invalid or incomplete data from being stored.

## NFR-05 Maintainability

The software should use a modular structure so that individual components can be modified without unnecessarily affecting the entire application.

## NFR-06 Performance

Normal CRUD operations should provide responses without unnecessary delays for the expected academic dataset.

## NFR-07 Recoverability

The system should provide database backup and recovery mechanisms to reduce the impact of failures.

## NFR-08 Auditability

Important operations should be traceable through audit records.

---

# 7. Main System Modules

The system will consist of the following modules:

```text
Authentication
      |
      v
Dashboard
      |
      +---- Patient Management
      |
      +---- Doctor Management
      |
      +---- Appointment Management
      |
      +---- Medical Records
      |
      +---- Billing
      |
      +---- User Management
      |
      +---- Audit Logs
      |
      +---- Backup & Recovery
```

---

# 8. Data Requirements

The initial database will contain tables for:

* Users
* Patients
* Doctors
* Appointments
* Medical Records
* Bills
* Audit Logs

The exact fields and relationships will be finalized during database design.

---

# 9. Q01 Reliability Requirements

The assigned Quality Goal is:

**Q01 – Improve Reliability**

The system shall implement the following five features:

| Feature          | Reliability Purpose                |
| ---------------- | ---------------------------------- |
| Automatic Backup | Reduce risk of permanent data loss |
| Audit Log        | Track important system activities  |
| Input Validation | Prevent invalid data               |
| Error Recovery   | Handle failures safely             |
| User Roles       | Prevent unauthorized operations    |

---

# 10. Critical to Quality (CTQ)

The main CTQ characteristics for the system are:

| CTQ            | Requirement                                     | Quality Measure              |
| -------------- | ----------------------------------------------- | ---------------------------- |
| Data Safety    | Database should be recoverable                  | Backup success rate          |
| Data Integrity | Invalid records should be prevented             | Validation failure rate      |
| Traceability   | Important actions should be recorded            | Audit logging coverage       |
| Access Control | Users should only access permitted functions    | Unauthorized access attempts |
| Recovery       | Application should recover from expected errors | Successful recovery rate     |

These CTQs will later be used when performing TQM and quality analysis.

---

# 11. Constraints

The project will be developed as an academic desktop application.

Primary constraints include:

* Python-based implementation
* SQLite-based local persistence
* Desktop GUI
* Limited to the defined academic scope
* No requirement for production hospital deployment
* No use of real patient information

---

# 12. Assumptions

The project assumes:

1. Users have authorized accounts.
2. The application runs on a supported desktop environment.
3. The SQLite database is accessible to the application.
4. Users provide information through the application interface.
5. Backup storage is available locally.
6. The system is primarily intended for demonstration and academic evaluation.

---

# 13. TQM and Quality Improvement

The project will apply the following TQM principles:

* Customer focus
* Continuous improvement
* Process-centric approach
* Fact-based decision making
* Error prevention

The quality-analysis phase will use:

* SIPOC
* CTQ Tree
* FMEA
* Checksheets
* Defect Logs
* Pareto Analysis
* Fishbone Diagram
* PDCA

The project guidelines identify these principles and SQC tools as part of the required project methodology.

---

# 14. Acceptance Criteria

The project will be considered functionally complete when:

1. Users can authenticate successfully.
2. Role-based permissions work correctly.
3. Core CRUD modules operate correctly.
4. Invalid inputs are rejected appropriately.
5. Database backups can be created.
6. Backup data can be recovered.
7. Important actions appear in audit logs.
8. Expected application errors are handled safely.
9. Unauthorized operations are prevented.
10. Required TQM and SQC deliverables are completed.
11. The system can be demonstrated successfully during the final evaluation.

---

# 15. Future Improvements

Possible future improvements include:

* Web-based deployment
* Cloud database integration
* Email/SMS notifications
* Advanced analytics
* Multi-hospital support
* Online appointment booking
* Integration with external healthcare systems

These improvements are outside the current project scope.
