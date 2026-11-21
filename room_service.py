
import sqlite3
from contextlib import closing

from database import get_connection


def validate_room(room_number, capacity):
    room_number = str(room_number).strip()

    if not room_number:
        raise ValueError("Room number is required.")

    try:
        capacity = int(str(capacity).strip())
    except (ValueError, TypeError):
        raise ValueError("Capacity must be a whole number.")

    if capacity <= 0:
        raise ValueError("Capacity must be greater than zero.")

    return room_number, capacity


# CREATE - Add room
def add_room(room_number, capacity):
    room_number, capacity = validate_room(
        room_number, capacity
    )

    with closing(get_connection()) as conn:
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO rooms (room_number, capacity)
                    VALUES (?, ?)
                    """,
                    (room_number, capacity)
                )
                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Room number already exists or data is invalid."
            ) from error


# READ - Get rooms with occupancy
def get_rooms():
    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT
                r.id,
                r.room_number,
                r.capacity,
                COUNT(a.id) AS occupied,
                r.capacity - COUNT(a.id) AS available
            FROM rooms r
            LEFT JOIN allocations a
                ON r.id = a.room_id
                AND a.vacated_at IS NULL
            GROUP BY r.id
            ORDER BY r.room_number
            """
        ).fetchall()

        return [dict(row) for row in rows]


# UPDATE - Edit room details
def update_room(room_id, room_number, capacity):
    room_number, capacity = validate_room(
        room_number, capacity
    )

    with closing(get_connection()) as conn:
        try:
            with conn:
                occupied = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM allocations
                    WHERE room_id = ?
                      AND vacated_at IS NULL
                    """,
                    (room_id,)
                ).fetchone()[0]

                if capacity < occupied:
                    raise ValueError(
                        "Capacity cannot be less than occupied beds."
                    )

                cursor = conn.execute(
                    """
                    UPDATE rooms
                    SET room_number = ?, capacity = ?
                    WHERE id = ?
                    """,
                    (room_number, capacity, room_id)
                )

                if cursor.rowcount == 0:
                    raise ValueError("Room not found.")

                return True

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Room number already exists or data is invalid."
            ) from error


# DELETE - Remove room
def delete_room(room_id):
    with closing(get_connection()) as conn:
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM rooms WHERE id = ?",
                    (room_id,)
                )
                return cursor.rowcount > 0

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Cannot delete a room with linked allocations."
            ) from error


# SEARCH - Find rooms
def search_rooms(keyword):
    keyword = f"%{str(keyword).strip()}%"

    return [
        room for room in get_rooms()
        if keyword.strip("%").lower()
        in room["room_number"].lower()
    ]
