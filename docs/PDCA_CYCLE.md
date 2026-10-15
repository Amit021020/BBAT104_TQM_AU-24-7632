# PDCA Cycle — Hospital Management System

## 1. Objective

The Plan–Do–Check–Act (PDCA) cycle provides a structured method for continuously improving the quality and reliability of the Hospital Management System.

The improvement objectives are to reduce patient waiting times, prevent duplicate patient records, and maintain reliable database operations.

## 2. PLAN — Identify the Improvement

### Problem Statement

Duplicate patient records and inefficient registration workflows are potential sources of data inconsistency and unnecessary delays. Their actual occurrence and impact must be measured before implementing targeted improvements.

### Improvement Goals

1. Validate patient information before saving it.
2. Investigate duplicate patient registration scenarios.
3. measure patient registration completion time.
4. Maintain reliable database operations through backup, error recovery, audit logging, and access control.

### Planned Actions

- Review the patient registration workflow.
- Define tests for duplicate registration attempts.
- Identify suitable patient identifiers for duplicate detection.
- Record registration completion times under defined test conditions.
- Document the baseline results before making changes.

## 3. DO — Implement the Improvement

### Actions

- Execute the existing input-validation tests.
- Test registration attempts using identical patient details.
- Review the database schema for appropriate constraints.
- Evaluate whether the registration service needs duplicate-detection logic.
- Record test observations and any changes made.

### Current Project Evidence

The project has implemented Q01 reliability services for input validation, database backups, audit logging, error recovery, and role-based permissions.

The latest reported test result was 12 passing tests. These results do not, by themselves, establish that duplicate records are prevented or that registration time has improved.

## 4. CHECK — Evaluate the Results

### Measurements

| Metric | Measurement Method | Baseline | Target |
|---|---|---|---|
| Registration time | Measure elapsed time for a defined registration workflow | Not yet measured | Establish a measurable improvement target after baseline testing |
| Duplicate records | Count duplicate records created during controlled registration tests | Not yet measured | Zero duplicates in the defined test scenarios |
| Invalid input handling | Run validation tests using invalid inputs | 12 tests passed overall; individual validation results should be recorded separately | All defined invalid-input tests reject invalid data |
| Error recovery | Execute controlled failure scenarios | Individual baseline not recorded here | All defined recovery tests pass |
| Audit logging | Verify expected audit entries after operations | Individual baseline not recorded here | All defined audit tests pass |

## 5. ACT — Standardize or Revise

### If the Improvement Succeeds

- Keep the verified change in the codebase.
- Add regression tests for the improved behavior.
- Update the user manual and technical documentation.
- Record the final measurements and testing conditions.

### If the Improvement Does Not Succeed

- Investigate the remaining failure.
- Review the proposed root cause.
- Modify the implementation or test approach.
- Repeat the PDCA cycle and compare the new results.

## 6. Evidence and Limitations

The project currently has 12 reported passing tests and implemented Q01 reliability services. Registration-time improvement and duplicate-prevention effectiveness have not been established by those results alone.

Further controlled testing is required to measure the baseline and verify the effectiveness of any additional improvement.

## 7. Conclusion

The PDCA cycle establishes a repeatable process for identifying quality problems, implementing improvements, measuring outcomes, and standardizing successful changes.

By collecting evidence before and after changes, the Hospital Management System can pursue improvements in reliability, patient registration, and data consistency without relying on unsupported assumptions.