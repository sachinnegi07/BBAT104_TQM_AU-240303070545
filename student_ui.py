
import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from student_service import (
    add_student,
    get_students,
    update_student,
    delete_student,
    search_students,
)


class StudentManagementFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_student_id = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Student Management",
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(
            row=0, column=0, columnspan=2,
            padx=20, pady=20, sticky="w"
        )

        # Student details form
        form = ctk.CTkFrame(self, width=300)
        form.grid(
            row=1, column=0, padx=(20, 10),
            pady=(0, 20), sticky="nsew"
        )

        ctk.CTkLabel(
            form,
            text="Student Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.student_code = self.make_entry(
            form, "Student ID"
        )
        self.full_name = self.make_entry(
            form, "Full Name"
        )
        self.phone = self.make_entry(
            form, "Phone Number"
        )
        self.course = self.make_entry(
            form, "Course"
        )

        buttons = [
            ("Add Student", self.add_record),
            ("Update Student", self.update_record),
            ("Delete Student", self.delete_record),
            ("Clear Form", self.clear_form),
        ]

        for text, command in buttons:
            ctk.CTkButton(
                form,
                text=text,
                command=command,
                height=35
            ).pack(fill="x", padx=20, pady=5)

        # Student list
        right = ctk.CTkFrame(self)
        right.grid(
            row=1, column=1, padx=(0, 20),
            pady=(0, 20), sticky="nsew"
        )

        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right,
            text="Student Records",
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
            placeholder_text="Search by ID or Name"
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

        self.records_frame = ctk.CTkScrollableFrame(right)
        self.records_frame.grid(
            row=2, column=0,
            padx=15, pady=10, sticky="nsew"
        )

        self.status = ctk.CTkLabel(
            right, text="Ready"
        )
        self.status.grid(row=3, column=0, pady=10)

        self.show_all()

    def make_entry(self, parent, label):
        ctk.CTkLabel(
            parent, text=label
        ).pack(anchor="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, width=250)
        entry.pack(fill="x", padx=20)
        return entry

    def get_form_data(self):
        return (
            self.student_code.get(),
            self.full_name.get(),
            self.phone.get(),
            self.course.get()
        )

    def clear_form(self):
        self.selected_student_id = None

        for entry in (
            self.student_code,
            self.full_name,
            self.phone,
            self.course
        ):
            entry.delete(0, "end")

    def add_record(self):
        try:
            add_student(*self.get_form_data())

            messagebox.showinfo(
                "Success", "Student added successfully!"
            )
            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def update_record(self):
        if self.selected_student_id is None:
            messagebox.showwarning(
                "Select Student",
                "Please select a student first."
            )
            return

        try:
            update_student(
                self.selected_student_id,
                *self.get_form_data()
            )

            messagebox.showinfo(
                "Success", "Student updated successfully!"
            )
            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def delete_record(self):
        if self.selected_student_id is None:
            messagebox.showwarning(
                "Select Student",
                "Please select a student first."
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            "Do you want to delete this student?"
        )

        if not confirmed:
            return

        try:
            deleted = delete_student(
                self.selected_student_id
            )

            if not deleted:
                messagebox.showwarning(
                    "Not Found", "Student no longer exists."
                )
            else:
                messagebox.showinfo(
                    "Success", "Student deleted successfully!"
                )

            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror("Delete Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def select_student(self, student):
        self.clear_form()
        self.selected_student_id = student["id"]

        values = [
            student["student_code"],
            student["full_name"],
            student["phone"] or "",
            student["course"] or ""
        ]

        entries = [
            self.student_code,
            self.full_name,
            self.phone,
            self.course
        ]

        for entry, value in zip(entries, values):
            entry.insert(0, value)

    def display_students(self, students):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        if not students:
            ctk.CTkLabel(
                self.records_frame,
                text="No students found."
            ).pack(pady=20)

        for student in students:
            row = ctk.CTkFrame(self.records_frame)
            row.pack(fill="x", padx=5, pady=5)

            details = (
                f"{student['student_code']}  |  "
                f"{student['full_name']}  |  "
                f"{student['course'] or 'N/A'}"
            )

            ctk.CTkLabel(
                row,
                text=details,
                anchor="w",
                wraplength=400
            ).pack(
                side="left", fill="x",
                expand=True, padx=10, pady=10
            )

            ctk.CTkButton(
                row,
                text="Select",
                width=70,
                command=lambda s=student: self.select_student(s)
            ).pack(side="right", padx=10)

        self.status.configure(
            text=f"Showing {len(students)} student(s)"
        )

    def show_all(self):
        try:
            self.search_input.delete(0, "end")
            self.display_students(get_students())
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def search_records(self):
        try:
            keyword = self.search_input.get().strip()

            if keyword:
                students = search_students(keyword)
            else:
                students = get_students()

            self.display_students(students)

        except Exception as error:
            messagebox.showerror("Search Error", str(error))


if __name__ == "__main__":
    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hostel Management | Student Management")
    app.geometry("1100x700")
    app.minsize(900, 600)

    student_ui = StudentManagementFrame(app)
    student_ui.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    app.mainloop()
