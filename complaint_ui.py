
import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from student_service import get_students
from complaint_service import (
    add_complaint,
    get_complaints,
    update_complaint,
    delete_complaint,
    search_complaints,
)


class ComplaintManagementFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.selected_complaint_id = None
        self.student_options = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Complaint Management",
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=20,
            sticky="w"
        )

        # LEFT: Complaint Form
        form = ctk.CTkScrollableFrame(
            self,
            width=310
        )
        form.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 20),
            sticky="nsew"
        )

        ctk.CTkLabel(
            form,
            text="Complaint Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 20))

        ctk.CTkLabel(
            form,
            text="Select Student"
        ).pack(anchor="w", padx=15)

        self.student_menu = ctk.CTkOptionMenu(
            form,
            values=["No students available"]
        )
        self.student_menu.pack(
            fill="x", padx=15, pady=(5, 15)
        )

        ctk.CTkLabel(
            form,
            text="Complaint Title"
        ).pack(anchor="w", padx=15)

        self.title_entry = ctk.CTkEntry(
            form,
            placeholder_text="Enter complaint title"
        )
        self.title_entry.pack(
            fill="x", padx=15, pady=(5, 15)
        )

        ctk.CTkLabel(
            form,
            text="Description"
        ).pack(anchor="w", padx=15)

        self.description_entry = ctk.CTkTextbox(
            form,
            height=100
        )
        self.description_entry.pack(
            fill="x", padx=15, pady=(5, 15)
        )

        ctk.CTkLabel(
            form,
            text="Complaint Status"
        ).pack(anchor="w", padx=15)

        self.status_menu = ctk.CTkOptionMenu(
            form,
            values=[
                "Pending",
                "In Progress",
                "Resolved"
            ]
        )
        self.status_menu.set("Pending")
        self.status_menu.pack(
            fill="x", padx=15, pady=(5, 20)
        )

        actions = [
            ("Register Complaint", self.add_record),
            ("Update Complaint", self.update_record),
            ("Delete Complaint", self.delete_record),
            ("Clear Form", self.clear_form),
        ]

        for label, command in actions:
            ctk.CTkButton(
                form,
                text=label,
                command=command,
                height=38
            ).pack(fill="x", padx=15, pady=5)

        # RIGHT: Complaint Records
        right = ctk.CTkFrame(self)
        right.grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=(0, 20),
            sticky="nsew"
        )
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right,
            text="Complaint Records",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=15)

        search_bar = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )
        search_bar.grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="ew"
        )
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search complaints"
        )
        self.search_entry.grid(
            row=0,
            column=0,
            padx=5,
            sticky="ew"
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
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="nsew"
        )

        self.status_label = ctk.CTkLabel(
            right,
            text="Ready"
        )
        self.status_label.grid(
            row=3,
            column=0,
            pady=10
        )

        self.show_all()

    # LOAD STUDENTS
    def load_students(self):
        previous_student_id = self.student_options.get(
            self.student_menu.get()
        )

        students = get_students()

        self.student_options = {
            f"{s['student_code']} - {s['full_name']} "
            f"(ID: {s['id']})": s["id"]
            for s in students
        }

        labels = list(self.student_options)

        self.student_menu.configure(
            values=labels or ["No students available"]
        )

        selected_label = next(
            (
                label
                for label, student_id
                in self.student_options.items()
                if student_id == previous_student_id
            ),
            labels[0] if labels else "No students available"
        )

        self.student_menu.set(selected_label)

    # READ FORM DATA
    def get_form_data(self):
        return (
            self.title_entry.get().strip(),
            self.description_entry.get(
                "1.0", "end-1c"
            ).strip(),
            self.status_menu.get()
        )

    # CLEAR FORM
    def clear_form(self):
        self.selected_complaint_id = None

        self.title_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")
        self.status_menu.set("Pending")

        self.student_menu.configure(state="normal")

    # ADD COMPLAINT
    def add_record(self):
        try:
            student_id = self.student_options.get(
                self.student_menu.get()
            )

            if student_id is None:
                raise ValueError(
                    "Please select a student first."
                )

            title, description, _ = self.get_form_data()

            add_complaint(
                student_id,
                title,
                description
            )

            messagebox.showinfo(
                "Success",
                "Complaint registered successfully!"
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

    # UPDATE COMPLAINT
    def update_record(self):
        if self.selected_complaint_id is None:
            messagebox.showwarning(
                "Select Complaint",
                "Please select a complaint first."
            )
            return

        try:
            title, description, status = self.get_form_data()

            update_complaint(
                self.selected_complaint_id,
                title,
                description,
                status
            )

            messagebox.showinfo(
                "Success",
                "Complaint updated successfully!"
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

    # DELETE COMPLAINT
    def delete_record(self):
        if self.selected_complaint_id is None:
            messagebox.showwarning(
                "Select Complaint",
                "Please select a complaint first."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Do you want to delete this complaint?"
        ):
            return

        try:
            deleted = delete_complaint(
                self.selected_complaint_id
            )

            if deleted:
                messagebox.showinfo(
                    "Success",
                    "Complaint deleted successfully!"
                )
            else:
                messagebox.showwarning(
                    "Not Found",
                    "Complaint no longer exists."
                )

            self.clear_form()
            self.show_all()

        except Exception as error:
            messagebox.showerror(
                "Delete Error", str(error)
            )

    # SELECT COMPLAINT
    def select_complaint(self, complaint):
        self.clear_form()

        self.selected_complaint_id = complaint["id"]

        for label, student_id in self.student_options.items():
            if student_id == complaint["student_id"]:
                self.student_menu.set(label)
                break

        # Student cannot be changed during edit
        self.student_menu.configure(state="disabled")

        self.title_entry.insert(
            0, complaint["title"]
        )

        self.description_entry.insert(
            "1.0",
            complaint["description"] or ""
        )

        self.status_menu.set(
            complaint["status"]
        )

    # DISPLAY RECORDS
    def display_complaints(self, complaints):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        if not complaints:
            ctk.CTkLabel(
                self.records_frame,
                text="No complaints found."
            ).pack(pady=20)

        for complaint in complaints:
            row = ctk.CTkFrame(self.records_frame)
            row.pack(
                fill="x",
                padx=5,
                pady=5
            )

            details = (
                f"#{complaint['id']} | "
                f"{complaint['student_code']} | "
                f"{complaint['title']}\n"
                f"Student: {complaint['full_name']}\n"
                f"Status: {complaint['status']}"
            )

            ctk.CTkLabel(
                row,
                text=details,
                anchor="w",
                justify="left",
                wraplength=440
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
                width=75,
                command=lambda c=complaint:
                    self.select_complaint(c)
            ).pack(side="right", padx=10)

        self.status_label.configure(
            text=f"Showing {len(complaints)} complaint(s)"
        )

    # SHOW ALL
    def show_all(self):
        try:
            self.load_students()
            self.search_entry.delete(0, "end")
            self.display_complaints(get_complaints())

        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

    # SEARCH
    def search_records(self):
        try:
            keyword = self.search_entry.get().strip()

            complaints = (
                search_complaints(keyword)
                if keyword
                else get_complaints()
            )

            self.display_complaints(complaints)

        except Exception as error:
            messagebox.showerror(
                "Search Error", str(error)
            )


if __name__ == "__main__":
    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hostel Management | Complaints")
    app.geometry("1150x720")
    app.minsize(950, 600)

    complaint_ui = ComplaintManagementFrame(app)
    complaint_ui.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    app.mainloop()
