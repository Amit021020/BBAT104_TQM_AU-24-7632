# SQC Check Sheet — Hospital Management System

## 1. Purpose

This check sheet records test observations for the Hospital Management System. The collected evidence supports Statistical Quality Control (SQC), defect analysis, and continuous improvement.

The primary quality objective is to improve system reliability, reduce patient wait times, and prevent duplicate patient records.

## 2. Test Information

- Test Date: 15 October 2026
- Tester: Amit Suyal
- Test Environment: Local development environment on Ubuntu
- Programming Language: Python 3.14.4
- Test Framework: Pytest
- Latest Reported Test Result: 12 tests passed

## 3. Observation Check Sheet

| Observation ID | Test Area | Check Performed | Expected Result | Observed Result | Status |
|---|---|---|---|---|---|
| OBS-001 | Input Validation | Validate input data | Invalid input should be rejected | Validation checks passed; invalid input was handled as expected | Pass |
| OBS-002 | User Roles | Check permissions | Unauthorized operations should be denied | Role-based permission checks passed | Pass |
| OBS-003 | Database Backup | Create a backup | A backup file should be created | Backup checks passed; backup creation worked as expected | Pass |
| OBS-004 | Error Recovery | Handle a failed operation | Failure should be handled safely | Error recovery checks passed; failed operations were handled as expected | Pass |
| OBS-005 | Audit Logging | Record an operation | An appropriate audit entry should be created | Audit logging checks passed; expected audit entries were recorded | Pass |

## 4. Test Summary

- Observations completed: 5
- Observations passed: 5
- Observations failed: 0
- Observation pass rate: 100%
- Confirmed application defects from these five checks: 0 observed

## 5. Quality-Control Procedure

1. Execute the test suite.
2. Record the expected and actual results for each test.
3. Investigate every failed test.
4. Categorize confirmed defects by type.
5. Record corrective actions and rerun relevant tests.

## 6. Conclusion

The latest reported test run completed with 12 passing tests. Individual test observations and verified defect frequencies must be collected before drawing conclusions about specific quality problems.

This check sheet provides the foundation for Pareto analysis and further quality improvement.