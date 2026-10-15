# Defect Log - Hospital Management System

## 1. Purpose

The defect log is used to record defects identified during development and testing of the Hospital Management System.

It helps track the problem, its impact, the cause, the corrective action and the result after retesting.

This document supports the Review 3 requirements of the BBAT104 TQM project.

## 2. Defect Recording Procedure

Whenever a defect is found, the following information should be recorded:

- Defect ID
- Date identified
- Module affected
- Description of the defect
- Steps to reproduce
- Expected result
- Actual result
- Severity
- Status
- Root cause
- Corrective action
- Retest result

A test that correctly rejects invalid input is not a defect. Similarly, an intentionally rejected database operation is not a defect when it behaves as expected.

## 3. Defect Log

| Defect ID | Module | Description | Severity | Status | Corrective Action |
|---|---|---|---|---|---|
| DEF-001 | Q01 Regression Tests | A test assertion depended on the capitalization of a validation error message, causing a test failure even though the validation message used different capitalization. | Low | Fixed and retested | Updated the assertion to compare the message using lowercase text. The regression suite subsequently passed all 12 tests. |

**Note:** DEF-001 records a test-suite issue rather than a confirmed defect in the hospital application's functionality. No additional application defects are claimed here without test evidence.

## 4. Test Findings

The following checks have been discussed or completed during development:

| Test Area | Expected Behavior | Finding |
|---|---|---|
| Patient validation | Invalid patient information should be rejected | Included in Q01 regression tests |
| Bill validation | A negative bill amount should be rejected | Rejection confirmed |
| Role permissions | Operations should follow the configured role permissions | Included in Q01 regression tests |
| Automatic backup | Backup files should be created | Included in Q01 regression tests |
| Audit logging | Expected operations should be recorded | Included in Q01 regression tests |
| Error recovery | Failed database operations should be handled and rolled back where applicable | Included in Q01 regression tests |
| CRUD operations | Create, read, update and delete operations should work correctly | CRUD tests passed during development |

These findings summarize the checks performed so far. Detailed test output should be retained as evidence where available.

## 5. New Defect Entry Template

Use the following template whenever a new defect is identified.

### Defect ID: DEF-XXX

- **Date identified:** YYYY-MM-DD
- **Module:** Name of the affected module
- **Description:** Describe what went wrong.
- **Steps to reproduce:** List the actions needed to reproduce the problem.
- **Expected result:** Describe the correct behavior.
- **Actual result:** Record what happened during testing.
- **Severity:** Low / Medium / High / Critical
- **Root cause:** Record the confirmed cause, or mark it as under investigation.
- **Corrective action:** Describe the fix.
- **Status:** Open / In Progress / Fixed / Closed
- **Retest result:** Pass / Fail / Pending
- **Evidence:** Screenshot, test output or relevant log.

## 6. Defect Severity

| Severity | Meaning |
|---|---|
| Low | Minor issue with limited impact |
| Medium | Affects a function but has a reasonable workaround |
| High | Important functionality is affected or data integrity may be at risk |
| Critical | A major failure involving serious data loss, security or system availability |

Severity should be assigned according to the actual impact of the defect.

## 7. Relationship with TQM

The defect log supports continuous improvement by helping the development team identify recurring problems and verify corrective actions.

The recorded defects can later be grouped by category and frequency for Pareto analysis. Their possible causes can also be investigated using a Fishbone diagram.

The defect log will be updated as additional tests are performed.

## 8. Conclusion

The defect log provides a structured record of issues found during development and testing.

It distinguishes confirmed problems from expected validation failures and potential risks. This helps maintain reliable evidence for the Review 3 evaluation and supports future quality improvement activities.