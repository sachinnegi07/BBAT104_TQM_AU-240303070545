
import tempfile
from pathlib import Path
from unittest.mock import patch

import database
from room_service import (
    add_room,
    get_rooms,
    update_room,
    delete_room,
    search_rooms,
)


def run_tests():
    # Temporary database: real data remains safe
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "test_rooms.db"

        with patch.object(database, "DB_PATH", test_db):
            database.initialize_database()

            # TEST 1: Add Room
            room_id = add_room("A101", 3)
            assert room_id > 0
            print("PASS: Add Room")

            # TEST 2: View Room
            rooms = get_rooms()
            assert len(rooms) == 1
            assert rooms[0]["room_number"] == "A101"
            print("PASS: View Room")

            # TEST 3: Available Beds
            assert rooms[0]["capacity"] == 3
            assert rooms[0]["occupied"] == 0
            assert rooms[0]["available"] == 3
            print("PASS: Available Beds")

            # TEST 4: Update Room
            update_room(room_id, "A102", 4)
            updated = get_rooms()[0]
            assert updated["room_number"] == "A102"
            assert updated["capacity"] == 4
            print("PASS: Update Room")

            # TEST 5: Search Room
            results = search_rooms("A102")
            assert len(results) == 1
            print("PASS: Search Room")

            # TEST 6: Duplicate Room Prevention
            try:
                add_room("A102", 2)
            except ValueError:
                print("PASS: Duplicate Room Prevention")
            else:
                raise AssertionError("Duplicate room accepted!")

            # TEST 7: Empty Room Number
            try:
                add_room("", 2)
            except ValueError:
                print("PASS: Empty Room Validation")
            else:
                raise AssertionError("Empty room accepted!")

            # TEST 8: Invalid Capacity
            try:
                add_room("B201", 0)
            except ValueError:
                print("PASS: Capacity Validation")
            else:
                raise AssertionError("Invalid capacity accepted!")

            # TEST 9: Delete Room
            assert delete_room(room_id) is True
            assert len(get_rooms()) == 0
            print("PASS: Delete Room")

    print("\nALL 9 ROOM MANAGEMENT TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
