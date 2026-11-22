
import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from room_service import (
    add_room,
    get_rooms,
    update_room,
    delete_room,
    search_rooms,
)


class RoomManagementFrame(ctk.CTkFrame):

    BG = ("#F4F7FB", "#101722")
    CARD = ("#FFFFFF", "#1A2432")
    BORDER = ("#E3E9F1", "#2C394A")
    TEXT = ("#172437", "#F3F6FA")
    MUTED = ("#64748B", "#9AA9BC")
    SOFT = ("#F5F7FB", "#222F40")
    ACCENT = ("#1F6AA5", "#60A5FA")

    GREEN = "#10B981"
    RED = "#EF4444"
    BLUE = "#3B82F6"

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=self.BG,
            corner_radius=12
        )

        self.selected_room_id = None
        self.room_rows = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()
        self.build_records()

        self.show_all()

    # ======================================
    # PAGE HEADER
    # ======================================

    def build_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=24,
            pady=(22, 18)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="HOSTEL INVENTORY",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.ACCENT
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Room Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=self.TEXT
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 2)
        )

        ctk.CTkLabel(
            header,
            text=(
                "Manage hostel rooms, capacities "
                "and bed availability."
            ),
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

    # ======================================
    # LEFT SIDE - ROOM FORM
    # ======================================

    def build_form(self):

        form = ctk.CTkScrollableFrame(
            self,
            width=300,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=16
        )
        form.grid(
            row=1,
            column=0,
            padx=(24, 12),
            pady=(0, 24),
            sticky="nsew"
        )

        title_row = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )
        title_row.pack(
            fill="x",
            padx=18,
            pady=(20, 4)
        )

        ctk.CTkLabel(
            title_row,
            text="RM",
            width=40,
            height=40,
            corner_radius=10,
            fg_color=self.SOFT,
            text_color=self.ACCENT,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            title_row,
            text="Room Details",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            form,
            text="Enter room information below.",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 14)
        )

        self.selection_label = ctk.CTkLabel(
            form,
            text="New room registration",
            height=35,
            corner_radius=8,
            fg_color=self.SOFT,
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )
        self.selection_label.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        self.room_number = self.make_entry(
            form,
            "Room Number",
            "Example: A101"
        )

        self.capacity = self.make_entry(
            form,
            "Room Capacity",
            "Enter total number of beds"
        )

        ctk.CTkLabel(
            form,
            text=(
                "Capacity means the total beds "
                "available in this room."
            ),
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            wraplength=260,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 4)
        )

        ctk.CTkFrame(
            form,
            height=1,
            fg_color=self.BORDER
        ).pack(
            fill="x",
            padx=18,
            pady=(22, 16)
        )

        ctk.CTkLabel(
            form,
            text="ROOM ACTIONS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        buttons = [
            ("Add Room", self.add_record),
            ("Update Selected Room", self.update_record),
            ("Delete Selected Room", self.delete_record),
            ("Clear Form", self.clear_form),
        ]

        for index, (text, command) in enumerate(buttons):
            ctk.CTkButton(
                form,
                text=text,
                command=command,
                height=42 if index == 0 else 40,
                corner_radius=10,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold" if index == 0
                    else "normal"
                )
            ).pack(
                fill="x",
                padx=18,
                pady=(0, 9)
            )

        ctk.CTkLabel(
            form,
            text=(
                "Select an existing room before "
                "updating or deleting it."
            ),
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            wraplength=260,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 20)
        )

    def make_entry(self, parent, label, placeholder=""):

        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 6)
        )

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=40,
            corner_radius=9,
            border_color=self.BORDER,
            fg_color=self.SOFT,
            text_color=self.TEXT
        )
        entry.pack(
            fill="x",
            padx=18
        )

        return entry

    # ======================================
    # RIGHT SIDE - ROOM RECORDS
    # ======================================

    def build_records(self):

        right = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=16
        )
        right.grid(
            row=1,
            column=1,
            padx=(0, 24),
            pady=(0, 24),
            sticky="nsew"
        )

        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        heading = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )
        heading.grid(
            row=0,
            column=0,
            padx=18,
            pady=(20, 12),
            sticky="ew"
        )

        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading,
            text="Room Records",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color=self.TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.count_label = ctk.CTkLabel(
            heading,
            text="0 records",
            height=30,
            width=82,
            corner_radius=8,
            fg_color=self.SOFT,
            text_color=self.ACCENT,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )
        self.count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        search_bar = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )
        search_bar.grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 12),
            sticky="ew"
        )
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_input = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search room number",
            height=40,
            corner_radius=9,
            border_color=self.BORDER,
            fg_color=self.SOFT
        )
        self.search_input.grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="ew"
        )

        self.search_input.bind(
            "<Return>",
            self.search_records
        )

        ctk.CTkButton(
            search_bar,
            text="Search",
            width=78,
            height=40,
            corner_radius=9,
            command=self.search_records
        ).grid(
            row=0,
            column=1,
            padx=(0, 8)
        )

        ctk.CTkButton(
            search_bar,
            text="Show All",
            width=78,
            height=40,
            corner_radius=9,
            command=self.show_all
        ).grid(
            row=0,
            column=2
        )

        self.records_frame = ctk.CTkScrollableFrame(
            right,
            fg_color="transparent"
        )
        self.records_frame.grid(
            row=2,
            column=0,
            padx=14,
            pady=(0, 12),
            sticky="nsew"
        )

        self.status = ctk.CTkLabel(
            right,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED
        )
        self.status.grid(
            row=3,
            column=0,
            pady=(0, 14)
        )

    # ======================================
    # FORM DATA
    # ======================================

    def get_form_data(self):
        return (
            self.room_number.get(),
            self.capacity.get()
        )

    def clear_form(self):

        self.selected_room_id = None

        self.room_number.delete(0, "end")
        self.capacity.delete(0, "end")

        self.selection_label.configure(
            text="New room registration",
            text_color=self.MUTED
        )

        for row in self.room_rows.values():
            row.configure(
                border_color=self.BORDER
            )

    # ======================================
    # SELECT ROOM
    # ======================================

    def select_room(self, room):

        self.clear_form()

        self.selected_room_id = room["id"]

        self.room_number.insert(
            0,
            str(room["room_number"])
        )

        self.capacity.insert(
            0,
            str(room["capacity"])
        )

        self.selection_label.configure(
            text=f"Selected: Room {room['room_number']}",
            text_color=self.ACCENT
        )

        selected_row = self.room_rows.get(
            room["id"]
        )

        if selected_row is not None:
            selected_row.configure(
                border_color=self.BLUE
            )

    # ======================================
    # CRUD - ADD
    # ======================================

    def add_record(self):

        try:
            add_room(
                *self.get_form_data()
            )

            messagebox.showinfo(
                "Success",
                "Room added successfully!"
            )

            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ======================================
    # CRUD - UPDATE
    # ======================================

    def update_record(self):

        if self.selected_room_id is None:
            messagebox.showwarning(
                "Select Room",
                "Please select a room first."
            )
            return

        try:
            update_room(
                self.selected_room_id,
                *self.get_form_data()
            )

            messagebox.showinfo(
                "Success",
                "Room updated successfully!"
            )

            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ======================================
    # CRUD - DELETE
    # ======================================

    def delete_record(self):

        if self.selected_room_id is None:
            messagebox.showwarning(
                "Select Room",
                "Please select a room first."
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            "Do you want to delete this room?"
        )

        if not confirmed:
            return

        try:
            deleted = delete_room(
                self.selected_room_id
            )

            if deleted:
                messagebox.showinfo(
                    "Success",
                    "Room deleted successfully!"
                )
            else:
                messagebox.showwarning(
                    "Not Found",
                    "Room no longer exists."
                )

            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror(
                "Delete Error",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ======================================
    # DISPLAY ROOM RECORDS
    # ======================================

    def display_rooms(self, rooms):

        for widget in self.records_frame.winfo_children():
            widget.destroy()

        self.room_rows = {}

        self.count_label.configure(
            text=f"{len(rooms)} records"
        )

        self.status.configure(
            text=f"Showing {len(rooms)} room(s)"
        )

        if not rooms:

            empty = ctk.CTkFrame(
                self.records_frame,
                fg_color=self.SOFT,
                corner_radius=12
            )
            empty.pack(
                fill="x",
                padx=5,
                pady=15
            )

            ctk.CTkLabel(
                empty,
                text="No rooms found",
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                ),
                text_color=self.TEXT
            ).pack(
                pady=(25, 6)
            )

            ctk.CTkLabel(
                empty,
                text="Try another search or add a room.",
                font=ctk.CTkFont(size=12),
                text_color=self.MUTED
            ).pack(
                pady=(0, 25)
            )

            return

        for room in rooms:
            self.create_room_card(room)

    # ======================================
    # PROFESSIONAL ROOM CARD
    # ======================================

    def create_room_card(self, room):

        room_id = room["id"]
        room_number = str(room["room_number"])

        capacity = int(room["capacity"])
        occupied = int(room["occupied"])
        available = int(room["available"])

        ratio = (
            occupied / capacity
            if capacity > 0
            else 0
        )

        ratio = max(0, min(ratio, 1))

        row = ctk.CTkFrame(
            self.records_frame,
            fg_color=self.SOFT,
            border_width=1,
            border_color=(
                self.BLUE
                if self.selected_room_id == room_id
                else self.BORDER
            ),
            corner_radius=12
        )
        row.pack(
            fill="x",
            padx=5,
            pady=6
        )

        row.grid_columnconfigure(1, weight=1)

        self.room_rows[room_id] = row

        # Room icon-style badge
        ctk.CTkLabel(
            row,
            text="RM",
            width=44,
            height=44,
            corner_radius=11,
            fg_color=("#E4EDF9", "#2B4058"),
            text_color=self.ACCENT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(12, 10),
            pady=12
        )

        ctk.CTkLabel(
            row,
            text=f"Room {room_number}",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=self.TEXT,
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(12, 2)
        )

        details = (
            f"Capacity: {capacity}    "
            f"Occupied: {occupied}    "
            f"Available: {available}"
        )

        ctk.CTkLabel(
            row,
            text=details,
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 5)
        )

        progress = ctk.CTkProgressBar(
            row,
            height=7,
            corner_radius=5,
            progress_color=self.BLUE,
            fg_color=self.BORDER
        )
        progress.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=(0, 12)
        )
        progress.set(ratio)

        # Availability status
        is_available = available > 0

        availability_text = (
            f"{available} Available"
            if is_available
            else "Full"
        )

        availability_color = (
            self.GREEN
            if is_available
            else self.RED
        )

        ctk.CTkLabel(
            row,
            text=availability_text,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=availability_color
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=(8, 0)
        )

        ctk.CTkButton(
            row,
            text="Select",
            command=lambda r=room: self.select_room(r),
            width=76,
            height=34,
            corner_radius=8
        ).grid(
            row=1,
            column=2,
            rowspan=2,
            padx=12,
            pady=(0, 10)
        )

    # ======================================
    # SHOW ALL / REFRESH
    # ======================================

    def show_all(self):

        try:
            self.search_input.delete(0, "end")

            self.display_rooms(
                get_rooms()
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ======================================
    # SEARCH ROOMS
    # ======================================

    def search_records(self, event=None):

        try:
            keyword = self.search_input.get().strip()

            if keyword:
                rooms = search_rooms(keyword)
            else:
                rooms = get_rooms()

            self.display_rooms(rooms)

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                str(error)
            )


# ==========================================
# STANDALONE TEST
# ==========================================

if __name__ == "__main__":

    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hostel Management | Room Management")
    app.geometry("1100x700")
    app.minsize(900, 600)

    room_ui = RoomManagementFrame(app)
    room_ui.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    app.mainloop()
