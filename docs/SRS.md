# Software Requirements Specification (SRS)

## Hostel Management System

**Course:** BBAT104 — Fundamentals of Total Quality Management (TQM)  
**Academic Session:** 2026–27  
**Student Name:** Sachin Negi  
**University Roll Number:** 2410307023  
**Enrollment Number:** AU-240303070545  
**Assigned Quality Goal:** Q03 — Improve Usability  
**Document Version:** 1.0  
**Project Stage:** Review 1 — Requirements and Planning

---

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to define the functional and non-functional requirements of the Hostel Management System.

The system will help hostel administrators manage student records, hostel rooms, room allocations, and complaints through a user-friendly desktop application.

### 1.2 Problem Statement

Manual hostel management can lead to:

- Difficulty finding student information.
- Incorrect or duplicate room allocations.
- Delays in managing student complaints.
- Poor visibility of available and occupied rooms.
- Difficulty navigating multiple records.

The proposed system aims to address these problems through computerized record management and improved usability.

### 1.3 Project Objectives

1. Digitize hostel administration.
2. Implement functional Create, Read, Update, and Delete (CRUD) operations.
3. Reduce manual data-entry mistakes.
4. Improve navigation and information accessibility.
5. Apply TQM principles to evaluate and improve software quality.

---

## 2. Project Scope

### 2.1 Included Modules

**Student Management**
- Add new student records.
- View student information.
- Update student details.
- Delete eligible records.
- Search students.

**Room Management**
- Add hostel rooms.
- View room capacity and availability.
- Update room information.
- Delete eligible rooms.

**Room Allocation**
- Assign students to available rooms.
- View existing allocations.
- Change room allocations.
- Vacate allocated rooms.
- Prevent allocations exceeding room capacity.

**Complaint Management**
- Register student complaints.
- View submitted complaints.
- Update complaint status.
- Delete eligible complaint records.

### 2.2 Out of Scope

The initial version will not include online payments, biometric attendance, SMS integration, or multi-hostel cloud synchronization.

---

## 3. Intended Users

**Primary User: Hostel Administrator**

The hostel administrator will operate the desktop application to manage records, allocate rooms, monitor complaints, and view dashboard information.

The initial release is intended for local administrative use rather than a multi-user online system.

---

## 4. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Add, view, edit, and delete student records | High |
| FR-02 | Add, view, edit, and delete room records | High |
| FR-03 | Allocate, update, and vacate rooms | High |
| FR-04 | Register and manage complaints | High |
| FR-05 | Validate required inputs | High |
| FR-06 | Prevent duplicate student IDs and room numbers | High |
| FR-07 | Prevent over-allocation of rooms | High |
| FR-08 | Display dashboard statistics | High |
| FR-09 | Filter and search records | High |
| FR-10 | Display calendar-based information | Medium |

Record deletion must not leave inconsistent linked data.

---

## 5. Assigned TQM Quality Goal

**Q03 — Improve Usability**

The project will implement the following five assigned usability features.

### 5.1 Dark Mode

Provide light and dark display modes to improve viewing comfort.

### 5.2 Custom Themes

Allow the administrator to select from predefined interface color themes.

### 5.3 Dashboard Overview

Display important statistics, including:

- Total registered students.
- Total hostel rooms.
- Available rooms and occupied rooms.
- Pending complaints.

### 5.4 Search Filters

Provide search and filtering options for students, rooms, allocations, and complaints.

### 5.5 Calendar

Provide a calendar interface to view relevant dates, including room allocation dates and complaint dates.

---

## 6. Non-Functional Requirements

### 6.1 Usability

The application should provide clear labels, consistent navigation, readable text, and understandable feedback messages.

### 6.2 Performance

Normal operations should respond promptly on a standard college computer. Performance will be evaluated using representative test data.

### 6.3 Reliability

The system should handle invalid inputs without crashing and preserve valid saved records.

### 6.4 Data Integrity

Student IDs and room numbers must remain unique. Room allocations must respect room capacity and student allocation rules.

### 6.5 Maintainability

Code should be divided into logical modules for easier testing, debugging, and future improvements.

### 6.6 Privacy

Student records will be stored locally. Real student personal information and local databases must not be published in the public GitHub repository.

---

## 7. Technology Requirements

| Component | Selected Technology |
|---|---|
| Programming Language | Python 3 |
| Desktop Interface | CustomTkinter |
| Database | SQLite |
| Quality Analysis Charts | Matplotlib |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |
| Operating System | Windows |

---

## 8. Usability Evaluation Plan

To measure the Q03 quality goal, selected tasks will be performed before and after usability improvements.

### Evaluation Tasks

1. Find a specific student.
2. Identify an available room.
3. Allocate a room to a student.
4. Locate a pending complaint.
5. Change the application theme.

### Measurement Metrics

- Task completion time.
- Task completion success rate.
- Number of user errors.
- Number of navigation actions.
- User satisfaction feedback.

**Measurement rule:** Actual test results will be recorded during development and evaluation. No improvement will be claimed without supporting observations.

---

## 9. TQM Quality Analysis Plan

The following tools will be prepared during later reviews:

- **CTQ Tree:** Identify critical software quality requirements.
- **SIPOC Diagram:** Map the hostel management process.
- **FMEA:** Identify software failure modes and calculate Risk Priority Numbers.
- **Checksheets:** Record observed defects.
- **Pareto Chart:** Identify major categories of defects.
- **Fishbone Diagram:** Investigate possible root causes.
- **PDCA Cycle:** Plan, implement, check, and refine improvements.

---

## 10. Acceptance Criteria

The software will be considered ready for final demonstration when:

1. All four core management modules function correctly.
2. All five Q03 usability features work.
3. Duplicate student IDs and room numbers are rejected.
4. Room capacity limits are enforced.
5. Existing allocations remain consistent after relevant record changes.
6. Important operations handle invalid inputs safely.
7. Usability tests and findings are documented.
8. Required TQM analysis artefacts are prepared.
9. Source code and documentation are maintained on GitHub.
10. The application can be demonstrated successfully during the viva.

---

## 11. Conclusion

The proposed Hostel Management System will combine essential hostel administration functions with usability-focused quality improvements.

The project will apply Total Quality Management principles to evaluate software processes, identify problems, and support continuous improvement through testing and documented evidence.

**Document Status:** Initial SRS prepared for Review 1. Implementation and validation are pending.