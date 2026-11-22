
# Review 3 - Critical to Quality (CTQ) Analysis

## Project
Hostel Management System

## Objective

Identify measurable quality requirements for the
Hostel Management System and connect them with
existing software tests and FMEA findings.

## What is CTQ?

Critical to Quality (CTQ) refers to measurable
characteristics that determine whether a product
or process meets user expectations.

In this project, CTQs focus on:
- Data accuracy
- Room allocation correctness
- Student record integrity
- Complaint tracking
- System reliability

## CTQ Matrix

| ID | User Requirement | CTQ Metric | Proposed Target | Verification Method |
|---|---|---|---|---|
| CTQ01 | Accurate student records | Duplicate student IDs accepted | 0 | Duplicate registration test |
| CTQ02 | Safe room allocation | Overcapacity allocations accepted | 0 | Full-room allocation test |
| CTQ03 | One active room per student | Duplicate active allocations accepted | 0 | Duplicate allocation test |
| CTQ04 | Accurate room availability | Availability mismatches in tested workflows | 0 | Compare occupancy and available beds |
| CTQ05 | Reliable room transfer | Invalid state after failed transfers | 0 | Failed transfer preservation test |
| CTQ06 | Valid complaint status | Invalid complaint statuses accepted | 0 | Complaint status validation test |
| CTQ07 | Complaint accountability | Deleted complaints without retained audit evidence | 0 | Complaint retention audit |

These are proposed quality targets, not measured
production performance results.

## CTQ Measurement Definitions

### CTQ01 - Student Record Integrity

Metric:
Number of duplicate student IDs accepted.

Target:
0 accepted duplicate IDs.

Evidence:
Duplicate ID prevention automated test passed.

### CTQ02 - Room Capacity Protection

Metric:
Number of successful allocations exceeding room
capacity.

Target:
0 overcapacity allocations.

Evidence:
Room capacity protection automated test passed.

### CTQ03 - Allocation Uniqueness

Metric:
Number of students with more than one active
room allocation.

Target:
0 duplicate active allocations.

Evidence:
Duplicate allocation prevention test passed.

### CTQ04 - Room Availability Accuracy

Metric:
Number of mismatches between displayed availability
and expected database availability.

Formula:
Available Beds = Room Capacity - Active Occupancy

Target:
0 mismatches in tested workflows.

Evidence:
A101 before allocation: 2 available.
A101 after allocation: 1 available.
A101 after vacating: 2 available.

B201 remained at 2 available beds.

Observed result:
Tested workflow passed.

### CTQ05 - Transfer Reliability

Metric:
Number of failed transfers that leave invalid
allocation records.

Target:
0 inconsistent allocation states.

Evidence:
Failed transfer preservation test passed.

### CTQ06 - Complaint Status Validity

Metric:
Number of invalid complaint statuses accepted.

Target:
0 invalid statuses.

Evidence:
Invalid complaint status test passed.

### CTQ07 - Complaint Auditability

Metric:
Number of complaint deletion operations that lose
the only available complaint record without
retaining a usable audit history.

Target:
0 untracked deletions.

Evidence:
The current service uses SQL DELETE.
No complaint audit table or database trigger
was found in the inspected SQLite database.

Assessment:
Retention control gap identified.

Corrective action:
Consider soft deletion or a complaint audit table.

Implementation:
Not yet completed.

## CTQ Verification Summary

Existing automated tests:
- Student Management: 7 passed
- Room Management: 9 passed
- Room Allocation: 13 passed
- Complaint Management: 10 passed

Total: 39 tests passed.

Additional manual evidence:
- Room allocation updated occupancy correctly.
- Vacating restored room availability correctly.
- Show All refreshed room records.

## Important Limitations

Automated test results establish correctness for
the tested scenarios only.

The proposed zero-defect targets have not been
validated using production failure-rate data.

CTQ07 identifies an unresolved retention risk.

## Conclusion

The Hostel Management System has verified controls
for student validation, room capacity, allocation
uniqueness, transfer protection, and complaint status.

Further improvement is recommended for preserving
complaint deletion history.

CTQ metrics provide a measurable basis for future
quality monitoring and continuous improvement.
