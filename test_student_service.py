
import tempfile
from pathlib import Path
from unittest.mock import patch

import database
from student_service import (
    add_student,
    get_students,
    update_student,
    delete_student,
    search_students,
)


def run_tests():
    # Real database ko change kiye bina testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "test_hostel.db"

        with patch.object(database, "DB_PATH", test_db):
            database.initialize_database()

            # TEST 1: Add Student
            student_id = add_student(
                "TEST101", "Aman", "9876543210", "BCA"
            )
            assert student_id > 0
            print("PASS: Add Student")

            # TEST 2: View Students
            students = get_students()
            assert len(students) == 1
            assert students[0]["full_name"] == "Aman"
            print("PASS: View Students")

            # TEST 3: Update Student
            update_student(
                student_id, "TEST101",
                "Aman Sharma", "9876543210", "BCA"
            )
            assert get_students()[0]["full_name"] == "Aman Sharma"
            print("PASS: Update Student")

            # TEST 4: Search Student
            results = search_students("Sharma")
            assert len(results) == 1
            print("PASS: Search Student")

            # TEST 5: Duplicate ID
            try:
                add_student("TEST101", "Another Student")
                raise AssertionError("Duplicate ID accepted!")
            except ValueError:
                print("PASS: Duplicate ID Prevention")

            # TEST 6: Empty Student ID
            try:
                add_student("", "Test Student")
                raise AssertionError("Empty ID accepted!")
            except ValueError:
                print("PASS: Required Field Validation")

            # TEST 7: Delete Student
            assert delete_student(student_id) is True
            assert len(get_students()) == 0
            print("PASS: Delete Student")

    print("\nALL 7 STUDENT CRUD TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
