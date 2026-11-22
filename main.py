
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

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

from themes import apply_accent_theme, THEME_COLORS


# ==========================================
# DASHBOARD V2 - PROFESSIONAL UI
# ==========================================

class DashboardFrame(ctk.CTkFrame):

    BG = ("#F4F7FB", "#101722")
    CARD = ("#FFFFFF", "#1A2432")
    BORDER = ("#E3E9F1", "#2C394A")
    TEXT = ("#172437", "#F3F6FA")
    MUTED = ("#64748B", "#9AA9BC")
    SOFT = ("#F5F7FB", "#222F40")

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=self.BG,
            corner_radius=12
        )

        self.metric_labels = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.scroll.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scroll.grid_columnconfigure(0, weight=1)

        self.build_header()
        self.build_metrics()
        self.build_bottom_sections()

        self.refresh_dashboard()

    # --------------------------------------
    # HEADER
    # --------------------------------------

    def build_header(self):

        header = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=24,
            pady=(24, 22)
        )

        header.grid_columnconfigure(0, weight=1)

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_area,
            text="HOSTEL OPERATIONS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="#3B82F6"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="Dashboard Overview",
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            anchor="w",
            pady=(6, 3)
        )

        ctk.CTkLabel(
            title_area,
            text="Monitor hostel capacity, allocations and complaints.",
            font=ctk.CTkFont(size=13),
            text_color=self.MUTED
        ).pack(anchor="w")

        self.refresh_button = ctk.CTkButton(
            header,
            text="Refresh Dashboard",
            command=self.refresh_dashboard,
            height=40,
            width=160,
            corner_radius=10,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )
        self.refresh_button.grid(
            row=0,
            column=1,
            padx=(16, 0),
            sticky="e"
        )

    # --------------------------------------
    # METRIC CARDS
    # --------------------------------------

    def build_metrics(self):

        container = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )
        container.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=24
        )

        for column in range(3):
            container.grid_columnconfigure(
                column,
                weight=1,
                uniform="metrics"
            )

        metrics = [
            {
                "title": "Total Students",
                "key": "students",
                "code": "ST",
                "color": "#3B82F6",
                "description": "Registered students"
            },
            {
                "title": "Total Rooms",
                "key": "rooms",
                "code": "RM",
                "color": "#8B5CF6",
                "description": "Hostel rooms"
            },
            {
                "title": "Occupied Beds",
                "key": "occupied",
                "code": "OC",
                "color": "#F59E0B",
                "description": "Beds currently occupied"
            },
            {
                "title": "Available Beds",
                "key": "available",
                "code": "AV",
                "color": "#10B981",
                "description": "Beds ready for allocation"
            },
            {
                "title": "Active Allocations",
                "key": "allocations",
                "code": "AL",
                "color": "#06B6D4",
                "description": "Current room assignments"
            },
            {
                "title": "Pending Complaints",
                "key": "pending",
                "code": "CP",
                "color": "#EF4444",
                "description": "Complaints awaiting action"
            }
        ]

        for index, metric in enumerate(metrics):

            row = index // 3
            column = index % 3

            card = ctk.CTkFrame(
                container,
                fg_color=self.CARD,
                border_width=1,
                border_color=self.BORDER,
                corner_radius=16,
                height=185
            )

            card.grid(
                row=row,
                column=column,
                padx=(0, 12) if column < 2 else (0, 0),
                pady=(0, 12),
                sticky="nsew"
            )

            card.grid_propagate(False)

            top = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            top.pack(
                fill="x",
                padx=18,
                pady=(16, 4)
            )

            ctk.CTkLabel(
                top,
                text=metric["title"],
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=self.MUTED
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                top,
                text=metric["code"],
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                text_color=metric["color"],
                width=32,
                height=28,
                corner_radius=8,
                fg_color=self.SOFT
            ).pack(side="right")

            value_label = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=36,
                    weight="bold"
                ),
                text_color=self.TEXT
            )
            value_label.pack(
                anchor="w",
                padx=18,
                pady=(4, 0)
            )

            ctk.CTkLabel(
                card,
                text=metric["description"],
                font=ctk.CTkFont(size=11),
                text_color=self.MUTED
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 16)
            )

            self.metric_labels[
                metric["key"]
            ] = value_label

    # --------------------------------------
    # COMPLAINTS AND OCCUPANCY
    # --------------------------------------

    def build_bottom_sections(self):

        sections = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )
        sections.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=24,
            pady=(12, 14)
        )

        sections.grid_columnconfigure(0, weight=3)
        sections.grid_columnconfigure(1, weight=2)

        # Recent complaints panel
        complaints_card = ctk.CTkFrame(
            sections,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=16
        )
        complaints_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        ctk.CTkLabel(
            complaints_card,
            text="Recent Complaints",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            complaints_card,
            text="Latest registered complaints",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.recent_frame = ctk.CTkFrame(
            complaints_card,
            fg_color="transparent"
        )
        self.recent_frame.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(0, 18)
        )

        # Occupancy panel
        occupancy_card = ctk.CTkFrame(
            sections,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=16
        )
        occupancy_card.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        ctk.CTkLabel(
            occupancy_card,
            text="Room Utilization",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            occupancy_card,
            text="Current hostel occupancy",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        self.occupancy_label = ctk.CTkLabel(
            occupancy_card,
            text="0%",
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            ),
            text_color=self.TEXT
        )
        self.occupancy_label.pack(
            anchor="w",
            padx=20
        )

        self.occupancy_bar = ctk.CTkProgressBar(
            occupancy_card,
            height=12,
            corner_radius=8,
            progress_color="#3B82F6",
            fg_color=self.SOFT
        )
        self.occupancy_bar.pack(
            fill="x",
            padx=20,
            pady=(12, 18)
        )
        self.occupancy_bar.set(0)

        self.bed_summary = ctk.CTkLabel(
            occupancy_card,
            text="0 occupied / 0 total beds",
            font=ctk.CTkFont(size=12),
            text_color=self.MUTED
        )
        self.bed_summary.pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        divider = ctk.CTkFrame(
            occupancy_card,
            height=1,
            fg_color=self.BORDER
        )
        divider.pack(
            fill="x",
            padx=20,
            pady=(4, 14)
        )

        self.available_summary = ctk.CTkLabel(
            occupancy_card,
            text="Available beds: 0",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#10B981"
        )
        self.available_summary.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        self.last_updated_label = ctk.CTkLabel(
            self.scroll,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED
        )
        self.last_updated_label.grid(
            row=3,
            column=0,
            padx=26,
            pady=(0, 16),
            sticky="w"
        )

    # --------------------------------------
    # RECENT COMPLAINT RENDERING
    # --------------------------------------

    def render_complaints(self, complaints):

        for widget in self.recent_frame.winfo_children():
            widget.destroy()

        if not complaints:

            empty = ctk.CTkFrame(
                self.recent_frame,
                fg_color=self.SOFT,
                corner_radius=12
            )
            empty.pack(
                fill="x",
                pady=6
            )

            ctk.CTkLabel(
                empty,
                text="No complaints registered",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                text_color=self.TEXT
            ).pack(pady=(22, 5))

            ctk.CTkLabel(
                empty,
                text="New complaints will appear here.",
                font=ctk.CTkFont(size=12),
                text_color=self.MUTED
            ).pack(pady=(0, 22))

            return

        status_colors = {
            "Pending": "#EF4444",
            "In Progress": "#F59E0B",
            "Resolved": "#10B981"
        }

        for complaint in complaints[:5]:

            item = ctk.CTkFrame(
                self.recent_frame,
                fg_color=self.SOFT,
                corner_radius=10
            )
            item.pack(
                fill="x",
                pady=5
            )

            item.grid_columnconfigure(0, weight=1)

            title = str(
                complaint.get("title") or "Untitled"
            )

            if len(title) > 40:
                title = title[:37] + "..."

            complaint_id = complaint.get("id", "-")
            status = str(
                complaint.get("status") or "Pending"
            )

            ctk.CTkLabel(
                item,
                text=f"#{complaint_id}  {title}",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                text_color=self.TEXT,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=12,
                pady=(10, 2)
            )

            ctk.CTkLabel(
                item,
                text=status,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                text_color=status_colors.get(
                    status, "#3B82F6"
                )
            ).grid(
                row=0,
                column=1,
                padx=12,
                pady=(10, 2)
            )

            student_name = str(
                complaint.get("full_name") or "Unknown"
            )

            ctk.CTkLabel(
                item,
                text=student_name,
                font=ctk.CTkFont(size=11),
                text_color=self.MUTED,
                anchor="w"
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="w",
                padx=12,
                pady=(0, 10)
            )

    # --------------------------------------
    # LIVE DATA REFRESH
    # --------------------------------------

    def refresh_dashboard(self):

        try:
            students = get_students()
            rooms = get_rooms()
            allocations = get_allocations()
            complaints = get_complaints()

            occupied = sum(
                int(room["occupied"])
                for room in rooms
            )

            available = sum(
                int(room["available"])
                for room in rooms
            )

            total_beds = occupied + available

            metrics = {
                "students": len(students),
                "rooms": len(rooms),
                "occupied": occupied,
                "available": available,
                "allocations": len(allocations),
                "pending": sum(
                    1 for complaint in complaints
                    if complaint["status"] == "Pending"
                )
            }

            for key, value in metrics.items():
                self.metric_labels[key].configure(
                    text=str(value)
                )

            occupancy_ratio = (
                occupied / total_beds
                if total_beds > 0
                else 0
            )

            self.occupancy_bar.set(
                occupancy_ratio
            )

            self.occupancy_label.configure(
                text=f"{occupancy_ratio * 100:.0f}%"
            )

            self.bed_summary.configure(
                text=(
                    f"{occupied} occupied / "
                    f"{total_beds} total beds"
                )
            )

            self.available_summary.configure(
                text=f"Available beds: {available}"
            )

            self.render_complaints(complaints)

            timestamp = datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )

            self.last_updated_label.configure(
                text=f"Last refreshed: {timestamp}"
            )

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                str(error)
            )


# ==========================================
# MAIN APPLICATION
# EXISTING NAVIGATION PRESERVED
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
        self.accent_theme_name = "Blue"
        self.active_page_name = None
        self.nav_buttons = {}

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="HOSTEL HMS",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
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
            button = ctk.CTkButton(
                self.sidebar,
                text=f"  {name}",
                height=44,
                corner_radius=10,
                border_spacing=10,
                anchor="w",
                font=ctk.CTkFont(size=14),
                command=lambda n=name, f=frame_class:
                    self.show_page(n, f)
            )
            button.pack(
                fill="x",
                padx=14,
                pady=4
            )
            self.nav_buttons[name] = button

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
            fill="x",
            padx=15
        )

        # Custom Accent Theme
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
            fill="x",
            padx=15
        )

        # Main content area
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.grid(
            row=0,
            column=1,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        self.show_page(
            "Dashboard",
            DashboardFrame
        )

    # --------------------------------------
    # CUSTOM THEME HANDLER
    # --------------------------------------

    def style_navigation(self):
        colors = THEME_COLORS[self.accent_theme_name]

        for name, button in self.nav_buttons.items():
            selected = name == self.active_page_name

            button.configure(
                fg_color=(
                    colors["primary"] if selected else "transparent"
                ),
                hover_color=(
                    colors["hover"] if selected
                    else ("#E7ECF3", "#353E4B")
                ),
                text_color=(
                    "#FFFFFF" if selected
                    else ("#273548", "#D6DEE8")
                ),
                font=ctk.CTkFont(
                    size=14,
                    weight="bold" if selected else "normal"
                )
            )

    def change_accent_theme(self, theme_name):
        try:
            apply_accent_theme(self, theme_name)
            self.accent_theme_name = theme_name
            self.style_navigation()

        except Exception as error:
            messagebox.showerror(
                "Theme Error",
                str(error)
            )

    # --------------------------------------
    # NAVIGATION
    # --------------------------------------

    def show_page(self, name, frame_class):
        try:
            new_page = frame_class(self.content)
            old_page = self.current_page

            new_page.pack(
                fill="both",
                expand=True
            )

            self.current_page = new_page

            if old_page is not None:
                old_page.destroy()

            apply_accent_theme(
                self,
                self.accent_theme_name
            )
            self.active_page_name = name
            self.style_navigation()

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
