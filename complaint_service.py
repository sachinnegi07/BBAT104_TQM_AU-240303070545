
import sqlite3
from contextlib import closing

from database import get_connection


# ==========================================
# VALIDATION HELPERS
# ==========================================

ALLOWED_STATUSES = (
    "Pending",
    "In Progress",
    "Resolved"
)


def validate_id(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a valid ID.")

    try:
        number = int(str(value).strip())
    except (ValueError, TypeError):
        raise ValueError(f"{label} must be a valid ID.")

    if number <= 0:
        raise ValueError(f"{label} must be positive.")

    return number


def validate_complaint(title, description, status):
    title = str(title or "").strip()
    description = str(description or "").strip()
    status = str(status or "").strip()

    if not title:
        raise ValueError("Complaint title is required.")

    if len(title) > 150:
        raise ValueError(
            "Complaint title must not exceed 150 characters."
        )

    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid complaint status.")

    return title, description, status


# ==========================================
# CREATE - REGISTER COMPLAINT
# ==========================================

def add_complaint(student_id, title, description=""):
    student_id = validate_id(student_id, "Student ID")

    title, description, status = validate_complaint(
        title, description, "Pending"
    )

    with closing(get_connection()) as conn:
        with conn:
            student = conn.execute(
                "SELECT id FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()

            if student is None:
                raise ValueError("Student not found.")

            cursor = conn.execute(
                """
                INSERT INTO complaints
                    (student_id, title, description, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    title,
                    description,
                    status
                )
            )

            return cursor.lastrowid


# ==========================================
# READ - VIEW COMPLAINTS
# ==========================================

def get_complaints():
    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT
                c.id,
                c.student_id,
                s.student_code,
                s.full_name,
                c.title,
                c.description,
                c.status,
                c.created_at
            FROM complaints c
            JOIN students s
                ON c.student_id = s.id
            ORDER BY c.id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


# ==========================================
# UPDATE - EDIT COMPLAINT
# ==========================================

def update_complaint(
    complaint_id,
    title,
    description,
    status
):
    complaint_id = validate_id(
        complaint_id, "Complaint ID"
    )

    title, description, status = validate_complaint(
        title, description, status
    )

    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE complaints
                SET title = ?,
                    description = ?,
                    status = ?
                WHERE id = ?
                """,
                (
                    title,
                    description,
                    status,
                    complaint_id
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Complaint not found.")

            return True


# ==========================================
# UPDATE - CHANGE COMPLAINT STATUS
# ==========================================

def update_complaint_status(
    complaint_id,
    new_status
):
    complaint_id = validate_id(
        complaint_id, "Complaint ID"
    )

    new_status = str(new_status or "").strip()

    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid complaint status.")

    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE complaints
                SET status = ?
                WHERE id = ?
                """,
                (new_status, complaint_id)
            )

            if cursor.rowcount == 0:
                raise ValueError("Complaint not found.")

            return True


# ==========================================
# DELETE - REMOVE COMPLAINT
# ==========================================

def delete_complaint(complaint_id):
    complaint_id = validate_id(
        complaint_id, "Complaint ID"
    )

    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                DELETE FROM complaints
                WHERE id = ?
                """,
                (complaint_id,)
            )

            return cursor.rowcount > 0


# ==========================================
# SEARCH - FIND COMPLAINTS
# ==========================================

def search_complaints(keyword):
    keyword = f"%{str(keyword or '').strip()}%"

    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT
                c.id,
                c.student_id,
                s.student_code,
                s.full_name,
                c.title,
                c.description,
                c.status,
                c.created_at
            FROM complaints c
            JOIN students s
                ON c.student_id = s.id
            WHERE c.title LIKE ?
               OR c.description LIKE ?
               OR c.status LIKE ?
               OR s.full_name LIKE ?
               OR s.student_code LIKE ?
            ORDER BY c.id DESC
            """,
            (keyword,) * 5
        ).fetchall()

        return [dict(row) for row in rows]
