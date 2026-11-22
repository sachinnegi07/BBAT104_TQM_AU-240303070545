
# Review 3 - Risk Audit and Quality Analysis Report

## Project Information

Project: Hostel Management System
Subject: Fundamentals of Total Quality Management (BBAT104)
Review: 3
Technology: Python, CustomTkinter, SQLite

## 1. Executive Summary

Review 3 evaluates the quality and reliability of
the Hostel Management System using TQM methods.

The analysis includes:

- Failure Mode and Effects Analysis (FMEA)
- Risk Priority Number (RPN)
- Risk Mitigation Matrix
- Risk Verification
- SIPOC Process Analysis
- Critical to Quality (CTQ) Analysis

The application previously passed 39 automated
backend tests across four management modules.

Two priority risks were investigated in detail.

F06: Complaint history retention gap identified.
F05: Room availability update workflow passed.

## 2. Audit Objectives

1. Identify possible system failure modes.
2. Assess risk using S, O, and D scores.
3. Prioritize failures using RPN.
4. Evaluate existing preventive controls.
5. Verify important risks through actual testing.
6. Recommend corrective actions.
7. Define measurable quality requirements.

## 3. FMEA Risk Assessment

RPN = Severity x Occurrence x Detection

| Rank | ID | Failure Mode | RPN |
|---|---|---|---:|
| 1 | F06 | Permanent complaint deletion | 196 |
| 2 | F05 | Stale room availability | 120 |
| 3 | F03 | Duplicate active allocation | 96 |
| 4 | F04 | Partial room transfer | 80 |
| 5 | F02 | Room overcapacity | 72 |
| 6 | F01 | Duplicate student registration | 54 |

The original RPN values are preliminary estimates.
They do not represent measured failure frequencies.

## 4. Automated Test Results

| Module | Tests Passed |
|---|---:|
| Student Management | 7 |
| Room Management | 9 |
| Room Allocation | 13 |
| Complaint Management | 10 |
| Total | 39 |

All 39 tests passed during the Review 2
regression testing session.

Relevant controls tested include:

- Duplicate student ID prevention
- Room capacity validation
- Duplicate active allocation prevention
- Failed transfer preservation
- Vacate and occupancy updates
- Complaint status validation

These results apply to the tested scenarios.

## 5. Verified Finding - F06

Risk: Loss of complaint history after deletion.

### Technical Evidence

File: complaint_service.py

The delete_complaint function executes:

DELETE FROM complaints WHERE id = ?

A read-only SQLite schema inspection found:

- allocations
- complaints
- rooms
- students
- sqlite_sequence

No separate complaint audit table or database
trigger was found.

### Audit Conclusion

The inspected database design does not provide
database-level preservation of deleted complaints.

This creates a confirmed data-retention risk.

External logging mechanisms were not verified.

### Recommended Action

Introduce soft deletion or a dedicated complaint
audit-history table.

### Implementation Status

Not implemented.

### Risk Status

Open - corrective action recommended.

## 6. Verified Finding - F05

Risk: Room availability displayed incorrectly
after allocation or vacating.

### Test Environment

Test Student: TEST201 - Rahul Sharma

Rooms:
- A101: Capacity 2
- B201: Capacity 2

### Actual Test Results

| Stage | A101 Occupied | A101 Available |
|---|---:|---:|
| Before allocation | 0 | 2 |
| After allocation | 1 | 1 |
| After vacating | 0 | 2 |

Room B201 remained:
- Occupied: 0
- Available: 2

After allocation and vacating, the Rooms screen
displayed the expected occupancy and availability.

The active allocation count returned to zero
after vacating the test student.

### Audit Conclusion

The tested workflow passed.

No stale availability issue was reproduced during
the observed allocation, navigation, refresh,
and vacate operations.

### Residual Risk

Other scenarios, including concurrent database
changes and long-running screens, were not tested.

### Implementation Status

Existing controls worked in the tested scenario.
No code correction was required.

## 7. SIPOC Analysis

The Room Allocation process was examined using:

S - Suppliers
I - Inputs
P - Process
O - Outputs
C - Customers

The process includes:

1. Student and room selection
2. Student validation
3. Duplicate allocation checking
4. Room capacity checking
5. Allocation creation
6. Occupancy display update

Detailed analysis:
SIPOC_Analysis.md

## 8. CTQ Analysis

The following quality characteristics were
identified:

- Student record integrity
- Room capacity protection
- Allocation uniqueness
- Room availability accuracy
- Transfer reliability
- Complaint status validity
- Complaint auditability

Targets and verification methods are documented
in CTQ_Analysis.md.

The proposed zero-defect targets are quality
objectives, not measured production results.

## 9. Corrective Action Recommendations

Priority 1:
Preserve deleted complaint history using soft
deletion or an audit mechanism.

Priority 2:
Continue verifying availability consistency
after allocation, transfer, and vacate.

Priority 3:
Maintain existing validation and regression tests.

Priority 4:
Consider adding automated tests for additional
edge cases and database consistency.

## 10. Limitations

- RPN scores are preliminary estimates.
- Production defect rates were not measured.
- F06 corrective action remains unimplemented.
- F05 passed only the observed test workflow.
- Manual test screenshots were reviewed during
  development but have not yet been archived
  in the project documentation.

## 11. Overall Conclusion

The Hostel Management System demonstrated
working controls for student records,
room capacity, allocations, and complaints.

All 39 automated backend tests passed.

The room availability workflow behaved correctly
during the observed allocation and vacate tests.

A complaint history retention weakness was
identified and documented for future correction.

The audit establishes a basis for further
quality improvement and risk monitoring.

## 12. Supporting Documents

- FMEA.md
- Risk_Mitigation_Matrix.md
- SIPOC_Analysis.md
- CTQ_Analysis.md
- test_student_service.py
- test_room_service.py
- test_allocation_service.py
- test_complaint_service.py

## 13. Review Status

Risk analysis: Documented
Automated test evidence: Available
F05 manual verification: Completed
F06 corrective action: Pending
Final review approval: Pending faculty evaluation
