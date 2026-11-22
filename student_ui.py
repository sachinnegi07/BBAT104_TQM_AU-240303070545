
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

    BG = ("#F4F7FB", "#101722")
    CARD = ("#FFFFFF", "#1A2432")
    BORDER = ("#E3E9F1", "#2C394A")
    TEXT = ("#172437", "#F3F6FA")
    MUTED = ("#64748B", "#9AA9BC")
    SOFT = ("#F5F7FB", "#222F40")
    ACCENT = ("#1F6AA5", "#60A5FA")

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=self.BG,
            corner_radius=12
        )

        self.selected_student_id = None
        self.student_rows = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()
        self.build_records()

        self.show_all()

    # ======================================
    # HEADER
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
            text="STUDENT REGISTRY",
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
            text="Student Management",
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
            text="Manage student profiles, records and registration.",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

    # ======================================
    # STUDENT FORM
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

        self.form_frame = form

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
            text="ST",
            width=38,
            height=38,
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
            text="Student Details",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            form,
            text="Enter student information below.",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        self.selection_label = ctk.CTkLabel(
            form,
            text="New student registration",
            fg_color=self.SOFT,
            corner_radius=8,
            height=34,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        )
        self.selection_label.pack(
            fill="x",
            padx=18,
            pady=(0, 12)
        )

        self.student_code = self.make_entry(
            form,
            "Student ID",
            "Enter registration ID"
        )

        self.full_name = self.make_entry(
            form,
            "Full Name",
            "Enter full name"
        )

        self.phone = self.make_entry(
            form,
            "Phone Number",
            "Enter phone number"
        )

        self.course = self.make_entry(
            form,
            "Course",
            "Example: BCA"
        )

        ctk.CTkFrame(
            form,
            height=1,
            fg_color=self.BORDER
        ).pack(
            fill="x",
            padx=18,
            pady=(20, 14)
        )

        ctk.CTkLabel(
            form,
            text="RECORD ACTIONS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkButton(
            form,
            text="Add Student",
            command=self.add_record,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        ctk.CTkButton(
            form,
            text="Update Selected Student",
            command=self.update_record,
            height=40,
            corner_radius=10
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        ctk.CTkButton(
            form,
            text="Delete Selected Student",
            command=self.delete_record,
            height=40,
            corner_radius=10
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        ctk.CTkButton(
            form,
            text="Clear Form",
            command=self.clear_form,
            height=38,
            corner_radius=10
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 20)
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
            height=39,
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
    # STUDENT RECORDS PANEL
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
            sticky="ew",
            padx=18,
            pady=(20, 12)
        )

        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading,
            text="Student Records",
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
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            fg_color=self.SOFT,
            text_color=self.ACCENT,
            corner_radius=8,
            height=30,
            width=78
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
            sticky="ew",
            padx=18,
            pady=(0, 12)
        )

        search_bar.grid_columnconfigure(0, weight=1)

        self.search_input = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search student ID or name",
            height=40,
            corner_radius=9,
            border_color=self.BORDER,
            fg_color=self.SOFT
        )
        self.search_input.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        self.search_input.bind(
            "<Return>",
            self.search_records
        )

        ctk.CTkButton(
            search_bar,
            text="Search",
            command=self.search_records,
            width=76,
            height=40,
            corner_radius=9
        ).grid(
            row=0,
            column=1,
            padx=(0, 8)
        )

        ctk.CTkButton(
            search_bar,
            text="Show All",
            command=self.show_all,
            width=76,
            height=40,
            corner_radius=9
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
            pady=(0, 10),
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
    # FORM DATA AND SELECTION
    # ======================================

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

        self.selection_label.configure(
            text="New student registration",
            text_color=self.MUTED
        )

        for row in self.student_rows.values():
            row.configure(
                border_color=self.BORDER
            )

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
            entry.insert(0, str(value))

        self.selection_label.configure(
            text=f"Selected: {student['student_code']}",
            text_color=self.ACCENT
        )

        selected_row = self.student_rows.get(
            student["id"]
        )

        if selected_row is not None:
            selected_row.configure(
                border_color="#3B82F6"
            )

    # ======================================
    # CRUD OPERATIONS
    # ======================================

    def add_record(self):
        try:
            add_student(*self.get_form_data())

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
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
                "Success",
                "Student updated successfully!"
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
                    "Not Found",
                    "Student no longer exists."
                )
            else:
                messagebox.showinfo(
                    "Success",
                    "Student deleted successfully!"
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
    # RECORDS DISPLAY
    # ======================================

    def display_students(self, students):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        self.student_rows = {}

        self.count_label.configure(
            text=f"{len(students)} records"
        )

        self.status.configure(
            text=f"Showing {len(students)} student(s)"
        )

        if not students:
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
                text="No students found",
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
                text="Try another search or add a student.",
                font=ctk.CTkFont(size=12),
                text_color=self.MUTED
            ).pack(
                pady=(0, 25)
            )
            return

        for student in students:
            row = ctk.CTkFrame(
                self.records_frame,
                fg_color=self.SOFT,
                border_width=1,
                border_color=(
                    "#3B82F6"
                    if self.selected_student_id == student["id"]
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

            self.student_rows[student["id"]] = row

            name = str(
                student["full_name"] or "Unknown"
            )

            initials = "".join(
                part[0]
                for part in name.split()[:2]
                if part
            ).upper() or "ST"

            ctk.CTkLabel(
                row,
                text=initials,
                width=44,
                height=44,
                corner_radius=11,
                fg_color=("#E4EDF9", "#2B4058"),
                text_color=self.ACCENT,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(12, 10),
                pady=13
            )

            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(
                    size=13,
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

            code = str(
                student["student_code"]
            )

            course = str(
                student["course"] or "N/A"
            )

            ctk.CTkLabel(
                row,
                text=f"ID: {code}  |  {course}",
                font=ctk.CTkFont(size=11),
                text_color=self.MUTED,
                anchor="w"
            ).grid(
                row=1,
                column=1,
                sticky="ew",
                pady=(0, 12)
            )

            ctk.CTkButton(
                row,
                text="Select",
                width=68,
                height=34,
                corner_radius=8,
                command=lambda s=student:
                    self.select_student(s)
            ).grid(
                row=0,
                column=2,
                rowspan=2,
                padx=12,
                pady=12
            )

    # ======================================
    # SEARCH AND REFRESH
    # ======================================

    def show_all(self):
        try:
            self.search_input.delete(0, "end")
            self.display_students(
                get_students()
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def search_records(self, event=None):
        try:
            keyword = self.search_input.get().strip()

            if keyword:
                students = search_students(keyword)
            else:
                students = get_students()

            self.display_students(students)

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
