# Database Design

## 1. Introduction

The Hospital Management System will use SQLite as its database.

The database will store information related to patients, doctors, appointments, medical records, bills, users and system activities.

The main purpose of the database is to keep the data organized and reduce problems such as duplicate records, missing information and incorrect entries.

SQLite is being used because the project is a desktop application and SQLite is simple to set up and does not require a separate database server.

---

## 2. Database Tables

The system will have the following main tables:

1. users
2. patients
3. doctors
4. appointments
5. medical_records
6. bills
7. audit_logs

Each table has a specific purpose and the tables are connected using primary keys and foreign keys where required.

---

## 3. users

This table stores the users who can access the hospital management system.

| Column        | Type    | Description                         |
| ------------- | ------- | ----------------------------------- |
| id            | INTEGER | Primary key                         |
| username      | TEXT    | Login username                      |
| password_hash | TEXT    | Hashed password                     |
| role          | TEXT    | User role                           |
| created_at    | TEXT    | Account creation date               |
| is_active     | INTEGER | Shows whether the account is active |

### Roles

The main roles are:

* Administrator
* Doctor
* Receptionist

The role will be used for access control so that users only get access to the functions they are allowed to use.

---

## 4. patients

This table stores the basic information of patients.

| Column            | Type    | Description                        |
| ----------------- | ------- | ---------------------------------- |
| id                | INTEGER | Primary key                        |
| patient_code      | TEXT    | Unique patient identification code |
| name              | TEXT    | Patient name                       |
| age               | INTEGER | Patient age                        |
| gender            | TEXT    | Patient gender                     |
| blood_group       | TEXT    | Blood group                        |
| phone             | TEXT    | Contact number                     |
| address           | TEXT    | Patient address                    |
| emergency_contact | TEXT    | Emergency contact number           |
| created_at        | TEXT    | Date the patient was added         |

The patient_code will help identify patients and will also help prevent duplicate patient records.

---

## 5. doctors

This table stores information about doctors working in the hospital.

| Column         | Type    | Description                       |
| -------------- | ------- | --------------------------------- |
| id             | INTEGER | Primary key                       |
| doctor_code    | TEXT    | Unique doctor identification code |
| name           | TEXT    | Doctor name                       |
| specialization | TEXT    | Doctor specialization             |
| department     | TEXT    | Hospital department               |
| phone          | TEXT    | Contact number                    |
| email          | TEXT    | Email address                     |
| created_at     | TEXT    | Date the doctor was added         |

The doctor_code will be used to uniquely identify doctors.

---

## 6. appointments

This table stores appointments between patients and doctors.

| Column           | Type    | Description                      |
| ---------------- | ------- | -------------------------------- |
| id               | INTEGER | Primary key                      |
| patient_id       | INTEGER | ID of the patient                |
| doctor_id        | INTEGER | ID of the doctor                 |
| appointment_date | TEXT    | Appointment date                 |
| appointment_time | TEXT    | Appointment time                 |
| reason           | TEXT    | Reason for appointment           |
| status           | TEXT    | Appointment status               |
| created_at       | TEXT    | Date the appointment was created |

### Foreign Keys

* patient_id references patients.id
* doctor_id references doctors.id

The appointment table connects a patient with a doctor.

---

## 7. medical_records

This table stores the medical information created during patient treatment.

| Column       | Type    | Description                |
| ------------ | ------- | -------------------------- |
| id           | INTEGER | Primary key                |
| patient_id   | INTEGER | ID of the patient          |
| doctor_id    | INTEGER | ID of the doctor           |
| diagnosis    | TEXT    | Patient diagnosis          |
| prescription | TEXT    | Prescribed medicines       |
| notes        | TEXT    | Additional medical notes   |
| record_date  | TEXT    | Date of the medical record |

### Foreign Keys

* patient_id references patients.id
* doctor_id references doctors.id

A patient can have multiple medical records over time.

---

## 8. bills

This table stores billing information for patients.

| Column         | Type    | Description       |
| -------------- | ------- | ----------------- |
| id             | INTEGER | Primary key       |
| patient_id     | INTEGER | ID of the patient |
| amount         | REAL    | Bill amount       |
| payment_status | TEXT    | Payment status    |
| bill_date      | TEXT    | Date of the bill  |

### Foreign Key

* patient_id references patients.id

A patient can have multiple bills.

---

## 9. audit_logs

This table is used to keep a record of important actions performed in the system.

| Column      | Type    | Description                   |
| ----------- | ------- | ----------------------------- |
| id          | INTEGER | Primary key                   |
| user_id     | INTEGER | User who performed the action |
| action      | TEXT    | Action performed              |
| module      | TEXT    | Module where action happened  |
| record_id   | INTEGER | ID of affected record         |
| description | TEXT    | Details of the action         |
| timestamp   | TEXT    | Time of the action            |

### Foreign Key

* user_id references users.id

Examples of actions that can be stored:

* Patient created
* Patient updated
* Patient deleted
* Appointment created
* Medical record updated
* Bill created
* User login

The audit log will be useful for checking what happened when a problem occurs.

---

## 10. Relationships

The main relationships between the tables are:

```text
users
  |
  | 1
  |
  | many
audit_logs


patients
  |
  | 1
  +--------------------+
  |                    |
  | many               | many
  v                    v
appointments       medical_records
  |                    |
  |                    |
  +---- doctor --------+
        |
        v
     doctors


patients
  |
  | 1
  |
  | many
  v
bills
```

More specifically:

* One user can create many audit log entries.
* One patient can have many appointments.
* One doctor can have many appointments.
* One patient can have many medical records.
* One doctor can create many medical records.
* One patient can have many bills.

---

## 11. Primary Keys

Every main table will have an `id` column as its primary key.

Primary keys are used to uniquely identify records.

For example:

```text
patients
id = 1
id = 2
id = 3
```

The patient_code will also be used as a meaningful identifier for patients.

---

## 12. Foreign Keys

Foreign keys are used to connect related tables.

Examples:

```text
appointments.patient_id -> patients.id

appointments.doctor_id -> doctors.id

medical_records.patient_id -> patients.id

medical_records.doctor_id -> doctors.id

bills.patient_id -> patients.id

audit_logs.user_id -> users.id
```

This helps maintain relationships between records and reduces inconsistent data.

---

## 13. Data Validation

The application will perform validation before storing data in the database.

Some examples are:

* Patient name should not be empty.
* Patient age should contain a valid number.
* Phone number should contain valid input.
* Patient code should be unique.
* Doctor code should be unique.
* Required appointment fields should not be empty.
* Bill amount should not be negative.
* Invalid record IDs should not be accepted.

Validation will be handled mainly in the application before database operations.

---

## 14. Duplicate Record Prevention

Duplicate patient records are one of the problems that this project is intended to reduce.

The system will use unique patient codes and validation checks before creating a new patient.

For example, if a patient code already exists, the system should not create another patient using the same code.

This supports the project's TQM goal of preventing record duplication.

---

## 15. Backup and Recovery

The database will be stored as an SQLite database file.

The project will also include a backup mechanism as part of the reliability features.

Before important database operations or at defined backup points, a copy of the database can be stored in the `backups` directory.

If the main database becomes corrupted or an important problem occurs, the backup can be used for recovery.

The exact backup process will be implemented during the development stage.

---

## 16. Audit and Reliability

The database design also supports the assigned quality goal:

**Q01 - Improve Reliability**

The following features are connected to the database design:

* Input Validation
* Audit Log
* Auto Backup
* Error Recovery
* User Roles

The database provides the persistent storage required for these features.

For example, audit logs help identify changes made to records, while backups provide a recovery option if database data is lost or damaged.

---

## 17. Database Storage

The SQLite database file will be stored separately from the application source code.

A possible project structure is:

```text
BBAT104_TQM_AU-24-7632/
|
├── app/
├── backups/
├── database/
│   └── hospital.db
├── docs/
├── logs/
├── sqc/
├── tests/
└── README.md
```

The actual database file will not be committed to GitHub. The database structure and initialization code will be stored in the project instead.

---

## 18. Future Changes

The database design may be modified during development if a requirement is found to be missing.

Any changes should be documented and tested before being used in the final system.

The main goal is to keep the database simple enough for the desktop application while maintaining proper relationships and data integrity.

---

## 19. Summary

The database is designed around the main functions of the Hospital Management System.

The seven main tables are:

* users
* patients
* doctors
* appointments
* medical_records
* bills
* audit_logs

The design supports CRUD operations, user roles, input validation, audit logging, backup and recovery.

It also provides the database foundation needed for the TQM activities and the Q01 reliability requirements of the project.
