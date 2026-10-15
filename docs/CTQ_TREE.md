# CTQ Tree - Hospital Management System

## 1. Purpose

A Critical to Quality (CTQ) Tree converts customer needs into measurable quality requirements.

For this project, the main TQM goal is to reduce patient waiting time and prevent record duplication.

The CTQ Tree identifies the important requirements that the Hospital Management System should satisfy and explains how they can be measured during testing.

## 2. Customer Needs

The main customer needs identified for the system are:

1. Patients should be registered without unnecessary delays.
2. Patient information should be accurate and consistent.
3. Duplicate patient records should be prevented.
4. Appointments should be recorded correctly.
5. Hospital data should remain reliable when database operations fail.
6. Only authorized users should perform restricted operations.

## 3. CTQ Tree

| Customer Need | Quality Driver | Critical to Quality Requirement |
|---|---|---|
| Faster patient registration | Efficient registration process | Measure the time required to complete patient registration |
| Accurate patient information | Input validation | Invalid patient data must be rejected |
| No duplicate patient records | Duplicate detection | Existing patient records must be checked before creating a duplicate |
| Correct appointment handling | Data integrity | Appointments must reference valid patients and doctors |
| Reliable database operations | Error recovery | Failed database operations must be handled without unintended partial changes |
| Protection of hospital records | Role-based permissions | Unauthorized operations must be rejected |
| Reduced risk of data loss | Automatic backup | A database backup must be created successfully before a protected write operation |
| Traceability of operations | Audit logging | Successful and failed operations should be recorded where supported by the operation flow |

## 4. Measurement Plan

The following measures can be used during testing.

| CTQ Measure | Measurement Method | Proposed Test Target |
|---|---|---|
| Patient registration time | Record the time from submitting the registration form to receiving the result | Establish a baseline, then reduce the average time |
| Invalid input rejection rate | Compare invalid-input test cases rejected against all invalid-input test cases | 100% of defined invalid-input test cases rejected |
| Duplicate patient creation | Attempt to register the same test patient more than once | Zero duplicate records in the defined test cases |
| Appointment data integrity | Attempt to create appointments using valid and invalid patient or doctor IDs | All invalid foreign-key references rejected |
| Database error recovery | Simulate a database operation failure and inspect the result | Failed operation handled and rollback verified where applicable |
| Unauthorized operation rejection | Test operations using roles without the required permission | 100% of defined unauthorized-operation test cases rejected |
| Backup creation | Execute a protected write operation and check the backup directory | A valid backup exists before the operation proceeds |
| Audit logging | Perform successful and failed test operations and inspect audit entries | Expected audit entries are present |

The targets above are proposed project-level test criteria, not measured results. They must be verified through actual testing.

## 5. Relationship with the Q01 Reliability Goal

The assigned Q01 goal is to improve reliability.

The following existing services support the CTQ requirements:

- `validation_service.py` checks input data.
- `role_service.py` checks user permissions.
- `backup_service.py` creates and manages database backups.
- `error_recovery_service.py` handles database errors and rollback.
- `audit_service.py` records important operations.
- `reliable_operation_service.py` integrates these features into the operation flow.

These services support data reliability and controlled database operations. Patient registration time and duplicate prevention require separate measurement and verification.

## 6. Verification Plan

The CTQ requirements will be checked using automated tests and, when the GUI is available, practical workflow testing.

The verification process will include:

1. Measure registration time using a consistent test procedure.
2. Test repeated patient registration to identify duplicate records.
3. Submit invalid patient and appointment data.
4. Test database operations with valid and invalid references.
5. Simulate database errors and verify recovery behavior.
6. Attempt restricted operations using different user roles.
7. Inspect backup files and audit log entries.

The results will be recorded as test evidence. Any failures will be added to the defect log and considered during FMEA.

## 7. Conclusion

The CTQ Tree converts the hospital's quality goals into requirements that can be measured and tested.

It provides a basis for risk analysis, defect logging and future statistical quality control activities.

The next stage is to use these requirements to identify possible failures and calculate their Risk Priority Numbers in the FMEA.