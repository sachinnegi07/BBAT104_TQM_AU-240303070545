
import sqlite3
from contextlib import closing

from database import get_connection


def validate_student(student_code, full_name):
    student_code = student_code.strip()
    full_name = full_name.strip()

    if not student_code:
        raise ValueError("Student ID is required.")

    if not full_name:
        raise ValueError("Student name is required.")

    return student_code, full_name


# CREATE - Add student
def add_student(student_code, full_name, phone="", course=""):
    student_code, full_name = validate_student(
        student_code, full_name
    )

    with closing(get_connection()) as conn:
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO students
                        (student_code, full_name, phone, course)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        student_code,
                        full_name,
                        phone.strip(),
                        course.strip()
                    )
                )

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Student ID already exists or data is invalid."
            ) from error


# READ - View all students
def get_students():
    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT id, student_code, full_name, phone, course
            FROM students
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


# UPDATE - Edit student
def update_student(
    student_id, student_code, full_name,
    phone="", course=""
):
    student_code, full_name = validate_student(
        student_code, full_name
    )

    with closing(get_connection()) as conn:
        try:
            with conn:
                cursor = conn.execute(
                    """
                    UPDATE students
                    SET student_code = ?,
                        full_name = ?,
                        phone = ?,
                        course = ?
                    WHERE id = ?
                    """,
                    (
                        student_code,
                        full_name,
                        phone.strip(),
                        course.strip(),
                        student_id
                    )
                )

                if cursor.rowcount == 0:
                    raise ValueError("Student not found.")

                return True

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Student ID already exists or data is invalid."
            ) from error


# DELETE - Remove student
def delete_student(student_id):
    with closing(get_connection()) as conn:
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM students WHERE id = ?",
                    (student_id,)
                )

                return cursor.rowcount > 0

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Cannot delete student with linked "
                "allocations or complaints."
            ) from error


# SEARCH - Find students
def search_students(keyword):
    keyword = f"%{keyword.strip()}%"

    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT id, student_code, full_name, phone, course
            FROM students
            WHERE student_code LIKE ?
               OR full_name LIKE ?
            ORDER BY id DESC
            """,
            (keyword, keyword)
        ).fetchall()

        return [dict(row) for row in rows]
