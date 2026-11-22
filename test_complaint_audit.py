
import tempfile
from pathlib import Path
from contextlib import closing
from unittest.mock import patch

import database
from student_service import add_student
from complaint_service import (
    add_complaint,
    delete_complaint,
    get_complaints,
)


def run_tests():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "audit_tests.db"

        with patch.object(database, "DB_PATH", test_db):
            database.initialize_database()

            student_id = add_student(
                "AUD701",
                "Audit Test Student",
                "9876543210",
                "BCA",
            )

            # TEST 1: Service deletion preserves history
            complaint_id = add_complaint(
                student_id,
                "Water Supply Issue",
                "Water unavailable in hostel.",
            )

            assert delete_complaint(complaint_id) is True
            assert not any(
                row["id"] == complaint_id
                for row in get_complaints()
            )

            with closing(database.get_connection()) as conn:
                audit = conn.execute(
                    """
                    SELECT *
                    FROM complaint_delete_audit
                    WHERE complaint_id = ?
                    """,
                    (complaint_id,),
                ).fetchone()

                assert audit is not None
                assert audit["student_code"] == "AUD701"
                assert audit["student_name"] == "Audit Test Student"
                assert audit["title"] == "Water Supply Issue"
                assert audit["description"] == "Water unavailable in hostel."
                assert audit["status"] == "Pending"
                assert audit["deleted_at"] is not None

            print("PASS: Service deletion preserves audit history")

            # TEST 2: Invalid deletion adds no audit record
            assert delete_complaint(999999) is False

            with closing(database.get_connection()) as conn:
                count = conn.execute(
                    "SELECT COUNT(*) FROM complaint_delete_audit"
                ).fetchone()[0]

                assert count == 1

            print("PASS: Missing complaint creates no audit entry")

            # TEST 3: Direct SQL deletion also triggers audit
            second_id = add_complaint(
                student_id,
                "Electricity Issue",
                "Power supply interrupted.",
            )

            with closing(database.get_connection()) as conn:
                with conn:
                    conn.execute(
                        "DELETE FROM complaints WHERE id = ?",
                        (second_id,),
                    )

                audit = conn.execute(
                    """
                    SELECT title
                    FROM complaint_delete_audit
                    WHERE complaint_id = ?
                    """,
                    (second_id,),
                ).fetchone()

                assert audit is not None
                assert audit["title"] == "Electricity Issue"

            print("PASS: Direct SQL deletion is audited")

            # TEST 4: Failed transaction leaves records intact
            third_id = add_complaint(
                student_id,
                "Internet Issue",
                "Wi-Fi unavailable.",
            )

            with closing(database.get_connection()) as conn:
                try:
                    with conn:
                        conn.execute(
                            "DELETE FROM complaints WHERE id = ?",
                            (third_id,),
                        )

                        raise RuntimeError("Simulated failure")

                except RuntimeError:
                    pass

                original = conn.execute(
                    "SELECT id FROM complaints WHERE id = ?",
                    (third_id,),
                ).fetchone()

                audit = conn.execute(
                    """
                    SELECT id
                    FROM complaint_delete_audit
                    WHERE complaint_id = ?
                    """,
                    (third_id,),
                ).fetchone()

                assert original is not None
                assert audit is None

            print("PASS: Failed transaction rolls back deletion and audit")

            # TEST 5: Student deletion does not erase audit snapshot
            assert delete_complaint(third_id) is True

            with closing(database.get_connection()) as conn:
                with conn:
                    conn.execute(
                        "DELETE FROM students WHERE id = ?",
                        (student_id,),
                    )

                audit = conn.execute(
                    """
                    SELECT student_code, student_name
                    FROM complaint_delete_audit
                    WHERE complaint_id = ?
                    """,
                    (complaint_id,),
                ).fetchone()

                assert audit is not None
                assert audit["student_code"] == "AUD701"
                assert audit["student_name"] == "Audit Test Student"

            print("PASS: Audit snapshot survives student deletion")

    print("\nALL 5 COMPLAINT AUDIT TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
