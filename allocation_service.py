
from contextlib import closing, contextmanager

from database import get_connection


def validate_id(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a valid ID.")

    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a valid ID.")

    if number <= 0:
        raise ValueError(f"{label} must be positive.")

    return number


@contextmanager
def write_transaction():
    with closing(get_connection()) as conn:
        conn.execute("BEGIN IMMEDIATE")

        with conn:
            yield conn


def check_student(conn, student_id):
    student = conn.execute(
        "SELECT id FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        raise ValueError("Student not found.")


def check_room_availability(conn, room_id):
    room = conn.execute(
        """
        SELECT id, capacity
        FROM rooms
        WHERE id = ?
        """,
        (room_id,)
    ).fetchone()

    if room is None:
        raise ValueError("Room not found.")

    occupied = conn.execute(
        """
        SELECT COUNT(*)
        FROM allocations
        WHERE room_id = ?
          AND vacated_at IS NULL
        """,
        (room_id,)
    ).fetchone()[0]

    if occupied >= room["capacity"]:
        raise ValueError("Room is full. No beds available.")


def get_active_allocation(conn, student_id):
    return conn.execute(
        """
        SELECT id, room_id
        FROM allocations
        WHERE student_id = ?
          AND vacated_at IS NULL
        """,
        (student_id,)
    ).fetchone()


# CREATE - Allocate room to student
def allocate_room(student_id, room_id):
    student_id = validate_id(student_id, "Student ID")
    room_id = validate_id(room_id, "Room ID")

    with write_transaction() as conn:
        check_student(conn, student_id)

        if get_active_allocation(conn, student_id):
            raise ValueError(
                "Student already has an allocated room."
            )

        check_room_availability(conn, room_id)

        cursor = conn.execute(
            """
            INSERT INTO allocations (student_id, room_id)
            VALUES (?, ?)
            """,
            (student_id, room_id)
        )

        return cursor.lastrowid


# READ - View room allocations
def get_allocations(active_only=True):
    query = """
        SELECT
            a.id,
            a.student_id,
            s.student_code,
            s.full_name,
            a.room_id,
            r.room_number,
            a.allocation_date,
            a.vacated_at
        FROM allocations a
        JOIN students s ON a.student_id = s.id
        JOIN rooms r ON a.room_id = r.id
    """

    if active_only:
        query += " WHERE a.vacated_at IS NULL"

    query += " ORDER BY a.id DESC"

    with closing(get_connection()) as conn:
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]


# UPDATE - Transfer student to another room
def transfer_room(student_id, new_room_id):
    student_id = validate_id(student_id, "Student ID")
    new_room_id = validate_id(new_room_id, "Room ID")

    with write_transaction() as conn:
        check_student(conn, student_id)

        current = get_active_allocation(conn, student_id)

        if current is None:
            raise ValueError(
                "Student does not have an allocated room."
            )

        if current["room_id"] == new_room_id:
            raise ValueError(
                "Student is already in this room."
            )

        check_room_availability(conn, new_room_id)

        # Close previous allocation history
        conn.execute(
            """
            UPDATE allocations
            SET vacated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (current["id"],)
        )

        # Create new active allocation
        cursor = conn.execute(
            """
            INSERT INTO allocations (student_id, room_id)
            VALUES (?, ?)
            """,
            (student_id, new_room_id)
        )

        return cursor.lastrowid


# VACATE - Release student's allocated bed
def vacate_room(student_id):
    student_id = validate_id(student_id, "Student ID")

    with write_transaction() as conn:
        current = get_active_allocation(conn, student_id)

        if current is None:
            return False

        conn.execute(
            """
            UPDATE allocations
            SET vacated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (current["id"],)
        )

        return True
