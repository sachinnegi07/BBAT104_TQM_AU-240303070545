
import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from student_service import get_students
from room_service import get_rooms
from allocation_service import get_allocations
from complaint_service import get_complaints

from student_ui import StudentManagementFrame
from room_ui import RoomManagementFrame
from allocation_ui import AllocationManagementFrame
from complaint_ui import ComplaintManagementFrame
from calendar_ui import HostelCalendarFrame

from themes import apply_accent_theme


# ==========================================
# DASHBOARD
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.metric_labels = {}

        ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(
            row=0, column=0, columnspan=2,
            padx=25, pady=(25, 10), sticky="w"
        )

        ctk.CTkButton(
            self,
            text="Refresh Dashboard",
            command=self.refresh_dashboard,
            width=160
        ).grid(
            row=0, column=2,
            padx=25, pady=(25, 10), sticky="e"
        )

        metrics = [
            ("Total Students", "students"),
            ("Total Rooms", "rooms"),
            ("Occupied Beds", "occupied"),
            ("Available Beds", "available"),
            ("Active Allocations", "allocations"),
            ("Pending Complaints", "pending"),
        ]

        for index, (title, key) in enumerate(metrics):
            row = 1 + index // 3
            column = index % 3

            card = ctk.CTkFrame(
                self,
                corner_radius=15,
                height=150
            )
            card.grid(
                row=row, column=column,
                padx=12, pady=12, sticky="nsew"
            )
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=16),
                text_color=("gray35", "gray75")
            ).pack(pady=(28, 8))

            value_label = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=38, weight="bold"
                )
            )
            value_label.pack()

            self.metric_labels[key] = value_label

        ctk.CTkLabel(
            self,
            text="Recent Complaints",
            font=ctk.CTkFont(size=21, weight="bold")
        ).grid(
            row=3, column=0, columnspan=3,
            padx=25, pady=(20, 8), sticky="w"
        )

        self.recent_frame = ctk.CTkScrollableFrame(
            self,
            height=180
        )
        self.recent_frame.grid(
            row=4, column=0, columnspan=3,
            padx=25, pady=(0, 20), sticky="nsew"
        )

        self.grid_rowconfigure(4, weight=1)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        try:
            students = get_students()
            rooms = get_rooms()
            allocations = get_allocations()
            complaints = get_complaints()

            metrics = {
                "students": len(students),
                "rooms": len(rooms),
                "occupied": sum(
                    r["occupied"] for r in rooms
                ),
                "available": sum(
                    r["available"] for r in rooms
                ),
                "allocations": len(allocations),
                "pending": sum(
                    1 for c in complaints
                    if c["status"] == "Pending"
                ),
            }

            for key, value in metrics.items():
                self.metric_labels[key].configure(
                    text=str(value)
                )

            for widget in self.recent_frame.winfo_children():
                widget.destroy()

            if not complaints:
                ctk.CTkLabel(
                    self.recent_frame,
                    text="No complaints registered yet."
                ).pack(pady=20)

            for complaint in complaints[:5]:
                details = (
                    f"#{complaint['id']} | "
                    f"{complaint['title']} | "
                    f"{complaint['full_name']} | "
                    f"{complaint['status']}"
                )

                ctk.CTkLabel(
                    self.recent_frame,
                    text=details,
                    anchor="w"
                ).pack(
                    fill="x", padx=15, pady=8
                )

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                str(error)
            )


# ==========================================
# MAIN APPLICATION
# ==========================================

class HostelManagementApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(
            "Hostel Management System | BBAT104"
        )
        self.geometry("1350x800")
        self.minsize(1100, 650)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_page = None

        # Track selected accent theme
        self.accent_theme_name = "Blue"

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0, column=0, sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="HOSTEL HMS",
            font=ctk.CTkFont(
                size=24, weight="bold"
            )
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="BBAT104 | Q03",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(0, 35))

        pages = [
    ("Dashboard", DashboardFrame),
    ("Students", StudentManagementFrame),
    ("Rooms", RoomManagementFrame),
    ("Allocations", AllocationManagementFrame),
    ("Complaints", ComplaintManagementFrame),
    ("Calendar", HostelCalendarFrame),
]

        for name, frame_class in pages:
            ctk.CTkButton(
                self.sidebar,
                text=name,
                height=43,
                anchor="w",
                command=lambda n=name, f=frame_class:
                    self.show_page(n, f)
            ).pack(
                fill="x",
                padx=15,
                pady=6
            )

        # Appearance Mode
        ctk.CTkLabel(
            self.sidebar,
            text="Appearance Mode"
        ).pack(pady=(35, 10))

        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["System", "Light", "Dark"],
            command=ctk.set_appearance_mode
        )
        self.appearance_menu.set("System")
        self.appearance_menu.pack(
            fill="x", padx=15
        )

        # NEW - Custom Accent Theme
        ctk.CTkLabel(
            self.sidebar,
            text="Custom Theme"
        ).pack(pady=(20, 10))

        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Blue", "Green", "Purple"],
            command=self.change_accent_theme
        )
        self.theme_menu.set("Blue")
        self.theme_menu.pack(
            fill="x", padx=15
        )

        # Main content area
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.grid(
            row=0, column=1,
            padx=12, pady=12, sticky="nsew"
        )

        self.show_page(
            "Dashboard",
            DashboardFrame
        )

    # ==========================================
    # CUSTOM THEME HANDLER
    # ==========================================

    def change_accent_theme(self, theme_name):
        try:
            apply_accent_theme(self, theme_name)
            self.accent_theme_name = theme_name

        except Exception as error:
            messagebox.showerror(
                "Theme Error",
                str(error)
            )

    # ==========================================
    # NAVIGATION
    # ==========================================

    def show_page(self, name, frame_class):
        try:
            # Create new page first
            new_page = frame_class(self.content)

            old_page = self.current_page

            new_page.pack(
                fill="both",
                expand=True
            )

            self.current_page = new_page

            if old_page is not None:
                old_page.destroy()

            # Reapply theme to newly opened modules
            apply_accent_theme(
                self,
                self.accent_theme_name
            )

        except Exception as error:
            messagebox.showerror(
                "Navigation Error",
                f"Cannot open {name}:\n{error}"
            )


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = HostelManagementApp()
    app.mainloop()
