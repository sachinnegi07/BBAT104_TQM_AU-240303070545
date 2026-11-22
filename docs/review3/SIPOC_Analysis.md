
# Review 3 - SIPOC Analysis

## Project
Hostel Management System

## Objective
Analyze the Room Allocation process using the
SIPOC model to identify process inputs, outputs,
participants, and quality requirements.

## SIPOC Table - Room Allocation

| Supplier | Input | Process | Output | Customer |
|---|---|---|---|---|
| Hostel Administrator | Student ID and room selection | Validate student and room | Validation result | Administrator |
| Student Management Module | Registered student record | Check student eligibility | Valid student confirmation | Allocation Module |
| Room Management Module | Room capacity and occupancy | Check bed availability | Availability result | Allocation Module |
| Allocation Module | Valid student and available room | Create allocation record | Confirmed room allocation | Student and Administrator |
| Allocation Database | Existing allocation records | Prevent duplicate active allocation | Consistent allocation history | Administrator |

The roles above represent the proposed system workflow.

## Process Boundaries

Start:
Administrator selects a registered student and room.

End:
The system confirms or rejects the allocation request.

## Process Steps

1. Select a registered student.
2. Select a hostel room.
3. Check whether the student already has an active allocation.
4. Verify that the room has available capacity.
5. Create the allocation when validation succeeds.
6. Update the displayed allocation and occupancy information.
7. Show a success message or appropriate validation error.

## Critical Process Requirements

- Student must exist in the database.
- Room must exist in the database.
- Room occupancy must not exceed capacity.
- Duplicate active allocations must be prevented.
- Failed operations must not create invalid allocations.
- Displayed availability should reflect current records.

## Existing Verification Evidence

The Room Allocation backend passed 13 automated tests.

Relevant tests include:

- Allocate Room
- Room Occupancy Tracking
- Duplicate Allocation Prevention
- Room Capacity Protection
- Failed Transfer Preserves Allocation
- Vacate Room
- Availability After Transfer

## Review 3 Observations

F05 - Room Availability:
The tested allocation and vacate workflow updated
room availability correctly.

F06 - Complaint History Loss:
A separate complaint retention risk was identified.
It is outside this Room Allocation SIPOC process.

## Conclusion

SIPOC provides a clear view of the participants,
inputs, steps, outputs, and customers involved in
room allocation.

It helps identify where quality controls should
be applied before an allocation is confirmed.
