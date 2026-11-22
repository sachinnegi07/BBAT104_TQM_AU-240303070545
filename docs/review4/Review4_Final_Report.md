
# Review 4 - Final Quality Improvement Report

## Project Information

Project: Hostel Management System
Subject: Fundamentals of Total Quality Management
Subject Code: BBAT104
Review: 4
Date: 22 November 2026

Technology:
- Python
- CustomTkinter
- SQLite

## 1. Executive Summary

Review 4 focuses on improving the quality and
reliability of the Hostel Management System.

During Review 3, a complaint history retention
risk was identified.

Review 4 addressed this risk through a database
audit-history mechanism.

The improvement was implemented and verified
using automated tests and a real application test.

The review also applies PDCA and descriptive
Statistical Quality Control (SQC) analysis.

## 2. Problem Identified

FMEA Risk ID: F06

Problem:
Complaint History Loss

Original Risk Priority Number (RPN):
196 (preliminary assessment)

The original complaint deletion operation used:

DELETE FROM complaints WHERE id = ?

The inspected database had no complaint deletion
audit table or audit trigger.

Consequently, deleted complaint records were
not preserved by the database design.

## 3. Quality Improvement Objective

Preserve the history of deleted complaints
without changing existing Complaint Management
behaviour.

Expected requirements:

1. Deleted complaints disappear from active lists.
2. Deleted complaint details remain in audit history.
3. Student details are preserved in the snapshot.
4. Failed transactions do not create false audit records.
5. Existing CRUD functions continue to work.

## 4. Improvement Implementation

Modified file:
database.py

New database table:
complaint_delete_audit

New SQLite trigger:
trg_complaint_delete_audit

The trigger runs before complaint deletion.

It creates a historical snapshot containing:

- Complaint ID
- Student ID
- Student code
- Student name
- Complaint title
- Complaint description
- Complaint status
- Complaint creation timestamp
- Deletion timestamp

The active complaint record is then deleted.

The history snapshot is preserved separately.

## 5. PDCA Application

### PLAN

Review 3 identified complaint history loss
as a quality risk.

The objective was to preserve deletion history
without breaking existing application features.

### DO

Implemented an audit table and SQLite trigger.

Created a pre-migration database backup.

Applied the new database objects to the
existing SQLite database.

### CHECK

Verified the implementation using:

- Existing regression testing
- New complaint audit tests
- Database integrity checks
- Manual GUI deletion
- Read-only inspection of saved audit history

### ACT

Integrated the audit mechanism into
database initialization.

Added a dedicated automated test file.

Recommended future monitoring, access control,
retention policies and regular regression testing.

## 6. Automated Test Results

| Test Module | Passed | Failed |
|---|---:|---:|
| Student Management | 7 | 0 |
| Room Management | 9 | 0 |
| Room Allocation | 13 | 0 |
| Complaint Management | 10 | 0 |
| Complaint Audit History | 5 | 0 |
| Total | 44 | 0 |

Observed automated test pass rate:

44 / 44 x 100 = 100%

All 44 automated tests passed during
the reported verification sessions.

This result does not establish a zero
production defect rate.

## 7. New Complaint Audit Tests

The following five tests passed:

1. Service deletion preserves audit history.
2. Missing complaint creates no audit entry.
3. Direct SQL deletion creates audit history.
4. Failed transaction rolls back deletion and audit.
5. Student deletion does not remove the snapshot.

Test file:

test_complaint_audit.py

These tests use temporary databases to
avoid modifying live hostel records.

## 8. Real Application Verification

Test Student:
TEST201 - Rahul Sharma

Complaint Title:
Review4 Audit GUI Test

Complaint ID:
2

Original Complaint Status:
Pending

The complaint was created and deleted
through the Complaint Management GUI.

After deletion:

- The complaint disappeared from the active list.
- An audit record was found in SQLite.
- Student information was preserved.
- Complaint details were preserved.
- Deletion timestamp was recorded.

Database-recorded deletion timestamp:
2026-11-22 07:33:57

Result:
PASS

This was one controlled live-database
verification, not a production sample.

## 9. Statistical Quality Control

The available evidence supports descriptive
quality analysis.

### Observed Results

Automated tests executed: 44
Automated tests passed: 44
Automated tests failed: 0

Test pass rate: 100%

Controlled real-database deletion samples
verified: 1

Audit records confirmed for the sample: 1

### Data Limitations

Production defect frequencies were not collected.

Therefore:

- No production defect rate was estimated.
- No statistical control limits were calculated.
- No defect-frequency Pareto chart was produced.
- No long-term process stability was claimed.

Future repeated observations can support
run charts and appropriate control charts.

## 10. Before and After Comparison

| Quality Indicator | Before | After |
|---|---|---|
| Complaint audit table | Absent | Present |
| Automatic delete trigger | Absent | Present |
| Deleted complaint snapshot | No DB-level retention | Verified preservation |
| Existing regression tests | 39 passed | 39 passed |
| Dedicated audit tests | None | 5 passed |
| Live audit verification | Not available | 1 sample passed |
| Total automated tests | 39 passed | 44 passed |

The additional five tests increased
automated coverage.

The observed evidence supports improved
complaint deletion auditability.

It does not measure a reduction in
production failure frequency.

## 11. Risk Assessment After Improvement

Original FMEA Risk:
F06 - Complaint History Loss

Original RPN:
196

Improvement Status:
Implemented and tested for the verified
deletion scenarios.

Remaining concerns:

- Historical deletions cannot be recovered
  automatically.
- Audit history is not tamper-proof.
- Unauthorized database modifications
  have not been independently tested.
- Long-term retention is not yet measured.
- Audit access controls are not implemented.
- A revised RPN has not been established.

The improvement mitigates the tested
risk but does not eliminate every risk.

## 12. Recommendations

1. Continue running all 44 automated tests
   after important software changes.

2. Maintain regular verified SQLite backups.

3. Restrict unauthorized access to the
   complaint audit history.

4. Define a complaint data retention policy.

5. Consider an authorized audit-history
   viewing feature if required.

6. Collect repeated operational quality data
   to support future statistical monitoring.

7. Reassess FMEA scores after additional
   evidence becomes available.

## 13. Supporting Evidence

Source files:
- database.py
- complaint_service.py
- complaint_ui.py
- test_complaint_service.py
- test_complaint_audit.py

Review documentation:
- docs/review3/FMEA.md
- docs/review3/Risk_Mitigation_Matrix.md
- docs/review3/Review3_Risk_Audit_Report.md
- docs/review4/PDCA_Improvement.md
- docs/review4/SQC_Analysis.md

Additional evidence:
- Automated test execution output
- Database migration verification output
- Complaint GUI verification
- Read-only SQLite audit record verification

## 14. Conclusion

Review 4 implemented a verified quality
improvement in the Hostel Management System.

The complaint deletion process now preserves
an audit snapshot in the tested scenarios.

All 44 automated tests passed, and one
controlled real application deletion was
successfully verified.

PDCA documents the improvement cycle, while
SQC summarizes the available testing evidence.

Further operational monitoring and access
controls are recommended.

## 15. Review Status

Development improvement:
Implemented

Automated verification:
44 tests passed

Real database verification:
Passed for one controlled deletion

PDCA documentation:
Completed

SQC descriptive analysis:
Completed

Final GitHub checkpoint and backup:
Pending

Faculty approval:
Pending
