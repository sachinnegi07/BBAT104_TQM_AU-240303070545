
import tempfile
from pathlib import Path
from unittest.mock import patch

import database
from student_service import add_student
from complaint_service import (
    add_complaint,
    get_complaints,
    update_complaint,
    update_complaint_status,
    delete_complaint,
    search_complaints,
)


def expect_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return

    raise AssertionError(
        f"{function.__name__} accepted invalid data!"
    )


def run_tests():

    # Use a temporary database to protect real data
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "test_complaints.db"

        with patch.object(database, "DB_PATH", test_db):

            database.initialize_database()

            # Create test student
            student_id = add_student(
                "TEST301", "Aman Sharma", "9876543210", "BCA"
            )

            # TEST 1: Add Complaint
            complaint_id = add_complaint(
                student_id,
                "Water Supply Issue",
                "No water available in hostel bathroom."
            )

            assert complaint_id > 0
            print("PASS: Add Complaint")

            # TEST 2: View Complaint
            complaints = get_complaints()

            assert len(complaints) == 1
            assert complaints[0]["title"] == "Water Supply Issue"
            print("PASS: View Complaint")

            # TEST 3: Default Status
            assert complaints[0]["status"] == "Pending"
            print("PASS: Default Pending Status")

            # TEST 4: Update Complaint Details
            update_complaint(
                complaint_id,
                "Water Supply Problem",
                "Water supply interrupted since morning.",
                "In Progress"
            )

            updated = get_complaints()[0]

            assert updated["title"] == "Water Supply Problem"
            assert updated["status"] == "In Progress"
            print("PASS: Update Complaint")

            # TEST 5: Search Complaint
            results = search_complaints("Water Supply")

            assert len(results) == 1
            print("PASS: Search Complaint")

            # TEST 6: Update Status
            update_complaint_status(
                complaint_id, "Resolved"
            )

            assert get_complaints()[0]["status"] == "Resolved"
            print("PASS: Update Complaint Status")

            # TEST 7: Invalid Student
            expect_error(
                add_complaint,
                999999,
                "Test Complaint"
            )
            print("PASS: Invalid Student Prevention")

            # TEST 8: Empty Complaint Title
            expect_error(
                add_complaint,
                student_id,
                ""
            )
            print("PASS: Empty Title Validation")

            # TEST 9: Invalid Status
            expect_error(
                update_complaint_status,
                complaint_id,
                "Unknown"
            )
            print("PASS: Invalid Status Prevention")

            # TEST 10: Delete Complaint
            assert delete_complaint(complaint_id) is True
            assert len(get_complaints()) == 0

            print("PASS: Delete Complaint")

    print("\nALL 10 COMPLAINT MANAGEMENT TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
