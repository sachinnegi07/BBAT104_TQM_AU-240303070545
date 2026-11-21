
import calendar
from collections import defaultdict
from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from database import initialize_database
from allocation_service import get_allocations
from complaint_service import get_complaints


EVENT_STYLES = {
    "allocation": {
        "label": "ROOM ALLOCATED",
        "color": "#22C55E",
    },
    "vacated": {
        "label": "ROOM VACATED",
        "color": "#F59E0B",
    },
    "complaint": {
        "label": "COMPLAINT",
        "color": "#A78BFA",
    },
}


class HostelCalendarFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        today = date.today()

        self.current_month = today.replace(day=1)
        self.selected_date = today
        self.events = defaultdict(list)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # =====================================
        # PAGE HEADER
        # =====================================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 10),
            sticky="ew"
        )
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Hostel Calendar",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text="Manage dates, room activities and complaints",
            text_color=("gray40", "gray70"),
            font=ctk.CTkFont(size=13)
        ).grid(
            row=1,
            column=0,
            pady=(3, 0),
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="Refresh Events",
            width=130,
            height=36,
            command=self.refresh_data
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=5,
            sticky="e"
        )

        # =====================================
        # MONTHLY STATISTICS
        # =====================================

        stats = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats.grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="ew"
        )

        for column in range(3):
            stats.grid_columnconfigure(
                column,
                weight=1
            )

        self.stat_values = {}

        stat_items = [
            ("Allocations", "allocation"),
            ("Room Vacates", "vacated"),
            ("Complaints", "complaint"),
        ]

        for index, (title, kind) in enumerate(stat_items):
            color = EVENT_STYLES[kind]["color"]

            card = ctk.CTkFrame(
                stats,
                corner_radius=12,
                border_width=1,
                border_color=(
                    "#E5E7EB",
                    "#404040"
                )
            )
            card.grid(
                row=0,
                column=index,
                padx=6,
                pady=5,
                sticky="ew"
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14),
                text_color=("gray35", "gray75")
            ).pack(pady=(12, 2))

            value = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                ),
                text_color=color
            )
            value.pack(pady=(0, 12))

            self.stat_values[kind] = value

        # =====================================
        # MAIN CONTENT
        # =====================================

        body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        body.grid(
            row=2,
            column=0,
            padx=15,
            pady=8,
            sticky="nsew"
        )

        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # LEFT - CALENDAR PANEL
        calendar_panel = ctk.CTkFrame(
            body,
            corner_radius=14
        )
        calendar_panel.grid(
            row=0,
            column=0,
            padx=(5, 7),
            sticky="nsew"
        )
        calendar_panel.grid_columnconfigure(0, weight=1)

        # Month navigation
        navigation = ctk.CTkFrame(
            calendar_panel,
            fg_color="transparent"
        )
        navigation.grid(
            row=0,
            column=0,
            padx=12,
            pady=(15, 12),
            sticky="ew"
        )
        navigation.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            navigation,
            text="<",
            width=40,
            height=34,
            command=lambda: self.change_month(-1)
        ).grid(row=0, column=0, padx=3)

        self.month_label = ctk.CTkLabel(
            navigation,
            text="",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )
        self.month_label.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        ctk.CTkButton(
            navigation,
            text=">",
            width=40,
            height=34,
            command=lambda: self.change_month(1)
        ).grid(row=0, column=2, padx=3)

        ctk.CTkButton(
            navigation,
            text="Today",
            width=65,
            height=34,
            command=self.go_to_today
        ).grid(row=0, column=3, padx=3)

        # Day grid
        self.days_frame = ctk.CTkFrame(
            calendar_panel,
            fg_color="transparent"
        )
        self.days_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 15),
            sticky="nsew"
        )

        for column in range(7):
            self.days_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="day"
            )

        # Legend
        legend = ctk.CTkFrame(
            calendar_panel,
            fg_color="transparent"
        )
        legend.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        for kind in EVENT_STYLES:
            style = EVENT_STYLES[kind]

            item = ctk.CTkFrame(
                legend,
                fg_color="transparent"
            )
            item.pack(
                side="left",
                padx=(0, 12)
            )

            ctk.CTkLabel(
                item,
                text="",
                width=9,
                height=9,
                corner_radius=5,
                fg_color=style["color"]
            ).pack(
                side="left",
                padx=(0, 5)
            )

            ctk.CTkLabel(
                item,
                text=kind.title(),
                font=ctk.CTkFont(size=11)
            ).pack(side="left")

        # =====================================
        # RIGHT - EVENT DETAILS
        # =====================================

        detail_panel = ctk.CTkFrame(
            body,
            corner_radius=14
        )
        detail_panel.grid(
            row=0,
            column=1,
            padx=(7, 5),
            sticky="nsew"
        )
        detail_panel.grid_columnconfigure(0, weight=1)
        detail_panel.grid_rowconfigure(2, weight=1)

        self.date_title = ctk.CTkLabel(
            detail_panel,
            text="",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )
        self.date_title.grid(
            row=0,
            column=0,
            padx=15,
            pady=(20, 5),
            sticky="w"
        )

        self.event_count_label = ctk.CTkLabel(
            detail_panel,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray70")
        )
        self.event_count_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        self.event_list = ctk.CTkScrollableFrame(
            detail_panel,
            fg_color="transparent"
        )
        self.event_list.grid(
            row=2,
            column=0,
            padx=10,
            pady=(0, 15),
            sticky="nsew"
        )

        self.refresh_data()

    # =====================================
    # ADD DATABASE EVENT
    # =====================================

    def add_event(
        self,
        date_value,
        kind,
        title,
        description
    ):
        if not date_value:
            return

        try:
            event_date = date.fromisoformat(
                str(date_value)[:10]
            )
        except (ValueError, TypeError):
            return

        self.events[
            event_date.isoformat()
        ].append({
            "kind": kind,
            "title": title,
            "description": description
        })

    # =====================================
    # LOAD DATABASE EVENTS
    # =====================================

    def refresh_data(self):
        try:
            new_events = defaultdict(list)
            self.events = new_events

            allocations = get_allocations(
                active_only=False
            )

            for record in allocations:
                student = record["full_name"]
                room = record["room_number"]

                self.add_event(
                    record["allocation_date"],
                    "allocation",
                    "Room Allocated",
                    f"{student} - Room {room}"
                )

                if record["vacated_at"]:
                    self.add_event(
                        record["vacated_at"],
                        "vacated",
                        "Room Vacated",
                        f"{student} - Room {room}"
                    )

            complaints = get_complaints()

            for complaint in complaints:
                self.add_event(
                    complaint["created_at"],
                    "complaint",
                    "Complaint Registered",
                    (
                        f"{complaint['title']}\n"
                        f"Student: {complaint['full_name']}\n"
                        f"Status: {complaint['status']}"
                    )
                )

            self.render_calendar()

        except Exception as error:
            messagebox.showerror(
                "Calendar Error",
                str(error)
            )

    # =====================================
    # MONTHLY STATISTICS
    # =====================================

    def update_statistics(self):
        prefix = self.current_month.strftime(
            "%Y-%m"
        )

        counts = {
            "allocation": 0,
            "vacated": 0,
            "complaint": 0
        }

        for day, events in self.events.items():
            if not day.startswith(prefix):
                continue

            for event in events:
                counts[event["kind"]] += 1

        for kind, count in counts.items():
            self.stat_values[kind].configure(
                text=str(count)
            )

    # =====================================
    # CALENDAR RENDERING
    # =====================================

    def render_calendar(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        year = self.current_month.year
        month = self.current_month.month

        self.month_label.configure(
            text=self.current_month.strftime(
                "%B %Y"
            )
        )

        self.update_statistics()

        weekday_names = [
            "Mon", "Tue", "Wed", "Thu",
            "Fri", "Sat", "Sun"
        ]

        for col, name in enumerate(weekday_names):
            ctk.CTkLabel(
                self.days_frame,
                text=name,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                text_color=("gray40", "gray70")
            ).grid(
                row=0,
                column=col,
                pady=(2, 9)
            )

        weeks = calendar.monthcalendar(
            year,
            month
        )

        # Always reserve 6 rows for stable layout
        while len(weeks) < 6:
            weeks.append([0] * 7)

        for row_index, week in enumerate(
            weeks,
            start=1
        ):
            for column, day_number in enumerate(week):
                if day_number == 0:
                    empty_cell = ctk.CTkFrame(
                        self.days_frame,
                        width=62,
                        height=62,
                        fg_color="transparent"
                    )
                    empty_cell.grid(
                        row=row_index,
                        column=column,
                        padx=3,
                        pady=3,
                        sticky="nsew"
                    )
                    continue

                current_date = date(
                    year,
                    month,
                    day_number
                )

                selected = (
                    current_date == self.selected_date
                )
                is_today = (
                    current_date == date.today()
                )

                border_color = (
                    "#F59E0B"
                    if selected
                    else (
                        "#38BDF8"
                        if is_today
                        else ("#E5E7EB", "#454545")
                    )
                )

                cell = ctk.CTkFrame(
                    self.days_frame,
                    width=62,
                    height=62,
                    corner_radius=9,
                    fg_color=(
                        "#FFFFFF",
                        "#303030"
                    ),
                    border_width=2 if (
                        selected or is_today
                    ) else 1,
                    border_color=border_color
                )
                cell.grid(
                    row=row_index,
                    column=column,
                    padx=3,
                    pady=3,
                    sticky="nsew"
                )
                cell.pack_propagate(False)

                ctk.CTkButton(
                    cell,
                    text=str(day_number),
                    width=28,
                    height=28,
                    corner_radius=6,
                    fg_color="transparent",
                    hover_color=(
                        "#E2E8F0",
                        "#454545"
                    ),
                    text_color=(
                        "#111827",
                        "#F9FAFB"
                    ),
                    font=ctk.CTkFont(
                        size=14,
                        weight="bold" if selected else "normal"
                    ),
                    command=lambda d=current_date:
                        self.select_date(d)
                ).pack(pady=(4, 1))

                day_events = self.events.get(
                    current_date.isoformat(),
                    []
                )

                indicators = ctk.CTkFrame(
                    cell,
                    fg_color="transparent"
                )
                indicators.pack()

                # Show one colored dot per event type
                event_types = list(dict.fromkeys(
                    event["kind"]
                    for event in day_events
                ))

                for kind in event_types:
                    ctk.CTkLabel(
                        indicators,
                        text="",
                        width=7,
                        height=7,
                        corner_radius=4,
                        fg_color=EVENT_STYLES[
                            kind
                        ]["color"]
                    ).pack(
                        side="left",
                        padx=2
                    )

        self.display_selected_events()

    # =====================================
    # SELECT DATE
    # =====================================

    def select_date(self, selected_date):
        self.selected_date = selected_date
        self.render_calendar()

    # =====================================
    # EVENT DETAILS
    # =====================================

    def display_selected_events(self):
        for widget in self.event_list.winfo_children():
            widget.destroy()

        self.date_title.configure(
            text=self.selected_date.strftime(
                "%d %B %Y"
            )
        )

        day_events = self.events.get(
            self.selected_date.isoformat(),
            []
        )

        self.event_count_label.configure(
            text=(
                f"{len(day_events)} recorded event(s)"
            )
        )

        if not day_events:
            ctk.CTkLabel(
                self.event_list,
                text="No events recorded for this date.",
                font=ctk.CTkFont(size=13),
                text_color=("gray40", "gray70"),
                wraplength=260
            ).pack(
                padx=12,
                pady=25
            )
            return

        for event in day_events:
            style = EVENT_STYLES[
                event["kind"]
            ]

            event_card = ctk.CTkFrame(
                self.event_list,
                corner_radius=10,
                border_width=1,
                border_color=style["color"]
            )
            event_card.pack(
                fill="x",
                padx=5,
                pady=6
            )

            ctk.CTkLabel(
                event_card,
                text=style["label"],
                text_color=style["color"],
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=12,
                pady=(10, 3)
            )

            ctk.CTkLabel(
                event_card,
                text=event["title"],
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=12,
                pady=2
            )

            ctk.CTkLabel(
                event_card,
                text=event["description"],
                font=ctk.CTkFont(size=12),
                text_color=("gray30", "gray80"),
                justify="left",
                anchor="w",
                wraplength=250
            ).pack(
                fill="x",
                padx=12,
                pady=(2, 12)
            )

    # =====================================
    # MONTH NAVIGATION
    # =====================================

    def change_month(self, direction):
        month_index = (
            self.current_month.year * 12
            + self.current_month.month - 1
            + direction
        )

        year, zero_based_month = divmod(
            month_index,
            12
        )

        self.current_month = date(
            year,
            zero_based_month + 1,
            1
        )

        self.selected_date = self.current_month

        self.render_calendar()

    # =====================================
    # TODAY BUTTON
    # =====================================

    def go_to_today(self):
        self.selected_date = date.today()
        self.current_month = (
            self.selected_date.replace(day=1)
        )

        self.render_calendar()


# =====================================
# STANDALONE APPLICATION
# =====================================

if __name__ == "__main__":

    initialize_database()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(
        "Hostel Management | Modern Calendar"
    )
    app.geometry("1200x760")
    app.minsize(950, 680)

    calendar_ui = HostelCalendarFrame(app)
    calendar_ui.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    app.mainloop()
