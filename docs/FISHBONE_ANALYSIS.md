# Fishbone Analysis — Hospital Management System

## 1. Objective

The Fishbone Diagram, also known as an Ishikawa Diagram, is used to identify and organize potential causes of quality problems.

This analysis focuses on two quality objectives:

1. Reduce patient waiting times.
2. Prevent duplicate patient records.

The causes listed below are hypotheses for investigation, not confirmed defects.

## 2. Problem Statement A: Increased Patient Waiting Time

### Potential Causes

| Category | Potential Cause | Proposed Verification |
|---|---|---|
| People | Staff enter patient information slowly | Measure registration completion time |
| Methods | Patient registration and appointment workflows require unnecessary steps | Review the workflow and count steps |
| Technology | Slow database queries or repeated database operations | Measure query execution time |
| Data | Incomplete patient information requires correction | Review validation failures and incomplete submissions |
| Measurement | Registration and waiting times are not consistently recorded | Introduce a timestamp-based measurement process |
| Environment | Multiple patients require service at the same time | Compare waiting times across different workloads |

## 3. Problem Statement B: Duplicate Patient Records

### Potential Causes

| Category | Potential Cause | Proposed Verification |
|---|---|---|
| People | Staff enter an existing patient again | Test registration with an existing patient's details |
| Methods | Patient registration does not include a duplicate-checking step | Review the registration workflow |
| Technology | Duplicate-check logic may not handle simultaneous requests | Test concurrent registration attempts |
| Data | Variations in names, phone numbers, or formatting may bypass matching | Test records with different capitalization and spacing |
| Database | No suitable uniqueness constraint exists for the selected identifier | Inspect database schema and constraints |
| Measurement | Duplicate records are not routinely counted | Create a periodic duplicate-record audit |

## 4. Relationship to Q01 Reliability

The assigned Q01 quality goal is to improve reliability through backup, audit logging, input validation, error recovery, and user roles.

These features support reliable operation, but they do not automatically guarantee reduced waiting times or prevent duplicate records. Those outcomes require their own workflow checks, measurements, and corrective actions.

## 5. Root-Cause Investigation Plan

1. Select one potential cause from the tables.
2. Reproduce the scenario under controlled conditions.
3. Record the expected and actual behavior.
4. Collect evidence such as execution time, duplicate counts, or validation results.
5. Confirm whether the suspected cause is supported by evidence.
6. Propose and implement an appropriate corrective action.
7. Repeat the test to evaluate the improvement.

## 6. Conclusion

The Fishbone analysis organizes possible causes of patient waiting time and duplicate patient records into people, methods, technology, data, measurement, environment, and database-related categories.

The listed causes must be verified before they are treated as actual root causes. This approach supports evidence-based quality improvement in the Hospital Management System.