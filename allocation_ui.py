
import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from student_service import get_students
from room_service import get_rooms
from allocation_service import (
    allocate_room,
    get_allocations,
    transfer_room,
    vacate_room,
)


class AllocationManagementFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.student_options = {}
        self.room_options = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text="Room Allocation Management",
            font=ctk.CTkFont(size=27, weight="bold")
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="w"
        )

        # Selection section
        form = ctk.CTkFrame(self)
        form.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )

        form.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            form,
            text="Select Student"
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            form,
            text="Select Room"
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=(15, 5),
            sticky="w"
        )

        self.student_menu = ctk.CTkOptionMenu(
            form,
            values=["No students available"],
            width=300
        )

        self.student_menu.grid(
            row=1,
            column=0,
            padx=20,
            pady=5,
            sticky="ew"
        )

        self.room_menu = ctk.CTkOptionMenu(
            form,
            values=["No rooms available"],
            width=300
        )

        self.room_menu.grid(
            row=1,
            column=1,
            padx=20,
            pady=5,
            sticky="ew"
        )

        # Action buttons
        buttons = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        buttons.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=15,
            pady=20
        )

        actions = [
            ("Allocate Room", self.allocate),
            ("Transfer Room", self.transfer),
            ("Vacate Room", self.vacate),
            ("Refresh", self.refresh_data),
        ]

        for index, (label, command) in enumerate(actions):
            ctk.CTkButton(
                buttons,
                text=label,
                command=command,
                width=150,
                height=38
            ).grid(
                row=0,
                column=index,
                padx=6,
                pady=5
            )

        # Active allocations section
        records = ctk.CTkFrame(self)

        records.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        records.grid_columnconfigure(0, weight=1)
        records.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            records,
            text="Active Room Allocations",
            font=ctk.CTkFont(size=21, weight="bold")
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=15
        )

        self.records_frame = ctk.CTkScrollableFrame(
            records
        )

        self.records_frame.grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="nsew"
        )

        self.status = ctk.CTkLabel(
            self,
            text="Ready"
        )

        self.status.grid(
            row=3,
            column=0,
            pady=(0, 15)
        )

        self.refresh_data()

    # ==========================================
    # REFRESH DATA - FIXED
    # ==========================================

    def refresh_data(self):
        try:
            # Remember previously selected IDs
            previous_student_id = self.student_options.get(
                self.student_menu.get()
            )

            previous_room_id = self.room_options.get(
                self.room_menu.get()
            )

            # Load latest data
            students = get_students()
            rooms = get_rooms()
            allocations = get_allocations()

            # Student dropdown options
            self.student_options = {
                f"{s['student_code']} - {s['full_name']} "
                f"(ID: {s['id']})": s["id"]
                for s in students
            }

            # Room dropdown options
            self.room_options = {
                f"{r['room_number']} | "
                f"Available: {r['available']}/{r['capacity']} "
                f"(ID: {r['id']})": r["id"]
                for r in rooms
            }

            student_labels = list(self.student_options)
            room_labels = list(self.room_options)

            # Update student menu
            self.student_menu.configure(
                values=student_labels or [
                    "No students available"
                ]
            )

            # Preserve selected student
            selected_student_label = next(
                (
                    label
                    for label, student_id
                    in self.student_options.items()
                    if student_id == previous_student_id
                ),
                (
                    student_labels[0]
                    if student_labels
                    else "No students available"
                )
            )

            self.student_menu.set(
                selected_student_label
            )

            # Update room menu
            self.room_menu.configure(
                values=room_labels or [
                    "No rooms available"
                ]
            )

            # Preserve selected room using its ID
            selected_room_label = next(
                (
                    label
                    for label, room_id
                    in self.room_options.items()
                    if room_id == previous_room_id
                ),
                (
                    room_labels[0]
                    if room_labels
                    else "No rooms available"
                )
            )

            self.room_menu.set(
                selected_room_label
            )

            # Refresh allocation records
            self.display_allocations(allocations)

        except Exception as error:
            messagebox.showerror(
                "Refresh Error",
                str(error)
            )

    # ==========================================
    # SELECT STUDENT
    # ==========================================

    def selected_student(self):
        value = self.student_menu.get()
        student_id = self.student_options.get(value)

        if student_id is None:
            raise ValueError(
                "Please add or select a student first."
            )

        return student_id

    # ==========================================
    # SELECT ROOM
    # ==========================================

    def selected_room(self):
        value = self.room_menu.get()
        room_id = self.room_options.get(value)

        if room_id is None:
            raise ValueError(
                "Please add or select a room first."
            )

        return room_id

    # ==========================================
    # ALLOCATE ROOM
    # ==========================================

    def allocate(self):
        try:
            student_id = self.selected_student()
            room_id = self.selected_room()

            allocate_room(
                student_id,
                room_id
            )

            messagebox.showinfo(
                "Success",
                "Room allocated successfully!"
            )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Allocation Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==========================================
    # TRANSFER ROOM
    # ==========================================

    def transfer(self):
        try:
            student_id = self.selected_student()
            room_id = self.selected_room()

            confirmed = messagebox.askyesno(
                "Confirm Transfer",
                "Transfer this student to the selected room?"
            )

            if not confirmed:
                return

            transfer_room(
                student_id,
                room_id
            )

            messagebox.showinfo(
                "Success",
                "Student transferred successfully!"
            )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Transfer Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==========================================
    # VACATE ROOM
    # ==========================================

    def vacate(self):
        try:
            student_id = self.selected_student()

            confirmed = messagebox.askyesno(
                "Confirm Vacate",
                "Vacate the selected student's room?"
            )

            if not confirmed:
                return

            success = vacate_room(student_id)

            if success:
                messagebox.showinfo(
                    "Success",
                    "Room vacated successfully!"
                )
            else:
                messagebox.showwarning(
                    "Not Allocated",
                    "Student has no active room allocation."
                )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Vacate Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==========================================
    # DISPLAY ALLOCATIONS
    # ==========================================

    def display_allocations(self, allocations):

        # Clear previous rows
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        if not allocations:
            ctk.CTkLabel(
                self.records_frame,
                text="No active room allocations found."
            ).pack(pady=25)

        # Display current allocations
        for allocation in allocations:

            row = ctk.CTkFrame(
                self.records_frame
            )

            row.pack(
                fill="x",
                padx=5,
                pady=5
            )

            details = (
                f"{allocation['student_code']} | "
                f"{allocation['full_name']} | "
                f"Room: {allocation['room_number']} | "
                f"Date: {allocation['allocation_date']}"
            )

            ctk.CTkLabel(
                row,
                text=details,
                anchor="w",
                wraplength=800
            ).pack(
                fill="x",
                padx=15,
                pady=12
            )

        self.status.configure(
            text=(
                f"Active Allocations: "
                f"{len(allocations)}"
            )
        )


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title(
        "Hostel Management | Room Allocation"
    )

    app.geometry("1100x700")
    app.minsize(900, 600)

    allocation_ui = AllocationManagementFrame(app)

    allocation_ui.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    app.mainloop()
