
# Review 3 - Risk Mitigation Matrix

## Project
Hostel Management System

## Objective
Document the causes, effects, existing controls,
recommended actions, and verification methods
for risks identified during FMEA.

## Risk Mitigation Matrix

| ID | Failure Mode | RPN | Possible Cause | Existing Control | Recommended Action | Verification |
|---|---|---:|---|---|---|---|
| F06 | Permanent complaint deletion | 196 | Records are permanently removed | Complaint delete operation works | Introduce soft deletion or audit history | Verify deleted complaints remain accessible to authorized auditors |
| F05 | Stale room availability | 120 | UI may retain outdated values | Refresh functionality exists | Ensure availability refreshes after room and allocation changes | Compare displayed beds with database records |
| F03 | Duplicate active allocation | 96 | Repeated allocation attempts | Duplicate allocation validation | Maintain validation and consider database-level protection | Attempt duplicate allocation and verify rejection |
| F04 | Partial room transfer | 80 | Transfer operation interrupted | Failed-transfer protection tested | Preserve transactional behavior and add interruption tests | Confirm failed transfer leaves original allocation intact |
| F02 | Room overcapacity | 72 | Beds allocated beyond capacity | Capacity validation | Retain checks and test boundary conditions | Attempt allocation to a full room |
| F01 | Duplicate student registration | 54 | Same student ID submitted again | Duplicate ID validation | Maintain unique IDs and provide clear error feedback | Attempt registration with an existing ID |

## Existing Test Evidence

### Student Management
7 tests passed, including duplicate student prevention.

### Room Management
9 tests passed, including room capacity validation.

### Room Allocation
13 tests passed, including:
- Duplicate allocation prevention
- Room capacity protection
- Failed transfer preservation
- Double vacate protection

### Complaint Management
10 tests passed, including:
- Complaint validation
- Status validation
- Complaint deletion

Total: 39 automated backend tests passed.

## Risk Treatment Status

### Controls Already Tested
- F01: Duplicate student prevention
- F02: Room capacity protection
- F03: Duplicate active allocation prevention
- F04: Failed-transfer protection

### Further Verification Required
- F05: UI availability consistency after updates

### Improvement Proposed
- F06: Complaint deletion audit history

## Responsibilities

- Developer: Implement safeguards and run tests.
- Hostel Administrator: Validate operational workflows.
- Reviewer: Review evidence and assess remaining risks.

These are proposed responsibility roles,
not confirmed individual assignments.

## Important Limitations

RPN scores are preliminary estimates, not
measured failure frequencies.

Passing automated tests verifies the tested
conditions only. It does not prove that every
possible failure has been eliminated.

Recommended actions are not considered
implemented until their behavior is verified.

## Conclusion

The system already contains important validation
controls for students, rooms, and allocations.

Priority should now focus on verifying room
availability consistency and protecting
historical complaint records.

Further validation will determine whether
additional implementation changes are required.


## F06 - Verified Risk Audit Finding

### Risk
Permanent Complaint History Loss

### Original RPN
196 (Preliminary Estimate)

### Evidence Collected

1. complaint_service.py uses:
   DELETE FROM complaints WHERE id = ?

2. SQLite database inspection found:
   - allocations
   - complaints
   - rooms
   - students
   - sqlite_sequence (internal SQLite table)

3. No database triggers were found.

4. No separate complaint audit/history table was found.

### Audit Conclusion

F06 is confirmed as a data-retention risk in the
current SQLite database design.

The complaint deletion operation removes records
from the complaints table without a database-level
history preservation mechanism.

External logging has not been verified.

### Recommended Corrective Action

Introduce soft deletion or a dedicated audit table
to preserve historical complaint records.

### Implementation Status

Recommendation documented.
Corrective action not yet implemented.

### Verification Required After Implementation

- Delete a test complaint.
- Confirm it disappears from the active complaint list.
- Confirm authorized audit access can retrieve its history.
- Confirm existing complaint CRUD tests still pass.


## F05 - Verified Room Availability Audit

### Risk
Stale Room Availability Display

### Original RPN
120 (Preliminary Estimate)

### Evidence Collected

1. Room Management uses get_rooms() to reload records.
2. Show All displays the latest room data.
3. Initial database and UI values matched.

### Allocation Verification

Test Student: TEST201 - Rahul Sharma
Test Room: A101

Before Allocation:
- Capacity: 2
- Occupied: 0
- Available: 2

After Allocation:
- Capacity: 2
- Occupied: 1
- Available: 1

After Vacating:
- Capacity: 2
- Occupied: 0
- Available: 2

Room B201 remained unchanged.

### Audit Conclusion

All observed availability values matched the
expected results during the tested workflow.

The stale availability failure was not reproduced
during allocation, navigation, refresh, and vacate.

### Existing Controls Verified

- Room availability calculation
- Room list reloading through Show All
- Allocation occupancy updates
- Vacate occupancy restoration

### Implementation Status

Existing controls passed the tested scenarios.
No corrective code change required at this stage.

### Residual Risk

Other refresh scenarios, including concurrent
changes and long-running screens, have not
been fully tested.

The original RPN remains a preliminary estimate
until risk scores are formally reassessed.
