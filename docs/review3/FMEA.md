
# Review 3 - Failure Mode and Effects Analysis (FMEA)

## Project
Hostel Management System

## Objective
Identify potential system failures, assess their risks,
and recommend preventive or corrective actions.

## FMEA Scoring Method

Severity (S): 1 = Minor impact, 10 = Critical impact

Occurrence (O): 1 = Unlikely, 10 = Very frequent

Detection (D): 1 = Easily detected, 10 = Difficult to detect

Risk Priority Number (RPN) = S × O × D

Note: Initial scores are preliminary risk estimates.
They are not measured failure frequencies.

## Initial Risk Register

| ID | Potential Failure | Effect | S | O | D | RPN |
|---|---|---|---|---|---|---|
| F01 | Duplicate student registration | Incorrect student records | 6 | 3 | 3 | 54 |
| F02 | Room overcapacity | More students than available beds | 8 | 3 | 3 | 72 |
| F03 | Duplicate active allocation | One student assigned multiple rooms | 8 | 3 | 4 | 96 |
| F04 | Partial room transfer | Inconsistent allocation records | 8 | 2 | 5 | 80 |
| F05 | Stale room availability displayed | Incorrect information to administrator | 6 | 4 | 5 | 120 |
| F06 | Permanent complaint deletion | Loss of complaint history | 7 | 4 | 7 | 196 |

## Existing Quality Controls

- Student ID duplicate prevention
- Room capacity validation
- Duplicate active allocation prevention
- Database transactions for room transfer
- Refresh functionality for room availability
- Complaint validation and status tracking

## Test Evidence

- Student Management: 7 tests passed
- Room Management: 9 tests passed
- Room Allocation: 13 tests passed
- Complaint Management: 10 tests passed

Total: 39 automated backend tests passed.

## Important Findings

- Existing validation reduces several operational risks.
- Stale availability is a usability risk that requires testing.
- Permanent complaint deletion may remove useful audit history.
- Risk scores must be reviewed using actual evidence.

## Next Actions

1. Review failure causes and existing safeguards.
2. Validate Severity, Occurrence, and Detection scores.
3. Prioritize failure modes using RPN.
4. Assign preventive actions and verification tests.
5. Document residual risks and recommendations.


## RPN Risk Prioritization

The initial FMEA scores are ranked in descending RPN order.

| Rank | Failure ID | Failure Mode | RPN |
|---|---|---|---|
| 1 | F06 | Permanent complaint deletion | 196 |
| 2 | F05 | Stale room availability | 120 |
| 3 | F03 | Duplicate active allocation | 96 |
| 4 | F04 | Partial room transfer | 80 |
| 5 | F02 | Room overcapacity | 72 |
| 6 | F01 | Duplicate student registration | 54 |

### Priority Interpretation

**Priority 1 - Complaint History Loss (F06)**

Permanent deletion can remove historical complaint evidence.
Recommended action: Introduce soft deletion or an audit log.
Verification: Confirm deleted complaints remain available to
authorized audit processes without appearing as active complaints.

**Priority 2 - Stale Room Availability (F05)**

The interface may display outdated availability after changes.
Recommended action: Refresh availability following relevant
room and allocation operations.
Verification: Compare UI availability against database values.

**Priority 3 - Duplicate Active Allocation (F03)**

A student should not receive multiple active room assignments.
Existing control: Unique active allocation constraint and
backend validation.
Verification: Attempt repeated room allocation and confirm
that only one active record exists.

### Limitations

RPN values are preliminary expert estimates. They are not
measured defect frequencies or validated probabilities.

Priorities may change after additional testing and evidence
collection.
