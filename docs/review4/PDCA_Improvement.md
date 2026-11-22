
# Review 4 - PDCA Quality Improvement

## Project Information

Project: Hostel Management System
Subject: Fundamentals of TQM (BBAT104)
Review: 4

## Improvement Objective

Reduce the risk of complaint history loss during
deletion while preserving existing CRUD behaviour.

## PLAN - Identify the Quality Problem

### Problem

The original complaint deletion function used:

DELETE FROM complaints WHERE id = ?

No separate complaint audit table or database
trigger existed in the inspected database.

### Risk Reference

FMEA Risk ID: F06
Failure Mode: Complaint History Loss
Original RPN: 196 (preliminary estimate)

### Improvement Target

Preserve deleted complaint details without
changing the existing active complaint list.

## DO - Implement the Improvement

### Implementation

Modified File:
database.py

New SQLite Table:
complaint_delete_audit

New SQLite Trigger:
trg_complaint_delete_audit

### Working Principle

1. Administrator deletes a complaint.
2. SQLite BEFORE DELETE trigger executes.
3. A snapshot is inserted into the audit table.
4. The original complaint is deleted.
5. Active complaint lists remain unchanged.

### Preserved Data

- Original complaint ID
- Student ID
- Student code
- Student name
- Complaint title
- Complaint description
- Complaint status
- Original creation timestamp
- Deletion timestamp

### Safety Measures

- Pre-migration database backup created.
- Existing complaint service preserved.
- Existing complaint UI preserved.
- New audit table and trigger created.
- Migration verified using integrity checks.

## CHECK - Verify the Improvement

### Existing Automated Tests

Student Management: 7 passed
Room Management: 9 passed
Room Allocation: 13 passed
Complaint Management: 10 passed

Existing regression total: 39 passed

### New Audit Tests

1. Service deletion preserves audit history.
2. Missing complaint produces no audit entry.
3. Direct SQL deletion is audited.
4. Failed transaction rolls back deletion and audit.
5. Audit snapshot survives student deletion.

New audit tests: 5 passed

Total automated tests: 44 passed

### Real Database Verification

Test Student:
TEST201 - Rahul Sharma

Deleted Complaint:
Review4 Audit GUI Test

Complaint ID:
2

Verification Result:
- Complaint removed from active GUI list.
- Complaint snapshot found in audit table.
- Student details preserved.
- Complaint status preserved.
- Deletion timestamp recorded.

Result: PASS

### Outcome

The previous database design lacked complaint
deletion audit preservation.

The updated design preserved the deletion
history in automated tests and a real GUI test.

This is verified improvement evidence,
not a measured production defect reduction.

## ACT - Standardize the Improvement

### Completed

- New audit table integrated into database setup.
- Audit trigger integrated into database setup.
- Dedicated regression test file added:
  test_complaint_audit.py

### Recommended Future Controls

- Include all 44 tests in future regression runs.
- Back up the audit table with the SQLite database.
- Restrict unauthorized database modifications.
- Define complaint retention and access policies.
- Add authorized audit-history viewing if required.
- Recheck audit behaviour after future schema changes.

### Current Limitations

- Previously deleted complaints were not recovered.
- Long-term data retention has not been verified.
- Audit-table access control has not been assessed.
- The original FMEA RPN has not been recalculated.
- Production complaint deletion rates are unavailable.

## Before and After Comparison

| Quality Characteristic | Before | After |
|---|---|---|
| Audit table | Absent | Present |
| Delete trigger | Absent | Present |
| Deleted complaint snapshot | Not preserved by DB design | Preserved in tests |
| Existing complaint tests | 10 passed | 10 passed |
| Dedicated audit tests | Not available | 5 passed |
| Real GUI audit verification | Not available | Passed |

## Conclusion

The PDCA cycle produced a verified improvement
in complaint deletion auditability.

The implemented database mechanism preserves
historical complaint snapshots while maintaining
the tested existing application functionality.

Further improvements should focus on audit
access control, retention and monitoring.
