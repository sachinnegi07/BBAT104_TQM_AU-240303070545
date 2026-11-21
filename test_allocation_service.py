
import tempfile
from pathlib import Path
from unittest.mock import patch

import database
from student_service import add_student
from room_service import add_room, get_rooms
from allocation_service import (
    allocate_room,
    get_allocations,
    transfer_room,
    vacate_room,
)


def expect_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return

    raise AssertionError(
        f"{function.__name__} should reject this operation."
    )


def run_tests():
    # Testing uses a temporary database.
    # Actual hostel records remain unchanged.
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "test_allocations.db"

        with patch.object(database, "DB_PATH", test_db):
            database.initialize_database()

            # Create test students
            s1 = add_student("S101", "Aman")
            s2 = add_student("S102", "Rahul")
            s3 = add_student("S103", "Neha")

            # Create test rooms
            r1 = add_room("A101", 1)
            r2 = add_room("B201", 2)

            # TEST 1: Allocate a student
            allocation_id = allocate_room(s1, r1)
            assert allocation_id > 0
            print("PASS: Allocate Room")

            # TEST 2: Room occupancy
            rooms = {
                r["room_number"]: r for r in get_rooms()
            }
            assert rooms["A101"]["occupied"] == 1
            assert rooms["A101"]["available"] == 0
            print("PASS: Room Occupancy Tracking")

            # TEST 3: Reject duplicate allocation
            expect_error(allocate_room, s1, r2)
            print("PASS: Duplicate Allocation Prevention")

            # TEST 4: Reject allocation to full room
            expect_error(allocate_room, s2, r1)
            print("PASS: Room Capacity Protection")

            # TEST 5: Allocate remaining students
            allocate_room(s2, r2)
            allocate_room(s3, r2)
            assert len(get_allocations()) == 3
            print("PASS: Multiple Student Allocations")

            # TEST 6: Reject transfer to full room
            expect_error(transfer_room, s1, r2)

            active = get_allocations()
            s1_record = next(
                a for a in active if a["student_id"] == s1
            )
            assert s1_record["room_id"] == r1
            print("PASS: Failed Transfer Preserves Allocation")

            # TEST 7: Vacate room
            assert vacate_room(s3) is True
            assert len(get_allocations()) == 2
            print("PASS: Vacate Room")

            # TEST 8: Transfer student
            new_id = transfer_room(s1, r2)
            assert new_id > 0

            active = get_allocations()
            s1_record = next(
                a for a in active if a["student_id"] == s1
            )
            assert s1_record["room_id"] == r2
            print("PASS: Transfer Room")

            # TEST 9: Updated availability
            rooms = {
                r["room_number"]: r for r in get_rooms()
            }
            assert rooms["A101"]["available"] == 1
            assert rooms["B201"]["occupied"] == 2
            assert rooms["B201"]["available"] == 0
            print("PASS: Availability After Transfer")

            # TEST 10: Allocation history
            history = get_allocations(active_only=False)
            assert len(history) == 4
            assert len(get_allocations()) == 2
            print("PASS: Allocation History Preserved")

            # TEST 11: Reject same-room transfer
            expect_error(transfer_room, s1, r2)
            print("PASS: Same Room Transfer Prevention")

            # TEST 12: Reject nonexistent student
            expect_error(allocate_room, 999999, r1)
            print("PASS: Invalid Student Prevention")

            # TEST 13: Prevent double vacating
            assert vacate_room(s1) is True
            assert vacate_room(s1) is False
            print("PASS: Double Vacate Protection")

    print("\nALL 13 ALLOCATION TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
