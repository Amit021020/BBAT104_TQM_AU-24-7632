# Hospital Management System - Architecture

## 1. Overview

The Hospital Management System is a Python based desktop application developed for the BBAT104 TQM project.

The main purpose of the system is to manage basic hospital information such as patients, doctors, appointments, medical records and billing.

The system uses CustomTkinter for the user interface and SQLite for storing the data.

The project also focuses on improving reliability through the Q01 quality goal.

The five reliability features are:

* Automatic Backup
* Audit Log
* Input Validation
* Error Recovery
* User Roles

---

## 2. Technology Used

The main technologies used in this project are:

* Python 3.14.4
* CustomTkinter
* SQLite
* Pandas
* Matplotlib
* Git and GitHub

---

## 3. Basic Architecture

The application follows a simple layered structure.

```text
User
  |
  v
Login Screen
  |
  v
Dashboard
  |
  +-------------------+
  |                   |
  v                   v
Hospital Modules    User Roles
  |
  +---- Patients
  |
  +---- Doctors
  |
  +---- Appointments
  |
  +---- Medical Records
  |
  +---- Billing
  |
  v
Validation
  |
  v
SQLite Database
  |
  +---- Audit Log
  |
  +---- Backup
```

The user interacts with the application through the GUI. The application processes the request, validates the input and then performs the required database operation.

---

## 4. Main Components

### 4.1 User Interface

The GUI will be developed using CustomTkinter.

It will contain the login screen, dashboard and different screens for managing hospital records.

The interface will be kept simple so that users can easily move between the different modules.

---

### 4.2 Authentication

The login system will verify the username and password before allowing access to the application.

After login, the system will identify the user's role.

Different users will have different permissions.

For example:

* Administrator can manage most parts of the system.
* Doctor can access patient and medical record related functions.
* Receptionist can manage patients and appointments.

---

### 4.3 Patient Management

The patient module will be used to manage patient information.

It will support:

* Adding patients
* Viewing patients
* Updating patient information
* Deleting patients

Input validation will be performed before saving the information.

---

### 4.4 Doctor Management

The doctor module will store information about doctors working in the hospital.

It will support the basic CRUD operations:

* Create
* Read
* Update
* Delete

---

### 4.5 Appointment Management

The appointment module will connect patients with doctors.

It will store information such as:

* Patient
* Doctor
* Date
* Time
* Reason
* Appointment status

The system will validate the appointment information before saving it.

---

### 4.6 Medical Records

The medical record module will store information related to a patient's diagnosis and treatment.

Doctors or authorized users will be able to create and update medical records according to their permissions.

---

### 4.7 Billing

The billing module will manage basic billing information for patients.

It will store information such as:

* Patient
* Amount
* Payment status
* Date

---

## 5. Database

SQLite will be used as the database because this is a desktop based academic project and does not require a separate database server.

The database will contain tables for:

```text
Users
Patients
Doctors
Appointments
Medical Records
Bills
Audit Logs
```

The exact fields and relationships between these tables will be finalized during the database design stage.

---

## 6. Reliability Features

Reliability is the main quality goal assigned to this project.

### Automatic Backup

The system will create backups of the SQLite database.

The purpose of the backup is to reduce the risk of losing hospital information if the main database is damaged or deleted.

---

### Audit Log

Important actions performed by users will be recorded.

An audit entry will contain information such as:

```text
User
Action
Module
Date/Time
Result
```

This will make it possible to identify what action was performed and by whom.

---

### Input Validation

The application will validate data before storing it in the database.

Examples include:

* Required fields
* Valid phone numbers
* Valid dates
* Numeric values
* Duplicate records

The main purpose is to prevent incorrect data from entering the system.

---

### Error Recovery

The application will handle expected errors instead of simply closing.

For example, if a database operation fails, the system should show a useful error message and allow the user to continue where possible.

Errors will also be logged for later analysis.

---

### User Roles

The system will use role-based access control.

Users will only be allowed to perform operations that are appropriate for their role.

This reduces the possibility of unauthorized changes to hospital records.

---

## 7. Data Flow

The basic flow of the application is:

```text
User
 |
 v
GUI
 |
 v
Check User Role
 |
 v
Validate Input
 |
 v
Perform Operation
 |
 v
SQLite Database
 |
 +-------> Audit Log
 |
 +-------> Backup
 |
 v
Show Result to User
```

If an error occurs during the operation:

```text
Operation
    |
    v
Error
    |
    v
Error Handler
    |
    +----> Log Error
    |
    +----> Show Error Message
    |
    +----> Recover if possible
```

---

## 8. Reliability Flow

The reliability features are connected to the main application rather than being separate modules.

```text
                 Hospital Management System
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     Validation        User Roles       Error Handling
          |                |                |
          +----------------+----------------+
                           |
                           v
                     SQLite Database
                           |
                    +------+------+
                    |             |
                    v             v
                Audit Log      Backup
```

This structure helps the system prevent errors before they happen and also provides mechanisms to trace and recover from problems when they occur.

---

## 9. TQM Integration

The architecture will also support the TQM activities required for the project.

The system will generate or provide data that can be used for:

* Defect logging
* Checksheets
* FMEA
* Pareto analysis
* Fishbone analysis
* PDCA

The purpose is not only to build the software but also to evaluate its quality and identify areas for improvement.

---

## 10. Future Changes

The architecture may be modified during development if a better structure is required.

For example, additional modules or services may be separated as the application grows.

Any major architecture change will be documented in the project repository.

---

## 11. Summary

The Hospital Management System uses a simple Python desktop architecture with CustomTkinter as the interface and SQLite as the database.

The main focus of the architecture is reliability.

Input validation, user roles, audit logging, automatic backups and error recovery are included around the core hospital management functions.

The architecture is designed to keep the project simple enough for the academic requirements while still demonstrating the TQM principles required by the BBAT104 project.
