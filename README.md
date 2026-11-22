# Hostel Management System

**BBAT104 — Fundamentals of Total Quality Management**

**Academic Session:** 2026–27

**Assigned Quality Goal:** Q03 — Improve Usability

**Application Type:** Python Desktop Application

## 1. Project Overview

The Hostel Management System is a Python-based desktop application designed to manage hostel students, rooms, room allocations and complaints.

The project focuses on improving usability, maintaining accurate hostel records and applying Total Quality Management principles.

## 2. Main Features

- **Dashboard:** View total students, rooms, occupied beds, available beds, active allocations and pending complaints.
- **Student Management:** Add, view, search, update and delete student records.
- **Room Management:** Manage room details, capacity, occupancy and availability.
- **Room Allocation:** Allocate rooms, transfer students, prevent duplicate allocations and vacate rooms.
- **Complaint Management:** Register, search, update and delete complaints.
- **Complaint Audit History:** Preserve deleted complaint information for accountability.
- **Calendar:** View room allocation, vacate and complaint-related activities.

## 3. Five Quality Features — Q03

1. Dark and Light Mode
2. Custom Colour Themes
3. Dashboard Overview
4. Search Filters
5. Calendar

These features support the assigned goal of improving application usability.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| CustomTkinter | Desktop user interface |
| SQLite | Local database |
| Pillow | Image processing support |
| Tkinter | Desktop GUI support |

SQLite and Tkinter are included with standard Python installations that provide Tkinter support.

## 5. Project Setup

### Requirements

- Windows computer
- Python installed
- Git (optional, for cloning the repository)

The application was developed and tested in a Python 3.14.7 environment.

### Installation

**Step 1:** Download or clone the project.

Repository: https://github.com/sachinnegi07/BBAT104_TQM_AU-240303070545

**Step 2:** Open the project folder in VS Code.

**Step 3:** Open PowerShell Terminal and create a virtual environment.

`python -m venv .venv`

**Step 4:** Install the required Python packages.

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

**Step 5:** Run the application.

`.\.venv\Scripts\python.exe main.py`

The application initializes its SQLite database automatically when required.

## 6. Database

The project uses SQLite to store information about students, rooms, allocations and complaints.

The database also maintains complaint deletion audit history.

**Note:** The local `data/hostel.db` file should not be uploaded to a public repository when it contains private records.

## 7. Testing

Automated tests are available for the major application modules.

Run tests individually:

- `python test_student_service.py`
- `python test_room_service.py`
- `python test_allocation_service.py`
- `python test_complaint_service.py`
- `python test_complaint_audit.py`

The existing project testing workflow has verified 44 automated tests, along with GUI interaction and complaint audit-history checks.

## 8. TQM Documentation

Project documentation is available inside the `docs` folder.

- `docs/SRS.md` — Software Requirements Specification
- `docs/architecture.md` — System Architecture
- `docs/review3/` — FMEA, Risk Mitigation, SIPOC and CTQ Analysis
- `docs/review4/` — PDCA Improvement, SQC Analysis and Quality Report

## 9. Project Status

The main application modules, usability features and complaint audit system have been implemented and tested.

Review 3 and Review 4 documentation has been prepared. Final submission packaging and demonstration preparation are the remaining activities.

## 10. Future Improvements

Potential future enhancements include role-based login, report exports and more advanced hostel analytics. These are not part of the currently verified implementation.

---

**Project:** Hostel Management System

**Course:** BBAT104 — Fundamentals of TQM

**Quality Goal:** Q03 — Improve Usability