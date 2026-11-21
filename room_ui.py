
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

    def __init__(self, master):
        super().__init__(master)

        self.selected_room_id = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Room Management",
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(
            row=0, column=0, columnspan=2,
            padx=20, pady=20, sticky="w"
        )

        # LEFT SIDE - Room Form
        form = ctk.CTkFrame(self, width=300)
        form.grid(
            row=1, column=0,
            padx=(20, 10), pady=(0, 20),
            sticky="nsew"
        )

        ctk.CTkLabel(
            form,
            text="Room Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.room_number = self.make_entry(
            form, "Room Number"
        )

        self.capacity = self.make_entry(
            form, "Room Capacity"
        )

        buttons = [
            ("Add Room", self.add_record),
            ("Update Room", self.update_record),
            ("Delete Room", self.delete_record),
            ("Clear Form", self.clear_form),
        ]

        for text, command in buttons:
            ctk.CTkButton(
                form,
                text=text,
                command=command,
                height=38
            ).pack(
                fill="x", padx=20, pady=7
            )

        # RIGHT SIDE - Room Records
        right = ctk.CTkFrame(self)
        right.grid(
            row=1, column=1,
            padx=(0, 20), pady=(0, 20),
            sticky="nsew"
        )

        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right,
            text="Room Records",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=15)

        search_bar = ctk.CTkFrame(
            right, fg_color="transparent"
        )
        search_bar.grid(
            row=1, column=0,
            padx=15, pady=10, sticky="ew"
        )
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_input = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search Room Number"
        )
        self.search_input.grid(
            row=0, column=0,
            padx=5, sticky="ew"
        )

        ctk.CTkButton(
            search_bar,
            text="Search",
            width=80,
            command=self.search_records
        ).grid(row=0, column=1, padx=5)

        ctk.CTkButton(
            search_bar,
            text="Show All",
            width=80,
            command=self.show_all
        ).grid(row=0, column=2, padx=5)

        self.records_frame = ctk.CTkScrollableFrame(
            right
        )
        self.records_frame.grid(
            row=2, column=0,
            padx=15, pady=10,
            sticky="nsew"
        )

        self.status = ctk.CTkLabel(
            right, text="Ready"
        )
        self.status.grid(
            row=3, column=0, pady=10
        )

        self.show_all()

    def make_entry(self, parent, label):
        ctk.CTkLabel(
            parent, text=label
        ).pack(
            anchor="w",
            padx=20, pady=(10, 2)
        )

        entry = ctk.CTkEntry(
            parent, width=250
        )
        entry.pack(
            fill="x", padx=20
        )
        return entry

    def get_form_data(self):
        return (
            self.room_number.get(),
            self.capacity.get()
        )

    def clear_form(self):
        self.selected_room_id = None

        self.room_number.delete(0, "end")
        self.capacity.delete(0, "end")

    def add_record(self):
        try:
            add_room(*self.get_form_data())

            messagebox.showinfo(
                "Success",
                "Room added successfully!"
            )

            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror(
                "Validation Error", str(error)
            )
        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

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
                "Validation Error", str(error)
            )
        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

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
                "Delete Error", str(error)
            )
        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

    def select_room(self, room):
        self.clear_form()

        self.selected_room_id = room["id"]

        self.room_number.insert(
            0, room["room_number"]
        )

        self.capacity.insert(
            0, str(room["capacity"])
        )

    def display_rooms(self, rooms):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        if not rooms:
            ctk.CTkLabel(
                self.records_frame,
                text="No rooms found."
            ).pack(pady=20)

        for room in rooms:
            row = ctk.CTkFrame(
                self.records_frame
            )
            row.pack(
                fill="x", padx=5, pady=5
            )

            details = (
                f"Room {room['room_number']}  |  "
                f"Capacity: {room['capacity']}  |  "
                f"Occupied: {room['occupied']}  |  "
                f"Available: {room['available']}"
            )

            ctk.CTkLabel(
                row,
                text=details,
                anchor="w",
                wraplength=500
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=10
            )

            ctk.CTkButton(
                row,
                text="Select",
                width=70,
                command=lambda r=room: self.select_room(r)
            ).pack(
                side="right", padx=10
            )

        self.status.configure(
            text=f"Showing {len(rooms)} room(s)"
        )

    def show_all(self):
        try:
            self.search_input.delete(0, "end")
            self.display_rooms(get_rooms())

        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

    def search_records(self):
        try:
            keyword = self.search_input.get().strip()

            if keyword:
                rooms = search_rooms(keyword)
            else:
                rooms = get_rooms()

            self.display_rooms(rooms)

        except Exception as error:
            messagebox.showerror(
                "Search Error", str(error)
            )


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
