# SIPOC Analysis - Hospital Management System

## 1. Purpose

SIPOC is a process analysis tool used to identify the Suppliers, Inputs, Process, Outputs and Customers of a system.

For this project, SIPOC is used to understand the main hospital workflow and identify areas where delays, incorrect information and duplicate records may occur.

The assigned TQM goal is to reduce patient wait times and prevent record duplication.

## 2. SIPOC Table

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Patient | Patient details | Receive patient information | Patient record | Patient |
| Receptionist / Staff | Registration details | Validate patient information | Validated patient data | Hospital staff |
| Patient | Appointment request | Check and register appointment | Appointment record | Patient and doctor |
| Doctor | Diagnosis and prescription | Create or update medical record | Medical record | Doctor and patient |
| Hospital staff | Billing information | Create and update bill | Bill and payment status | Patient and accounts staff |
| System administrator | User account details and roles | Manage user access | Authorized user access | Hospital staff |
| Application services | Database operation request | Validate, back up and execute database operation | Operation result and audit entry | Authorized users and administrators |

## 3. Process Steps

The main hospital workflow can be described as follows:

1. Receive patient registration details.
2. Validate the supplied information.
3. Check existing records to help identify possible duplicate patients.
4. Create or update the patient record.
5. Register an appointment with the selected doctor.
6. Store medical records when required.
7. Generate and update billing information.
8. Record important operations in the audit log.

## 4. Possible Quality Problems

The following problems may affect the quality of the hospital workflow:

- Duplicate patient records may cause confusion and inconsistent information.
- Incorrect patient details may lead to errors in hospital records.
- Slow registration and appointment handling may increase patient waiting time.
- Failed database operations may prevent information from being saved correctly.
- Unauthorized changes may affect the reliability of hospital information.
- Missing backups may increase the risk of data loss.

These are potential failure points for analysis. They should not be treated as confirmed defects unless testing or other evidence demonstrates that they occur.

## 5. Relationship with Q01 Reliability

The project also has the assigned Q01 quality goal of improving reliability.

The implemented reliability features support the workflow in the following ways:

| Reliability Feature | Contribution |
|---|---|
| Automatic Backup | Provides database copies for recovery |
| Audit Log | Records important database operations |
| Input Validation | Rejects invalid input before database operations |
| Error Recovery | Handles database failures and performs rollback where possible |
| User Roles | Restricts operations according to permissions |

These features support reliable data handling, but they do not by themselves prove that patient waiting time or duplicate records have been reduced.

## 6. Improvement Opportunities

The SIPOC analysis identifies several areas for further investigation:

1. Measure the time taken to register a patient.
2. Check whether duplicate patient information can be detected before registration.
3. Record validation failures and database errors during testing.
4. Review appointment processing time.
5. Use test results to identify the most important quality problems.

The findings will be used in the CTQ Tree, FMEA and subsequent statistical quality control activities.

## 7. Conclusion

The SIPOC analysis provides a high-level understanding of the Hospital Management System workflow.

It identifies the people providing information, the data used by the system, the major processing steps, the resulting records and the users who depend on them.

This analysis will help identify risks and define measurable quality requirements for the next stages of the TQM project.