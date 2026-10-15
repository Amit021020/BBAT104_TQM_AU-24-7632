# Pareto Analysis — Hospital Management System

## 1. Objective

The objective of Pareto analysis is to identify and prioritize the most frequent confirmed defects in the Hospital Management System.

The analysis supports the Q01 reliability goal and the broader objectives of reducing patient wait times and preventing duplicate patient records.

## 2. Available Test Evidence

- Test Framework: Pytest
- Latest Reported Test Result: 12 tests passed
- Reported Failed Tests: 0
- Verified Defect Categories: Not yet established
- Verified Defect Frequencies: Not yet available
- Analysis Status: Awaiting verified observations

## 3. Defect Frequency Table

| Rank | Defect Category | Frequency | Percentage | Cumulative Percentage |
|---|---|---:|---:|---:|
| — | Verified frequency data not yet available | — | — | — |

A ranked Pareto table and chart cannot be calculated accurately until confirmed defects and their frequencies have been recorded.

## 4. Calculation Method

**Total Defects**

Total defects = Sum of the frequencies of all confirmed defect categories.

**Category Percentage**

Percentage = (Frequency of category / Total defects) × 100

**Cumulative Percentage**

Cumulative percentage = Sum of the current category percentage and all preceding category percentages after sorting categories by frequency in descending order.

## 5. Interpretation

The latest reported test run passed all 12 tests. This demonstrates that the tested cases passed, but it does not establish the overall defect frequency of the application.

Potential failure modes identified during risk analysis must not be counted as actual defects unless testing or other evidence confirms them.

Once verified observations are available, the category with the highest frequency should be investigated first.

## 6. Proposed Improvement Process

1. Collect observations from test execution.
2. Confirm and categorize genuine defects.
3. Count defects in each category.
4. Sort categories from highest to lowest frequency.
5. Calculate percentages and cumulative percentages.
6. Prioritize the most frequent confirmed defect category.
7. Implement a corrective action.
8. Rerun tests and compare the results.

## 7. Limitations

This analysis is provisional because verified defect-frequency data has not yet been established.

No defect counts, percentages, or Pareto rankings have been invented. If no defects are observed in a defined testing scope, report that result separately rather than generating a misleading Pareto chart.

## 8. Conclusion

The current test evidence reports 12 passing tests. Further categorized observations are required to produce a meaningful Pareto analysis and determine which confirmed defect category should receive the highest improvement priority.