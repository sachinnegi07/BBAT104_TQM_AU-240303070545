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
    """Complaint registry UI. Database operations remain in complaint_service."""

    BG = ("#F4F7FB", "#101722")
    CARD = ("#FFFFFF", "#1A2432")
    BORDER = ("#E3E9F1", "#2C394A")
    TEXT = ("#172437", "#F3F6FA")
    MUTED = ("#64748B", "#9AA9BC")
    SOFT = ("#F5F7FB", "#222F40")
    ACCENT = ("#1F6AA5", "#60A5FA")

    STATUS_STYLE = {
        "Pending": {
            "text": ("#B45309", "#FBBF24"),
            "background": ("#FFF4D6", "#453720"),
        },
        "In Progress": {
            "text": ("#1D4ED8", "#93C5FD"),
            "background": ("#E3EEFF", "#253C5A"),
        },
        "Resolved": {
            "text": ("#047857", "#6EE7B7"),
            "background": ("#DFF8ED", "#21483C"),
        },
    }

    def __init__(self, master):
        super().__init__(master, fg_color=self.BG, corner_radius=12)

        self.selected_complaint_id = None
        self.student_options = {}
        self.complaint_rows = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()
        self.build_records()
        self.show_all()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(
            row=0, column=0, columnspan=2, sticky="ew",
            padx=24, pady=(22, 18),
        )

        ctk.CTkLabel(
            header,
            text="STUDENT SUPPORT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.ACCENT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Complaint Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", pady=(5, 2))

        ctk.CTkLabel(
            header,
            text="Register, track and resolve hostel complaints.",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED,
        ).pack(anchor="w")

    # --------------------------------------------------
    # Form (scrollable so all actions stay accessible)
    # --------------------------------------------------
    def build_form(self):
        form = ctk.CTkScrollableFrame(
            self,
            width=325,
            corner_radius=16,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
        )
        form.grid(
            row=1, column=0, padx=(24, 12),
            pady=(0, 24), sticky="nsew",
        )

        title_row = ctk.CTkFrame(form, fg_color="transparent")
        title_row.pack(fill="x", padx=18, pady=(18, 5))

        ctk.CTkLabel(
            title_row, text="CP", width=40, height=40,
            corner_radius=10, fg_color=self.SOFT,
            text_color=self.ACCENT,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            title_row, text="Complaint Details",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.TEXT,
        ).pack(side="left")

        ctk.CTkLabel(
            form, text="Enter complaint information below.",
            font=ctk.CTkFont(size=12), text_color=self.MUTED,
        ).pack(anchor="w", padx=20, pady=(0, 13))

        self.selection_label = ctk.CTkLabel(
            form,
            text="New complaint registration",
            height=35, corner_radius=8,
            fg_color=self.SOFT,
            text_color=self.MUTED,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.selection_label.pack(fill="x", padx=18, pady=(0, 12))

        self.form_label(form, "Select Student")
        self.student_menu = ctk.CTkOptionMenu(
            form, values=["No students available"], height=40,
            corner_radius=9,
        )
        self.student_menu.pack(fill="x", padx=18, pady=(0, 10))

        self.form_label(form, "Complaint Title")
        self.title_entry = ctk.CTkEntry(
            form,
            placeholder_text="Example: Water supply issue",
            height=40, corner_radius=9,
            fg_color=self.SOFT, text_color=self.TEXT,
            border_color=self.BORDER,
        )
        self.title_entry.pack(fill="x", padx=18, pady=(0, 9))

        self.form_label(form, "Description")
        self.description_entry = ctk.CTkTextbox(
            form, height=105, corner_radius=9,
            fg_color=self.SOFT, text_color=self.TEXT,
            border_color=self.BORDER, border_width=1,
            wrap="word",
        )
        self.description_entry.pack(fill="x", padx=18, pady=(0, 9))

        self.form_label(form, "Complaint Status")
        self.status_menu = ctk.CTkOptionMenu(
            form,
            values=["Pending", "In Progress", "Resolved"],
            height=40, corner_radius=9,
        )
        self.status_menu.set("Pending")
        self.status_menu.pack(fill="x", padx=18, pady=(0, 5))

        self.status_help = ctk.CTkLabel(
            form,
            text="New complaints start as Pending. Select a record to change its status.",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            justify="left", wraplength=285,
        )
        self.status_help.pack(anchor="w", padx=20, pady=(0, 8))
        self.status_menu.configure(state="disabled")

        ctk.CTkFrame(
            form, height=1, fg_color=self.BORDER,
        ).pack(fill="x", padx=18, pady=(15, 14))

        ctk.CTkLabel(
            form,
            text="COMPLAINT ACTIONS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.MUTED,
        ).pack(anchor="w", padx=20, pady=(0, 10))

        actions = [
            ("Register Complaint", self.add_record),
            ("Update Selected Complaint", self.update_record),
            ("Delete Selected Complaint", self.delete_record),
            ("Clear Form", self.clear_form),
        ]
        for index, (label, command) in enumerate(actions):
            ctk.CTkButton(
                form,
                text=label,
                command=command,
                height=42 if index == 0 else 40,
                corner_radius=10,
                font=ctk.CTkFont(
                    size=13, weight="bold" if index == 0 else "normal"
                ),
            ).pack(fill="x", padx=18, pady=(0, 9))

        ctk.CTkLabel(
            form,
            text="Deleting a complaint requires confirmation.",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            justify="left", wraplength=285,
        ).pack(anchor="w", padx=20, pady=(7, 20))

    def form_label(self, parent, text):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", padx=20, pady=(11, 6))

    # --------------------------------------------------
    # Complaint records and search
    # --------------------------------------------------
    def build_records(self):
        right = ctk.CTkFrame(
            self,
            fg_color=self.CARD, corner_radius=16,
            border_width=1, border_color=self.BORDER,
        )
        right.grid(
            row=1, column=1, padx=(0, 24),
            pady=(0, 24), sticky="nsew",
        )
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        heading = ctk.CTkFrame(right, fg_color="transparent")
        heading.grid(
            row=0, column=0, sticky="ew",
            padx=18, pady=(20, 12),
        )
        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading,
            text="Complaint Records",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=self.TEXT,
        ).grid(row=0, column=0, sticky="w")

        self.count_label = ctk.CTkLabel(
            heading,
            text="0 records", width=90, height=30,
            corner_radius=8, fg_color=self.SOFT,
            text_color=self.ACCENT,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.count_label.grid(row=0, column=1, sticky="e")

        search_bar = ctk.CTkFrame(right, fg_color="transparent")
        search_bar.grid(
            row=1, column=0, sticky="ew",
            padx=18, pady=(0, 12),
        )
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search complaints, student or title",
            height=40, corner_radius=9,
            fg_color=self.SOFT, border_color=self.BORDER,
        )
        self.search_entry.grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )
        self.search_entry.bind("<Return>", self.search_records)

        ctk.CTkButton(
            search_bar,
            text="Search", width=78, height=40,
            corner_radius=9, command=self.search_records,
        ).grid(row=0, column=1, padx=(0, 8))

        ctk.CTkButton(
            search_bar,
            text="Show All", width=78, height=40,
            corner_radius=9, command=self.show_all,
        ).grid(row=0, column=2)

        self.records_frame = ctk.CTkScrollableFrame(
            right, fg_color="transparent",
        )
        self.records_frame.grid(
            row=2, column=0, padx=14,
            pady=(0, 10), sticky="nsew",
        )

        self.status_label = ctk.CTkLabel(
            right,
            text="Ready", font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        )
        self.status_label.grid(row=3, column=0, pady=(0, 14))

    # --------------------------------------------------
    # Read-only student options; preserve selection by ID
    # --------------------------------------------------
    def load_students(self):
        previous_student_id = self.student_options.get(
            self.student_menu.get()
        )

        students = get_students()
        self.student_options = {
            f"{student['student_code']} - {student['full_name']} "
            f"(ID: {student['id']})": student["id"]
            for student in students
        }
        labels = list(self.student_options)
        self.student_menu.configure(
            values=labels or ["No students available"]
        )
        selected_label = next(
            (
                label
                for label, student_id in self.student_options.items()
                if student_id == previous_student_id
            ),
            labels[0] if labels else "No students available",
        )
        self.student_menu.set(selected_label)

    def get_form_data(self):
        return (
            self.title_entry.get().strip(),
            self.description_entry.get("1.0", "end-1c").strip(),
            self.status_menu.get(),
        )

    def clear_form(self):
        self.selected_complaint_id = None
        self.title_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")
        self.status_menu.configure(state="normal")
        self.status_menu.set("Pending")
        self.status_menu.configure(state="disabled")
        self.student_menu.configure(state="normal")
        self.selection_label.configure(
            text="New complaint registration", text_color=self.MUTED
        )
        self.status_help.configure(
            text="New complaints start as Pending. Select a record to change its status."
        )
        for row in self.complaint_rows.values():
            row.configure(border_color=self.BORDER)

    # --------------------------------------------------
    # CRUD: service calls preserved
    # --------------------------------------------------
    def add_record(self):
        try:
            student_id = self.student_options.get(
                self.student_menu.get()
            )
            if student_id is None:
                raise ValueError("Please select a student first.")

            title, description, _ = self.get_form_data()
            add_complaint(student_id, title, description)

            messagebox.showinfo(
                "Success", "Complaint registered successfully!"
            )
            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def update_record(self):
        if self.selected_complaint_id is None:
            messagebox.showwarning(
                "Select Complaint", "Please select a complaint first."
            )
            return

        try:
            title, description, status = self.get_form_data()
            update_complaint(
                self.selected_complaint_id, title, description, status
            )

            messagebox.showinfo(
                "Success", "Complaint updated successfully!"
            )
            self.clear_form()
            self.show_all()

        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def delete_record(self):
        if self.selected_complaint_id is None:
            messagebox.showwarning(
                "Select Complaint", "Please select a complaint first."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete", "Do you want to delete this complaint?"
        ):
            return

        try:
            deleted = delete_complaint(self.selected_complaint_id)
            if deleted:
                messagebox.showinfo(
                    "Success", "Complaint deleted successfully!"
                )
            else:
                messagebox.showwarning(
                    "Not Found", "Complaint no longer exists."
                )
            self.clear_form()
            self.show_all()

        except Exception as error:
            messagebox.showerror("Delete Error", str(error))

    def select_complaint(self, complaint):
        self.clear_form()
        self.selected_complaint_id = complaint["id"]

        for label, student_id in self.student_options.items():
            if student_id == complaint["student_id"]:
                self.student_menu.set(label)
                break

        # Student is intentionally locked during editing.
        self.student_menu.configure(state="disabled")

        self.title_entry.insert(0, complaint["title"])
        self.description_entry.insert(
            "1.0", complaint["description"] or ""
        )
        self.status_menu.configure(state="normal")
        self.status_menu.set(complaint["status"])

        self.selection_label.configure(
            text=f"Editing Complaint #{complaint['id']}",
            text_color=self.ACCENT,
        )
        self.status_help.configure(
            text="Editing mode: choose a status, then click Update Selected Complaint."
        )

        row = self.complaint_rows.get(complaint["id"])
        if row is not None:
            row.configure(border_color="#3B82F6")

    # --------------------------------------------------
    # Records and status indicators
    # --------------------------------------------------
    def display_complaints(self, complaints):
        for widget in self.records_frame.winfo_children():
            widget.destroy()
        self.complaint_rows = {}

        count = len(complaints)
        self.count_label.configure(text=f"{count} records")
        self.status_label.configure(
            text=f"Showing {count} complaint(s)"
        )

        if not complaints:
            empty = ctk.CTkFrame(
                self.records_frame,
                fg_color=self.SOFT, corner_radius=12,
            )
            empty.pack(fill="x", padx=5, pady=15)
            ctk.CTkLabel(
                empty,
                text="No complaints found",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.TEXT,
            ).pack(pady=(25, 6))
            ctk.CTkLabel(
                empty,
                text="Register a complaint or try another search.",
                font=ctk.CTkFont(size=12),
                text_color=self.MUTED,
            ).pack(pady=(0, 25))
            return

        for complaint in complaints:
            self.create_complaint_card(complaint)

    def create_complaint_card(self, complaint):
        complaint_id = complaint["id"]
        status = str(complaint["status"])
        style = self.STATUS_STYLE.get(
            status,
            {"text": self.ACCENT, "background": self.SOFT},
        )

        row = ctk.CTkFrame(
            self.records_frame,
            fg_color=self.SOFT,
            corner_radius=12,
            border_width=1,
            border_color=(
                "#3B82F6"
                if complaint_id == self.selected_complaint_id
                else self.BORDER
            ),
        )
        row.pack(fill="x", padx=5, pady=6)
        row.grid_columnconfigure(1, weight=1)
        self.complaint_rows[complaint_id] = row

        ctk.CTkLabel(
            row,
            text="CP", width=44, height=44,
            corner_radius=11,
            fg_color=("#E4EDF9", "#2B4058"),
            text_color=self.ACCENT,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, rowspan=2, padx=(12, 10), pady=14)

        ctk.CTkLabel(
            row,
            text=f"#{complaint_id}  {complaint['title']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.TEXT,
            anchor="w", justify="left",
            wraplength=420,
        ).grid(row=0, column=1, sticky="ew", pady=(12, 2))

        student = complaint["full_name"] or "Unknown"
        student_code = complaint["student_code"] or "N/A"
        date = str(complaint.get("created_at") or "")[:10]
        subtitle = f"{student_code}  |  {student}"
        if date:
            subtitle += f"  |  {date}"

        ctk.CTkLabel(
            row,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
            anchor="w", justify="left",
            wraplength=420,
        ).grid(row=1, column=1, sticky="ew", pady=(0, 12))

        ctk.CTkLabel(
            row,
            text=status,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=style["text"],
            fg_color=style["background"],
            corner_radius=8,
            height=27,
        ).grid(row=0, column=2, padx=12, pady=(8, 0))

        ctk.CTkButton(
            row,
            text="Select", width=76, height=34,
            corner_radius=8,
            command=lambda c=complaint: self.select_complaint(c),
        ).grid(row=1, column=2, padx=12, pady=(0, 10))

    # --------------------------------------------------
    # Search and refresh
    # --------------------------------------------------
    def show_all(self):
        try:
            self.load_students()
            self.search_entry.delete(0, "end")
            self.display_complaints(get_complaints())
        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    def search_records(self, event=None):
        try:
            keyword = self.search_entry.get().strip()
            complaints = (
                search_complaints(keyword)
                if keyword else get_complaints()
            )
            self.display_complaints(complaints)
        except Exception as error:
            messagebox.showerror("Search Error", str(error))


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
        fill="both", expand=True, padx=10, pady=10
    )

    app.mainloop()
