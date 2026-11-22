
# Review 4 - Statistical Quality Control (SQC)

## Project Information

Project: Hostel Management System
Subject: Fundamentals of TQM (BBAT104)
Review: 4
Technology: Python, CustomTkinter, SQLite

## 1. Objective

Evaluate observed software quality using actual
test results, quality measurements, and evidence.

Do not confuse test pass rates with production
defect rates.

## 2. What is SQC?

Statistical Quality Control uses statistical
techniques to monitor process performance,
detect quality problems, and support improvement.

For this project, the available data supports
descriptive test-result analysis.

Long-term statistical process control requires
repeated, comparable observations.

## 3. Quality Check Sheet

The check sheet summarizes the verified results
of the automated testing session.

| Module | Tests Executed | Passed | Failed |
|---|---:|---:|---:|
| Student Management | 7 | 7 | 0 |
| Room Management | 9 | 9 | 0 |
| Room Allocation | 13 | 13 | 0 |
| Complaint Management | 10 | 10 | 0 |
| Complaint Audit History | 5 | 5 | 0 |
| Total | 44 | 44 | 0 |

These counts reflect the reported automated
test execution, not production transactions.

## 4. Test Pass Rate

Formula:

Test Pass Rate =
(Passed Tests / Executed Tests) x 100

Calculation:

(44 / 44) x 100 = 100%

Observed Automated Test Pass Rate: 100%

Observed Failed Tests: 0

Interpretation:

All 44 automated test cases passed during
the reported testing session.

This does not guarantee that the system
has no bugs or will never fail.

## 5. Complaint Audit Quality Verification

### Previous System

The original complaint deletion mechanism
removed records from the complaints table.

No database-level deletion audit mechanism
was found during the Review 3 audit.

### Improved System

The following objects were implemented:

- complaint_delete_audit table
- trg_complaint_delete_audit trigger

### Automated Verification

Five audit-specific tests passed:

1. Service deletion preserves history.
2. Missing complaint creates no audit entry.
3. Direct SQL deletion is audited.
4. Failed transactions roll back both operations.
5. Audit snapshots survive student deletion.

### Real Application Verification

One controlled complaint deletion was
verified in the real application.

Complaint ID: 2
Test Student: TEST201
Complaint Title: Review4 Audit GUI Test

Observed result:

- Complaint disappeared from the active GUI list.
- A corresponding audit record existed.
- Student and complaint details were preserved.
- A deletion timestamp was recorded.

Verified live sample: 1 deletion
Audit records confirmed for that sample: 1

This sample is too small to estimate a
reliable long-term audit success rate.

## 6. Before and After Quality Comparison

| Indicator | Before Improvement | After Improvement |
|---|---|---|
| Deletion audit table | Absent | Present |
| Automatic deletion trigger | Absent | Present |
| Audit-specific automated tests | 0 | 5 passed |
| Existing complaint tests | 10 passed | 10 passed |
| Real deletion audit proof | Not available | 1 verified sample |
| Overall automated tests | 39 passed | 44 passed |

The increase in test count reflects additional
test coverage, not a measured reduction in
production failures.

## 7. Defect Analysis Limitations

No production defect-frequency dataset was
collected during this review.

Therefore, a valid defect-frequency Pareto
chart cannot yet be created.

A control chart is also not justified because
repeated, comparable time-based samples
are unavailable.

Inventing defect counts or control limits
would produce misleading conclusions.

## 8. Proposed Future SQC Monitoring

The following metrics can be collected
during actual hostel operations.

### Metric 1: Audit Capture Completeness

Formula:

Deletion Audit Capture Rate =
(Audited Deletions / Completed Deletions) x 100

Proposed Target: 100%

Measurement Frequency: Weekly

Both counts should refer to the same
reporting period and deletion population.

### Metric 2: Room Availability Mismatches

Metric:

Number of verified mismatches between
displayed and expected available beds.

Proposed Target: 0 mismatches

Measurement Frequency: Weekly

### Metric 3: Duplicate Active Allocations

Metric:

Number of students with more than
one active room allocation.

Proposed Target: 0

Measurement Frequency: Weekly

### Metric 4: Automated Regression Pass Rate

Formula:

(Passed Tests / Executed Tests) x 100

Proposed Target: 100% for required tests

Measurement Frequency: After code changes

## 9. Future Statistical Analysis

Once repeated operational observations
are available, the project can use:

- Check sheets to record quality problems.
- Pareto charts to rank actual defect categories.
- Run charts to observe trends over time.
- Suitable control charts when sampling
  assumptions and denominators are satisfied.

No production control limits have been
calculated in this review.

## 10. Findings

1. All 44 automated tests passed.
2. Database audit-history preservation was
   verified through dedicated tests.
3. One real GUI deletion was successfully
   matched with a preserved audit record.
4. Existing complaint CRUD functionality
   continued passing its regression tests.
5. Additional operational data is required
   for meaningful statistical process control.

## 11. Recommendations

- Run regression tests after code changes.
- Monitor complaint deletion audit records.
- Record real operational quality incidents.
- Investigate recurring defects using Pareto
  analysis after sufficient data collection.
- Review quality results periodically.
- Maintain secure database backups.

## 12. Conclusion

Review 4 demonstrated a verified quality
improvement in complaint deletion auditability.

The reported automated testing session achieved
44 passed tests out of 44 executed tests.

A controlled real-world application test
confirmed preservation of a deleted complaint.

The current evidence supports descriptive
quality analysis. Future operational measurements
are required for full statistical process control.
