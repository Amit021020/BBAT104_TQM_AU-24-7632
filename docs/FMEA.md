# FMEA - Hospital Management System

## 1. Purpose

Failure Mode and Effects Analysis (FMEA) is a quality management technique used to identify possible failures, understand their effects and prioritize corrective actions.

For this project, FMEA is used to analyze risks in the Hospital Management System, with particular attention to data reliability, patient registration, appointment management and the assigned Q01 reliability features.

The analysis supports the TQM goal of reducing patient waiting time and preventing record duplication.

## 2. Scoring Method

Each potential failure is evaluated using three factors.

- **Severity (S):** The seriousness of the effect if the failure occurs.
- **Occurrence (O):** The estimated likelihood that the failure will occur.
- **Detection (D):** The estimated difficulty of detecting the failure before it affects the system.

Each factor is scored from 1 to 10. A higher Detection score means the failure is more difficult to detect.

The Risk Priority Number is calculated as:

**RPN = Severity × Occurrence × Detection**

The maximum possible RPN is 1,000.

The scores in this initial analysis are engineering estimates for academic risk assessment. They are not based on production incident data.

## 3. FMEA Matrix

| No. | Process / Component | Potential Failure Mode | Potential Effect | Possible Cause | S | O | D | RPN | Recommended Action |
|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | Patient Management | Duplicate patient record created | Conflicting or repeated patient information | No effective duplicate check | 7 | 5 | 6 | 210 | Add duplicate detection using an appropriate patient identifier and test repeated registration |
| 2 | Input Validation | Invalid patient or billing data accepted | Incorrect or inconsistent records | Validation missing or bypassed | 7 | 4 | 4 | 112 | Validate all inputs before database writes and test invalid cases |
| 3 | Automatic Backup | Database backup fails | Recovery copy may be unavailable | File permission, disk space or file operation error | 9 | 3 | 6 | 162 | Handle backup errors and verify that the backup file can be opened |
| 4 | Error Recovery | Failed database operation leaves unintended changes | Inconsistent data | Transaction handling or rollback failure | 9 | 3 | 6 | 162 | Test transaction rollback using simulated database failures |
| 5 | User Roles | Unauthorized operation is allowed | Records may be changed by an unapproved user | Incorrect permission mapping or missing permission check | 9 | 3 | 5 | 135 | Test every protected operation against the defined roles |
| 6 | Audit Logging | Important operation is not recorded | Reduced traceability during investigation | Audit function fails or is not called | 6 | 4 | 6 | 144 | Test successful and failed operations and verify expected audit entries |
| 7 | Appointment Management | Appointment references an invalid patient or doctor | Appointment cannot be associated correctly | Invalid identifier or missing integrity check | 7 | 3 | 3 | 63 | Retain foreign key enforcement and test invalid references |
| 8 | Patient Registration | Registration takes too long | Increased patient waiting time | Slow workflow or unnecessary repeated steps | 6 | 5 | 5 | 150 | Measure registration time and investigate avoidable steps |

## 4. RPN Calculation Examples

### Example 1: Duplicate Patient Record

Severity = 7

Occurrence = 5

Detection = 6

RPN = 7 × 5 × 6 = **210**

This failure receives a relatively high initial score because duplicate records may cause confusion and inconsistent patient information.

### Example 2: Backup Failure

Severity = 9

Occurrence = 3

Detection = 6

RPN = 9 × 3 × 6 = **162**

A backup failure may prevent recovery from data loss. The recommended action is to verify backup creation and test whether the resulting database copy is usable.

### Example 3: Invalid Appointment Reference

Severity = 7

Occurrence = 3

Detection = 3

RPN = 7 × 3 × 3 = **63**

The current SQLite database enables foreign key enforcement. This helps prevent appointments from referencing nonexistent patients or doctors. The behavior should still be verified through tests.

## 5. Risk Prioritization

Based on the initial estimated RPN values, the risks can be ordered as follows:

| Priority Order | Failure Mode | Initial RPN |
|---:|---|---:|
| 1 | Duplicate patient record | 210 |
| 2 | Backup failure | 162 |
| 3 | Database rollback failure | 162 |
| 4 | Slow patient registration | 150 |
| 5 | Missing audit entry | 144 |
| 6 | Unauthorized operation | 135 |
| 7 | Invalid data accepted | 112 |
| 8 | Invalid appointment reference | 63 |

These scores are an initial prioritization aid, not proof that one failure is actually more frequent than another. The scoring assumptions should be reviewed against test evidence.

## 6. Corrective and Preventive Actions

The following actions are recommended:

1. Implement and test duplicate patient detection.
2. Test whether backups are created correctly and can be restored.
3. Simulate database failures and verify rollback behavior.
4. Test role permissions for Admin, Doctor and Staff.
5. Verify audit records after successful and failed operations.
6. Test invalid appointment references.
7. Measure patient registration time using a consistent procedure.
8. Record all observed failures in the defect log.

## 7. Reassessment

After corrective actions are implemented, Severity, Occurrence and Detection should be reassessed where justified.

The revised RPN must be calculated from the new scores:

**Revised RPN = Revised S × Revised O × Revised D**

The revised values must not be entered until the corrective actions have been tested and evidence has been collected.

| Failure Mode | Initial RPN | Corrective Action Completed? | Test Evidence | Revised RPN |
|---|---:|---|---|---|
| Duplicate patient record | 210 | Pending verification | To be recorded | Pending |
| Backup failure | 162 | Pending verification | To be recorded | Pending |
| Database rollback failure | 162 | Pending verification | To be recorded | Pending |
| Slow patient registration | 150 | Pending measurement | To be recorded | Pending |
| Missing audit entry | 144 | Pending verification | To be recorded | Pending |
| Unauthorized operation | 135 | Pending verification | To be recorded | Pending |
| Invalid data accepted | 112 | Pending verification | To be recorded | Pending |
| Invalid appointment reference | 63 | Pending verification | To be recorded | Pending |

## 8. Conclusion

The FMEA identifies possible failures that could affect the reliability and quality of the Hospital Management System.

Duplicate patient records, backup failures and database rollback failures are among the risks selected for further investigation based on the initial scoring.

The recommended actions will be checked through testing. The results will support the defect log and subsequent statistical quality control activities.

This analysis supports the project's TQM approach by identifying risks early, prioritizing improvements and using evidence to evaluate the results.