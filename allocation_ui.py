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
    """Room allocation UI. All database changes use existing services."""

    BG = ("#F4F7FB", "#101722")
    CARD = ("#FFFFFF", "#1A2432")
    BORDER = ("#E3E9F1", "#2C394A")
    TEXT = ("#172437", "#F3F6FA")
    MUTED = ("#64748B", "#9AA9BC")
    SOFT = ("#F5F7FB", "#222F40")
    ACCENT = ("#1F6AA5", "#60A5FA")
    GREEN = "#10B981"

    def __init__(self, master):
        super().__init__(master, fg_color=self.BG, corner_radius=12)

        self.student_options = {}
        self.room_options = {}
        self.student_lookup = {}
        self.room_lookup = {}
        self.allocations_data = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.build_header()
        self.build_selection_panel()
        self.build_records_panel()
        self.refresh_data()

    # ==========================================
    # PAGE HEADER
    # ==========================================

    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 16))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="HOSTEL OPERATIONS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.ACCENT,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Room Allocation Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=1, column=0, sticky="w", pady=(5, 2))

        ctk.CTkLabel(
            header,
            text="Assign rooms, transfer students and manage vacates.",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED,
        ).grid(row=2, column=0, sticky="w")

    # ==========================================
    # SELECTION AND ACTION PANEL
    # ==========================================

    def build_selection_panel(self):
        panel = ctk.CTkFrame(
            self, fg_color=self.CARD, border_width=1,
            border_color=self.BORDER, corner_radius=16,
        )
        panel.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 14))
        panel.grid_columnconfigure((0, 1), weight=1, uniform="selectors")

        heading = ctk.CTkFrame(panel, fg_color="transparent")
        heading.grid(row=0, column=0, columnspan=2, sticky="ew",
                     padx=20, pady=(16, 10))
        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading, text="Manage Room Assignment",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            heading, text="SELECT AND ACT",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.MUTED,
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            panel, text="Select Student",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=1, column=0, sticky="w", padx=(20, 10))

        ctk.CTkLabel(
            panel, text="Select Room / Transfer Destination",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=1, column=1, sticky="w", padx=(10, 20))

        self.student_menu = ctk.CTkOptionMenu(
            panel,
            values=["No students available"],
            height=42,
            corner_radius=9,
            command=lambda _value: self.update_selection_hints(),
        )
        self.student_menu.grid(row=2, column=0, sticky="ew",
                               padx=(20, 10), pady=(8, 5))

        self.room_menu = ctk.CTkOptionMenu(
            panel,
            values=["No rooms available"],
            height=42,
            corner_radius=9,
            command=lambda _value: self.update_selection_hints(),
        )
        self.room_menu.grid(row=2, column=1, sticky="ew",
                            padx=(10, 20), pady=(8, 5))

        self.student_hint = ctk.CTkLabel(
            panel, text="Current assignment: Not available",
            font=ctk.CTkFont(size=11), text_color=self.MUTED,
            anchor="w",
        )
        self.student_hint.grid(row=3, column=0, sticky="ew",
                               padx=(22, 10), pady=(0, 12))

        self.room_hint = ctk.CTkLabel(
            panel, text="Room availability: Not available",
            font=ctk.CTkFont(size=11), text_color=self.MUTED,
            anchor="w",
        )
        self.room_hint.grid(row=3, column=1, sticky="ew",
                            padx=(12, 20), pady=(0, 12))

        action_bar = ctk.CTkFrame(panel, fg_color="transparent")
        action_bar.grid(row=4, column=0, columnspan=2, sticky="ew",
                        padx=15, pady=(2, 8))

        for column in range(4):
            action_bar.grid_columnconfigure(column, weight=1, uniform="actions")

        actions = (
            ("Allocate Room", self.allocate),
            ("Transfer Room", self.transfer),
            ("Vacate Room", self.vacate),
            ("Refresh", self.refresh_data),
        )
        for column, (title, handler) in enumerate(actions):
            ctk.CTkButton(
                action_bar,
                text=title,
                command=handler,
                height=40,
                corner_radius=9,
                font=ctk.CTkFont(
                    size=12, weight="bold" if column == 0 else "normal"
                ),
            ).grid(row=0, column=column, sticky="ew", padx=5)

        ctk.CTkLabel(
            panel,
            text="Transfer uses the selected room as the destination. "
                 "Vacate applies to the selected student.",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        ).grid(row=5, column=0, columnspan=2, sticky="w",
               padx=22, pady=(2, 14))

    # ==========================================
    # ACTIVE ALLOCATIONS PANEL
    # ==========================================

    def build_records_panel(self):
        panel = ctk.CTkFrame(
            self, fg_color=self.CARD, border_width=1,
            border_color=self.BORDER, corner_radius=16,
        )
        panel.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        heading = ctk.CTkFrame(panel, fg_color="transparent")
        heading.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 10))
        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading, text="Active Room Allocations",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=0, column=0, sticky="w")

        self.count_label = ctk.CTkLabel(
            heading, text="0 active", width=92, height=30,
            corner_radius=8, fg_color=self.SOFT,
            text_color=self.ACCENT,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.count_label.grid(row=0, column=1, sticky="e")

        self.records_frame = ctk.CTkScrollableFrame(
            panel, fg_color="transparent",
        )
        self.records_frame.grid(row=1, column=0, sticky="nsew",
                                padx=14, pady=(0, 8))

        self.status = ctk.CTkLabel(
            panel, text="Ready", font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        )
        self.status.grid(row=2, column=0, pady=(0, 12))

    # ==========================================
    # REFRESH - PRESERVE SELECTED IDS
    # ==========================================

    def refresh_data(self):
        try:
            previous_student_id = self.student_options.get(
                self.student_menu.get()
            )
            previous_room_id = self.room_options.get(
                self.room_menu.get()
            )

            students = get_students()
            rooms = get_rooms()
            allocations = get_allocations()

            self.student_lookup = {s["id"]: s for s in students}
            self.room_lookup = {r["id"]: r for r in rooms}
            self.allocations_data = allocations

            self.student_options = {
                f"{s['student_code']} - {s['full_name']} (ID: {s['id']})": s["id"]
                for s in students
            }
            self.room_options = {
                f"{r['room_number']} | Available: {r['available']}/{r['capacity']} "
                f"(ID: {r['id']})": r["id"]
                for r in rooms
            }

            student_labels = list(self.student_options)
            room_labels = list(self.room_options)

            self.student_menu.configure(
                values=student_labels or ["No students available"]
            )
            self.room_menu.configure(
                values=room_labels or ["No rooms available"]
            )

            student_label = next(
                (label for label, value in self.student_options.items()
                 if value == previous_student_id),
                student_labels[0] if student_labels else "No students available",
            )
            room_label = next(
                (label for label, value in self.room_options.items()
                 if value == previous_room_id),
                room_labels[0] if room_labels else "No rooms available",
            )

            self.student_menu.set(student_label)
            self.room_menu.set(room_label)
            self.update_selection_hints()
            self.display_allocations(allocations)

        except Exception as error:
            messagebox.showerror("Refresh Error", str(error))

    def update_selection_hints(self):
        student_id = self.student_options.get(self.student_menu.get())
        room_id = self.room_options.get(self.room_menu.get())

        student = self.student_lookup.get(student_id)
        if student is None:
            student_text = "Current assignment: No student selected"
        else:
            active = next(
                (
                    allocation for allocation in self.allocations_data
                    if allocation["student_code"] == student["student_code"]
                ),
                None,
            )
            if active:
                student_text = f"Current assignment: {active['room_number']}"
            else:
                student_text = "Current assignment: Not allocated"

        room = self.room_lookup.get(room_id)
        if room is None:
            room_text = "Room availability: No room selected"
        else:
            room_text = (
                f"Room availability: {room['available']} of "
                f"{room['capacity']} beds free"
            )

        self.student_hint.configure(text=student_text)
        self.room_hint.configure(text=room_text)

    # ==========================================
    # EXISTING SELECTION AND SERVICE OPERATIONS
    # ==========================================

    def selected_student(self):
        student_id = self.student_options.get(self.student_menu.get())
        if student_id is None:
            raise ValueError("Please add or select a student first.")
        return student_id

    def selected_room(self):
        room_id = self.room_options.get(self.room_menu.get())
        if room_id is None:
            raise ValueError("Please add or select a room first.")
        return room_id

    def allocate(self):
        try:
            student_id = self.selected_student()
            room_id = self.selected_room()

            allocate_room(student_id, room_id)
            messagebox.showinfo("Success", "Room allocated successfully!")
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror("Allocation Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def transfer(self):
        try:
            student_id = self.selected_student()
            room_id = self.selected_room()

            confirmed = messagebox.askyesno(
                "Confirm Transfer", "Transfer this student to the selected room?"
            )
            if not confirmed:
                return

            transfer_room(student_id, room_id)
            messagebox.showinfo("Success", "Student transferred successfully!")
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror("Transfer Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def vacate(self):
        try:
            student_id = self.selected_student()

            confirmed = messagebox.askyesno(
                "Confirm Vacate", "Vacate the selected student's room?"
            )
            if not confirmed:
                return

            success = vacate_room(student_id)
            if success:
                messagebox.showinfo("Success", "Room vacated successfully!")
            else:
                messagebox.showwarning(
                    "Not Allocated", "Student has no active room allocation."
                )
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror("Vacate Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    # ==========================================
    # RECORDS DISPLAY
    # ==========================================

    def display_allocations(self, allocations):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        self.count_label.configure(text=f"{len(allocations)} active")
        self.status.configure(text=f"Active Allocations: {len(allocations)}")

        if not allocations:
            empty = ctk.CTkFrame(
                self.records_frame, fg_color=self.SOFT, corner_radius=12,
            )
            empty.pack(fill="x", padx=5, pady=10)
            ctk.CTkLabel(
                empty, text="No active room allocations",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.TEXT,
            ).pack(pady=(24, 5))
            ctk.CTkLabel(
                empty, text="Select a student and room to create an allocation.",
                font=ctk.CTkFont(size=12), text_color=self.MUTED,
            ).pack(pady=(0, 24))
            return

        for allocation in allocations:
            row = ctk.CTkFrame(
                self.records_frame,
                fg_color=self.SOFT,
                border_width=1,
                border_color=self.BORDER,
                corner_radius=12,
            )
            row.pack(fill="x", padx=5, pady=6)
            row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row, text="AL", width=44, height=44,
                corner_radius=11, fg_color=("#E4EDF9", "#2B4058"),
                text_color=self.ACCENT,
                font=ctk.CTkFont(size=13, weight="bold"),
            ).grid(row=0, column=0, rowspan=2, padx=(14, 12), pady=14)

            ctk.CTkLabel(
                row,
                text=str(allocation["full_name"]),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.TEXT, anchor="w",
            ).grid(row=0, column=1, sticky="ew", pady=(12, 2))

            details = (
                f"ID: {allocation['student_code']}   |   "
                f"Room: {allocation['room_number']}   |   "
                f"Date: {allocation['allocation_date']}"
            )
            ctk.CTkLabel(
                row, text=details,
                font=ctk.CTkFont(size=11),
                text_color=self.MUTED, anchor="w",
            ).grid(row=1, column=1, sticky="ew", pady=(0, 12))

            ctk.CTkLabel(
                row, text="ACTIVE",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.GREEN,
            ).grid(row=0, column=2, rowspan=2, padx=(10, 18))


if __name__ == "__main__":
    initialize_database()
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hostel Management | Room Allocation")
    app.geometry("1100x700")
    app.minsize(900, 600)

    allocation_ui = AllocationManagementFrame(app)
    allocation_ui.pack(fill="both", expand=True, padx=10, pady=10)
    app.mainloop()
